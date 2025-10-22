from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .hardcover_service import HardcoverService
from django.shortcuts import render

def dashboard(request):
    """
    Serve the dashboard HTML page.
    This page fetches data from the API using JavaScript.
    """
    return render(request, 'dashboard.html')

@api_view(['GET'])
def reading_stats(request):
    """
    API endpoint to get reading statistics.
    
    Query Parameters:
        start_date (optional): ISO date string (e.g., "2024-01-01")
        end_date (optional): ISO date string (e.g., "2024-12-31")
    
    Returns JSON with:
        - currently_reading: List of books currently being read
        - books_read_count: Number of books read in date range
        - date_range: The date range queried
        - goal: Reading goal for the date range (if exists)
    
    Example:
        GET /api/reading-stats/
        GET /api/reading-stats/?start_date=2024-01-01
        GET /api/reading-stats/?start_date=2024-01-01&end_date=2024-06-30
    """
    
    # Get query parameters from the request
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    
    try:
        # Call the service to fetch data
        service = HardcoverService()
        data = service.get_reading_stats(start_date, end_date)
        
        # Return JSON response
        return Response(data, status=status.HTTP_200_OK)
    
    except Exception as e:
        # Handle errors gracefully
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )