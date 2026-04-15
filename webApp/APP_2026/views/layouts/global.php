<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= $t->e($t->slot('title', 'Learnagement')) ?></title>
    <link rel="icon" type="image/png" sizes="32x32" href="/APP_2026/assets/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/APP_2026/assets/favicon-16x16.png">
    <link rel="icon" href="/APP_2026/assets/favicon.ico">
    <!-- Using CND -->
    <!-- Tailwindcsss -->
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <!-- Flowbite -->
    <link href="https://cdn.jsdelivr.net/npm/flowbite@4.0.1/dist/flowbite.min.css" rel="stylesheet" />
    <!-- Extension -->
    <link rel="stylesheet" href="/APP_2026/theme/theme.css">
    <link rel="stylesheet" href="/APP_2026/theme/tailwind.extension.css">
    <?= $t->slot('style.top') ?>
</head>
<body>
    <?= $t->slot('body') ?>
    <script src="https://cdn.jsdelivr.net/npm/flowbite@4.0.1/dist/flowbite.min.js"></script>
</body>
</html>