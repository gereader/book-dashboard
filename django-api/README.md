# Django API-First Architecture

This is the "correct way" with an API-first approach that provides separation of concerns and reusability.

## How It Works

1. **API Endpoint** (`/api/reading-stats/`) returns JSON data
2. **Service Layer** (`hardcover_service.py`) handles all Hardcover API interactions
3. **Frontend** fetches from the API using JavaScript
4. **Complete separation** - API can be consumed by web, mobile, CLI, or any other client

## Architecture Benefits

### 1. **Separation of Concerns**
- **Service Layer**: Handles Hardcover API calls
- **API View**: Processes requests, returns JSON
- **Frontend**: Fetches and displays data

Each layer has a single responsibility.

### 2. **Reusability**
The API can be consumed by:
- Web frontend (what we built)
- Mobile apps (iOS, Android)
- CLI tools
- Other services
- Third-party integrations

No code duplication needed!

### 3. **Flexibility**
Query parameters allow dynamic filtering:
```
/api/reading-stats/                                    # Current year
/api/reading-stats/?start_date=2024-01-01              # Specific year
/api/reading-stats/?start_date=2024-01-01&end_date=2024-06-30  # Date range
```

### 4. **Easy to Test**
- Service layer can be tested independently
- API can be tested with HTTP requests
- Frontend can be tested with mocked API responses

### 5. **Scalability**
- Add caching at the API layer
- Rate limiting
- Background jobs for data updates
- API versioning (`/api/v2/reading-stats/`)

## API Response Format
```json
{
  "currently_reading": [
    {
      "title": "Fight and Flight",
      "author": "Scott Meyer",
      "pages": null
    }
  ],
  "books_read_count": 26,
  "date_range": {
    "start": "2025-01-01",
    "end": "2025-12-31"
  },
  "goal": {
    "target": 12,
    "progress": 26,
    "percentage": 217,
    "description": "2025 Reading Goal",
    "start_date": "2025-01-01",
    "end_date": "2025-12-31"
  }
}
```

## Running This Version
```bash
# Install dependencies
uv sync

# Add your Hardcover token to .env
echo "HARDCOVER_TOKEN=Bearer your_token_here" > .env

# Run migrations (if needed in the future)
uv run python manage.py migrate

# Start the server
uv run python manage.py runserver
```

**Visit the dashboard:**
- Web UI: `http://localhost:8000/`
- API endpoint: `http://localhost:8000/api/reading-stats/`

## Testing the API

### Using curl:
```bash
# Current year stats
curl http://localhost:8000/api/reading-stats/

# 2024 stats
curl "http://localhost:8000/api/reading-stats/?start_date=2024-01-01&end_date=2024-12-31"
```

### Using Python:
```python
import requests

response = requests.get('http://localhost:8000/api/reading-stats/')
data = response.json()
print(f"Books read: {data['books_read_count']}")
```


## Why This Is Better

Compare this to `../flask-antipattern/` - the API-first approach:
- Can be consumed by any client
- Supports dynamic filtering via query params
- Easy to test and extend
- Scales better (caching, rate limiting, etc.)
- Frontend and backend are decoupled

## Future Enhancements

With this architecture, you could easily add:
- Authentication/Authorization (JWT tokens)
- Additional endpoints (book search, reading history, etc.)
- GraphQL layer on top of REST
- WebSocket support for real-time updates
- Mobile app using the same API
- CLI tool for quick stats in terminal