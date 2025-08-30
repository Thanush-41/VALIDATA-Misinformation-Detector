import requests
import logging
import json
from typing import Dict, Optional, List
from urllib.parse import quote

class FactChecker:
    def __init__(self):
        """Initialize the fact checker with various API endpoints"""
        self.google_fact_check_api_key = None  # Set your API key here
        self.politifact_base_url = "https://www.politifact.com/api/statements/truth-o-meter/"
        
        # Free fact-checking sources (web scraping approach)
        self.fact_check_sources = [
            "snopes.com",
            "factcheck.org", 
            "politifact.com",
            "reuters.com/fact-check",
            "apnews.com/hub/ap-fact-check"
        ]
    
    def search_google_fact_check(self, query: str) -> Optional[Dict]:
        """
        Search Google Fact Check Tools API
        
        Args:
            query (str): Query to search for fact checks
            
        Returns:
            Dict containing fact check results or None
        """
        if not self.google_fact_check_api_key:
            logging.warning("Google Fact Check API key not configured")
            return None
        
        try:
            url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
            params = {
                'key': self.google_fact_check_api_key,
                'query': query,
                'languageCode': 'en'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'claims' in data and len(data['claims']) > 0:
                    claim = data['claims'][0]  # Get first result
                    
                    return {
                        'source': 'Google Fact Check',
                        'claim': claim.get('text', ''),
                        'rating': claim.get('claimReview', [{}])[0].get('textualRating', 'Unknown'),
                        'url': claim.get('claimReview', [{}])[0].get('url', ''),
                        'publisher': claim.get('claimReview', [{}])[0].get('publisher', {}).get('name', 'Unknown')
                    }
            
        except Exception as e:
            logging.error(f"Error searching Google Fact Check: {e}")
        
        return None
    
    def search_web_fact_checks(self, query: str) -> List[Dict]:
        """
        Search for fact checks using web search (simplified approach)
        
        Args:
            query (str): Query to search for
            
        Returns:
            List of potential fact check results
        """
        results = []
        
        # This is a simplified approach - in practice, you'd use a proper web scraping library
        # or search API to find fact checks
        
        search_terms = [
            f"{query} fact check",
            f"{query} debunked", 
            f"{query} verified",
            f"{query} true or false"
        ]
        
        for term in search_terms:
            # Simulate fact check search results
            # In a real implementation, you would use libraries like requests + BeautifulSoup
            # to search and scrape fact-checking websites
            
            mock_result = {
                'query': term,
                'potential_sources': self.fact_check_sources,
                'search_url': f"https://www.google.com/search?q={quote(term)}",
                'note': 'This is a mock result - implement actual web scraping for real fact checks'
            }
            results.append(mock_result)
        
        return results
    
    def extract_key_claims(self, tweet_content: str) -> List[str]:
        """
        Extract key factual claims from tweet content
        
        Args:
            tweet_content (str): Tweet text to analyze
            
        Returns:
            List of extracted claims
        """
        # Simple claim extraction - in practice, use NLP techniques
        claims = []
        
        # Look for common claim patterns
        claim_indicators = [
            "studies show", "research proves", "scientists say",
            "government confirms", "data reveals", "reports indicate",
            "breaking news", "confirmed cases", "official statement"
        ]
        
        tweet_lower = tweet_content.lower()
        
        for indicator in claim_indicators:
            if indicator in tweet_lower:
                # Extract sentence containing the indicator
                sentences = tweet_content.split('.')
                for sentence in sentences:
                    if indicator in sentence.lower():
                        claims.append(sentence.strip())
        
        # If no specific claims found, use the whole tweet as a claim
        if not claims:
            claims.append(tweet_content)
        
        return claims
    
    def fact_check_tweet(self, tweet_content: str, tweet_id: str) -> Dict:
        """
        Perform fact checking on a tweet
        
        Args:
            tweet_content (str): Tweet content to fact check
            tweet_id (str): Tweet ID
            
        Returns:
            Dict containing fact check results
        """
        logging.info(f"Fact checking tweet {tweet_id}")
        
        # Extract key claims
        claims = self.extract_key_claims(tweet_content)
        
        fact_check_results = {
            'tweet_id': tweet_id,
            'claims_found': len(claims),
            'fact_checks': [],
            'overall_verdict': 'Unknown',
            'sources_checked': 0,
            'reliability_score': 0.0
        }
        
        for claim in claims:
            # Try Google Fact Check API first
            google_result = self.search_google_fact_check(claim)
            if google_result:
                fact_check_results['fact_checks'].append(google_result)
                fact_check_results['sources_checked'] += 1
            
            # Search web for fact checks
            web_results = self.search_web_fact_checks(claim)
            fact_check_results['fact_checks'].extend(web_results)
        
        # Determine overall verdict based on fact checks found
        if fact_check_results['sources_checked'] > 0:
            # Simple logic - in practice, use more sophisticated analysis
            ratings = [fc.get('rating', '').lower() for fc in fact_check_results['fact_checks'] 
                      if isinstance(fc, dict) and 'rating' in fc]
            
            false_indicators = ['false', 'misleading', 'incorrect', 'debunked']
            true_indicators = ['true', 'correct', 'verified', 'accurate']
            
            false_count = sum(1 for rating in ratings if any(indicator in rating for indicator in false_indicators))
            true_count = sum(1 for rating in ratings if any(indicator in rating for indicator in true_indicators))
            
            if false_count > true_count:
                fact_check_results['overall_verdict'] = 'Likely False'
                fact_check_results['reliability_score'] = 0.2
            elif true_count > false_count:
                fact_check_results['overall_verdict'] = 'Likely True'
                fact_check_results['reliability_score'] = 0.8
            else:
                fact_check_results['overall_verdict'] = 'Mixed Evidence'
                fact_check_results['reliability_score'] = 0.5
        else:
            fact_check_results['overall_verdict'] = 'No Fact Checks Found'
            fact_check_results['reliability_score'] = 0.3
        
        return fact_check_results
    
    def cross_verify_classification(self, llm_classification: Dict, tweet_content: str) -> Dict:
        """
        Cross-verify LLM classification with fact checking results
        
        Args:
            llm_classification (Dict): Results from LLM classification
            tweet_content (str): Original tweet content
            
        Returns:
            Dict containing combined results
        """
        fact_check_result = self.fact_check_tweet(tweet_content, llm_classification['tweet_id'])
        
        # Combine LLM and fact check results
        combined_result = llm_classification.copy()
        combined_result['fact_check_verdict'] = fact_check_result['overall_verdict']
        combined_result['fact_check_sources'] = fact_check_result['sources_checked']
        combined_result['reliability_score'] = fact_check_result['reliability_score']
        
        # Adjust final classification based on fact check results
        llm_class = llm_classification['classification'].lower()
        fact_verdict = fact_check_result['overall_verdict'].lower()
        
        if 'false' in fact_verdict and 'false' not in llm_class:
            combined_result['final_classification'] = 'Likely False'
            combined_result['final_reasoning'] = f"LLM classified as '{llm_classification['classification']}' but fact-checking suggests false information"
        elif 'true' in fact_verdict and 'true' not in llm_class:
            combined_result['final_classification'] = 'Likely True'
            combined_result['final_reasoning'] = f"LLM classified as '{llm_classification['classification']}' but fact-checking suggests accurate information"
        else:
            combined_result['final_classification'] = llm_classification['classification']
            combined_result['final_reasoning'] = llm_classification['reasoning']
        
        return combined_result

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Initialize fact checker
    fact_checker = FactChecker()
    
    # Example tweet content
    test_content = "Breaking: Studies show vaccines cause autism in 90% of children. Government hiding the truth!"
    
    # Perform fact check
    result = fact_checker.fact_check_tweet(test_content, "test_123")
    
    print(f"Claims found: {result['claims_found']}")
    print(f"Overall verdict: {result['overall_verdict']}")
    print(f"Sources checked: {result['sources_checked']}")
    print(f"Reliability score: {result['reliability_score']}")
    
    # Example LLM classification to cross-verify
    llm_result = {
        'tweet_id': 'test_123',
        'classification': 'Likely False',
        'reasoning': 'Contains conspiracy theory language and unsubstantiated claims',
        'confidence': 'High'
    }
    
    # Cross-verify
    combined_result = fact_checker.cross_verify_classification(llm_result, test_content)
    print(f"Final classification: {combined_result['final_classification']}")
    print(f"Final reasoning: {combined_result['final_reasoning']}")
