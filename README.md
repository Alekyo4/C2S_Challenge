# C2S Challenge

A back-end challenge project that implements an asynchronous client-server application in Python, featuring interaction with a PostgreSQL database, Generative AI integration, and a fully containerized environment with Docker.

-----

## 🚀 Getting Started

To set up the environment, install dependencies, and run the project, please follow our detailed guide:

➡️ **[Usage and Execution Guide (docs/usage.md)](https://www.google.com/search?q=docs/usage.md)**

-----

## 📖 About the Project

This project was developed as a technical challenge to demonstrate skills in software architecture, back-end development, and programming best practices. The application consists of an asynchronous TCP server that manages connections from multiple clients, processes events, performs CRUD operations on a database, and interacts with a generative language model to provide intelligent responses.

The architecture was carefully planned to be modular, testable, and scalable, utilizing patterns such as Manual Dependency Injection (Composition Root) and the Router-Handler pattern for event dispatching. For an in-depth analysis, please refer to the architecture document.

### ✨ Key Features

  * **Asynchronous Client-Server Communication:** Uses `asyncio` to efficiently manage multiple connections.
  * **Data Persistence:** Integration with PostgreSQL using SQLAlchemy ORM and schema management with Alembic for production.
  * **Generative AI Integration:** Capable of connecting to AI services (like Google Gemini) to process and respond to requests.
  * **Containerized Environment:** Uses Docker and Docker Compose to ensure a consistent and isolated development and production environment.

-----

## 📚 Documentation

For an in-depth understanding of the project, please refer to the following documents in the `/docs` folder:

  * **🏛️ [Project Architecture (docs/architecture.md)](https://www.google.com/search?q=docs/architecture.md)**
    <br>A complete explanation of the design patterns, execution flow, component diagrams, and the overall software structure.

  * **🗄️ [Database Model (docs/database.md)](https://www.google.com/search?q=docs/database.md)**
    <br>Entity-Relationship Diagram (ERD) and details about the tables and columns.

  * **📄 [Usage and Execution Guide (docs/usage.md)](https://www.google.com/search?q=docs/usage.md)**
    <br>Detailed instructions on how to set up the environment, run the project, and all available development commands.

## 📝 License

This project is distributed under the MIT License. See the `LICENSE` file for more details.