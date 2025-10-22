from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from hardcover_service import HardcoverService

app = Flask(__name__)
CORS(app)  # Allow frontend to fetch from API

# API Endpoint - Returns JSON
@app.route('/api/reading-stats', strict_slashes=False)
def api_reading_stats():
    """
    API endpoint that returns JSON data.
    
    This is the key difference from flask-antipattern - 
    we return JSON, not HTML!
    
    Query Parameters:
        start_date: ISO date string (e.g., "2024-01-01")
        end_date: ISO date string (e.g., "2024-12-31")
    
    Example:
        /api/reading-stats
        /api/reading-stats?start_date=2024-01-01&end_date=2024-12-31
    """
    # Get query parameters
    start_date = request.args.get('start_date', None)
    end_date = request.args.get('end_date', None)

    # DEBUG: Print what we received
    print(f"Received params - start_date: {start_date}, end_date: {end_date}")
    
    try:
        # Use the service to fetch data
        service = HardcoverService()
        data = service.get_reading_stats(start_date, end_date)
        
        # Return JSON (not HTML!)
        return jsonify(data), 200
    
    except Exception as e:
        print(f"ERROR: {e}")  # DEBUG

        return jsonify({'error': str(e)}), 500


# Frontend - Serves HTML that fetches from API
@app.route('/')
def dashboard():
    """
    Serve the dashboard HTML.
    
    Notice: This route doesn't fetch any data!
    The HTML will fetch from /api/reading-stats using JavaScript.
    
    This is the separation of concerns for the route, it only serves HTML,
    the API provides data.
    """
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Use 5001 to avoid conflict