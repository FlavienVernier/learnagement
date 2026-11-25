# auth/login_throttle.py
import logging
import time
from threading import Lock
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)

# ToDo une seule instance uvicorn : stockage mémoire. Passage à Redis à prévoir si plusieurs workers.

# échecs tolérés avant verrouillage, par type de clé
FREE_ATTEMPTS = {
    "ui": 5,    # couple compte + IP : strict
    "ip": 30,   # IP seule : tolérant (NAT, campus)
}
BASE_DELAY_S  = 30
MAX_DELAY_S   = 900     # plafond : 15 min
WINDOW_S      = 3600    # oubli des échecs après 1 h sans échec
PURGE_EVERY_S = 60
U_ALERT_FAILS = 50      # alerte (log seulement) si un compte reçoit trop d'échecs toutes IP confondues

_lock = Lock()
_state: dict[str, dict] = {}   # clé -> {"fails", "locked_until", "last"}
_u_fails: dict[str, list[float]] = {}   # compte -> horodatages d'échecs, sans aucun blocage
_last_purge = 0.0


def _norm(username: str) -> str:
    return (username or "").strip().lower()[:128]


def _keys(username: str, ip: str) -> list[tuple[str, str]]:
    u = _norm(username)
    return [("ui", f"ui:{u}|{ip}"), ("ip", f"ip:{ip}")]


def _delay(kind: str, fails: int) -> float:
    free = FREE_ATTEMPTS[kind]
    if fails < free:
        return 0.0
    exponent = min(fails - free, 10)   # évite les puissances géantes
    return min(BASE_DELAY_S * 2 ** exponent, MAX_DELAY_S)


def _purge(now: float) -> None:
    """À appeler sous verrou."""
    global _last_purge
    if now - _last_purge < PURGE_EVERY_S:
        return
    _last_purge = now
    for k in [k for k, s in _state.items() if now - s["last"] > WINDOW_S]:
        del _state[k]
    for u in list(_u_fails):
        _u_fails[u] = [t for t in _u_fails[u] if now - t < WINDOW_S]
        if not _u_fails[u]:
            del _u_fails[u]


def check(username: str, ip: str) -> None:
    """Lève 429 si le couple compte+IP ou l'IP est verrouillé."""
    now = time.time()
    wait = 0.0
    with _lock:
        _purge(now)
        for _, k in _keys(username, ip):
            s = _state.get(k)
            if s and now - s["last"] <= WINDOW_S:
                wait = max(wait, s["locked_until"] - now)
    if wait > 0:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Trop de tentatives, réessayez plus tard",
            headers={"Retry-After": str(int(wait) + 1)},
        )


def register_failure(username: str, ip: str) -> None:
    now = time.time()
    u = _norm(username)
    with _lock:
        for kind, k in _keys(username, ip):
            s = _state.setdefault(k, {"fails": 0, "locked_until": 0.0, "last": now})
            if now - s["last"] > WINDOW_S:      # entrée périmée : on repart de zéro
                s["fails"], s["locked_until"] = 0, 0.0
            s["fails"] += 1
            s["last"] = now
            s["locked_until"] = now + _delay(kind, s["fails"])

        # Compte seul : on compte, on ne bloque jamais.
        lst = [t for t in _u_fails.get(u, []) if now - t < WINDOW_S]
        lst.append(now)
        _u_fails[u] = lst
        if len(lst) == U_ALERT_FAILS:
            logger.warning("Possible brute force distribué sur le compte '%s' (%d échecs/h)", u, len(lst))


def reset(username: str, ip: str) -> None:
    """Après un succès : on efface le couple compte+IP, pas l'IP seule."""
    with _lock:
        _state.pop(f"ui:{_norm(username)}|{ip}", None)