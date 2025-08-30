import logging
import json
import re
from typing import Dict, List, Tuple
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from database import DatabaseManager

class MisinformationClassifier:
    def __init__(self, model_name="microsoft/DialoGPT-medium", db_manager=None):
        """
        Initialize the misinformation classifier
        
        Args:
            model_name (str): HuggingFace model name to use
            db_manager: Database manager instance
        """
        self.db_manager = db_manager or DatabaseManager()
        self.model_name = model_name
        self.classifier = None
        self.load_model()
        
    def load_model(self):
        """Load the language model for classification"""
        try:
            # Use a text generation pipeline for explanation
            self.classifier = pipeline(
                "text-generation",
                model="microsoft/DialoGPT-medium",
                tokenizer="microsoft/DialoGPT-medium",
                max_length=512,
                truncation=True
            )
            logging.info(f"Model {self.model_name} loaded successfully")
        except Exception as e:
            logging.error(f"Error loading model: {e}")
            # Fallback to a simpler approach
            self.classifier = None
    
    def create_classification_prompt(self, tweet_content: str) -> str:
        """
        Create a prompt for the LLM to classify and explain the tweet
        
        Args:
            tweet_content (str): The tweet content to classify
            
        Returns:
            str: Formatted prompt for the LLM
        """
        prompt = f"""
Analyze the following tweet for misinformation and classify it as one of: "Likely True", "Likely False", or "Misleading".

Tweet: "{tweet_content}"

Please provide:
1. Classification: [Likely True/Likely False/Misleading]
2. Reasoning: [Detailed explanation for your classification]
3. Confidence: [High/Medium/Low]

Classification:"""
        
        return prompt
    
    def parse_llm_response(self, response: str) -> Dict[str, str]:
        """
        Parse the LLM response to extract classification and reasoning
        
        Args:
            response (str): Raw response from the LLM
            
        Returns:
            Dict containing classification, reasoning, and confidence
        """
        result = {
            'classification': 'Unknown',
            'reasoning': 'Unable to determine',
            'confidence': 'Low'
        }
        
        try:
            # Extract classification
            classification_patterns = [
                r'Classification:\s*([^\\n]+)',
                r'(Likely True|Likely False|Misleading)',
                r'Answer:\s*(Likely True|Likely False|Misleading)'
            ]
            
            for pattern in classification_patterns:
                match = re.search(pattern, response, re.IGNORECASE)
                if match:
                    classification = match.group(1).strip()
                    if any(term in classification.lower() for term in ['true', 'false', 'misleading']):
                        result['classification'] = classification
                        break
            
            # Extract reasoning
            reasoning_patterns = [
                r'Reasoning:\s*([^\\n]+(?:\\n[^\\n]+)*?)(?=\\n\\d+\.|\\nConfidence:|$)',
                r'Explanation:\s*([^\\n]+(?:\\n[^\\n]+)*?)(?=\\n\\d+\.|\\nConfidence:|$)',
                r'Because\s+([^\\n]+(?:\\n[^\\n]+)*?)(?=\\n\\d+\.|\\nConfidence:|$)'
            ]
            
            for pattern in reasoning_patterns:
                match = re.search(pattern, response, re.IGNORECASE | re.DOTALL)
                if match:
                    result['reasoning'] = match.group(1).strip()
                    break
            
            # Extract confidence
            confidence_match = re.search(r'Confidence:\s*(High|Medium|Low)', response, re.IGNORECASE)
            if confidence_match:
                result['confidence'] = confidence_match.group(1).capitalize()
        
        except Exception as e:
            logging.error(f"Error parsing LLM response: {e}")
        
        return result
    
    def rule_based_classification(self, tweet_content: str) -> Dict[str, str]:
        """
        Fallback rule-based classification when LLM is not available
        
        Args:
            tweet_content (str): Tweet content to classify
            
        Returns:
            Dict containing classification and reasoning
        """
        content_lower = tweet_content.lower()
        
        # Suspicious keywords that might indicate misinformation
        false_indicators = [
            'conspiracy', 'cover-up', 'they don\'t want you to know', 'big pharma',
            'government lies', 'mainstream media lies', 'fake news', 'hoax',
            'secret agenda', 'wake up', 'sheep', 'truth they hide'
        ]
        
        misleading_indicators = [
            'some say', 'many believe', 'sources claim', 'rumor has it',
            'allegedly', 'supposedly', 'unconfirmed reports', 'breaking',
            'exclusive', 'insider information'
        ]
        
        credible_indicators = [
            'study shows', 'research indicates', 'scientists confirm',
            'official statement', 'peer-reviewed', 'clinical trial',
            'evidence suggests', 'data shows', 'according to experts'
        ]
        
        false_score = sum(1 for term in false_indicators if term in content_lower)
        misleading_score = sum(1 for term in misleading_indicators if term in content_lower)
        credible_score = sum(1 for term in credible_indicators if term in content_lower)
        
        if false_score > 0:
            return {
                'classification': 'Likely False',
                'reasoning': f'Contains {false_score} suspicious terms often associated with misinformation',
                'confidence': 'Medium'
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
                'confidence': 'Medium'
            }
        else:
            return {
                'classification': 'Misleading',
                'reasoning': 'Unable to determine credibility, marked as potentially misleading for safety',
                'confidence': 'Low'
            }
    
    def classify_tweet(self, tweet_content: str, tweet_id: str) -> Dict[str, str]:
        """
        Classify a single tweet for misinformation
        
        Args:
            tweet_content (str): The tweet content to classify
            tweet_id (str): The tweet ID
            
        Returns:
            Dict containing classification results
        """
        try:
            if self.classifier:
                # Use LLM for classification
                prompt = self.create_classification_prompt(tweet_content)
                
                try:
                    response = self.classifier(prompt, max_length=200, num_return_sequences=1)
                    llm_output = response[0]['generated_text']
                    result = self.parse_llm_response(llm_output)
                    result['model_used'] = self.model_name
                except Exception as e:
                    logging.error(f"LLM classification failed: {e}")
                    result = self.rule_based_classification(tweet_content)
                    result['model_used'] = 'rule_based'
            else:
                # Use rule-based classification
                result = self.rule_based_classification(tweet_content)
                result['model_used'] = 'rule_based'
            
            # Add tweet_id to result
            result['tweet_id'] = tweet_id
            
            return result
        
        except Exception as e:
            logging.error(f"Error classifying tweet {tweet_id}: {e}")
            return {
                'tweet_id': tweet_id,
                'classification': 'Unknown',
                'reasoning': f'Classification failed due to error: {str(e)}',
                'confidence': 'Low',
                'model_used': 'error'
            }
    
    def classify_tweets_batch(self, tweets: List[Dict], batch_size: int = 10) -> List[Dict]:
        """
        Classify multiple tweets in batches
        
        Args:
            tweets (List[Dict]): List of tweet dictionaries
            batch_size (int): Number of tweets to process at once
            
        Returns:
            List of classification results
        """
        results = []
        
        for i in range(0, len(tweets), batch_size):
            batch = tweets[i:i + batch_size]
            logging.info(f"Processing batch {i // batch_size + 1} of {len(tweets) // batch_size + 1}")
            
            for tweet in batch:
                result = self.classify_tweet(tweet['content'], tweet['tweet_id'])
                results.append(result)
                
                # Store result in database
                self.db_manager.insert_classification(result)
        
        return results
    
    def classify_unprocessed_tweets(self, limit: int = 100) -> List[Dict]:
        """
        Classify all unprocessed tweets in the database
        
        Args:
            limit (int): Maximum number of tweets to process
            
        Returns:
            List of classification results
        """
        # Get unprocessed tweets from database
        unprocessed_tweets = self.db_manager.get_tweets_for_classification(limit)
        
        if not unprocessed_tweets:
            logging.info("No unprocessed tweets found")
            return []
        
        logging.info(f"Found {len(unprocessed_tweets)} unprocessed tweets")
        
        # Classify tweets
        results = self.classify_tweets_batch(unprocessed_tweets)
        
        logging.info(f"Classified {len(results)} tweets successfully")
        return results

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Initialize classifier
    classifier = MisinformationClassifier()
    
    # Example tweet
    test_tweet = {
        'tweet_id': 'test_123',
        'content': 'Breaking: Government hiding vaccine side effects from public. Wake up sheeple!'
    }
    
    # Classify the tweet
    result = classifier.classify_tweet(test_tweet['content'], test_tweet['tweet_id'])
    
    print(f"Classification: {result['classification']}")
    print(f"Reasoning: {result['reasoning']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Model Used: {result['model_used']}")
