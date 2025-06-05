import requests
from bs4 import BeautifulSoup
import praw
from datetime import datetime, timezone
# We need to adjust the import path slightly for local execution
import config # Our configuration file

# --- Reddit Scraper ---
# Initialize the Reddit instance using our credentials from config.py
try:
    reddit = praw.Reddit(
        client_id=config.REDDIT_CLIENT_ID,
        client_secret=config.REDDIT_CLIENT_SECRET,
        user_agent=config.REDDIT_USER_AGENT,
    )
    print("Successfully connected to Reddit API.")
except Exception as e:
    print(f"Error connecting to Reddit API: {e}")
    reddit = None

def fetch_reddit_posts(ticker, limit=25):
    """Fetches posts from relevant subreddits for a given ticker."""
    if not reddit:
        print("Reddit instance not available. Skipping fetch.")
        return []

    # A simple mapping of tickers to relevant subreddits
    subreddit_map = {
        'AAPL': ['apple', 'stocks', 'investing'],
        'GOOGL': ['google', 'stocks', 'investing'],
        'TSLA': ['teslamotors', 'stocks', 'investing'],
        'BTC': ['Bitcoin', 'CryptoCurrency'],
        'ETH': ['ethereum', 'CryptoCurrency']
    }
    
    posts_data = []
    subreddits_to_search = subreddit_map.get(ticker.upper(), ['stocks', 'CryptoCurrency'])
    
    print(f"Searching Reddit for '{ticker}' in subreddits: {subreddits_to_search}")
    
    for sub in subreddits_to_search:
        try:
            subreddit = reddit.subreddit(sub)
            # Search for the ticker in titles of new posts
            for post in subreddit.search(f'title:"{ticker}"', sort='new', time_filter='week', limit=limit):
                posts_data.append({
                    'source': 'Reddit',
                    'ticker': ticker,
                    'title': post.title,
                    'text': post.selftext,
                    'url': post.url,
                    'created_utc': datetime.fromtimestamp(post.created_utc, tz=timezone.utc).isoformat()
                })
        except Exception as e:
            print(f"Could not fetch from subreddit r/{sub}: {e}")

    print(f"Found {len(posts_data)} posts for {ticker} on Reddit.")
    return posts_data

# --- News Scraper (Yahoo Finance) ---
def fetch_yahoo_finance_news(ticker):
    """Scrapes news headlines for a ticker from Yahoo Finance."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    url = f"https://finance.yahoo.com/quote/{ticker}/news"
    
    print(f"Fetching news for '{ticker}' from Yahoo Finance...")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching Yahoo Finance news for {ticker}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    news_items = []

    # Updated and more robust selector for finding headlines
    # This looks for list items with a specific data-test attribute
    for item in soup.find_all('li', class_='js-stream-content'):
        a_tag = item.find('a')
        h3_tag = item.find('h3')
        
        if a_tag and h3_tag and h3_tag.text:
            # Construct the full URL if it's a relative path
            href = a_tag['href']
            full_url = href if href.startswith('http') else f"https://finance.yahoo.com{href}"

            news_items.append({
                'source': 'Yahoo Finance',
                'ticker': ticker,
                'title': h3_tag.text.strip(),
                'text': '',
                'url': full_url,
                'created_utc': datetime.now(timezone.utc).isoformat()
            })

    print(f"Found {len(news_items)} headlines for {ticker} on Yahoo Finance.")
    return news_items[:10]