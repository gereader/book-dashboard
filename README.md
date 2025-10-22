# Book Dashboard: API Architecture Comparison

A hands-on demonstration of why API-first architecture matters, built using real data from [Hardcover](https://hardcover.app) (an alternative to Goodreads with an exposed API).

## The Experiment

Build the same reading dashboard three ways:
1. **Flask Antipattern** - Tightly coupled routes calling scripts
2. **Flask API-First** - Proper separation with JSON API
3. **Django API-First** - Same architecture, different framework

**Goal:** Prove that good architecture transcends framework choice.

## Why This Matters

In my work, I've seen dashboards built the "wrong way" with routes directly calling scripts, returning only HTML, with no reusability. It always peeves me that I have to consider screen scraping as a solution because there is no exposed API with the data. This project demonstrates the problem and shows what I believe to be a better alternative.

## Quick Start

Each directory is self-contained:
```bash
# Flask Antipattern (the "wrong" way)
cd flask-antipattern
uv sync
echo "HARDCOVER_TOKEN=Bearer your_token" > .env
uv run python app.py
# Visit http://localhost:5000

# Flask API (the "right" way)
cd flask-api
uv sync
echo "HARDCOVER_TOKEN=Bearer your_token" > .env
uv run python main.py
# Visit http://localhost:5001

# Django API (the "right" way)
cd django-api
uv sync
echo "HARDCOVER_TOKEN=Bearer your_token" > .env
uv run python manage.py runserver
# Visit http://localhost:8000
```

## Architecture Comparison

### Flask Antipattern (Bad)
```
User Request → Flask Route → Python Script → Hardcover API
                    ↓
              Render HTML Template
```

**Problems:**
- Route directly calls script
- Returns HTML only (no JSON)
- Can't reuse for mobile app, CLI, or other clients
- Data fetching mixed with presentation logic
- Hard to test independently
- No easy way to add query parameters (for example in the Hardcover api case, we can get data from different years)

### Flask API-First (Good)
```
User Request → Flask Route → Serve HTML
                    ↓
              JavaScript fetch()
                    ↓
              API Endpoint → Service Layer → Hardcover API
                    ↓
              Return JSON
```

**Benefits:**
- API returns JSON (reusable by any client)
- Frontend and backend are decoupled
- Easy to add query parameters
- Service layer can be tested independently
- Can build mobile app, CLI tool, etc. using same API

### Django API-First (Good)
```
User Request → Django View → Serve HTML
                    ↓
              JavaScript fetch()
                    ↓
              API Endpoint → Service Layer → Hardcover API
                    ↓
              Return JSON
```

**Benefits:**
- Same architectural benefits as Flask API
- Django REST Framework provides additional tooling
- Built-in admin panel
- ORM for database interactions (if needed later)

## Feature Comparison

| Feature | flask-antipattern | flask-api | django-api |
|---------|------------------|-----------|------------|
| **Returns JSON** | ❌ | ✅ | ✅ |
| **API Endpoint** | ❌ | ✅ | ✅ |
| **Reusable by Other Clients** | ❌ | ✅ | ✅ |
| **Query Parameters** | ❌ | ✅ | ✅ |
| **Testable** | ❌ | ✅ | ✅ |
| **Separation of Concerns** | ❌ | ✅ | ✅ |
| **Framework** | Flask | Flask | Django |
| **Lines of Code** | ~100 | ~120 | ~140 |
| **Complexity** | Low | Medium | Medium |

## Real-World Use Cases

### With the Antipattern (Wrong)

Want to use the data for another purpose? **You'd have to:**
- Scrape the HTML (fragile, breaks easily)
- OR duplicate all the logic
- OR completely refactor the backend

Want to add a CLI tool? **Same problems.**

### With API-First (Right)

Want to use the data for another purpose? **Just call the API:**
```rust
// Rust
let response = reqwest::get("https://api.example.com/api/reading-stats")
    .await?
    .json::<serde_json::Value>()
    .await?;
// Use the JSON data
```

Want a CLI tool? **Just call the API:**
```bash
# Shell script
curl https://api.example.com/api/reading-stats | jq '.books_read_count'
```

Want to integrate with another service? **Just call the API.**

## API Examples

Both `flask-api` and `django-api` provide the same API contract (endpoints, request/response format, behavior):

### Endpoints

- `GET /api/reading-stats` - Current year statistics
- `GET /api/reading-stats?start_date=2024-01-01` - Specific year
- `GET /api/reading-stats?start_date=2024-01-01&end_date=2024-06-30` - Date range

### Response Format
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

### Usage Examples

**Python:**
```python
import requests

response = requests.get('http://localhost:5001/api/reading-stats')
data = response.json()
print(f"Books read this year: {data['books_read_count']}")
```

**JavaScript:**
```javascript
fetch('/api/reading-stats')
  .then(response => response.json())
  .then(data => console.log(`Books read: ${data.books_read_count}`));
```

**curl:**
```bash
curl http://localhost:5001/api/reading-stats | jq '.books_read_count'
```

## Key Takeaways

### 1. **Architecture > Framework**
The problem isn't Flask vs Django. The problem is tightly-coupled vs API-first. Both frameworks can be used to build APIs. The way you build out your application matters, an API-first foundation is infinitely more scalable. 

### 2. **Separation of Concerns Matters**
- **Service Layer**: Handles external API calls
- **API Layer**: Processes requests, returns JSON
- **Frontend**: Consumes the API

Each layer has a single responsibility.

### 3. **Think Beyond the Web Browser**
Modern applications need to support:
- Web browsers (desktop & mobile)
- Native mobile apps
- CLI tools
- Third-party integrations
- Future unknown clients

API-first design supports all of these from day one.

### 4. **Reusability = Less Code in the Long Run**
The initial investment in API-first design pays off when you need to:
- Add a mobile app (no backend changes needed)
- Build a CLI tool (just consume the API)
- Let others integrate (publish API docs)

### 5. **Testing is Easier**
With API-first:
- Test the API with HTTP requests
- Test the service layer in isolation
- Mock the API for frontend tests

Each layer can be tested independently.

## Project Structure
```
book-dashboard/
├── README.md                          # This file
├── flask-antipattern/                 # The "bad" way
│   ├── app.py                         # Route calls script directly
│   ├── hardcover_script.py            # Script that fetches data
│   ├── templates/dashboard.html       # Server-rendered template
│   └── README.md
├── flask-api/                         # Flask done right
│   ├── main.py                        # API routes + frontend route
│   ├── hardcover_service.py           # Service layer
│   ├── templates/dashboard.html       # Client-side fetching
│   └── README.md
└── django-api/                        # Django done right
    ├── manage.py
    ├── bookdash/                      # Project settings
    ├── api/
    │   ├── views.py                   # API routes + frontend route
    │   ├── hardcover_service.py       # Service layer
    │   └── templates/dashboard.html   # Client-side fetching
    └── README.md
```

## Technologies Used

- **Python 3.x** - Programming language
- **Flask** - Lightweight web framework
- **Django + DRF** - Full-featured web framework with REST framework
- **uv** - Fast Python package manager
- **Hardcover API** - GraphQL API for book data
- **Vanilla JavaScript** - No frameworks needed for the frontend

## About Hardcover

[Hardcover](https://hardcover.app) is a modern alternative to Goodreads with:
- GraphQL API (same one used by their web/mobile apps)
- Better social features
- Cleaner interface
- Active development

This project uses real data from my personal Hardcover account that I imported from Goodreads.

## License

MIT - Feel free to use this as a learning resource or template for your own projects.

## Acknowledgments

Built as a birthday learning project to:
- Learn Django and API-first architecture
- Demonstrate architectural principles with a real-world comparison
- Explore Hardcover as a Goodreads alternative
- Have something more interesting than another todo app

**Development Notes:**
- HTML/CSS and project structure created with assistance from Claude AI
- Claude AI was used as an instructor and pair programming partner throughout the learning process
- GraphQL queries and API integration done through experimentation with Hardcover's API using the GraphQL Explorer