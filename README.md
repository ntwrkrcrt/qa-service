# Q&A API Service

A REST API service for questions and answers built with FastAPI and PostgreSQL.

## Project Description

This application provides a REST API for creating, retrieving, and deleting questions and answers. Users can create questions, answer them, and manage content.

### Key Features

- ✅ Create and retrieve questions
- ✅ Add answers to questions
- ✅ Cascade deletion (deleting a question removes all its answers)
- ✅ Input data validation
- ✅ Comprehensive logging
- ✅ Full test coverage

## Tech Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy (async)
- **Migrations**: Alembic
- **Testing**: pytest
- **Logging**: Loguru
- **Containerization**: Docker + Docker Compose

## Data Models

### Question
- `id`: int - unique identifier
- `text`: str - question text
- `created_at`: datetime - creation timestamp

### Answer
- `id`: int - unique identifier
- `question_id`: int - reference to question
- `user_id`: str - user identifier
- `text`: str - answer text
- `created_at`: datetime - creation timestamp

## API Endpoints

### Questions
- `GET /question/` - get list of all questions
- `POST /question/` - create new question
- `GET /question/{id}` - get question with all answers
- `DELETE /question/{id}` - delete question (and all its answers)
- `POST /question/{id}/answers/` - add answer to question

### Answers
- `GET /answers/{id}` - get specific answer
- `DELETE /answers/{id}` - delete answer

### Health
- `GET /health` - service health check

## Quick Start

### Prerequisites

- Docker
- Docker Compose

### Running the Application

1. Clone the repository:

2. Start the application:
```bash
docker-compose up --build
```

The application will be available at: http://localhost:8000

API documentation (Swagger): http://localhost:8000/docs

### Running Tests

```bash
# Run all tests

./run_tests.sh
```

## Environment Variables

Create a `.env` file with the following variables:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/qa_db
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=10
DB_POOL_TIMEOUT=30
DB_ECHO=false
POSTGRES_PASSWORD=postgres
```

## API Usage Examples

### Create a question
```bash
curl -X POST "http://localhost:8000/question/" \
  -H "Content-Type: application/json" \
  -d "text=Nice question?"
```

### Get all questions
```bash
curl -X GET "http://localhost:8000/question/"
```

### Add an answer
```bash
curl -X POST "http://localhost:8000/question/1/answers/" \
  -H "Content-Type: application/json" \
  -d "text=idk&user_id=user123"
```

### Get question with answers
```bash
curl -X GET "http://localhost:8000/question/1"
```

### Creating Migrations

```bash
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

## Testing

The project includes comprehensive test coverage:

- API endpoint tests
- Business logic tests
- Validation tests
- Cascade deletion tests

Run tests:
```bash
pytest tests/ -v
```

## Monitoring and Logging

The application uses Loguru for logging:
- Request and response logging
- Slow request tracking (>5 seconds)
- Error logging with stack traces

## License

MIT License