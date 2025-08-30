#!/usr/bin/env python3
"""
Example script demonstrating the Misinformation Detection System

This script shows how to use the various components of the system
to collect, classify, and analyze social media content for misinformation.
"""

import os
import sys
import logging
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from database import DatabaseManager
from data_collector import TwitterDataCollector
from classifier import MisinformationClassifier
from fact_checker import FactChecker
from main_pipeline import MisinformationDetectionPipeline
from utils import create_summary_stats, format_classification_result

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/example_run.log'),
            logging.StreamHandler()
        ]
    )

def example_1_basic_usage():
    """Example 1: Basic system usage"""
    print("="*60)
    print("EXAMPLE 1: Basic System Usage")
    print("="*60)
    
    # Initialize components
    db_manager = DatabaseManager()
    print("✓ Database initialized")
    
    # Test tweet classification
    classifier = MisinformationClassifier(db_manager=db_manager)
    
    # Example tweets to classify
    test_tweets = [
        {
            'tweet_id': 'example_1',
            'content': 'Breaking: Government hiding vaccine side effects! Wake up people!',
            'author': 'conspiracy_user',
            'date': datetime.now().isoformat(),
            'url': 'https://example.com/tweet1',
            'language': 'en'
        },
        {
            'tweet_id': 'example_2', 
            'content': 'New peer-reviewed study shows vaccines are safe and effective according to medical experts.',
            'author': 'science_user',
            'date': datetime.now().isoformat(),
            'url': 'https://example.com/tweet2',
            'language': 'en'
        },
        {
            'tweet_id': 'example_3',
            'content': 'Some people claim climate change is fake, but the evidence is not clear.',
            'author': 'neutral_user',
            'date': datetime.now().isoformat(),
            'url': 'https://example.com/tweet3',
            'language': 'en'
        }
    ]
    
    # Insert tweets into database
    for tweet in test_tweets:
        db_manager.insert_tweet(tweet)
    print(f"✓ Inserted {len(test_tweets)} test tweets")
    
    # Classify tweets
    results = classifier.classify_unprocessed_tweets(limit=10)
    print(f"✓ Classified {len(results)} tweets")
    
    # Display results
    for result in results:
        print(f"\nTweet ID: {result['tweet_id']}")
        print(f"Classification: {result['classification']}")
        print(f"Reasoning: {result['reasoning']}")
        print("-" * 40)
    
    return results

def example_2_data_collection():
    """Example 2: Data collection simulation"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Data Collection Simulation")
    print("="*60)
    
    # Note: This uses mock data since we can't actually scrape in this demo
    collector = TwitterDataCollector()
    
    # Simulate collecting tweets about health misinformation
    mock_tweets = [
        {
            'tweet_id': f'health_{i}',
            'content': f'Sample health-related tweet {i} with various claims about vaccines and treatments.',
            'author': f'user_{i}',
            'date': datetime.now().isoformat(),
            'url': f'https://example.com/health_{i}',
            'language': 'en'
        }
        for i in range(5)
    ]
    
    # Insert mock tweets
    for tweet in mock_tweets:
        collector.db_manager.insert_tweet(tweet)
    
    print(f"✓ Simulated collection of {len(mock_tweets)} health-related tweets")
    
    return mock_tweets

def example_3_fact_checking():
    """Example 3: Fact-checking demonstration"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Fact-checking Integration")
    print("="*60)
    
    fact_checker = FactChecker()
    
    # Example claims to fact-check
    test_claims = [
        "Vaccines cause autism in children",
        "Climate change is a natural phenomenon",
        "COVID-19 was created in a laboratory"
    ]
    
    for claim in test_claims:
        print(f"\nFact-checking: '{claim}'")
        
        # Extract key claims and perform fact check
        result = fact_checker.fact_check_tweet(claim, f"claim_{hash(claim)}")
        
        print(f"Overall Verdict: {result['overall_verdict']}")
        print(f"Claims Found: {result['claims_found']}")
        print(f"Reliability Score: {result['reliability_score']}")
        print("-" * 40)

def example_4_pipeline_run():
    """Example 4: Complete pipeline execution"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Complete Pipeline Execution")
    print("="*60)
    
    # Initialize pipeline
    pipeline = MisinformationDetectionPipeline()
    
    # Configure for demo (smaller numbers)
    pipeline.config['max_tweets_per_run'] = 10
    pipeline.config['enable_fact_checking'] = True
    
    print("Running complete pipeline...")
    
    # Note: In actual usage, this would collect real tweets
    # For demo, we'll use the mock data we already have
    
    # Classify any unprocessed tweets
    results = pipeline.classify_tweets(limit=10)
    
    # Get pipeline statistics
    stats = pipeline.get_pipeline_stats()
    
    print(f"✓ Pipeline completed")
    print(f"✓ Total tweets processed: {stats['total_tweets_processed']}")
    print(f"✓ Classification breakdown: {stats['classification_breakdown']}")
    
    return stats

def example_5_advanced_analysis():
    """Example 5: Advanced analysis and statistics"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Advanced Analysis")
    print("="*60)
    
    db_manager = DatabaseManager()
    
    # Get all classified tweets
    all_classified = db_manager.get_all_classified_tweets()
    
    if not all_classified:
        print("No classified tweets found. Run previous examples first.")
        return
    
    # Create summary statistics
    summary = create_summary_stats(all_classified)
    
    print("📊 Summary Statistics:")
    print(f"Total Tweets Analyzed: {summary['total']}")
    print(f"Average Confidence: {summary['average_confidence']}")
    print("\nClassification Breakdown:")
    
    for classification, data in summary['by_classification'].items():
        print(f"  {classification}: {data['count']} ({data['percentage']}%)")
    
    # Show some example classifications with reasoning
    print("\n🔍 Sample Classifications with Reasoning:")
    for i, tweet in enumerate(all_classified[:3]):
        print(f"\n{i+1}. Tweet: {tweet['content'][:100]}...")
        result = format_classification_result(tweet)
        print(result)

def main():
    """Main function to run all examples"""
    print("🔍 Misinformation Detection System - Example Usage")
    print("=" * 60)
    
    # Create necessary directories
    os.makedirs('data', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # Setup logging
    setup_logging()
    
    try:
        # Run examples
        example_1_basic_usage()
        example_2_data_collection()
        example_3_fact_checking()
        example_4_pipeline_run()
        example_5_advanced_analysis()
        
        print("\n" + "="*60)
        print("✅ All examples completed successfully!")
        print("="*60)
        
        print("\n📋 Next Steps:")
        print("1. Run 'streamlit run dashboard/app.py' to see the web dashboard")
        print("2. Modify the configuration in src/config.py")
        print("3. Implement real Twitter API or snscrape integration")
        print("4. Add your own fact-checking API keys")
        print("5. Customize the classification model")
        
    except Exception as e:
        logging.error(f"Error running examples: {e}")
        print(f"\n❌ Error: {e}")
        print("Check the logs for more details.")

if __name__ == "__main__":
    main()
