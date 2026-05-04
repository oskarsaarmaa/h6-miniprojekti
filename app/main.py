import os
import requests
from flask import Flask, render_template
from datetime import datetime, timedelta

app = Flask(__name__)

RAWG_API_KEY = "8dd3b98aadc54844964a64bdc08ab6eb"

@app.route('/')
def index():
    today = datetime.now().strftime('%Y-%m-%d')
    # Haetaan pelit viimeisen 12 kuukauden ajalta (365 päivää)
    last_year = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    
    url = f"https://api.rawg.io/api/games?key={RAWG_API_KEY}&dates={last_year},{today}&ordering=-added&page_size=20"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        games = []
        
        results = data.get('results')
        if not results:
            return "API ei palauttanut tuloksia juuri nyt."

        for game in results:
            ratings = game.get('ratings')
            if ratings and len(ratings) > 0:
                title = ratings[0].get('title', 'Hyvä').capitalize()
                percent = ratings[0].get('percent', 0)
                top_review = f"{title} ({percent}% arvioista)"
            else:
                top_review = "Odottaa pelaajien tuomioita"

            platforms_data = game.get('platforms') or []
            platform_list = [p['platform']['name'] for p in platforms_data if p.get('platform')]

            games.append({
                'name': game.get('name', 'Nimetön peli'),
                'released': game.get('released', 'Tuntematon'),
                'image': game.get('background_image') or '',
                'metacritic': game.get('metacritic'),
                'user_rating': game.get('rating') or 0,
                'sentiment': top_review,
                'platforms': platform_list[:3]
            })
                
        return render_template('index.html', games=games)

    except Exception as e:
        return f"Sovellusvirhe: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
