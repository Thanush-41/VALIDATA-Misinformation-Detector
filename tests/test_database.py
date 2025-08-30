import unittest
import sys
import os
import tempfile
import shutil

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from database import DatabaseManager

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        """Set up test database"""
        self.test_dir = tempfile.mkdtemp()
        self.test_db_path = os.path.join(self.test_dir, 'test_db.db')
        self.db_manager = DatabaseManager(self.test_db_path)
    
    def tearDown(self):
        """Clean up test database"""
        shutil.rmtree(self.test_dir)
    
    def test_database_initialization(self):
        """Test that database is initialized correctly"""
        self.assertTrue(os.path.exists(self.test_db_path))
    
    def test_insert_tweet(self):
        """Test inserting a tweet"""
        tweet_data = {
            'tweet_id': 'test_123',
            'content': 'This is a test tweet about vaccines.',
            'author': 'test_user',
            'date': '2024-01-01T12:00:00',
            'url': 'https://twitter.com/test',
            'language': 'en'
        }
        
        result = self.db_manager.insert_tweet(tweet_data)
        self.assertTrue(result)
        
        # Test duplicate insertion
        result = self.db_manager.insert_tweet(tweet_data)
        self.assertFalse(result)  # Should return False for duplicate
    
    def test_insert_classification(self):
        """Test inserting a classification"""
        # First insert a tweet
        tweet_data = {
            'tweet_id': 'test_456',
            'content': 'Test tweet content',
            'author': 'test_user',
            'date': '2024-01-01T12:00:00',
            'url': 'https://twitter.com/test',
            'language': 'en'
        }
        self.db_manager.insert_tweet(tweet_data)
        
        # Then insert classification
        classification_data = {
            'tweet_id': 'test_456',
            'classification': 'Likely False',
            'reasoning': 'Contains misinformation indicators',
            'confidence_score': 0.8,
            'model_used': 'test_model'
        }
        
        result = self.db_manager.insert_classification(classification_data)
        self.assertTrue(result)
    
    def test_get_tweets_for_classification(self):
        """Test getting unclassified tweets"""
        # Insert some tweets
        for i in range(3):
            tweet_data = {
                'tweet_id': f'test_{i}',
                'content': f'Test tweet {i}',
                'author': 'test_user',
                'date': '2024-01-01T12:00:00',
                'url': f'https://twitter.com/test{i}',
                'language': 'en'
            }
            self.db_manager.insert_tweet(tweet_data)
        
        # Get unclassified tweets
        unclassified = self.db_manager.get_tweets_for_classification()
        self.assertEqual(len(unclassified), 3)
        
        # Classify one tweet
        classification_data = {
            'tweet_id': 'test_0',
            'classification': 'Likely True',
            'reasoning': 'Test reasoning',
            'model_used': 'test'
        }
        self.db_manager.insert_classification(classification_data)
        
        # Should now have 2 unclassified tweets
        unclassified = self.db_manager.get_tweets_for_classification()
        self.assertEqual(len(unclassified), 2)
    
    def test_get_classification_stats(self):
        """Test getting classification statistics"""
        # Insert tweets and classifications
        classifications = [
            ('tweet_1', 'Likely True'),
            ('tweet_2', 'Likely False'),
            ('tweet_3', 'Likely True'),
            ('tweet_4', 'Misleading')
        ]
        
        for tweet_id, classification in classifications:
            # Insert tweet
            tweet_data = {
                'tweet_id': tweet_id,
                'content': f'Content for {tweet_id}',
                'author': 'test_user',
                'date': '2024-01-01T12:00:00',
                'url': f'https://twitter.com/{tweet_id}',
                'language': 'en'
            }
            self.db_manager.insert_tweet(tweet_data)
            
            # Insert classification
            classification_data = {
                'tweet_id': tweet_id,
                'classification': classification,
                'reasoning': 'Test reasoning',
                'model_used': 'test'
            }
            self.db_manager.insert_classification(classification_data)
        
        stats = self.db_manager.get_classification_stats()
        self.assertEqual(stats['Likely True'], 2)
        self.assertEqual(stats['Likely False'], 1)
        self.assertEqual(stats['Misleading'], 1)

if __name__ == '__main__':
    unittest.main()
