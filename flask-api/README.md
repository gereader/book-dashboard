# Flask API-First Architecture

This demonstrates that Flask can do API-first architecture well.
The issue with `../flask-antipattern/` isn't specific to Flask, but instead the tightly-coupled design.

## How It Works

1. **API Endpoint** (`/api/reading-stats`) returns JSON data
2. **Service Layer** (`hardcover_service.py`) handles all Hardcover API interactions  
3. **Frontend** (`/`) serves HTML that fetches from the API using JavaScript
4. **Complete separation** - API and frontend are decoupled

## Key Differences from flask-antipattern

### flask-antipattern (BAD):
```python
@app.route('/')
def dashboard():
    data = get_reading_data()  # Route calls script directly
    return render_template('dashboard.html', data=data)  # Returns HTML only
```

**Problems:**
- Tightly coupled
- Can't get JSON
- Hard to reuse

### flask-api (GOOD):
```python
@app.route('/api/reading-stats', strict_slashes=False)
def api_reading_stats():
    data = service.get_reading_stats()
    return jsonify(data)  # Returns JSON!

@app.route('/')
def dashboard():
    return render_template('dashboard.html')  # Just serves HTML
```

**Benefits:**
- API returns JSON
- Frontend fetches via JavaScript
- Can be used by any client

## Architecture
```
Frontend (HTML/JS)
      ↓ fetch()
API Endpoint (/api/reading-stats)
      ↓
Service Layer (hardcover_service.py)
      ↓
Hardcover GraphQL API
```

## Running This Version
```bash
# Install dependencies
uv sync

# Add your Hardcover token to .env
echo "HARDCOVER_TOKEN=Bearer your_token_here" > .env

# Start the server
uv run python main.py
```

**Visit the dashboard:**
- Web UI: `http://localhost:5001/`
- API endpoint: `http://localhost:5001/api/reading-stats`

## API Examples

### Using curl:
```bash
# Current year
curl http://localhost:5001/api/reading-stats

# Specific year
curl "http://localhost:5001/api/reading-stats?start_date=2024-01-01"

# Date range
curl "http://localhost:5001/api/reading-stats?start_date=2024-01-01&end_date=2024-06-30"
```

### Using Python:
```python
import requests

response = requests.get('http://localhost:5001/api/reading-stats')
data = response.json()
print(f"Books read: {data['books_read_count']}")
```

### Using JavaScript:
```javascript
fetch('/api/reading-stats')
  .then(response => response.json())
  .then(data => console.log(data));
```

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

## Why Flask for APIs?

Flask is excellent for APIs because:
- Lightweight and fast
- Simple to understand
- Great ecosystem (Flask-CORS, Flask-RESTful, etc.)
- Easy to deploy
- Flexible - use only what you need

## Same Frontend, Different Backend

Notice that `templates/dashboard.html` is identical to the Django version. Because both APIs return the same JSON format, the frontend doesn't care which framework powers the backend. This is the beauty of API-first design!
```
flask-api/templates/dashboard.html   <- Same file
django-api/api/templates/dashboard.html   <- Same file
```

The frontend just does `fetch('/api/reading-stats')` and works with either backend.