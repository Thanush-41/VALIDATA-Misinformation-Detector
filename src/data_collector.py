import snscrape.modules.twitter as sntwitter
import pandas as pd
import logging
import re
from datetime import datetime, timedelta
from langdetect import detect
from database import DatabaseManager

class TwitterDataCollector:
    def __init__(self, db_manager=None):
        self.db_manager = db_manager or DatabaseManager()
        
    def clean_tweet(self, text):
        """Clean tweet text by removing URLs, mentions, hashtags, and extra whitespace"""
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        # Remove mentions and hashtags
        text = re.sub(r'@\w+|#\w+', '', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def is_english(self, text):
        """Check if text is in English"""
        try:
            return detect(text) == 'en'
        except:
            return False
    
    def collect_tweets_by_keyword(self, keywords, max_tweets=1000, days_back=7):
        """
        Collect tweets based on keywords
        
        Args:
            keywords (list): List of keywords to search for
            max_tweets (int): Maximum number of tweets to collect
            days_back (int): Number of days to go back for tweet collection
        """
        collected_tweets = []
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        # Create search query
        search_query = ' OR '.join(keywords)
        search_query += f' since:{start_date.strftime("%Y-%m-%d")} until:{end_date.strftime("%Y-%m-%d")}'
        
        logging.info(f"Starting tweet collection with query: {search_query}")
        
        try:
            tweet_count = 0
            for tweet in sntwitter.TwitterSearchScraper(search_query).get_items():
                if tweet_count >= max_tweets:
                    break
                
                # Clean and filter tweets
                cleaned_content = self.clean_tweet(tweet.content)
                
                # Skip if too short or not English
                if len(cleaned_content) < 10 or not self.is_english(cleaned_content):
                    continue
                
                tweet_data = {
                    'tweet_id': str(tweet.id),
                    'content': cleaned_content,
                    'author': tweet.user.username,
                    'date': tweet.date.isoformat(),
                    'url': tweet.url,
                    'language': 'en'
                }
                
                # Insert into database
                if self.db_manager.insert_tweet(tweet_data):
                    collected_tweets.append(tweet_data)
                    tweet_count += 1
                    
                    if tweet_count % 10 == 0:
                        logging.info(f"Collected {tweet_count} tweets so far...")
        
        except Exception as e:
            logging.error(f"Error collecting tweets: {e}")
        
        logging.info(f"Collected {len(collected_tweets)} tweets successfully")
        return collected_tweets
    
    def collect_tweets_by_hashtag(self, hashtags, max_tweets=500, days_back=7):
        """
        Collect tweets based on hashtags
        
        Args:
            hashtags (list): List of hashtags to search for (without #)
            max_tweets (int): Maximum number of tweets to collect
            days_back (int): Number of days to go back for tweet collection
        """
        # Add # to hashtags if not present
        hashtags = [f"#{tag}" if not tag.startswith('#') else tag for tag in hashtags]
        return self.collect_tweets_by_keyword(hashtags, max_tweets, days_back)
    
    def collect_trending_topics_tweets(self, max_tweets=1000):
        """
        Collect tweets from predefined trending/controversial topics
        """
        # Predefined controversial topics for misinformation detection
        trending_topics = [
            "vaccine", "covid", "coronavirus", "climate change", "election",
            "politics", "conspiracy", "fake news", "misinformation", 
            "health", "science", "breaking news"
        ]
        
        all_tweets = []
        tweets_per_topic = max_tweets // len(trending_topics)
        
        for topic in trending_topics:
            logging.info(f"Collecting tweets for topic: {topic}")
            tweets = self.collect_tweets_by_keyword([topic], tweets_per_topic, days_back=3)
            all_tweets.extend(tweets)
        
        return all_tweets
    
    def collect_user_tweets(self, username, max_tweets=100):
        """
        Collect tweets from a specific user
        
        Args:
            username (str): Twitter username (without @)
            max_tweets (int): Maximum number of tweets to collect
        """
        collected_tweets = []
        
        try:
            tweet_count = 0
            for tweet in sntwitter.TwitterUserScraper(username).get_items():
                if tweet_count >= max_tweets:
                    break
                
                cleaned_content = self.clean_tweet(tweet.content)
                
                if len(cleaned_content) < 10 or not self.is_english(cleaned_content):
                    continue
                
                tweet_data = {
                    'tweet_id': str(tweet.id),
                    'content': cleaned_content,
                    'author': username,
                    'date': tweet.date.isoformat(),
                    'url': tweet.url,
                    'language': 'en'
                }
                
                if self.db_manager.insert_tweet(tweet_data):
                    collected_tweets.append(tweet_data)
                    tweet_count += 1
        
        except Exception as e:
            logging.error(f"Error collecting tweets from user {username}: {e}")
        
        return collected_tweets

# Example usage and testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Initialize collector
    collector = TwitterDataCollector()
    
    # Example: Collect tweets about vaccines and misinformation
    keywords = ["vaccine misinformation", "covid conspiracy", "fake news health"]
    tweets = collector.collect_tweets_by_keyword(keywords, max_tweets=50, days_back=7)
    
    print(f"Collected {len(tweets)} tweets")
    for tweet in tweets[:3]:  # Show first 3 tweets
        print(f"Tweet ID: {tweet['tweet_id']}")
        print(f"Content: {tweet['content'][:100]}...")
        print(f"Author: {tweet['author']}")
        print("-" * 50)
