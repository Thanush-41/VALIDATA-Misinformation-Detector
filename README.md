# VALIDATA Fake News Detector

🚀 **Live Demo**: [https://validata-two.vercel.app](https://validata-two.vercel.app)

Welcome to the Fake News Detector project! This AI-powered web application combines machine learning and large language models to detect fake news articles and provide intelligent fact-checking guidance. Built as a comprehensive full-stack solution with Django REST Framework and React.js, deployed on Vercel and Render.

## About VALIDATA

VALIDATA is an intelligent fake news detection system that leverages:
- **Machine Learning**: Naive Bayes classifier trained on 72,134 news articles (89% accuracy)
- **AI Analysis**: Google Gemini API integration for contextual fact-checking guidance
- **Real-time Detection**: Instant predictions with sub-second response times
- **Educational Features**: Interactive news quiz to improve media literacy

The system analyzes news headlines and content using natural language processing to identify potential misinformation, helping users make informed decisions about the news they consume.

## Features

- **🔍 Check News by Title**: Enter any news headline to get instant AI-powered predictions (Real/Fake) with fact-checking guidance
- **📰 Live News Monitoring**: Real-time predictions for current news articles with category filtering
- **🎮 News Quiz**: Interactive quiz to test and improve your fake news detection skills
- **🤖 AI-Powered Analysis**: Google Gemini integration provides contextual explanations and verification tips
- **⚡ Fast & Accurate**: Sub-second predictions with 89% accuracy
- **🎨 Modern UI**: Professional glassmorphism design with 4 color themes (Light, Dark, Blue, Purple)

## Technology Stack

### Backend
- **Framework**: Django 4.2.3 with Django REST Framework
- **ML Model**: Naive Bayes (MultinomialNB) - 89% accuracy
- **Vectorization**: CountVectorizer (Bag of Words)
- **AI Integration**: Google Generative AI (Gemini 1.5 Flash)
- **Web Scraping**: BeautifulSoup4 for live news fetching
- **Deployment**: Render.com with Gunicorn + WhiteNoise

### Frontend
- **Framework**: React.js 18 with Create React App
- **Styling**: Custom CSS with glassmorphism effects
- **State Management**: React Context API
- **Deployment**: Vercel

### Machine Learning Pipeline
- **Dataset**: WELFake Dataset (72,134 articles from Kaggle)
- **Distribution**: Balanced dataset (51% Real, 49% Fake)
- **Features**: Combined title + text content
- **Training Split**: 67% training, 33% testing (random_state=53)
- **Preprocessing**: CountVectorizer with English stop words removal
- **Model Selection**: Naive Bayes chosen for speed (Random Forest 94% accuracy trained but not deployed)

## Architecture

```
┌─────────────────┐
│   React.js UI   │
│  (Vercel)       │
└────────┬────────┘
         │ REST API
         ↓
┌─────────────────┐      ┌──────────────────┐
│  Django API     │─────→│  Google Gemini   │
│  (Render)       │      │  AI Analysis     │
└────────┬────────┘      └──────────────────┘
         │
    ┌────┴────┐
    ↓         ↓
┌────────┐ ┌──────────────┐
│ ML      │ │ SQLite       │
│ Models  │ │ Database     │
└────────┘ └──────────────┘
```

## Implementation Details

### ML Model Training Process

1. **Data Loading**: WELFake_Dataset.csv (72,134 news articles)
2. **Preprocessing**:
   - Combined title and text: `df['title_text'] = df['title'] + df['text']`
   - Handled missing values: `df.fillna('')`
3. **Vectorization**:
   - CountVectorizer with stop words removal
   - Converts text to numerical features (Bag of Words)
4. **Model Training**:
   - Naive Bayes: 89% accuracy (deployed)
   - Random Forest: 94% accuracy (not deployed - slower inference)
5. **Model Serialization**: Saved as `nb_model.pkl` and `vectorizer_model.pkl`

### Prediction Pipeline

1. User submits news headline via React frontend
2. POST request to `/api/usercheckbytitle/`
3. Backend vectorizes input using trained CountVectorizer
4. Naive Bayes model predicts: 0 (fake) or 1 (real)
5. Google Gemini API generates contextual analysis
6. Response includes prediction + AI fact-checking guidance
7. Frontend displays results with visual indicators

### API Endpoints

```
POST /api/usercheckbytitle/
Body: { "user_news": "headline text" }
Response: { 
  "prediction": true/false,
  "analysis": "AI-generated fact-checking guidance"
}

GET /api/livenews/
Response: Array of news articles with predictions

GET /api/newsquiz/
Response: Quiz questions with answers
```

## Performance Metrics

- **Model Accuracy**: 89%
- **Precision**: ~88-90%
- **Recall**: ~87-89%
- **F1-Score**: ~88-89%
- **Response Time**: <500ms (ML prediction) + <2s (with Gemini analysis)
- **Dataset Size**: 72,134 articles
- **Model Size**: ~15MB (combined models)

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- Google Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))

