<?php
    session_start();

    function requireAuth($user, $router) {
        if (!$user) {
            $router->redirect('login');
            exit;
        }
    }

    function requireGuest($user, $router) {
        if ($user) {
            $router->redirect('dashboard');
            exit;
        }
    }

    function requireRole($user, $role, $router) {
        if (!$user || $user['type'] !== $role) {
            $router->redirect('home');
            exit;
        }
    }

    function requireOneRole($user, $roles, $router) {
        if (!$user || !in_array($user['type'], $roles)) {
            $router->redirect('home');
            exit;
        }
    }

    function requireNotRole($user, $role, $router) {
        if ($user && $user['type'] === $role) {
            $router->redirect('home');
            exit;
        }
    }

    function getCurrentUser() {
        if (isset($_SESSION["jwt_token"])) {
            $expiration = getJWTExpiration($_SESSION["jwt_token"]);
            if ($expiration && $expiration < new DateTime()) {
                logout();
            }
        }

        if (isset($_SESSION["connecte"]) && $_SESSION["connecte"] === true) {
            return [
                "id" => $_SESSION["id"],
                "email" => $_SESSION["email"],
                "type" => $_SESSION["type"],
                "jwt_token" => $_SESSION["jwt_token"],
            ];
        }
        return null;
    }

    function getJWTExpiration(string $token): ?DateTime {
        $parts = explode('.', $token);
        if (count($parts) !== 3) {
            return null; // Invalid token format
        }

        $payload = json_decode(base64_decode($parts[1]), true);
        if (!isset($payload['exp'])) {
            return null; // No expiration claim
        }

        return (new DateTime())->setTimestamp($payload['exp']);
    }

    function login(int $id, string $email, string $type, string $jwt) {
        $_SESSION["connecte"] = true; 
        $_SESSION["email"] = $email;
        $_SESSION["type"] = $type;
        $_SESSION["id"] = $id;
        $_SESSION["jwt_token"] = $jwt;
    }

    function logout() {
        if (isset($_SESSION)){
            $_SESSION["connecte"] = false; 
            $_SESSION["email"] = null;
            $_SESSION["type"] = null;
            $_SESSION["id"] = null;

            $cookieFile = '/tmp/intranet_cookies_' . session_id() . '.txt';

            // Supprime le fichier de cookies
            if (file_exists($cookieFile)) {
                unlink($cookieFile);
            }

            // Détruit la session PHP
            session_destroy();
        }
    }