<?php
    $dotenv  = parse_ini_file(__DIR__ . '/.env');
    $api_url = sprintf('http://%s:%s',
        $dotenv['BACKEND_PYTHON_DOCKER_URL'],
        $dotenv['BACKEND_PYTHON_DOCKER_PORT']
    );
?>
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
    const API = '<?= $api_url ?>'; // injecté directement dans le JS
    const SESSION_ID = crypto.randomUUID();

    async function connect() {
        const login    = document.getElementById('login').value;
        const password = document.getElementById('password').value;

        setStatus('⏳ Authentification en cours...', 'waiting');

        const form = new FormData();
        form.append('session_id', SESSION_ID);
        form.append('login',      login);
        form.append('password',   password);

        try {
            const res  = await fetch(`${API}/login`, { method: 'POST', body: form });
            const data = await res.json();

            if (data.contains_wooclap) {
                setStatus('✅ Connecté ! Wooclap détecté.', 'success');
                document.getElementById('btn-logout').style.display = 'inline';
            } else if (data.error) {
                setStatus('❌ Erreur : ' + data.error, 'error');
            } else {
                setStatus('⚠️ Connecté mais Wooclap absent. URL : ' + data.final_url, 'warning');
                console.log('Extrait HTML :', data.html_excerpt);
            }
        } catch (e) {
            setStatus('❌ Erreur réseau : ' + e.message, 'error');
        }
    }

    async function disconnect() {
        const form = new FormData();
        form.append('session_id', SESSION_ID);

        try {
            await fetch(`${API}/logout`, { method: 'POST', body: form });
            setStatus('👋 Déconnecté.', 'waiting');
            document.getElementById('btn-logout').style.display = 'none';
        } catch (e) {
            setStatus('❌ Erreur de déconnexion : ' + e.message, 'error');
        }
    }

    function setStatus(msg, type) {
        const el = document.getElementById('status');
        el.textContent = msg;
        el.className = type;
    }
</script>
</body>
</html>