### Local Development Setup

1. **Clone the repository**

```bash
git clone https://github.com/Thanush-41/VALIDATA-Misinformation-Detector
cd Fake-News-Detector
```

2. **Backend Setup**

```bash
cd app/FakeNewsDetectorAPI
pip install -r requirements.txt
```

3. **Configure Environment Variables**

Create `.env` file in `app/FakeNewsDetectorAPI/`:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash-latest
```

4. **Initialize Database**

```bash
python manage.py migrate
python manage.py quiz_data_loader game_data/game_data.csv
```

5. **Start Backend Server**

```bash
python manage.py runserver
```

Backend runs on `http://localhost:8000`

6. **Frontend Setup** (in new terminal)

```bash
cd app/fake-news-detector-frontend
npm install
```

7. **Configure Frontend API**

Update `src/context/index.js` if needed to point to your backend URL:

```javascript
const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';
```

8. **Start Frontend**

```bash
npm start
```

Frontend opens at `http://localhost:3000`

### Production Deployment

#### Backend (Render)

1. Create new Web Service on Render.com
2. Connect GitHub repository
3. Configure:
   - **Root Directory**: `app/FakeNewsDetectorAPI`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn FakeNewsDetectorAPI.wsgi:application`
4. Add environment variables:
   - `GOOGLE_API_KEY`: Your Gemini API key
   - `GEMINI_MODEL`: `gemini-1.5-flash-latest`
   - `PYTHON_VERSION`: `3.11.0`
5. Deploy

#### Frontend (Vercel)

1. Import repository to Vercel
2. Configure:
   - **Framework Preset**: Create React App
   - **Root Directory**: `app/fake-news-detector-frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
3. Add environment variable:
   - `REACT_APP_API_URL`: Your Render backend URL
4. Deploy

### Model Training (Optional)

To retrain models with your own dataset:

1. Open `FakeNewsDetection_AIProject.ipynb` in Jupyter
2. Update dataset path
3. Run all cells
4. Copy generated `.pkl` files to `app/FakeNewsDetectorAPI/models/`
5. Restart Django server

## Project Structure

```
Fake-News-Detector/
├── FakeNewsDetection_AIProject.ipynb  # ML model training notebook
├── app/
│   ├── FakeNewsDetectorAPI/           # Django backend
│   │   ├── manage.py
│   │   ├── requirements.txt
│   │   ├── models/                    # Trained ML models
│   │   │   ├── nb_model.pkl
│   │   │   └── vectorizer_model.pkl
│   │   ├── core/                      # Core app
│   │   │   ├── model.py               # Model loading
│   │   │   ├── llm.py                 # Gemini integration
│   │   │   ├── views.py
│   │   │   ├── livenews/              # Live news API
│   │   │   ├── newsquiz/              # Quiz API
│   │   │   └── usercheckbytitle/      # Prediction API
│   │   └── FakeNewsDetectorAPI/       # Django settings
│   │       ├── settings.py
│   │       └── urls.py
│   └── fake-news-detector-frontend/   # React frontend
│       ├── package.json
│       ├── src/
│       │   ├── App.js
│       │   ├── components/            # React components
│       │   │   ├── home.js
│       │   │   ├── checkbytitle.js
│       │   │   ├── category.js
│       │   │   └── newsquiz.js
│       │   ├── context/               # Context API
│       │   └── styles/
│       │       └── main.css           # Modern UI styles
│       └── public/
├── render.yaml                        # Render deployment config
└── vercel.json                        # Vercel deployment config
```

## Key Features Explained

### 1. AI-Powered Fact-Checking

When you submit a headline, the system:
- Vectorizes the text using the trained CountVectorizer
- Predicts fake/real using Naive Bayes classifier
- Sends the headline to Google Gemini for contextual analysis
- Returns both ML prediction and AI-generated verification guidance

### 2. Live News Monitoring

- Fetches real-time news from multiple sources using BeautifulSoup4
- Automatically predicts credibility for each article
- Categorizes news by topic (Politics, Technology, Sports, etc.)
- Updates periodically to show latest articles

### 3. Interactive News Quiz

- Educational feature to train users on spotting fake news
- Database of curated questions with explanations
- Tracks scores and provides instant feedback
- Helps improve media literacy skills

## Why Naive Bayes?

Despite training a Random Forest model with 94% accuracy, we deployed Naive Bayes (89% accuracy) because:

1. **Speed**: Naive Bayes inference is 5-10x faster (~0.3ms vs 3-5ms)
2. **Real-time Requirements**: Web applications need instant responses
3. **Sufficient Accuracy**: 89% is excellent for this use case
4. **Resource Efficiency**: Lower memory footprint and CPU usage
5. **Scalability**: Can handle more concurrent requests

The 5% accuracy tradeoff is worth the significant performance gains for production deployment.

## Dataset Information

