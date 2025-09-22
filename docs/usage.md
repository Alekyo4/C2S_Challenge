# Usage Guide

This document describes the necessary steps to configure the environment, install dependencies, and run the project.

## 1. Prerequisites

Before you begin, ensure you have the following tools installed on your machine:

* **Python 3.12+**
* **Docker** and **Docker Compose**
* **uv**: A Python package and virtual environment manager.
    ```bash
    # Installation command (may vary depending on your system)
    pip install uv
    ```
* **Make**: A command automation utility (usually pre-installed on Linux/macOS systems).

## 2. Setup

Follow the steps below to prepare the project environment.

#### Step 1: Clone the Repository

```bash
git clone https://github.com/Alekyo4/C2S_Challenge
cd C2S_Challenge
```

#### Step 2: Configure Environment Variables

Docker Compose uses an environment file to configure the database. Create a file named `.env.development` in the project root.

```bash
touch .env.development
```

Open the `.env.development` file and add the contents from `.env.example`, replacing the values with your desired configuration.

#### Step 3: Install Dependencies

The project uses `uv` to manage the dependencies listed in `pyproject.toml`. `uv` will create a virtual environment (`.venv`) and install everything required.

```bash
uv sync
```

## 3. Running the Application

With the environment configured, you can start the services. In development mode, the database tables will be created automatically when the server starts.

#### Step 1: Start the Database

The `Makefile` contains a shortcut to start the database container with Docker Compose.

```bash
make up

# Use to view container logs
make logs
```

This command will start the PostgreSQL service in the background.

#### Step 2: Start the Server and Client

You will need two terminals open in the project directory.

**In the first terminal, start the server:**

```bash
# Primary command
uv run task dev server

# Alternative
uv run c2s dev server
```

**In the second terminal, start the client:**

```bash
# Primary command
uv run task client

# Alternative
uv run c2s client
```

## 4. Development vs. Production Environment

There are important differences in how the project is run in each environment.

### Database Creation

  * **Development:** To speed up the setup process, the server is configured to automatically create all tables defined in the ORM (`Base.metadata.create_all()`) on startup if they do not exist.

  * **Production:** Automatic table creation is **disabled** to prevent accidental data loss. In a production environment, it is **mandatory** to use Alembic to manage the database schema.

**Typical Alembic Commands (for Production):**

```bash
# To apply migrations to the database
uv run alembic upgrade head
```

## 5. Stopping the Application

To stop all services that were started (in this case, the database container), use the command from the `Makefile`:

```bash
make down
```

## 6. Development Tasks

The `pyproject.toml` defines several useful tasks for development, which can be executed with `uv run task <task_name>`.

| Action          | Task Name | Description                                                  |
|:----------------|:----------|:-------------------------------------------------------------|
| **Run Tests** | `test`    | Runs the test suite with `pytest`.                           |
| **Check Linting** | `lint`    | Analyzes the code for errors and style issues with `ruff`.     |
| **Format Code** | `format`    | Automatically formats all project code with `ruff format`.   |
| **Populate** | `populate` | Generates fake data for the database |