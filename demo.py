"""
Simple demo script for the Misinformation Detection System
This version uses mock data instead of real tweet collection to demonstrate the core functionality
"""

import os
import sys
import sqlite3
import logging
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def setup_logging():
    """Setup basic logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

class SimpleDatabaseManager:
    """Simplified database manager for demo"""
    def __init__(self, db_path="data/demo.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tweets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tweet_id TEXT UNIQUE,
                content TEXT NOT NULL,
                author TEXT,
                date TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS classifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tweet_id TEXT,
                classification TEXT NOT NULL,
                reasoning TEXT,
                confidence TEXT,
                model_used TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (tweet_id) REFERENCES tweets (tweet_id)
            )
        ''')
        
        conn.commit()
        conn.close()
        logging.info("Database initialized successfully")
    
    def insert_tweet(self, tweet_data):
        """Insert a tweet"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO tweets 
                (tweet_id, content, author, date)
                VALUES (?, ?, ?, ?)
            ''', (
                tweet_data['tweet_id'],
                tweet_data['content'],
                tweet_data['author'],
                tweet_data['date']
            ))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            logging.error(f"Error inserting tweet: {e}")
            return False
        finally:
            conn.close()
    
    def insert_classification(self, classification_data):
        """Insert a classification"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO classifications 
                (tweet_id, classification, reasoning, confidence, model_used)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                classification_data['tweet_id'],
                classification_data['classification'],
                classification_data['reasoning'],
                classification_data.get('confidence', 'Medium'),
                classification_data.get('model_used', 'demo')
            ))
            conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error inserting classification: {e}")
            return False
        finally:
            conn.close()
    
    def get_unclassified_tweets(self):
        """Get tweets without classifications"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT t.tweet_id, t.content, t.author, t.date 
            FROM tweets t
            LEFT JOIN classifications c ON t.tweet_id = c.tweet_id
            WHERE c.tweet_id IS NULL
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'tweet_id': row[0],
                'content': row[1],
                'author': row[2],
                'date': row[3]
            }
            for row in results
        ]
    
    def get_all_classifications(self):
        """Get all classifications with tweet content"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT t.content, t.author, c.classification, c.reasoning, c.confidence
            FROM tweets t
            JOIN classifications c ON t.tweet_id = c.tweet_id
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'content': row[0],
                'author': row[1],
                'classification': row[2],
                'reasoning': row[3],
                'confidence': row[4]
            }
            for row in results
        ]

class SimpleClassifier:
    """Simplified classifier using rule-based approach"""
    
    def __init__(self):
        self.false_indicators = [
            'conspiracy', 'cover-up', 'they don\'t want you to know', 'big pharma',
            'government lies', 'mainstream media lies', 'fake news', 'hoax',
            'secret agenda', 'wake up', 'sheep', 'truth they hide'
        ]
        
        self.misleading_indicators = [
            'some say', 'many believe', 'sources claim', 'rumor has it',
            'allegedly', 'supposedly', 'unconfirmed reports', 'breaking',
            'exclusive', 'insider information'
        ]
        
        self.credible_indicators = [
            'study shows', 'research indicates', 'scientists confirm',
            'official statement', 'peer-reviewed', 'clinical trial',
            'evidence suggests', 'data shows', 'according to experts'
        ]
    
    def classify_tweet(self, content):
        """Classify a tweet based on content"""
        content_lower = content.lower()
        
        false_score = sum(1 for term in self.false_indicators if term in content_lower)
        misleading_score = sum(1 for term in self.misleading_indicators if term in content_lower)
        credible_score = sum(1 for term in self.credible_indicators if term in content_lower)
        
        if false_score > 0:
            return {
                'classification': 'Likely False',
                'reasoning': f'Contains {false_score} suspicious terms often associated with misinformation',
                'confidence': 'High' if false_score > 1 else 'Medium'
            }
        elif misleading_score > credible_score:
            return {
                'classification': 'Misleading',
                'reasoning': f'Contains {misleading_score} terms suggesting unverified claims',
                'confidence': 'Medium'
            }
        elif credible_score > 0:
            return {
                'classification': 'Likely True',
                'reasoning': f'Contains {credible_score} terms suggesting credible sources',
                'confidence': 'High' if credible_score > 1 else 'Medium'
            }
        else:
            return {
                'classification': 'Misleading',
                'reasoning': 'Unable to determine credibility based on content analysis',
                'confidence': 'Low'
            }

def main():
    """Main demo function"""
    print("🔍 Misinformation Detection System - Simple Demo")
    print("=" * 60)
    
    setup_logging()
    
    # Initialize components
    db = SimpleDatabaseManager()
    classifier = SimpleClassifier()
    
    # Sample tweets for demonstration
    sample_tweets = [
        {
            'tweet_id': 'demo_1',
            'content': 'Breaking: Government hiding vaccine side effects! Big pharma conspiracy! Wake up people!',
            'author': 'conspiracy_user',
            'date': datetime.now().isoformat()
        },
        {
            'tweet_id': 'demo_2',
            'content': 'New peer-reviewed study shows vaccines are safe and effective according to medical experts.',
            'author': 'science_user',
            'date': datetime.now().isoformat()
        },
        {
            'tweet_id': 'demo_3',
            'content': 'Some people claim climate change is fake, but sources say the evidence is not clear.',
            'author': 'neutral_user',
            'date': datetime.now().isoformat()
        },
        {
            'tweet_id': 'demo_4',
            'content': 'Official health authorities confirm that masks help prevent disease spread.',
            'author': 'health_official',
            'date': datetime.now().isoformat()
        },
        {
            'tweet_id': 'demo_5',
            'content': 'Exclusive insider information: They don\'t want you to know the truth about 5G towers!',
            'author': 'truth_seeker',
            'date': datetime.now().isoformat()
        }
    ]
    
    print("📝 Step 1: Inserting sample tweets...")
    for tweet in sample_tweets:
        success = db.insert_tweet(tweet)
        if success:
            print(f"  ✓ Inserted: {tweet['content'][:50]}...")
    
    print(f"\n🤖 Step 2: Classifying tweets...")
    unclassified = db.get_unclassified_tweets()
    print(f"Found {len(unclassified)} tweets to classify")
    
    for tweet in unclassified:
        result = classifier.classify_tweet(tweet['content'])
        result['tweet_id'] = tweet['tweet_id']
        result['model_used'] = 'rule_based_demo'
        
        db.insert_classification(result)
        print(f"  ✓ Classified: {result['classification']} - {tweet['content'][:50]}...")
    
    print(f"\n📊 Step 3: Results Summary...")
    all_results = db.get_all_classifications()
    
    # Count classifications
    classification_counts = {}
    for result in all_results:
        classification = result['classification']
        classification_counts[classification] = classification_counts.get(classification, 0) + 1
    
    print(f"Total tweets analyzed: {len(all_results)}")
    for classification, count in classification_counts.items():
        percentage = (count / len(all_results)) * 100
        print(f"  {classification}: {count} ({percentage:.1f}%)")
    
    print(f"\n🔍 Step 4: Detailed Analysis...")
    for i, result in enumerate(all_results, 1):
        print(f"\n{i}. Tweet: \"{result['content'][:80]}...\"")
        print(f"   Author: {result['author']}")
        print(f"   Classification: {result['classification']}")
        print(f"   Confidence: {result['confidence']}")
        print(f"   Reasoning: {result['reasoning']}")
    
    print(f"\n✅ Demo completed successfully!")
    print(f"Database saved to: {db.db_path}")
    
    print(f"\n📋 Next Steps:")
    print("1. Install snscrape: pip install snscrape")
    print("2. Install transformers: pip install transformers torch")
    print("3. Run the full system: python example.py")
    print("4. Launch dashboard: streamlit run dashboard/app.py")
    
    return db.db_path

if __name__ == "__main__":
    main()
