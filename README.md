# Microshop FastAPI

A FastAPI-based microshop application with user management and API endpoints.

## Setup

1. Activate the virtual environment:

```bash
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies using Poetry:

```bash
poetry install
```

## Running the Application

Start the development server:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## API Documentation

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Testing

Run tests with pytest:

```bash
pytest
```
