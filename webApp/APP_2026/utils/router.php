<?php
    class Router {
        private string $baseURI;
        private array $routes = [];
        private array $namedRoutes = [];

        public function __construct(string $baseURI = '') {
            $this->baseURI = $baseURI;
        }

        private function addRoute(string $method, string $path, string $name, callable $handler): void {
            $this->routes[$method][$path] = $handler;
            $this->namedRoutes[$name] = $path;
        }

        public function get(string $path, string $name, callable $handler): void
        {
            $this->addRoute('GET', $path, $name, $handler);
        }

        public function post(string $path, string $name, callable $handler): void
        {
            $this->addRoute('POST', $path, $name, $handler);
        }

        public function put(string $path, string $name, callable $handler): void
        {
            $this->addRoute('PUT', $path, $name, $handler);
        }

        public function delete(string $path, string $name, callable $handler): void
        {
            $this->addRoute('DELETE', $path, $name, $handler);
        }

        public function patch(string $path, string $name, callable $handler): void
        {
            $this->addRoute('PATCH', $path, $name, $handler);
        }

        public function href(string $name, array $params = []): string {
            if (!isset($this->namedRoutes[$name])) {
                throw new Exception("Route not found: $name");
            }
            
            $path = $this->namedRoutes[$name];

            // Remplace chaque :param par sa valeur
            $path = preg_replace_callback(
                '/:([a-z_]+)/',
                function ($matches) use ($params, $name) {
                    $key = $matches[1];
                    if (!isset($params[$key])) {
                        throw new \InvalidArgumentException("Paramètre '{$key}' manquant pour la route '{$name}'.");
                    }
                    return $params[$key];
                }
            ,$path);

            return $this->baseURI . $path;

        }

        public function redirect(string $name, array $params = []): void {
            header('Location: ' . $this->href($name, $params));
            exit;
        }

        public function run(): void
        {
            $method = $_SERVER['REQUEST_METHOD'];
            $uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
            $uri = substr($uri, strlen($this->baseURI));

            foreach ($this->routes[$method] ?? [] as $path => $handler) {
                $pattern = $this->toRegex($path);
                if (preg_match($pattern, $uri, $matches)) {
                    $params = array_filter($matches, 'is_string', ARRAY_FILTER_USE_KEY);
                    $handler($params);
                    return;
                }
            }

            http_response_code(404);
            echo '404 Not Found';
        }

        private function toRegex(string $path): string
        {
            $pattern = preg_replace('/:([a-z_]+)/', '(?P<$1>[^/]+)', $path);
            return '#^' . $pattern . '$#';
        }
    }