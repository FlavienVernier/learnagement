<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="utf-8">
    <title>Intranet USMB</title>
    <style>
        body { font-family: sans-serif; padding: 2rem; max-width: 500px; margin: auto; }
        input { display: block; width: 100%; margin: 0.5rem 0 1rem; padding: 0.5rem; box-sizing: border-box; }
        button { padding: 0.6rem 1.5rem; cursor: pointer; }
        #status { margin-top: 1.5rem; padding: 1rem; border-radius: 8px; background: #f0f0f0; }
        .success { background: #d4edda !important; color: #155724; }
        .waiting { background: #fff3cd !important; color: #856404; }
        .error   { background: #f8d7da !important; color: #721c24; }
    </style>
</head>
<body>
<h2>Connexion Intranet USMB</h2>

<label>Login</label>
<input type="text" id="login" placeholder="votre login">

<label>Mot de passe</label>
<input type="password" id="password" placeholder="votre mot de passe">

<button onclick="connect()">Se connecter</button>

<button onclick="disconnect()" id="btn-logout" style="display:none; background:#dc3545; color:white; border:none;">
    Se déconnecter
</button>

<div id="status" class="waiting">En attente...</div>

<script>
    async function connect() {
        const login    = document.getElementById('login').value;
        const password = document.getElementById('password').value;

        setStatus('⏳ Authentification en cours...', 'waiting');

        const form = new FormData();
        form.append('login', login);
        form.append('password', password);

        try {
            const res  = await fetch('proxy.php', { method: 'POST', body: form });
            const text = await res.text();
            const data = JSON.parse(text);

            if (data.contains_wooclap) {
                setStatus('✅ Connecté ! Wooclap détecté.', 'success');
                document.getElementById('btn-logout').style.display = 'inline'; // ← affiche le bouton
            } else if (data.error) {
                setStatus('❌ Erreur : ' + data.error, 'error');
            } else {
                setStatus('⚠️ Connecté mais Wooclap absent. URL : ' + data.final_url, 'warning');
            }
        } catch (e) {
            setStatus('❌ Erreur : ' + e.message, 'error');
        }
    }

    async function disconnect() {
        try {
            await fetch('logout.php', { method: 'POST' });
            setStatus('👋 Déconnecté.', 'waiting');
            document.getElementById('btn-logout').style.display = 'none'; // ← cache le bouton
        } catch (e) {
            setStatus('❌ Erreur de déconnexion : ' + e.message, 'error');
        }
    }
    /*async function connect() {
        const login    = document.getElementById('login').value;
        const password = document.getElementById('password').value;

        setStatus('⏳ Authentification en cours...', 'waiting');

        const form = new FormData();
        form.append('login', login);
        form.append('password', password);

        try {
            const res  = await fetch('proxy.php', { method: 'POST', body: form });
            const text = await res.text(); // ← texte brut au lieu de JSON

            console.log('Réponse brute :', text); // ← inspecter dans F12 > Console

            const data = JSON.parse(text); // ← on parse manuellement pour voir l'erreur

            if (data.contains_wooclap) {
                setStatus('✅ Connecté ! Wooclap détecté.', 'success');
            } else if (data.error) {
                setStatus('❌ Erreur : ' + data.error, 'error');
            } else {
                setStatus('⚠️ Connecté mais Wooclap absent. URL : ' + data.final_url, 'warning');
            }
        } catch (e) {
            setStatus('❌ Erreur : ' + e.message, 'error');
        }
    }*/
    /*async function connect() {
        const login    = document.getElementById('login').value;
        const password = document.getElementById('password').value;

        setStatus('⏳ Authentification en cours...', 'waiting');

        const form = new FormData();
        form.append('login', login);
        form.append('password', password);

        try {
            const res  = await fetch('proxy.php', { method: 'POST', body: form });
            const data = await res.json();

            if (data.contains_wooclap) {
                setStatus('✅ Connecté ! Wooclap détecté sur l\'intranet.', 'success');
            } else if (data.error) {
                setStatus('❌ Erreur : ' + data.error, 'error');
            } else {
                setStatus('⚠️ Connecté mais Wooclap absent. URL finale : ' + data.final_url, 'warning');
                console.log('Extrait HTML :', data.html_excerpt);
            }
        } catch (e) {
            setStatus('❌ Erreur réseau : ' + e.message, 'error');
        }
    }*/

    function setStatus(msg, type) {
        const el = document.getElementById('status');
        el.textContent = msg;
        el.className = type;
    }
</script>
</body>
</html>