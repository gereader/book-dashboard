from flask import Flask, render_template
from hardcover_script import get_reading_data

app = Flask(__name__)

@app.route('/')
def dashboard():
    """
    This is the 'incorrect' way, the route directly calls a script.
    
    Problems with this approach:
    - Tightly coupled: Can't reuse this data for other needs
    - No API: Frontend can't fetch data independently
    - Hard to test: Have to boot up Flask to test the logic
    - No separation of concerns: Route logic mixed with data fetching
    """
    
    # Call the script to get data (this is the antipattern!)
    raw_data = get_reading_data()
    
    # Extract the data we need from the nested response
    me_data = raw_data['data']['me'][0]
    
    currently_reading = me_data['currently_reading']
    books_read = me_data['books_read_this_year']
    goals = me_data['goals'][0] if me_data['goals'] else None
    
    # Pass data to template
    return render_template(
        'dashboard.html',
        currently_reading=currently_reading,
        books_read_count=len(books_read),
        goal=goals['goal'] if goals else None,
        progress=goals['progress'] if goals else None
    )

if __name__ == '__main__':
    app.run(debug=True)