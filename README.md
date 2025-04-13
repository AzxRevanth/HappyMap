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
| NLP       | NLTK, Vadar            |

---


## 🚀 Getting Started

To run this project locally, follow these steps:

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/happymaps.git
cd happymaps
```

### 2. Set Up Your Google Maps API Key

Go to the Google Cloud Console.

Generate a Google Maps API key.

Open your HTML file (usually index.html or map.html) and replace the existing API key in the script tag:

```
<script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&callback=initMap" async defer></script>
```

### 3. Set Up Your API Keys for Data Collection

This project requires:

    NewsAPI Key

    Reddit App Client ID & Secret

Once you've obtained your keys, you can either:
Option 1: Create a .env file in the DataCollection folder:

```
NEWS_API_KEY=your_newsapi_key_here
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
```

    ⚠️ Make sure to use a package like dotenv in your Node.js backend to load these variables.

Option 2: Directly insert your keys into the code files if you prefer (not recommended for production).


### 4. Set Up MongoDB

    Sign up or log in at MongoDB Atlas.

    Create a new cluster and get your connection string.

    Paste the connection string in your server code (where MongoDB is connected), replacing:

```
const uri = "mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority";
```

✅ You're all set!

Now just run your backend and frontend servers (based on your project structure), and HappyMaps should be up and running locally! 🎉
💡 Notes

    Remember to keep your API keys and connection strings secure.

    Avoid committing .env files or secrets to version control.

📬 Questions or Issues?

Feel free to open an issue or contribute!
