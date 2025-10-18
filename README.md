# Parenting App Backend

A FastAPI-based backend for a parenting application with AI-powered conversations.

## Features

- FastAPI web framework
- SQLAlchemy ORM with async support
- OpenAI integration for AI conversations
- User authentication and authorization
- RESTful API design
- UV for dependency management

## Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/YOUR_USERNAME/parenting-app-backend.git
   cd parenting-app-backend
   ```

2. **Install UV** (if not already installed):

   ```bash
   # Windows
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

3. **Install dependencies:**

   ```bash
   uv sync
   ```

4. **Set up environment variables:**

   ```bash
   copy .env.example .env
   # Edit .env with your actual values
   ```

5. **Run the application:**
   ```bash
   uv run uvicorn app.main:app --reload
   ```

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── api/                 # API routes
│   ├── core/                # Core functionality (config, security)
│   ├── db/                  # Database models and operations
│   ├── services/            # Business logic services
│   └── schemas/             # Pydantic models
├── scripts/                 # Utility scripts
├── pyproject.toml          # UV project configuration
└── .env.example            # Environment variables template
```

## API Documentation

Once running, visit:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

```bash
# Format code
uv run black .
uv run ruff check . --fix

# Run tests
uv run pytest

# Run with auto-reload
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## License

MIT License
