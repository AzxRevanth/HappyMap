"""
🌍 News-based Location Happiness Mapper
=======================================
This script fetches recent news based on a query, extracts mentioned locations,
analyzes the sentiment of the news articles, and maps average sentiment to geocoordinates.

🔹 Powered by:
    - NewsAPI (https://newsapi.org)
    - spaCy (NER)
    - VADER (sentiment analysis)
    - geopy (geolocation)

🛠️ Output:
    location_coordinates_cleaned.json
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import time
from datetime import datetime, timedelta
from collections import defaultdict
import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

app = Flask(__name__)
CORS(app)  # allows cross-origin requests

# ========== SETUP ==========
nlp = spacy.load("en_core_web_sm")
analyzer = SentimentIntensityAnalyzer()
geolocator = Nominatim(user_agent="geo_location_happiness")

NEWS_API_KEY = "1a21511acb0f49498711df23877c5b7f"
PAGE_SIZE = 100
DAYS = 5

# ========== HELPERS ==========
def fetch_news(query):
    to_date = datetime.now()
    from_date = to_date - timedelta(days=DAYS)
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={query}&from={from_date.strftime('%Y-%m-%d')}&to={to_date.strftime('%Y-%m-%d')}"
        f"&language=en&pageSize={PAGE_SIZE}&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    )
    response = requests.get(url).json()
    return response.get("articles", [])

def extract_locations(text):
    doc = nlp(text)
    return list({ent.text for ent in doc.ents if ent.label_ == "GPE"})

def analyze_sentiments(articles):
    location_scores = defaultdict(list)
    for article in articles:
        text = f"{article.get('title', '')} {article.get('description', '')}"
        locations = extract_locations(text)
        if not locations:
            continue
        score = analyzer.polarity_scores(article.get("description", ""))['compound']
        for loc in locations:
            location_scores[loc].append(score)
    return {
        loc: round(sum(scores) / len(scores), 4)
        for loc, scores in location_scores.items() if scores
    }

def geocode_locations(location_scores):
    seen_coords = set()
    cleaned = []
    for location, score in location_scores.items():
        try:
            geo_result = geolocator.geocode(location, timeout=5)
            if geo_result:
                lat = round(geo_result.latitude, 6)
                lon = round(geo_result.longitude, 6)
                coord = (lat, lon)
                if coord not in seen_coords:
                    seen_coords.add(coord)
                    cleaned.append({
                        "happiness_score": score,
                        "latitude": lat,
                        "longitude": lon,
                        "location": location
                    })
        except (GeocoderTimedOut, GeocoderUnavailable):
            continue
        time.sleep(1)
    return cleaned

# ========== FLASK ROUTE ==========
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    query = data.get("query", "")
    if not query:
        return jsonify({"error": "Missing query"}), 400

    articles = fetch_news(query)
    location_scores = analyze_sentiments(articles)
    cleaned_data = geocode_locations(location_scores)
    return jsonify(cleaned_data)

# ========== ENTRY ==========
if __name__ == "__main__":
    app.run(debug=True, port=5000)
