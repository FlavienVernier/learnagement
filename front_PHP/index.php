<?php
    require_once __DIR__ . '/vendor/autoload.php'; // Add this line
    require __DIR__ . '/utils/template.php';
    require __DIR__ . '/utils/router.php';
    require __DIR__ . '/utils/alerts.php';
    require __DIR__ . '/utils/auth.php';
    require __DIR__ . '/utils/session.php';
    require __DIR__ . "/utils/endpoint.php";
    require_once __DIR__ . "/utils/cas.php";
    require_once __DIR__ . "/config.php";
    include __DIR__ . "/utils/connectDB.php"; # must be refactored to load env here



    create_session();
    $r = new Router('');
    $t = new Template(
        viewsPath: __DIR__ . '/views',
        router: $r,
        componentsPath: __DIR__ . '/components',
        scriptsPath: __DIR__ . '/scripts',
        assetsPath: __DIR__ . '/assets',
        baseUrl: ''
    );
    $user = getCurrentUser();

    // Global variables for templates
    $t->share('user', $user);
    $t->share('toasts', []);



    // Define routes

   // NO Prod env
    if (getenv("ENV") !== "prod") {

        // Test .../localhost/mock-cas-login?ticket=ST-MOCK-ENSEIGNANT
        // Test .../localhost/mock-cas-login?ticket=ST-MOCK-ETUDIANT
        $t->router->get('/mock-cas-login', 'mock-cas-login', function () use ($t, $user) {
            $ticket = $_GET['ticket'] ?? 'ST-MOCK-ENSEIGNANT';

            getLogger()->info("CAS Mock Login: " . $ticket);

            // Simule exactement le retour du serveur CAS :
            // CAS redirige vers /?ticket=ST-xxxx
            // On fait la même chose avec notre ticket de mock
            $redirectUrl = "/" . "?ticket=" . urlencode($ticket);
            header("Location: " . $redirectUrl);
            exit;
        });

        $t->router->get('/dashboard/nextjs', 'dashboard-nextjs', function () use ($t, $user) {
            requireAuth($user, $t->router);
            echo $t->render('dashboard/nextjs');
        });

    }
    // all env
    $t->router->get('/', 'home', function () use ($t, $user) {

        // Retour depuis le CAS avec un ticket
        if (isset($_GET['ticket'])) {
            require_once __DIR__ . "/utils/cas.php";

            getLogger()->info("CAS Login");

            $serviceUrl = getenv("FRONT_PHP_PROTOCOL") . "://" . getenv("INSTANCE_URL") . "/";
            $casData = validateCasTicket($_GET['ticket'], $serviceUrl);

            if ($casData === null) {
                getLogger()->warning('CAS ticket invalide', ['ticket' => $_GET['ticket']]);
                $t->router->redirect('login');
            }

            //getLogger()->info("Cas Data: " . json_encode($casData));

            $result = casLogin($casData);
            if ($result && isset($result['access_token'])) {
                // Le backend a géré seul le lookup/provisionnement
                login(
                    id: $result['id'],
                    email: $result['email'],
                    type: $result['type'],
                    jwt: $result['access_token']
                );
                $_SESSION['auth_method'] = 'cas';
                $t->router->redirect('dashboard');
            }

            $t->router->redirect('login');
        }
        // else direct user connexion or no user connected

        if ($user)
            $t->router->redirect('dashboard');
        echo $t->render('base/home'); // Make a home page
    });

    $t->router->get('/404', '404', function () use ($t) {
        echo $t->render('base/404');
    });

    $t->router->get('/login', 'login', function () use ($t, $user) {
        requireGuest($user, $t->router);
        echo $t->render('base/login');
    });
    
    $t->router->post('/login', 'login-post', function () use ($t, $user) {
        requireGuest($user, $t->router);
        echo $t->render('base/@post/login');
    });

    $t->router->get('/logout', 'logout', function () use ($t, $user) {
        requireAuth($user, $t->router);

        $wasCas = ($_SESSION['auth_method'] ?? '') === 'cas';
        logout();

        if ($wasCas) {
            $casLogoutUrl = "https://cas-uds.grenet.fr/cas/logout"
                . "?service=" . urlencode("https://learnagement.local.univ-savoie.fr/login");
            header("Location: " . $casLogoutUrl);
            exit;
        }

        $t->router->redirect('login');
    });

    $t->router->post('/inscription', 'inscription-post', function () use ($t, $user) {
        requireGuest($user, $t->router);
        echo $t->render('base/@post/inscription');
    });

    $t->router->get('/dashboard', 'dashboard', function () use ($t, $user) {
        requireAuth($user, $t->router);
        echo $t->render('dashboard/home');
    });

    $t->router->post('/profile/calendar', 'profile-calendar', function () use ($t, $user) {
        requireAuth($user, $t->router);
        echo $t->render('dashboard/@post/calendar');
    });

    $t->router->get('/dashboard/profile', 'dashboard-profile', function () use ($t, $user) {
        requireRole($user, "etudiant", $t->router);
        echo $t->render('dashboard/profile');
    });

    $t->router->get('/dashboard/stage', 'dashboard-stage', function () use ($t, $user) {
        requireAuth($user, $t->router);
        echo $t->render('dashboard/stage');
    });

    $t->router->post('/dashboard/stage', 'dashboard-stage-post', function () use ($t, $user) {
        requireAuth($user, $t->router);
        echo $t->render('dashboard/@post/stage');
    });

    $t->router->get('/dashboard/create-stage', 'dashboard-create-stage', function () use ($t, $user) {
        requireAuth($user, $t->router);
        echo $t->render('dashboard/create_stage');
    });

    $t->router->post('/dashboard/create-stage', 'dashboard-create-stage-post', function () use ($t, $user) {
        requireAuth($user, $t->router);
        echo $t->render('dashboard/@post/create_stage');
    });

    $t->router->get('/dashboard/mobility-map', 'dashboard-mobility-map', function () use ($t, $user) {
        requireAuth($user, $t->router);
        echo $t->render('dashboard/mobility-map');
    });

    $t->router->get('/dashboard/mobility-admin', 'dashboard-mobility-admin', function () use ($t, $user) {
        requireRole($user, "administratif", $t->router);
        echo $t->render('dashboard/mobility-admin');
    });
    
    $t->router->get('/dashboard/dependance_module', 'dashboard-dependance-module', function () use ($t, $user) {
        requireAuth($user, $t->router);
        echo $t->render('dashboard/dependance_module');
    });

    $t->router->post('/dashboard/dependance_module', 'dashboard-dependance-module-post', function () use ($t, $user) {
        requireAuth($user, $t->router);
        echo $t->render('dashboard/@post/dependance_module');
    });

    $t->router->get('/dashboard/python', 'dashboard-python', function () use ($t, $user) {
        requireAuth($user, $t->router);
        echo $t->render('dashboard/python');
    });

    $t->router->get('/dashboard/ressource', 'dashboard-ressource', function () use ($t, $user) {
        requireAuth($user, $t->router);
        echo $t->render('dashboard/ressource');
    });

    $t->router->get('/dashboard/annuaire', 'dashboard-annuaire', function () use ($t, $user) {
        requireAuth($user, $t->router);
        echo $t->render('dashboard/liste_personnel');
    });

    $t->router->post('/dashboard/annuaire', 'dashboard-annuaire-post', function () use ($t, $user) {
        requireAuth($user, $t->router);
        echo $t->render('dashboard/liste_personnel');
    });

    $t->router->get('/dashboard/rendus/etudiant', 'dashboard-rendus-student', function () use ($t, $user) {
        requireRole($user, 'etudiant', $t->router);
        echo $t->render('dashboard/rendus-student');
    });

    $t->router->get('/dashboard/rendus/enseignant', 'dashboard-rendus-enseignant', function () use ($t, $user) {
        requireRole($user, 'enseignant', $t->router);
        echo $t->render('dashboard/rendus-enseignant');
    });

    $t->router->get('/test', 'test', function () use ($t, $user) {
        requireAuth($user, $t->router);
        echo $t->render('dashboard/test');
    });

    getLogger()->info('PHP app start');
    $t->router->run();