**WELFake Dataset** (Kaggle)
- **Source**: Public dataset combining 4 popular news datasets
- **Size**: 72,134 articles
- **Balance**: 51% Real, 49% Fake (well-balanced)
- **Features**: 
  - Title: News headline
  - Text: Article body content
  - Label: 0 (Fake) or 1 (Real)
- **Coverage**: Diverse topics including politics, world news, entertainment
- **Quality**: Pre-cleaned and verified labels

## Contributing

I welcome contributions from fellow developers! Here's how you can help:

### Areas for Contribution

1. **ML Improvements**
   - Experiment with different models (LSTM, BERT, etc.)
   - Improve feature engineering
   - Add multilingual support

2. **Features**
   - Browser extension for real-time fact-checking
   - User accounts and history tracking
   - Social media integration
   - Batch analysis API

3. **UI/UX**
   - Mobile app development
   - Accessibility improvements
   - Additional themes and customization

4. **Documentation**
   - API documentation
   - Video tutorials
   - Translation to other languages

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure your code follows the existing style and includes appropriate tests.

## Roadmap

### Completed ✅
- Machine learning model training (Naive Bayes, Random Forest)
- Google Gemini AI integration
- REST API with Django
- React frontend with modern UI
- Live news scraping and prediction
- Interactive news quiz
- Production deployment (Vercel + Render)

### In Progress 🚧
- Browser extension for on-page fact-checking
- User authentication and profile system
- Historical prediction tracking

### Planned 📋
- **Enhanced ML Models**: BERT-based transformer models for higher accuracy
- **Multilingual Support**: Detect fake news in multiple languages
- **Mobile App**: Native iOS/Android applications
- **Social Media Integration**: Check tweets, Facebook posts, etc.
- **Batch Analysis API**: Upload CSV for bulk analysis
- **Credibility Scoring**: Source reputation tracking
- **User Profiles**: Personal dashboards with history and statistics
- **Community Features**: User feedback on predictions
- **Advanced Analytics**: Visualization of fake news trends
- **API Rate Limiting**: Implement usage tiers

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'core'`
- **Solution**: Ensure you're in the correct directory and have installed requirements

**Issue**: Gemini API returns errors
- **Solution**: Verify `GOOGLE_API_KEY` is set correctly and model name is `gemini-1.5-flash-latest`

**Issue**: Frontend can't connect to backend
- **Solution**: Check CORS settings in `settings.py` and update `REACT_APP_API_URL`

**Issue**: Models not loading
- **Solution**: Ensure `nb_model.pkl` and `vectorizer_model.pkl` exist in `models/` directory

**Issue**: Quiz data not loading
- **Solution**: Run `python manage.py quiz_data_loader game_data/game_data.csv`

## Performance Optimization Tips

1. **Caching**: Implement Redis for frequently checked headlines
2. **Database**: Switch to PostgreSQL for production (currently SQLite)
3. **CDN**: Use CDN for static assets
4. **Load Balancing**: Use multiple backend instances for high traffic
5. **Model Optimization**: Quantize models to reduce size and improve speed

## Security Considerations

- API keys stored in environment variables (never commit to Git)
- CORS configured to allow only specific origins
- Input validation on all API endpoints
- Rate limiting recommended for production
- Regular dependency updates for security patches

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **WELFake Dataset**: Kaggle dataset by Saurabh Shahane
- **Google Gemini**: AI-powered analysis capabilities
- **Scikit-learn**: Machine learning library
- **Django & React**: Excellent frameworks for full-stack development
- **Vercel & Render**: Reliable hosting platforms

## Citations

If you use this project in your research or application, please cite:

```bibtex
@software{validata2024,
  author = {Thanush Garimella},
  title = {VALIDATA: AI-Powered Fake News Detection System},
  year = {2024},
  url = {https://github.com/Thanush-41/VALIDATA-Misinformation-Detector}
}
```

## Contact

- **Developer**: Thanush Garimella
- **Email**: [thanushgarimella@gmail.com](mailto:thanushgarimella@gmail.com)
- **GitHub**: [@Thanush-41](https://github.com/Thanush-41)
- **Issues**: [Report Issues](https://github.com/Thanush-41/VALIDATA-Misinformation-Detector/issues)
- **Live Demo**: [https://validata-two.vercel.app](https://validata-two.vercel.app)

## Stats

![GitHub stars](https://img.shields.io/github/stars/Thanush-41/VALIDATA-Misinformation-Detector?style=social)
![GitHub forks](https://img.shields.io/github/forks/Thanush-41/VALIDATA-Misinformation-Detector?style=social)
![GitHub issues](https://img.shields.io/github/issues/Thanush-41/VALIDATA-Misinformation-Detector)
![GitHub license](https://img.shields.io/github/license/Thanush-41/VALIDATA-Misinformation-Detector)

---

**Made with ❤️ to combat misinformation**

Thank you for considering contributing to VALIDATA. Together, we can make a positive impact on the fight against misinformation and promote media literacy!

Happy coding! 🚀
