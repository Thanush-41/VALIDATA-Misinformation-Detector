# 🔍 Hybrid Large Language Model Framework for Explainable Misinformation Detection

A comprehensive system for detecting and explaining misinformation in social media streams using Large Language Models and fact-checking APIs.

## 🎯 Overview

This project implements a real-time misinformation detection system that:
- Collects tweets using `snscrape` (free alternative to Twitter API)
- Classifies content using Large Language Models with explanatory reasoning
- Cross-verifies results with fact-checking APIs
- Provides an interactive dashboard for visualization and analysis

## ✨ Features

- **Real-time Data Collection**: Scrapes tweets based on keywords and trending topics
- **Explainable AI**: LLM provides detailed reasoning for each classification
- **Hybrid Approach**: Combines AI reasoning with external fact-checking
- **Interactive Dashboard**: Web-based interface for data visualization and analysis
- **Flexible Classification**: Categorizes content as "Likely True", "Likely False", or "Misleading"
- **Export Functionality**: Export results in CSV format for further analysis

## 🏗️ System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Data          │    │   Classification │    │   Fact          │
│   Collection    │───▶│   Engine (LLM)   │───▶│   Checking      │
│   (snscrape)    │    │                  │    │   (APIs)        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
          │                       │                       │
          ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Database (SQLite)                            │
└─────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                Dashboard (Streamlit)                             │
└─────────────────────────────────────────────────────────────────┘
```

## 📋 Prerequisites

- Python 3.8 or higher
- Git
- Internet connection for data collection and model downloads

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd misinformation_detector
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create necessary directories**
   ```bash
   mkdir data logs
   ```

## 🏃‍♂️ Quick Start

### 1. Initialize the Database
```python
from src.database import DatabaseManager

# Initialize database
db = DatabaseManager()
print("Database initialized successfully!")
```

### 2. Collect Sample Data
```python
from src.data_collector import TwitterDataCollector

# Collect tweets about specific topics
collector = TwitterDataCollector()
keywords = ["vaccine misinformation", "covid conspiracy", "climate change hoax"]
tweets = collector.collect_tweets_by_keyword(keywords, max_tweets=50)
print(f"Collected {len(tweets)} tweets")
```

### 3. Classify Tweets
```python
from src.classifier import MisinformationClassifier

# Classify collected tweets
classifier = MisinformationClassifier()
results = classifier.classify_unprocessed_tweets(limit=50)
print(f"Classified {len(results)} tweets")
```

### 4. Run Complete Pipeline
```python
from src.main_pipeline import MisinformationDetectionPipeline

# Run full pipeline
pipeline = MisinformationDetectionPipeline()
summary = pipeline.run_full_pipeline(max_tweets=20)
print(f"Pipeline completed: {summary}")
```

### 5. Launch Dashboard
```bash
streamlit run dashboard/app.py
```

Then open your browser to `http://localhost:8501`

## 📊 Dashboard Features

The Streamlit dashboard provides:

- **Real-time Metrics**: Total tweets processed, classification breakdown
- **Interactive Charts**: Pie charts, timelines, confidence distributions
- **Data Filtering**: Filter by classification, author, date range
- **Individual Analysis**: Detailed view of specific tweets with reasoning
- **Export Options**: Download results as CSV files
- **Pipeline Controls**: Run data collection and classification from the UI

## 🔧 Configuration

Edit `src/config.py` to customize:

```python
# Data Collection Settings
TWITTER_CONFIG = {
    "max_tweets_per_run": 100,
    "days_back": 7,
    "languages": ["en"]
}

# Classification Settings
CLASSIFICATION_CONFIG = {
    "model_name": "microsoft/DialoGPT-medium",
    "batch_size": 10,
    "confidence_threshold": 0.7
}

# Fact-checking Settings
FACT_CHECK_CONFIG = {
    "enabled": True,
    "google_api_key": "your-api-key-here"  # Optional
}
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_database.py

# Run with coverage
python -m pytest tests/ --cov=src
```

## 📁 Project Structure

```
misinformation_detector/
├── src/
│   ├── database.py          # Database management
│   ├── data_collector.py    # Tweet collection using snscrape
│   ├── classifier.py        # LLM-based classification
│   ├── fact_checker.py      # Fact-checking integration
│   ├── main_pipeline.py     # Complete pipeline orchestration
│   ├── config.py           # Configuration settings
│   └── utils.py            # Utility functions
├── dashboard/
│   └── app.py              # Streamlit dashboard
├── tests/
│   ├── test_database.py    # Database tests
│   └── test_classifier.py  # Classification tests
├── data/                   # Database and data files
├── logs/                   # Log files
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🎯 Use Cases

### Research
- Analyze misinformation patterns in social media
- Study the spread of false information during events
- Evaluate the effectiveness of fact-checking

### Content Moderation
- Assist in identifying potentially false content
- Provide explanations for moderation decisions
- Track misinformation trends over time

### Journalism
- Fact-check viral claims quickly
- Monitor emerging conspiracy theories
- Research misinformation sources

## ⚠️ Important Notes

### Legal and Ethical Considerations
- **Terms of Service**: Web scraping may violate platform terms of service
- **Rate Limiting**: Be respectful with request frequency
- **Academic Use**: This tool is intended for research and educational purposes
- **Privacy**: Handle collected data responsibly and in compliance with privacy laws

### Limitations
- **Accuracy**: LLM classifications are not 100% accurate
- **Bias**: Models may have inherent biases
- **Context**: Some content requires human judgment
- **Real-time**: Not suitable for immediate content moderation decisions

### Data Quality
- Clean and preprocess data appropriately
- Validate classifications when possible
- Consider manual review for critical decisions

## 🔮 Future Enhancements

- [ ] Integration with multiple social media platforms
- [ ] Advanced NLP techniques for better accuracy
- [ ] Real-time streaming capabilities
- [ ] Machine learning model fine-tuning
- [ ] Multi-language support
- [ ] API endpoints for external integration
- [ ] Advanced visualization and analytics
- [ ] User feedback integration

## 📈 Performance Tips

1. **Batch Processing**: Process tweets in batches for better performance
2. **Database Indexing**: Add indexes for frequently queried fields
3. **Caching**: Cache classification results to avoid reprocessing
4. **Parallel Processing**: Use multiprocessing for large datasets

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- HuggingFace for providing pre-trained language models
- Streamlit for the dashboard framework
- snscrape developers for the social media scraping tool
- The research community working on misinformation detection

## 📞 Support

If you encounter issues or have questions:

1. Check the [Issues](https://github.com/your-repo/issues) page
2. Create a new issue with detailed information
3. Include logs and error messages when possible

## 📊 Example Output

```
Pipeline Execution Summary:
Tweets Collected: 45
Tweets Classified: 45
  - Likely True: 12 (26.7%)
  - Likely False: 18 (40.0%)
  - Misleading: 15 (33.3%)
Execution Time: 23.4 seconds
```

---

**⚠️ Disclaimer**: This tool is for research and educational purposes. Always verify important information through multiple reliable sources. The classifications provided are not definitive and should be used as one factor in a broader fact-checking process.
