import unittest
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from classifier import MisinformationClassifier
from utils import clean_text, extract_keywords, calculate_text_similarity

class TestMisinformationClassifier(unittest.TestCase):
    def setUp(self):
        """Set up test classifier"""
        self.classifier = MisinformationClassifier()
    
    def test_rule_based_classification(self):
        """Test rule-based classification fallback"""
        # Test false indicators
        false_tweet = "This is a conspiracy by big pharma to hide the truth from you!"
        result = self.classifier.rule_based_classification(false_tweet)
        self.assertEqual(result['classification'], 'Likely False')
        
        # Test misleading indicators
        misleading_tweet = "Some say that vaccines are dangerous, allegedly causing problems."
        result = self.classifier.rule_based_classification(misleading_tweet)
        self.assertEqual(result['classification'], 'Misleading')
        
        # Test credible indicators
        credible_tweet = "Recent study shows vaccines are effective according to peer-reviewed research."
        result = self.classifier.rule_based_classification(credible_tweet)
        self.assertEqual(result['classification'], 'Likely True')
    
    def test_create_classification_prompt(self):
        """Test prompt creation"""
        tweet_content = "Test tweet about vaccines"
        prompt = self.classifier.create_classification_prompt(tweet_content)
        
        self.assertIn("Likely True", prompt)
        self.assertIn("Likely False", prompt)
        self.assertIn("Misleading", prompt)
        self.assertIn(tweet_content, prompt)
    
    def test_parse_llm_response(self):
        """Test parsing LLM responses"""
        # Test successful parsing
        response = """
        Classification: Likely False
        Reasoning: This tweet contains conspiracy theory language and unsubstantiated claims.
        Confidence: High
        """
        
        result = self.classifier.parse_llm_response(response)
        self.assertEqual(result['classification'], 'Likely False')
        self.assertIn('conspiracy', result['reasoning'])
        self.assertEqual(result['confidence'], 'High')
    
    def test_classify_tweet(self):
        """Test tweet classification"""
        tweet_content = "Government is hiding vaccine side effects from the public!"
        tweet_id = "test_123"
        
        result = self.classifier.classify_tweet(tweet_content, tweet_id)
        
        self.assertEqual(result['tweet_id'], tweet_id)
        self.assertIn(result['classification'], ['Likely True', 'Likely False', 'Misleading', 'Unknown'])
        self.assertIsInstance(result['reasoning'], str)
        self.assertIn(result['model_used'], ['rule_based', 'error'])  # Since we don't have actual LLM

class TestUtils(unittest.TestCase):
    def test_clean_text(self):
        """Test text cleaning function"""
        dirty_text = "Check this out! https://example.com @user #hashtag 🔥"
        clean = clean_text(dirty_text)
        
        self.assertNotIn('https://example.com', clean)
        self.assertNotIn('@user', clean)
        self.assertNotIn('🔥', clean)
        self.assertIn('hashtag', clean)  # Should keep hashtag content
    
    def test_extract_keywords(self):
        """Test keyword extraction"""
        text = "This is a test about vaccine misinformation and conspiracy theories"
        keywords = extract_keywords(text)
        
        self.assertIn('vaccine', keywords)
        self.assertIn('misinformation', keywords)
        self.assertIn('conspiracy', keywords)
        self.assertIn('theories', keywords)
        
        # Should not contain stop words
        self.assertNotIn('this', keywords)
        self.assertNotIn('and', keywords)
    
    def test_calculate_text_similarity(self):
        """Test text similarity calculation"""
        text1 = "vaccine misinformation conspiracy"
        text2 = "vaccine conspiracy theory"
        
        similarity = calculate_text_similarity(text1, text2)
        self.assertGreater(similarity, 0)  # Should have some similarity
        self.assertLessEqual(similarity, 1)  # Should not exceed 1
        
        # Test identical texts
        similarity_identical = calculate_text_similarity(text1, text1)
        self.assertEqual(similarity_identical, 1.0)
        
        # Test completely different texts
        text3 = "weather forecast sunny"
        similarity_different = calculate_text_similarity(text1, text3)
        self.assertEqual(similarity_different, 0.0)

if __name__ == '__main__':
    unittest.main()
