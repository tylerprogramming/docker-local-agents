# Docker Local Agents

A production-ready, containerized FastAPI application with background task processing, AI model serving, and persistent storage. This project leverages Docker Compose to orchestrate a modern stack for scalable, automated workflows.

---

## Features

- **FastAPI**: High-performance Python web API.
- **Celery**: Distributed task queue for background and scheduled jobs.
- **PostgreSQL**: Reliable relational database.
- **Redis**: Fast in-memory broker for Celery.
- **Ollama**: Local AI model server for LLM inference.
- **CrewAI**: Agentic workflow orchestration (via `crewai` and `crewai-tools`).
- **Automated Model Management**: Scripts for managing Ollama models.

---

## Architecture

```
[FastAPI] <--> [PostgreSQL]
     |              ^
     v              |
 [Celery Worker]    |
     |              |
     v              |
   [Redis] <--------+
     |
     v
 [Ollama]
```

- **FastAPI** serves as the main API and interacts with the database and Ollama.
- **Celery Worker** runs background and scheduled tasks, including database checks and agentic workflows.
- **Ollama** provides local LLM inference, managed via helper scripts.
- **Celery Beat** schedules periodic tasks (e.g., database checks every minute).

---

## Getting Started

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Git](https://git-scm.com/)

### Quickstart

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>
   ```

2. **Build and start all services**
   ```bash
   docker compose up --build
   ```

3. **(Optional) Pull a default Ollama model**
   ```bash
   docker exec ollama ollama pull qwen3:1.7b
   ```

4. **Access the API**
   - FastAPI: [http://localhost:8000](http://localhost:8000)
   - Ollama: [http://localhost:11434](http://localhost:11434)

5. **Stop all services**
   ```bash
   docker compose down
   ```

---

## Service Details

### FastAPI

- Main entrypoint: `app/main.py`
- Auto-reloads on code changes (if configured)
- Connects to PostgreSQL and Redis

### Celery

- Worker and Beat services for background and scheduled tasks
- Example tasks: add, multiply, periodic DB check with agentic workflow

### Ollama

- Local LLM server, managed via `ollama-commands.sh` and `startup-ollama.sh`
- Pull, run, and manage models interactively

### PostgreSQL

- User: `postgres`
- Password: `postgres`
- Database: `tododb`
- Data persisted in Docker volume

### Redis

- Used as broker and result backend for Celery

---

## Model Management

Use the provided scripts to manage Ollama models:

- **List models**
  ```bash
  ./ollama-commands.sh list
  ```
- **Pull a model**
  ```bash
  ./ollama-commands.sh pull <model-name>
  ```
- **Run a model interactively**
  ```bash
  ./ollama-commands.sh run <model-name>
  ```
- **Remove a model**
  ```bash
  ./ollama-commands.sh remove <model-name>
  ```
- **Show logs**
  ```bash
  ./ollama-commands.sh logs
  ```

---

## Environment Variables

Set in `docker-compose.yml`:

- `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND`: Redis connection
- `DATABASE_URL`: PostgreSQL connection
- `OLLAMA_HOST` and `OLLAMA_PORT`: Ollama service

---

## Development

- Python dependencies in `requirements.txt`
- Dockerfile for reproducible builds
- All code in the `app/` directory (see `main.py`, `models.py`, `database.py`, and agentic logic in `todos_crew/`)

---

## Example API Usage

- Add your FastAPI endpoints in `app/main.py`
- Celery tasks in `tasks.py` (e.g., `add_task`, `multiply_task`, `check_database_task`)
- Scheduled DB checks trigger agentic workflows using CrewAI

---

## Notes

- Data for PostgreSQL and Ollama is persisted in Docker volumes.
- The system is designed for local development and experimentation with agentic workflows and LLMs.
- You can extend the agent logic in `app/todos_crew/`.

---