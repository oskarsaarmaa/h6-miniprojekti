import os
import requests
from flask import Flask, render_template
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Initialize environment variables and Flask app
load_dotenv()
app = Flask(__name__)

# Fetch API key from .env file
RAWG_API_KEY = os.getenv("RAWG_API_KEY")

@app.route('/')
def index():
    """
    Fetches top-rated games from the last 30 days using RAWG API.
    Returns a rendered dashboard with game metadata.
    """
    # Define the date range for 'New Releases' (Last 30 days)
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    
    # API endpoint with filters for date, ordering (Metacritic), and page size
    url = f"https://api.rawg.io/api/games?key={RAWG_API_KEY}&dates={start_date},{end_date}&ordering=-metacritic&page_size=10"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP request errors
        data = response.json()
        
        games = []
        for game in data.get('results', []):
            # Parse only necessary fields for the UI
            games.append({
                'name': game.get('name'),
                'released': game.get('released'),
                'image': game.get('background_image'),
                'rating': game.get('metacritic') or "N/A",
                'genres': [g['name'] for g in game.get('genres', [])],
                'platforms': [p['platform']['name'] for p in game.get('platforms', [])]
            })
            
        return render_template('index.html', games=games)
    
    except requests.exceptions.RequestException as e:
        # Basic error handling for API connection issues
        return f"Database connection error: {str(e)}", 500

if __name__ == '__main__':
    # Running on 0.0.0.0 to allow access from outside the Docker container
    app.run(debug=True, host='0.0.0.0', port=5000)
