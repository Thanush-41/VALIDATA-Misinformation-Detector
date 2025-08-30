import sqlite3
import logging
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="data/misinformation_detector.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tweets table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tweets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tweet_id TEXT UNIQUE,
                content TEXT NOT NULL,
                author TEXT,
                date TEXT,
                url TEXT,
                language TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create classifications table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS classifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tweet_id TEXT,
                classification TEXT NOT NULL,
                reasoning TEXT,
                confidence_score REAL,
                model_used TEXT,
                fact_check_result TEXT,
                fact_check_source TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (tweet_id) REFERENCES tweets (tweet_id)
            )
        ''')
        
        # Create topics table for tracking trending topics
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS topics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                keywords TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logging.info("Database initialized successfully")
    
    def insert_tweet(self, tweet_data):
        """Insert a tweet into the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO tweets 
                (tweet_id, content, author, date, url, language)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                tweet_data['tweet_id'],
                tweet_data['content'],
                tweet_data['author'],
                tweet_data['date'],
                tweet_data['url'],
                tweet_data['language']
            ))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            logging.error(f"Error inserting tweet: {e}")
            return False
        finally:
            conn.close()
    
    def insert_classification(self, classification_data):
        """Insert a classification result into the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO classifications 
                (tweet_id, classification, reasoning, confidence_score, model_used, fact_check_result, fact_check_source)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                classification_data['tweet_id'],
                classification_data['classification'],
                classification_data['reasoning'],
                classification_data.get('confidence_score'),
                classification_data.get('model_used'),
                classification_data.get('fact_check_result'),
                classification_data.get('fact_check_source')
            ))
            conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error inserting classification: {e}")
            return False
        finally:
            conn.close()
    
    def get_tweets_for_classification(self, limit=100):
        """Get tweets that haven't been classified yet"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT t.tweet_id, t.content, t.author, t.date, t.url 
            FROM tweets t
            LEFT JOIN classifications c ON t.tweet_id = c.tweet_id
            WHERE c.tweet_id IS NULL
            LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'tweet_id': row[0],
                'content': row[1],
                'author': row[2],
                'date': row[3],
                'url': row[4]
            }
            for row in results
        ]
    
    def get_classification_stats(self):
        """Get statistics about classifications"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT classification, COUNT(*) as count
            FROM classifications
            GROUP BY classification
        ''')
        
        stats = dict(cursor.fetchall())
        conn.close()
        return stats
    
    def get_all_classified_tweets(self):
        """Get all tweets with their classifications"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT t.tweet_id, t.content, t.author, t.date, t.url,
                   c.classification, c.reasoning, c.confidence_score, c.created_at
            FROM tweets t
            JOIN classifications c ON t.tweet_id = c.tweet_id
            ORDER BY c.created_at DESC
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'tweet_id': row[0],
                'content': row[1],
                'author': row[2],
                'date': row[3],
                'url': row[4],
                'classification': row[5],
                'reasoning': row[6],
                'confidence_score': row[7],
                'classified_at': row[8]
            }
            for row in results
        ]
