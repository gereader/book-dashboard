# Flask Antipattern: Tightly-Coupled Architecture

This is the "incorrect way" demonstration of why directly calling scripts from routes creates problems.

## How It Works

1. User visits `/` route
2. Flask route calls `hardcover_script.py`
3. Script fetches data from Hardcover API
4. Route renders HTML template with data
5. HTML is returned to user

## Problems With This Approach

### 1. **Tightly Coupled**
The route is directly tied to the script. Want to use this data in a mobile app? You'd have to duplicate the logic or make HTTP requests to scrape the HTML.

### 2. **No API / JSON Response**
This only returns HTML. If you want JSON (further data processing), you're out of luck scrape or add a new route. 

### 3. **Hard to Test**
To test `get_reading_data()`, you have to run Flask. The data fetching logic is tangled with the web framework.

### 4. **No Separation of Concerns**
The route handles:
- Data fetching
- Data transformation
- Presentation logic

All in a single place.

### 5. **Scaling Issues**
- Every page load hits Hardcover's API
- No easy way to add caching
- Can't easily add rate limiting
- Background jobs would be awkward

## Running This Version
```bash
# Install dependencies
uv sync

# Add your Hardcover token to .env
echo "HARDCOVER_TOKEN=Bearer your_token_here" > .env

# Run the app
uv run python app.py
```

Visit `http://localhost:5000`

## The Better Way

See `../django-api/` for an API-first approach that solves these problems.