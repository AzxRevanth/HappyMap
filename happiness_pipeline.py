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

# ==================== IMPORTS ====================
import requests
import json
import time
from datetime import datetime, timedelta
from collections import defaultdict
import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

# ==================== CONFIG =====================
NEWS_API_KEY = "1a21511acb0f49498711df23877c5b7f"   # 🔴 Replace with your own key
PAGE_SIZE = 100
DAYS = 5
FINAL_OUTPUT = "location_coordinates_cleaned.json"

# ==================== SETUP ======================
print("🧠 Initializing NLP and sentiment modules...")
nlp = spacy.load("en_core_web_sm")
analyzer = SentimentIntensityAnalyzer()
geolocator = Nominatim(user_agent="geo_location_happiness")

# ================= FETCH NEWS ====================
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

# ============== LOCATION EXTRACTOR ===============
def extract_locations(text):
    doc = nlp(text)
    return list({ent.text for ent in doc.ents if ent.label_ == "GPE"})

# ============= SENTIMENT AGGREGATOR ==============
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

# ================ GEOLOCATION =====================
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
                        "longitude": lon
                    })
        except (GeocoderTimedOut, GeocoderUnavailable):
            continue
        time.sleep(1)  # Respect Nominatim usage policy
    return cleaned

# ===================== MAIN =======================
def main():
    print("\n🔎 Enter your news topic of interest.")
    query = input("Topic: ").strip()
    if not query:
        print("❌ Empty query. Aborting.")
        return

    print(f"\n📡 Fetching news articles for: '{query}'...")
    articles = fetch_news(query)
    print(f"📰 Articles found: {len(articles)}")

    print("\n🧠 Extracting locations and scoring sentiment...")
    location_scores = analyze_sentiments(articles)
    print(f"📍 Unique locations mentioned: {len(location_scores)}")

    print("\n🌐 Converting locations to coordinates...")
    cleaned_data = geocode_locations(location_scores)

    with open(FINAL_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(cleaned_data, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Final dataset saved to '{FINAL_OUTPUT}' ({len(cleaned_data)} locations)")

# =================== ENTRY ========================
if __name__ == "__main__":
    main()
