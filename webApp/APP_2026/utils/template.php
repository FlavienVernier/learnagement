<?php

declare(strict_types=1);

class Template
{
    private string $viewsPath;
    private string $componentsPath;
    private string $assetsPath;
    private array $globals = [];

    private ?string $parentLayout = null;
    private array $slots = [];
    private ?string $currentSlot = null;

    public ?Router $router;

    public function __construct(
        string $viewsPath,
        ?Router $router = null,
        string $componentsPath = '',
        string $assetsPath = ''
        ) {
            $this->router = $router;
            $this->viewsPath = rtrim($viewsPath, '/');
            $this->assetsPath = rtrim($assetsPath, '/');
            $this->componentsPath = $componentsPath
                ? rtrim($componentsPath, '/')
                : $this->viewsPath . '/components';
    }

    public function share(string $key, mixed $value): void
    {
        $this->globals[$key] = $value;
    }

    public function render(string $view, array $data = []): string
    {
        $this->parentLayout = null;
        $this->slots = [];
        $this->currentSlot = null;

        $content = $this->renderFile($this->resolvePath($view), $data);

        // Remonte la chaîne de layouts jusqu'au sommet
        while ($this->parentLayout !== null) {
            $layout = $this->parentLayout;
            $this->parentLayout = null;
            $content = $this->renderFile($this->resolvePath($layout), $data);
        }

        return $content;
    }

    public function extend(string $layout): void
    {
        $this->parentLayout = $layout;
    }

    public function slot(string $name, string $default = ''): string
    {
        return $this->slots[$name] ?? $default;
    }

    public function startSlot(string $name): void
    {
        $this->currentSlot = $name;
        ob_start();
    }

    public function endSlot(): void
    {
        if ($this->currentSlot === null) {
            throw new RuntimeException('endSlot() appelé sans startSlot().');
        }
        $this->slots[$this->currentSlot] = ob_get_clean();
        $this->currentSlot = null;
    }

    public function component(string $name, array $props = []): string
    {
        $path = $this->componentsPath . '/' . str_replace('.', '/', $name) . '.php';
        if (!file_exists($path)) {
            throw new RuntimeException("Composant introuvable : {$path}");
        }
        $props['uuid'] = uniqid($name . '_');
        return $this->renderFile($path, $props);
    }

    public function asset(string $path): string
    {
        $path = $this->assetsPath . '/' . ltrim($path, '/');
        return $this->renderFile($path, []);
    }

    public function partial(string $view, array $data = []): string
    {
        return $this->renderFile($this->resolvePath($view), $data);
    }

    public function attrs(array $attrs): string
    {
        return implode(' ', array_map(
            fn($k, $v) => sprintf('%s="%s"', $k, htmlspecialchars($v, ENT_QUOTES)),
            array_keys($attrs),
            $attrs
        ));
    }

    public function e(mixed $value): string
    {
        return htmlspecialchars((string) $value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
    }

    // -------------------------------------------------------------------------
    // Internals
    // -------------------------------------------------------------------------

    private function resolvePath(string $view): string
    {
        $path = $this->viewsPath . '/' . str_replace('.', '/', $view);
        if (!str_ends_with($path, '.php')) {
            $path .= '.php';
        }
        return $path;
    }

    private function renderFile(string $__path, array $__data): string
    {
        if (!file_exists($__path)) {
            throw new RuntimeException("Template introuvable : {$__path}");
        }

        $t = $this;

        extract(array_merge($this->globals, $__data), EXTR_SKIP);

        ob_start();
        include $__path;
        return ob_get_clean();
    }
}