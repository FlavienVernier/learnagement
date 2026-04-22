<?php
    require __DIR__ . '/utils/template.php';
    require __DIR__ . '/utils/router.php';
    require __DIR__ . '/utils/auth.php';
    require __DIR__ . '/utils/session.php';
    require __DIR__ . "/utils/endpoint.php";
    include __DIR__ . "/utils/connectDB.php";

    create_session();
    $r = new Router('/APP_2026');
    $t = new Template(
        viewsPath: __DIR__ . '/views',
        router: $r,
        componentsPath: __DIR__ . '/components',
        scriptsPath: __DIR__ . '/scripts',
        assetsPath: __DIR__ . '/assets',
        baseUrl: '/APP_2026'
    );
    $user = getCurrentUser();

    // Global variables for templates
    $t->share('pdo', $pdo); # depreciated, prefer API
    $t->share('user', $user);

    // Define routes
    $t->router->get('/', 'home', function () use ($t) {
        echo $t->render('base/home'); // Make a home page
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
        logout();
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

    $t->router->get('/dashboard/profile', 'dashboard-profile', function () use ($t, $user) {
        requireRole($user, "etudiant", $t->router);
        echo $t->render('dashboard/profile');
    });

    $t->router->get('/dashboard/stage', 'dashboard-stage', function () use ($t, $user) {
        requireAuth($user, $t->router);
        echo $t->render('dashboard/stage');
    });

    $t->router->get('/dashboard/mobility-map', 'dashboard-mobility-map', function () use ($t, $user) {
        requireAuth($user, $t->router);
        echo $t->render('dashboard/mobility-map');
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

    $t->router->run();