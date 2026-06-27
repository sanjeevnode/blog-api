# Blog API

A production-ready FastAPI backend containerized with Docker, featuring PostgreSQL, Redis cache, Mailpit SMTP sink, and RustFS S3-compatible storage.

---

## Service Endpoints (Host Machine)

When the stack is running via `docker compose up`, the following ports and user interfaces are exposed on your host machine:

| Service | Port (Host) | URL / Connection |
| :--- | :--- | :--- |
| **FastAPI** | `7210` | [http://localhost:7210/docs](http://localhost:7210/docs) |
| **PostgreSQL** | `7211` | `postgresql://localhost:7211` |
| **Mailpit UI** | `7212` | [http://localhost:7212](http://localhost:7212) |
| **Redis** | `7213` | `redis://localhost:7213` |
| **RustFS S3 API** | `7214` | [http://localhost:7214](http://localhost:7214) |
| **RustFS Console** | `7215` | [http://localhost:7215](http://localhost:7215) |
| **pgAdmin** | `7217` | [http://localhost:7217](http://localhost:7217) |

---

## Local Development Commands

### Start Backing Services (Database, Cache, Object Storage, Mail)
```bash
docker compose up -d db redis mailpit rustfs pgadmin
```

### Build & Run the FastAPI Server
```bash
docker compose up -d --build api
```

### Run Migrations Locally
```bash
uv run alembic upgrade head
```