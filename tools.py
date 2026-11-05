import os
import socket
import sys

from getpass import getpass

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

import atexit, termios


def __protect_tty__():
    if not sys.stdin.isatty():
        return
    fd = sys.stdin.fileno()
    saved = termios.tcgetattr(fd)
    atexit.register(lambda: termios.tcsetattr(fd, termios.TCSADRAIN, saved))


def get_local_ip_and_hostname() -> tuple[str, str]:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Ne se connecte pas vraiment, juste pour déterminer l'interface sortante
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()

    # Résolution DNS inverse (équivalent nslookup) : si pas de PTR record, hostname = IP
    try:
        hostname = socket.gethostbyaddr(ip)[0]
    except (socket.herror, socket.gaierror):
        hostname = ip

    return ip, hostname


def __generate_secret__(info: str) -> bytes:
    base_secret = os.urandom(32).hex()
    """
    Génère une clé dérivée compatible avec NextAuth à partir d'un secret de base.
    """

    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,  # 32 octets pour une clé symétrique
        salt=b"",    # pas de sel ici, mais peut être personnalisé
        info=info.encode('utf-8')
    )
    derived_key = hkdf.derive(base_secret.encode('utf-8'))
    return derived_key

def __ask(prompt: str, secret: bool = False, env_key: str | None = None) -> str:
    if env_key and os.environ.get(env_key):
        return os.environ[env_key]
    if not sys.stdin.isatty():
        raise RuntimeError(
            f"Entrée interactive impossible (pas de TTY) : définis {env_key or 'la valeur'} "
            "en variable d'environnement."
        )
    return getpass(prompt) if secret else input(prompt)