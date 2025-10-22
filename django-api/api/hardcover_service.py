import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class HardcoverService:
    """
    Service class for interacting with Hardcover API.
    
    This is separate from views as it can be used by API endpoints,
    background jobs, CLI tools, etc.
    """
    
    def __init__(self):
        self.token = os.getenv('HARDCOVER_TOKEN')
        self.url = "https://api.hardcover.app/v1/graphql"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"{self.token}"
        }
    
    def get_reading_stats(self, start_date=None, end_date=None):
        """
        Fetch reading statistics from Hardcover API.
        
        Args:
            start_date: ISO date string (e.g., "2025-01-01"). Defaults to current year Jan 1.
            end_date: ISO date string (e.g., "2025-12-31"). Defaults to current year Dec 31.
        
        Returns a clean, formatted dict ready for API response.
        """
        # Default to current year if no dates provided
        if start_date is None:
            current_year = datetime.now().year
            start_date = f"{current_year}-01-01"
        
        if end_date is None:
            current_year = datetime.now().year
            end_date = f"{current_year}-12-31"
        
        # Build the where clause for books read
        books_read_filter = f'status_id: {{ _eq: 3 }}, reviewed_at: {{ _gte: "{start_date}", _lte: "{end_date}" }}'
        
        # Build the where clause for goals (find goals that overlap with our date range)
        goals_filter = f'start_date: {{ _lte: "{end_date}" }}, end_date: {{ _gte: "{start_date}" }}'
        
        query = f"""
        query {{
          me {{
            currently_reading: user_books(where: {{ status_id: {{ _eq: 2 }} }}) {{
              book {{
                title
                pages
                contributions {{
                  author {{
                    name
                  }}
                }}
              }}
            }}
            books_read_in_range: user_books(where: {{ {books_read_filter} }}) {{
              book {{
                title
              }}
            }}
            goals(where: {{ {goals_filter} }}) {{
              description
              goal
              progress
              start_date
              end_date
            }}
          }}
        }}
        """
        
        response = requests.post(
            self.url,
            json={"query": query},
            headers=self.headers
        )
        
        data = response.json()
        
        # Transform the nested API response into a clean format
        return self._format_response(data, start_date, end_date)
    
    def _format_response(self, raw_data, start_date, end_date):
        """
        Transform the raw Hardcover response into a clean API response.
        """
        me_data = raw_data['data']['me'][0]
        
        # Extract currently reading books
        currently_reading = []
        for user_book in me_data['currently_reading']:
            book = user_book['book']
            author = book['contributions'][0]['author']['name'] if book['contributions'] else 'Unknown'
            currently_reading.append({
                'title': book['title'],
                'author': author,
                'pages': book['pages']
            })
        
        # Count books read in the date range
        books_read_count = len(me_data['books_read_in_range'])
        
        # Extract goal info (if a goal exists for this date range)
        goal_data = me_data['goals'][0] if me_data['goals'] else None
        goal = None
        if goal_data:
            goal = {
                'target': goal_data['goal'],
                'progress': goal_data['progress'],
                'percentage': round((goal_data['progress'] / goal_data['goal']) * 100) if goal_data['goal'] > 0 else 0,
                'description': goal_data['description'],
                'start_date': goal_data['start_date'],
                'end_date': goal_data['end_date']
            }
        
        return {
            'currently_reading': currently_reading,
            'books_read_count': books_read_count,
            'date_range': {
                'start': start_date,
                'end': end_date
            },
            'goal': goal
        }