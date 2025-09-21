# Project Architecture

## 1. Overview

This document describes the software architecture for the project, an asynchronous client-server application. The goal is to establish a robust and modular network communication system, where the server processes requests, interacts with a database, and communicates with Generative Artificial Intelligence services.

The architecture is heavily based on **Manual Dependency Injection** and **Separation of Concerns (SoC)**, with a directory structure that isolates layers such as `client`, `server`, `database`, and `common`.

## 2. Technology Stack

* **Language:** Python 3.11+
* **Asynchronous Programming:** `asyncio`
* **Database ORM:** `SQLAlchemy`
* **Communication:** `asyncio.streams` TCP/IP Sockets
* **Dependency Injection:** Custom framework with Factory Functions (Composition Root Pattern)
* **Artificial Intelligence:** Integration with Generative Models (e.g., Google Gemini)
* **Command-Line Interface:** `cli.py` (`Typer`)

## 3. Directory Structure

The project structure is modular and domain-oriented, facilitating maintenance and testability.

```
c2s_challenge/
├── client/
│   └── __init__.py         # Contains the `make_client_async` factory
├── common/
│   ├── protocol/
│   └── setting/
└── server/
    ├── __init__.py         # Contains the `make_server_async` factory
    ├── agent/              # Business logic and AI integration (AgentAI)
    ├── database/           # Data access layer (ORM, Repository)
    ├── event/              # Event routing (Router, Handlers)
    └── server.py
```

## 4. Architectural Patterns and Key Concepts

#### 4.1. Manual Dependency Injection (Composition Root Pattern)

The architecture employs Dependency Injection (DI) manually. This pattern is centralized in the `__init__.py` files of the `server` and `client` modules.

* **Factory Functions (`make_server_async`):** These functions are responsible for instantiating all classes and their dependencies, building the complete object graph, and manually "injecting" the instances into the constructors.
* **Entry Point (`cli.py`):** The CLI is the sole component responsible for calling these factory functions to assemble the application and start its lifecycle.

#### 4.2. Router-Handler Pattern (Event Dispatcher)

The server's core operates on a dispatcher pattern to process requests.

* **`Server` (`server.py`):** Manages the connection and delegates processing.
* **`EventRouter` (`event/router.py`):** Acts as a central dispatcher that inspects the request's event type and invokes the appropriate `Handler`.
* **`EventHandler` (`event/handler.py`):** Small, focused classes, each responsible for the logic of a single event type.

#### 4.3. `AgentAI` - Artificial Intelligence Layer

The `AgentAI` component (`server/agent`) encapsulates all logic for interacting with the generative language model. It abstracts the complexity of formatting prompts, calling the external API, and processing responses, providing simple methods for the `Handlers` to use.

## 5. Execution Flow

#### 5.1. Server Component Diagram

```mermaid
graph TD
    subgraph "Initialization"
        CLI["cli.py"]
        Factory["server/__init__.py (factory)"]
    end

    subgraph "Injected Components"
        Repo["Repository"]
        AgentAI["AgentAI"]
        Handlers["EventHandlers"]
        Router["EventRouter"]
    end

    subgraph "Request Flow"
        Server["Server (Socket Loop)"]
        HandlerImpl["Specific EventHandler"]
        RepoImpl["Repository"]
        AgentAIImpl["AgentAI"]
        DB["Database"]
        GenAI["AI Service (External)"]
    end

    CLI -->|calls| Factory
    Factory -- builds and injects --> Server & Router & Handlers & Repo & AgentAI

    Server -- forwards to --> Router
    Router -- dispatches to --> HandlerImpl
    HandlerImpl -- uses --> RepoImpl
    HandlerImpl -- uses --> AgentAIImpl
    RepoImpl -- interacts with --> DB
    AgentAIImpl -- interacts with --> GenAI
```

#### 5.2. CRUD Request Flow (Sequence Diagram)

```mermaid
sequenceDiagram
    participant Client
    participant Server
    participant Router
    participant GetVehicleHandler as Handler
    participant VehicleRepository as Repository
    participant Database

    Client->>+Server: Sends request (bytes)
    Server->>Router: handle(Request DTO)
    activate Router
    Router->>GetVehicleHandler: handle(Request DTO)
    activate GetVehicleHandler
    GetVehicleHandler->>VehicleRepository: find_by_id(...)
    activate VehicleRepository
    VehicleRepository->>Database: executes query
    Database-->>VehicleRepository: returns result
    VehicleRepository-->>GetVehicleHandler: Returns VehicleORM
    deactivate VehicleRepository
    GetVehicleHandler-->>Router: Returns Response DTO
    deactivate GetVehicleHandler
    Router-->>-Server: Returns Response DTO
    Server-->>-Client: Sends response (bytes)
```

#### 5.3. AI-Powered Request Flow (Sequence Diagram)

```mermaid
sequenceDiagram
    participant Client
    participant Server
    participant Router
    participant AIChatHandler as Handler
    participant AgentAI
    participant GenAI as "AI Service (External)"

    Client->>+Server: Sends question (bytes)
    Server->>Router: handle(Request DTO)
    activate Router
    Router->>AIChatHandler: handle(Request DTO)
    activate AIChatHandler
    AIChatHandler->>AgentAI: get_chat_response(prompt)
    activate AgentAI
    AgentAI->>GenAI: calls model API
    GenAI-->>AgentAI: returns model response
    AgentAI-->>AIChatHandler: Returns processed text
    deactivate AgentAI
    AIChatHandler-->>Router: Returns Response DTO
    deactivate AIChatHandler
    Router-->>-Server: Returns Response DTO
    Server-->>-Client: Sends response (bytes)
```

#### 5.4. Server Initialization (Sequence Diagram)

```mermaid
sequenceDiagram
    participant CLI as "cli.py"
    participant Factory as "server/__init__.py (factory)"
    participant Server as "Server Instance"

    CLI->>+Factory: make_server_async()
    Note over Factory: Building the dependency graph
    Factory->>Factory: new AgentAI()
    Factory->>Factory: new Repository()
    Factory->>Factory: new AIHandler(agent_ai)
    Factory->>Factory: new EventRouter(handlers={...})
    Factory->>Server: new AsyncServer(router, ...)
    Factory-->>-CLI: Returns complete Server instance
    
    CLI->>Server: server.listen()
    activate Server
```