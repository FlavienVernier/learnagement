from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta, timezone
from pathlib import Path
import os
import dotenv

def generate_self_signed_cert(
    common_name: str,
    san_dns_names: list[str],
    san_ip_addresses: list[str],
    output_dir: str,
    days_valid: int = 365,
) -> None:
    """
    Génère une paire cert.pem / key.pem auto-signée avec SAN (DNS + IP).

    :param common_name: CN du certificat (ex: "localhost" ou "learnagement.univ-smb.fr")
    :param san_dns_names: liste de noms DNS à inclure dans le SAN (ex: ["backend_python_cas"])
    :param san_ip_addresses: liste d'IP à inclure dans le SAN (ex: ["127.0.0.1"])
    :param output_dir: dossier de sortie (créé s'il n'existe pas)
    :param days_valid: durée de validité en jours
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # 1. Génération de la clé privée RSA 4096 bits
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
    )

    # 2. Construction du sujet/émetteur (auto-signé => sujet = émetteur)
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, common_name),
    ])

    # 3. Construction du SAN (Subject Alternative Names)
    import ipaddress
    san_entries = [x509.DNSName(name) for name in san_dns_names]
    san_entries += [x509.IPAddress(ipaddress.ip_address(ip)) for ip in san_ip_addresses]

    # 4. Construction du certificat
    now = datetime.now(timezone.utc)
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now)
        .not_valid_after(now + timedelta(days=days_valid))
        .add_extension(x509.SubjectAlternativeName(san_entries), critical=False)
        .add_extension(
            x509.BasicConstraints(ca=True, path_length=None), critical=True
        )
        .sign(private_key, hashes.SHA256())
    )

    # 5. Écriture de la clé privée (non chiffrée, équivalent -nodes)
    key_path = output_path / "key.pem"
    key_path.write_bytes(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )

    # 6. Écriture du certificat
    cert_path = output_path / "cert.pem"
    cert_path.write_bytes(cert.public_bytes(serialization.Encoding.PEM))

    print(f"Certificat généré : {cert_path}")
    print(f"Clé privée générée : {key_path}")


def generate_internal_cert(output_dir: str = "./certs/internal") -> None:
    """Certificat interne pour la communication PHP <-> Backend Python (réseau Docker)."""
    generate_self_signed_cert(
        common_name="localhost",
        san_dns_names=[
            "localhost",
            "backend_python_cas",
            "learnagement_backend_python_cas",
        ],
        san_ip_addresses=["127.0.0.1"],
        output_dir=output_dir,
        days_valid=365,
    )


def generate_external_cert(
    domain: str,
    public_ip: str | None = None,
    output_dir: str = "./certs/external",
) -> None:
    """
    Certificat externe pour l'accès web (fronts). À terme, à remplacer
    par Let's Encrypt / un reverse proxy tiers.

    :param domain: nom de domaine public réel (ex: "learnagement.univ-smb.fr")
    :param public_ip: IP publique du serveur, optionnelle
    """
    san_ips = ["127.0.0.1"]
    if public_ip:
        san_ips.append(public_ip)

    generate_self_signed_cert(
        common_name=domain,
        san_dns_names=[domain, "localhost"],
        san_ip_addresses=san_ips,
        output_dir=output_dir,
        days_valid=365,
    )


if __name__ == "__main__":
    dotenv.load_dotenv()
    generate_internal_cert()
    generate_external_cert(domain=os.environ["INSTANCE_URL"], public_ip=os.environ["INSTANCE_IP"])