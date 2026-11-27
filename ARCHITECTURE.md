# Learnagement architecture

> Objectif : présenter les services Learnagement, leurs flux et les limites entre la configuration déclarée et le runtime.

Cette vue résume la topologie Learnagement telle qu'elle est préparée dans le dépôt. Elle décrit les interfaces PHP, Next.js et Dash, le Backend Python, MySQL, les réseaux Front/Back, phpMyAdmin et les intégrations externes confirmées. Traefik, le socket proxy et Groq sont représentés seulement selon leur usage réel ou leur caractère optionnel.

Le diagramme est une description statique de Docker Compose et ne prouve ni un démarrage runtime, ni les communications réelles. Le socle Kubernetes présent dans le dépôt est préliminaire et n'a pas été appliqué à un cluster.

## Docker Compose topology

<!-- mermaid-checked: no \n, no em-dash/en-dash, no {} in labels, subgraphs are id["label"], arrows are -->|"label"|, all subgraphs closed by end, ids unique -->
```mermaid
flowchart LR
    Browser["Navigateur"]

    subgraph Interfaces["Interfaces utilisateur"]
        PHP["PHP"]
        Next["Next.js"]
        Dash["Dash"]
    end

    Backend["Backend Python"]
    MySQL[("MySQL")]
    PMA["phpMyAdmin"]
    Volume[("Volume MySQL Docker")]

    FrontNet["Réseau Front Docker"]
    BackNet["Réseau Back Docker"]
    SocketNet["Réseau socket proxy"]

    subgraph ProxyOptionnel["Proxy optionnel"]
        Traefik["Traefik"]
        SocketProxy["Socket proxy Docker"]
    end

    CAS["CAS externe"]
    Groq["API Groq"]

    PHP -.->|"membre du réseau"| FrontNet
    Next -.->|"membre du réseau"| FrontNet
    Dash -.->|"membre du réseau"| FrontNet
    Backend -.->|"membre du réseau"| FrontNet
    Backend -.->|"membre du réseau"| BackNet
    MySQL -.->|"membre du réseau"| BackNet
    PMA -.->|"membre du réseau"| BackNet
    Traefik -.->|"membre du réseau"| FrontNet
    Traefik -.->|"membre du réseau"| BackNet
    Traefik -.->|"membre du réseau"| SocketNet
    SocketProxy -.->|"membre du réseau"| SocketNet

    Browser -->|"port direct sans proxy"| PHP
    Browser -->|"port direct sans proxy"| Next
    Browser -->|"port direct sans proxy"| Dash
    Browser -->|"port local ou route protégée"| PMA
    Browser -->|"HTTPS si configuré"| Traefik
    Traefik -->|"route HTTPS"| PHP
    Traefik -->|"route HTTPS"| Dash
    Traefik -->|"route HTTPS avec BasicAuth"| PMA

    PHP -->|"HTTP ou HTTPS configuré"| Backend
    Next -->|"HTTP ou HTTPS configuré"| Backend
    Dash -->|"HTTP ou HTTPS configuré"| Backend
    Backend -->|"TCP 3306"| MySQL
    PMA -->|"administration SQL"| MySQL
    MySQL -->|"données persistantes"| Volume
    PHP -->|"validation de ticket"| CAS
    Dash -->|"requêtes chatbot"| Groq

    MySQL -.->|"service healthy requis"| Backend
    MySQL -.->|"service healthy requis"| PMA
    Backend -.->|"service healthy requis"| PHP
    Backend -.->|"service healthy requis"| Next
    Backend -.->|"service healthy requis"| Dash
    SocketProxy -.->|"service healthy requis"| Traefik
    Traefik -.->|"service healthy requis"| PHP
    Traefik -.->|"service healthy requis"| PMA

    classDef ui fill:#DBEAFE,stroke:#1D4ED8,color:#1E3A8A,stroke-width:2px;
    classDef backend fill:#DCFCE7,stroke:#15803D,color:#14532D,stroke-width:2px;
    classDef data fill:#FEF3C7,stroke:#B45309,color:#78350F,stroke-width:2px;
    classDef network fill:#E5E7EB,stroke:#4B5563,color:#111827,stroke-width:2px;
    classDef optional fill:#F3E8FF,stroke:#7E22CE,color:#581C87,stroke-width:2px;
    classDef external fill:#FCE7F3,stroke:#BE185D,color:#831843,stroke-width:2px;

    class Browser,PHP,Next,Dash ui;
    class Backend backend;
    class MySQL,Volume data;
    class FrontNet,BackNet,SocketNet network;
    class PMA,Traefik,SocketProxy optional;
    class CAS,Groq external;
```

**Légende :** bleu = interfaces; vert = Backend; ambre = MySQL et persistance; gris = réseaux; violet = composants optionnels; rose = intégrations externes. Les traits pleins représentent les appels et les données; les pointillés représentent l'appartenance réseau ou une dépendance de santé Compose.

Le Backend est connecté aux deux réseaux; MySQL et phpMyAdmin sont sur Back. Le port MySQL n'est pas publié sur l'hôte. Groq est appelé directement par le chatbot Dash; aucun service IA autonome ni Ollama n'est représenté comme composant Learnagement confirmé.