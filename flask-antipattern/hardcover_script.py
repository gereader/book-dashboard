import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_reading_data():
    """
    This function calls the Hardcover GraphQL API and returns reading stats.
    
    GraphQL is just a POST request with a 'query' in the JSON body.
    """
    
    # Get the token from environment variable
    token = os.getenv('HARDCOVER_TOKEN')
    
    # The GraphQL endpoint URL
    url = "https://api.hardcover.app/v1/graphql"
    
    # Headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"{token}"
    }
    
    # GraphQL query explanation:
    # - me: gets data about the logged-in user
    # - currently_reading: books where status_id = 2 (Currently Reading status)
    # - books_read_this_year: books where status_id = 3 (Read) AND reviewed_at is after Jan 1, 2025
    # - goals: reading goals with progress tracking
    query = """
    query {
      me {
        currently_reading: user_books(where: { status_id: { _eq: 2 } }) {
          book {
            title
            pages
            contributions {
              author {
                name
              }
            }
          }
        }
        books_read_this_year: user_books(where: { 
          status_id: { _eq: 3 },
          reviewed_at: { _gte: "2025-01-01" }
        }) {
          book {
            title
          }
        }
        goals {
          description
          goal
          progress
          start_date
          end_date
        }
      }
    }
    """
    
    # Make the POST request
    # GraphQL always uses POST, even for "queries"
    response = requests.post(
        url,
        json={"query": query},  # The query goes in the JSON body
        headers=headers
    )
    
    # Parse the JSON response
    data = response.json()
    
    # Return just the data we care about
    return data

# Test it out if run directly
if __name__ == "__main__":
    result = get_reading_data()
    import json
    print(json.dumps(result, indent=2))  # Pretty print for easier reading