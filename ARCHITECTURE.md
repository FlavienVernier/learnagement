# Learnagement architecture

This diagram describes the Docker Compose configuration generated for one instance. It is a static view: it does not prove that services start or communicate at runtime. No Kubernetes manifest is present on this branch.

## Docker Compose topology

<!-- mermaid-checked: no \n, no em-dash/en-dash, no {} in labels, subgraphs are id["label"], arrows are -->|"label"|, all subgraphs closed by end, ids unique -->
```mermaid
flowchart LR
    U["Navigateur"]
    CAS["CAS externe"]

    subgraph SERVICES["Services Compose sélectionnés pour l'instance"]
        MYSQL["data_mysql_INSTANCE"]
        PMA["phpmyadmin_INSTANCE"]
        API["backend_python_INSTANCE"]
        PHP["front_php_INSTANCE"]
        NEXT["front_nextjs_INSTANCE"]
        DASH["front_dashplotly_INSTANCE"]
        DB[("Compose volume learnagement_persistent_db_INSTANCE")]
    end

    FRONTNET["Réseau bridge learnagement_front_INSTANCE"]
    BACKNET["Réseau bridge learnagement_back_INSTANCE"]
    SOCKETNET["Socket network key learnagement_socket_proxy_INSTANCE"]

    subgraph OPTIONAL["Proxy optionnel si Traefik est sélectionné"]
        SOCKET["socket_proxy_INSTANCE"]
        TRAEFIK["reverse_proxy_traefik_INSTANCE"]
    end

    PHP -.->|"member"| FRONTNET
    NEXT -.->|"member"| FRONTNET
    DASH -.->|"member"| FRONTNET
    API -.->|"member"| FRONTNET
    API -.->|"member"| BACKNET
    MYSQL -.->|"member"| BACKNET
    PMA -.->|"member"| BACKNET
    TRAEFIK -.->|"member"| FRONTNET
    TRAEFIK -.->|"member"| BACKNET
    TRAEFIK -.->|"member"| SOCKETNET
    SOCKET -.->|"member"| SOCKETNET

    MYSQL -->|"stores data"| DB
    MYSQL -.->|"health gate: service_healthy"| API
    MYSQL -.->|"health gate: service_healthy"| PMA
    API -.->|"health gate: service_healthy"| PHP
    API -.->|"health gate: service_healthy"| NEXT
    API -.->|"health gate: service_healthy"| DASH
    SOCKET -.->|"service_healthy prerequisite"| TRAEFIK
    TRAEFIK -.->|"health gate when selected"| PHP
    TRAEFIK -.->|"health gate when selected"| PMA

    U -->|"published port when no proxy"| PHP
    U -->|"published port when proxy is off"| NEXT
    U -->|"published port when proxy is off"| DASH
    U -->|"loopback port when no proxy"| PMA
    U -->|"HTTPS route when proxy selected"| TRAEFIK
    TRAEFIK -->|"HTTPS route"| PHP
    TRAEFIK -->|"HTTPS route"| DASH
    TRAEFIK -->|"HTTPS route with BasicAuth"| PMA

    PHP -->|"HTTP dev; HTTPS configured prod"| API
    DASH -->|"HTTP dev; HTTPS configured prod"| API
    NEXT -->|"configured scheme; TLS trust unverified"| API
    API -->|"MySQL TCP 3306; TLS not enforced"| MYSQL
    PMA -->|"MySQL protocol; TLS not configured here"| MYSQL
    U -.->|"CAS login if configured"| CAS
    PHP -.->|"CAS_HOST serviceValidate; scheme is configurable"| CAS
```

MySQL uses TCP 3306 only on the Back network; Compose does not publish that port on the host. For health dependencies, arrows point from the required healthy service to the service it gates. The socket-proxy network and MySQL volume use Compose keys; Docker applies the project scope where no explicit network or volume name is set.