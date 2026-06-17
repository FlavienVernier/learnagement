<?php

class Alert {
    public static function success($message) {
        self::add('success', $message);
    }

    public static function error($message) {
        self::add('error', $message);
    }

    public static function info($message) {
        self::add('info', $message);
    }

    private static function add(string $type, string $message): void {
        if (session_status() === PHP_SESSION_NONE)
            session_start();

        $_SESSION['toasts'][] = ['type' => $type, 'message' => $message];
    }

    public static function flush() {
        if (session_status() === PHP_SESSION_NONE)
            session_start();

        $toasts = $_SESSION['toasts'] ?? [];
        unset($_SESSION['toasts']);
        return $toasts;
    }
}