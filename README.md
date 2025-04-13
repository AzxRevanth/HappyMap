# HappyMap - Real-Time Sentiment and Emotion Mapping from Social Data

**HappyMaps** is a pipeline that extracts real-time textual data from Twitter and news sources, processes and analyzes it using NLP techniques, and visualizes the emotional landscape of different geographic regions using expressive emojis on an interactive Google Map.

---

## 📦 What It Does
- Data Collection
    - Scrapes and aggregates georeferenced data from Twitter and news outlets.
    - Stores raw data into structured CSV files.

- Natural Language Processing
    - Uses an NLP toolkit to analyze sentiment and emotional tone of the collected text.
    - Assigns a simplified emotion rating (e.g., happy, sad, angry, neutral) to each location.

- Visualization
    - Plots geolocated data points on Google Maps.
    - Uses emojis to represent the dominant emotion in each area for an intuitive and engaging display.

---
## 🧰 Tech Stack

| Layer     | Technology             |
|-----------|------------------------|
| Frontend  | React, HTML, CSS       |
| Backend   | Node.js, Express.js    |
| Database  | MongoDB                |
| Tools     | CORS, Axios/Fetch API  |

---


## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/AzxRevanth/HappyMaps.git
cd HappyMaps
