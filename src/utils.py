import re
import logging
from typing import List, Dict, Any
from datetime import datetime
import json

def clean_text(text: str) -> str:
    """
    Clean and normalize text content
    
    Args:
        text (str): Raw text to clean
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove mentions and hashtags (but keep the content)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'#(\w+)', r'\1', text)  # Keep hashtag content without #
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    
    return text

def extract_keywords(text: str) -> List[str]:
    """
    Extract potential keywords from text
    
    Args:
        text (str): Text to extract keywords from
        
    Returns:
        List[str]: Extracted keywords
    """
    # Convert to lowercase and split
    words = clean_text(text.lower()).split()
    
    # Filter out common stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
        'before', 'after', 'above', 'below', 'between', 'among', 'this', 'that',
        'these', 'those', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves',
        'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his',
        'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they',
        'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom',
        'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be',
        'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did',
        'doing', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can'
    }
    
    # Filter words that are longer than 2 characters and not stop words
    keywords = [word for word in words if len(word) > 2 and word not in stop_words]
    
    return keywords

def calculate_text_similarity(text1: str, text2: str) -> float:
    """
    Calculate simple similarity between two texts based on common words
    
    Args:
        text1 (str): First text
        text2 (str): Second text
        
    Returns:
        float: Similarity score between 0 and 1
    """
    keywords1 = set(extract_keywords(text1))
    keywords2 = set(extract_keywords(text2))
    
    if not keywords1 or not keywords2:
        return 0.0
    
    # Calculate Jaccard similarity
    intersection = keywords1.intersection(keywords2)
    union = keywords1.union(keywords2)
    
    return len(intersection) / len(union) if union else 0.0

def format_classification_result(result: Dict[str, Any]) -> str:
    """
    Format classification result for display
    
    Args:
        result (Dict): Classification result
        
    Returns:
        str: Formatted result string
    """
    classification = result.get('classification', 'Unknown')
    reasoning = result.get('reasoning', 'No reasoning provided')
    confidence = result.get('confidence', 'Unknown')
    
    formatted = f"""
Classification: {classification}
Confidence: {confidence}
Reasoning: {reasoning}
"""
    
    if 'fact_check_verdict' in result:
        formatted += f"Fact Check: {result['fact_check_verdict']}\n"
    
    return formatted.strip()

def validate_tweet_data(tweet_data: Dict[str, Any]) -> bool:
    """
    Validate tweet data structure
    
    Args:
        tweet_data (Dict): Tweet data to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    required_fields = ['tweet_id', 'content', 'author', 'date']
    
    for field in required_fields:
        if field not in tweet_data or not tweet_data[field]:
            logging.warning(f"Missing or empty required field: {field}")
            return False
    
    # Validate content length
    content = tweet_data['content']
    if len(content) < 5 or len(content) > 500:
        logging.warning(f"Content length invalid: {len(content)} characters")
        return False
    
    return True

def create_search_query(keywords: List[str], date_range: tuple = None) -> str:
    """
    Create a search query string from keywords and optional date range
    
    Args:
        keywords (List[str]): Keywords to search for
        date_range (tuple): Optional (start_date, end_date) tuple
        
    Returns:
        str: Formatted search query
    """
    # Join keywords with OR
    query = ' OR '.join(f'"{keyword}"' for keyword in keywords)
    
    # Add date range if provided
    if date_range and len(date_range) == 2:
        start_date, end_date = date_range
        query += f' since:{start_date.strftime("%Y-%m-%d")} until:{end_date.strftime("%Y-%m-%d")}'
    
    return query

def export_data_to_json(data: List[Dict], filename: str = None) -> str:
    """
    Export data to JSON format
    
    Args:
        data (List[Dict]): Data to export
        filename (str): Optional filename to save to
        
    Returns:
        str: JSON string
    """
    # Add export metadata
    export_data = {
        'export_timestamp': datetime.now().isoformat(),
        'total_records': len(data),
        'data': data
    }
    
    json_string = json.dumps(export_data, indent=2, default=str)
    
    if filename:
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(json_string)
            logging.info(f"Data exported to {filename}")
        except Exception as e:
            logging.error(f"Error exporting to file: {e}")
    
    return json_string

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters
    
    Args:
        filename (str): Filename to sanitize
        
    Returns:
        str: Sanitized filename
    """
    # Remove invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove multiple underscores
    sanitized = re.sub(r'_+', '_', sanitized)
    
    # Trim underscores from start and end
    sanitized = sanitized.strip('_')
    
    return sanitized

def get_confidence_score(classification: str, reasoning: str) -> float:
    """
    Calculate confidence score based on classification and reasoning
    
    Args:
        classification (str): Classification result
        reasoning (str): Reasoning text
        
    Returns:
        float: Confidence score between 0 and 1
    """
    base_score = 0.5
    
    # Adjust based on classification certainty
    if 'likely' in classification.lower():
        base_score += 0.2
    elif 'definite' in classification.lower() or 'certain' in classification.lower():
        base_score += 0.3
    
    # Adjust based on reasoning quality
    reasoning_lower = reasoning.lower()
    
    # Positive indicators
    if any(term in reasoning_lower for term in ['evidence', 'study', 'research', 'verified']):
        base_score += 0.1
    
    if any(term in reasoning_lower for term in ['multiple sources', 'peer-reviewed', 'official']):
        base_score += 0.1
    
    # Negative indicators
    if any(term in reasoning_lower for term in ['unable to', 'unclear', 'uncertain', 'may be']):
        base_score -= 0.1
    
    # Ensure score is between 0 and 1
    return max(0.0, min(1.0, base_score))

def create_summary_stats(classifications: List[Dict]) -> Dict[str, Any]:
    """
    Create summary statistics from classification results
    
    Args:
        classifications (List[Dict]): List of classification results
        
    Returns:
        Dict: Summary statistics
    """
    if not classifications:
        return {'total': 0, 'by_classification': {}, 'average_confidence': 0.0}
    
    total = len(classifications)
    
    # Count by classification
    by_classification = {}
    confidence_scores = []
    
    for result in classifications:
        classification = result.get('classification', 'Unknown')
        by_classification[classification] = by_classification.get(classification, 0) + 1
        
        if 'confidence_score' in result and result['confidence_score']:
            try:
                confidence_scores.append(float(result['confidence_score']))
            except (ValueError, TypeError):
                pass
    
    # Calculate percentages
    for classification in by_classification:
        count = by_classification[classification]
        by_classification[classification] = {
            'count': count,
            'percentage': round(count / total * 100, 2)
        }
    
    # Calculate average confidence
    avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0
    
    return {
        'total': total,
        'by_classification': by_classification,
        'average_confidence': round(avg_confidence, 3),
        'confidence_scores_available': len(confidence_scores)
    }
