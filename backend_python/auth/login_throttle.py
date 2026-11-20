# auth/login_throttle.py
import time
from threading import Lock
from fastapi import HTTPException, status

# ToDo, une seule instance uvicorn lancée, donc un stockage en mémoire suffit pour démarrer. Passage a Redis à prévoir

MAX_FREE_ATTEMPTS = 5      # échecs tolérés sans pénalité
BASE_DELAY_S      = 30     # premier verrouillage
MAX_DELAY_S       = 900    # plafond : 15 min
WINDOW_S          = 3600   # oubli des échecs après 1 h sans tentative

_lock = Lock()
_state: dict[str, dict] = {}   # clé -> {"fails": int, "locked_until": float, "last": float}


def _keys(username: str, ip: str) -> list[str]:
    u = (username or "").strip().lower()
    return [f"u:{u}", f"ip:{ip}", f"ui:{u}|{ip}"]


def _delay(fails: int) -> float:
    if fails < MAX_FREE_ATTEMPTS:
        return 0
    return min(BASE_DELAY_S * 2 ** (fails - MAX_FREE_ATTEMPTS), MAX_DELAY_S)


def check(username: str, ip: str) -> None:
    """Lève 429 si l'une des clés est verrouillée."""
    now = time.time()
    with _lock:
        wait = 0.0
        for k in _keys(username, ip):
            s = _state.get(k)
            if not s:
                continue
            if now - s["last"] > WINDOW_S:
                del _state[k]
                continue
            wait = max(wait, s["locked_until"] - now)
    if wait > 0:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Trop de tentatives, réessayez plus tard",
            headers={"Retry-After": str(int(wait) + 1)},
        )


def register_failure(username: str, ip: str) -> None:
    now = time.time()
    with _lock:
        for k in _keys(username, ip):
            s = _state.setdefault(k, {"fails": 0, "locked_until": 0.0, "last": now})
            s["fails"] += 1
            s["last"] = now
            s["locked_until"] = now + _delay(s["fails"])


def reset(username: str, ip: str) -> None:
    """Après un succès : on efface le compte et le couple compte+IP, pas l'IP seule."""
    with _lock:
        _state.pop(f"u:{(username or '').strip().lower()}", None)
        _state.pop(f"ui:{(username or '').strip().lower()}|{ip}", None)