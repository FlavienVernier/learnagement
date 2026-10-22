import os
import socket

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


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


