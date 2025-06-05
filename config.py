import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- API KEYS ---
# We will fill these in later phases
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "IntelliWatch_v1 by u/your_reddit_username")

# --- DATABASE ---
MONGO_URI = os.getenv("MONGO_URI")

# --- ALERTS ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# --- WATCHLIST ---
# Define the stocks/cryptos to track
WATCHLIST = ['AAPL', 'GOOGL', 'TSLA', 'BTC', 'ETH']