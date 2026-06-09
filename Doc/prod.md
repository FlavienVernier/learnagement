# Certificats

## auto-signé 

Création d'un certificat autosigné.

```bash
# générer le certificat
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 3650 -nodes
```

```bash
# Renommer pour correspondre à ton SSL_DIR
mv cert.pem  certs/cert.pem
mv key.pem   certs/key.pem
```
Les problèmes classiques du certificat auto-signé :
- le  navigateur ne fait pas confiance à une autorité inconnue ;
- Firefox lève l'erreur `SSL_ERROR_RX_RECORD_TOO_LONG`.

La solution dépend de ton contexte.

---

## En dev local → `mkcert` (recommandé)

`mkcert` crée une autorité de certification locale reconnue par ton navigateur.

```bash
# Installer mkcert
sudo apt install mkcert        # Linux
brew install mkcert            # Mac
choco install mkcert           # Windows

# Installer l'autorité locale dans le navigateur
mkcert -install

# Générer le certificat pour ton domaine local
mkcert localhost 127.0.0.1 monapp.local
# génère localhost+2.pem et localhost+2-key.pem
```

```bash
# Renommer pour correspondre à ton SSL_DIR
mv localhost+2.pem     certs/cert.pem
mv localhost+2-key.pem certs/key.pem
```

✅ Plus d'avertissement dans le navigateur, valable pour toute la machine.

---

## En prod → Let's Encrypt (certificat reconnu officiellement)

```bash
# Via certbot
sudo apt install certbot
sudo certbot certonly --standalone -d mondomaine.com

# Les certs sont générés dans :
# /etc/letsencrypt/live/mondomaine.com/fullchain.pem
# /etc/letsencrypt/live/mondomaine.com/privkey.pem
```

Ou via **Caddy** qui gère Let's Encrypt automatiquement sans rien faire.


