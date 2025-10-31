import React from 'react';
import { Container, Row, Col, Card, Table, Badge } from 'react-bootstrap';
import Header from './header';
import '../styles/documentation.css';

function Documentation() {
  document.title = 'News Guardian | Documentation';
  let stage = 4;

  return (
    <>
      <Header activeContainer={stage} />
      <Container fluid="lg" className="documentation-container">
        <h1 className="doc-title">Project Documentation</h1>
        
        {/* Project Overview */}
        <Card className="doc-card">
          <Card.Body>
            <h2 className="doc-section-title">📋 Project Overview</h2>
            <p className="doc-text">
              <strong>News Guardian</strong> is an AI-powered fake news detection system that combines 
              traditional machine learning with modern Large Language Models (LLMs) to help users identify 
              misinformation and assess news credibility.
            </p>
            <p className="doc-text">
              The system provides real-time news monitoring, interactive quizzes, and detailed analysis 
              of news articles using both classical ML models and LLM-based insights.
            </p>
          </Card.Body>
        </Card>

        {/* Tech Stack */}
        <Card className="doc-card">
          <Card.Body>
            <h2 className="doc-section-title">🛠️ Technology Stack</h2>
            <Row>
              <Col md={6}>
                <h4 className="doc-subsection-title">Frontend</h4>
                <ul className="tech-list">
                  <li><Badge bg="primary">React.js</Badge> - UI Framework</li>
                  <li><Badge bg="info">React Bootstrap</Badge> - Component Library</li>
                  <li><Badge bg="secondary">React Router</Badge> - Navigation</li>
                  <li><Badge bg="success">Axios</Badge> - HTTP Client</li>
                  <li><Badge bg="warning">React Toastify</Badge> - Notifications</li>
                  <li><Badge bg="dark">React Icons</Badge> - Icon Library</li>
                </ul>
              </Col>
              <Col md={6}>
                <h4 className="doc-subsection-title">Backend</h4>
                <ul className="tech-list">
                  <li><Badge bg="success">Django 4.2.3</Badge> - Web Framework</li>
                  <li><Badge bg="primary">Django REST Framework</Badge> - API</li>
                  <li><Badge bg="info">SQLite</Badge> - Database</li>
                  <li><Badge bg="warning">scikit-learn</Badge> - ML Library</li>
                  <li><Badge bg="danger">Requests</Badge> - HTTP Library</li>
                  <li><Badge bg="secondary">CORS Headers</Badge> - Cross-Origin</li>
                </ul>
              </Col>
            </Row>
            <Row className="mt-3">
              <Col md={6}>
                <h4 className="doc-subsection-title">Machine Learning</h4>
                <ul className="tech-list">
                  <li><Badge bg="primary">Multinomial Naive Bayes</Badge> - Classifier</li>
                  <li><Badge bg="info">CountVectorizer</Badge> - Text Vectorization</li>
                  <li><Badge bg="success">Ollama</Badge> - Local LLM Runtime</li>
                  <li><Badge bg="warning">Llama 3</Badge> - Language Model</li>
                </ul>
              </Col>
              <Col md={6}>
                <h4 className="doc-subsection-title">External APIs</h4>
                <ul className="tech-list">
                  <li><Badge bg="dark">The Guardian API</Badge> - Live News Data</li>
                </ul>
              </Col>
            </Row>
          </Card.Body>
        </Card>

        {/* System Architecture */}
        <Card className="doc-card">
          <Card.Body>
            <h2 className="doc-section-title">🏗️ System Architecture</h2>
            <div className="architecture-section">
              <h4 className="doc-subsection-title">Data Flow</h4>
              <ol className="doc-text">
                <li><strong>User Input:</strong> User submits news title/article through React frontend</li>
                <li><strong>API Request:</strong> Frontend sends POST request to Django REST API</li>
                <li><strong>Text Vectorization:</strong> CountVectorizer transforms text into numerical features</li>
                <li><strong>ML Prediction:</strong> Multinomial Naive Bayes classifier predicts Real/Fake</li>
                <li><strong>LLM Analysis:</strong> Ollama (Llama 3) generates detailed credibility analysis</li>
                <li><strong>Response:</strong> Combined prediction + analysis returned to frontend</li>
                <li><strong>Display:</strong> Results shown with visual indicators and LLM insights</li>
              </ol>
            </div>
          </Card.Body>
        </Card>

        {/* Training Data */}
        <Card className="doc-card">
          <Card.Body>
            <h2 className="doc-section-title">📊 Training Data & Model Performance</h2>
            <h4 className="doc-subsection-title">Dataset Information</h4>
            <p className="doc-text">
              The model was trained on a curated dataset of news articles labeled as "Real" or "Fake". 
              The dataset includes diverse news sources and topics to ensure broad coverage.
            </p>
            
            <h4 className="doc-subsection-title mt-3">Model Metrics</h4>
            <Table striped bordered hover className="metrics-table">
              <thead>
                <tr>
                  <th>Metric</th>
                  <th>Value</th>
                  <th>Description</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>Algorithm</strong></td>
                  <td>Multinomial Naive Bayes</td>
                  <td>Probabilistic classifier for text classification</td>
                </tr>
                <tr>
                  <td><strong>Vectorization</strong></td>
                  <td>CountVectorizer</td>
                  <td>Converts text to token count matrix</td>
                </tr>
                <tr>
                  <td><strong>Model Version</strong></td>
                  <td>scikit-learn 1.2.2</td>
                  <td>Training framework version</td>
                </tr>
                <tr>
                  <td><strong>Prediction Classes</strong></td>
                  <td>Binary (0: Fake, 1: Real)</td>
                  <td>Classification output format</td>
                </tr>
              </tbody>
            </Table>

            <div className="info-box">
              <p className="doc-text">
                <strong>⚠️ Note:</strong> The current deployment shows version warnings 
                (model trained on scikit-learn 1.2.2 but running on 1.7.1). This may affect 
                prediction accuracy slightly. Retraining the model with the current version 
                is recommended for production use.
              </p>
            </div>
          </Card.Body>
        </Card>

        {/* Ollama Integration */}
        <Card className="doc-card">
          <Card.Body>
            <h2 className="doc-section-title">🤖 Ollama LLM Integration</h2>
            <h4 className="doc-subsection-title">What is Ollama?</h4>
            <p className="doc-text">
              Ollama is a lightweight framework for running Large Language Models (LLMs) locally. 
              It allows the News Guardian system to provide detailed, context-aware analysis of 
              news articles without relying on external API services.
            </p>

            <h4 className="doc-subsection-title mt-3">Implementation Details</h4>
            <ul className="doc-text">
              <li><strong>Model:</strong> Llama 3 (Meta's open-source language model)</li>
              <li><strong>Endpoint:</strong> Local HTTP API at http://127.0.0.1:11434</li>
              <li><strong>Timeout:</strong> 60 seconds for response generation</li>
              <li><strong>Streaming:</strong> Disabled for simplified response handling</li>
            </ul>

            <h4 className="doc-subsection-title mt-3">Analysis Prompt</h4>
            <div className="code-block">
              <pre>
{`Analyze this headline: "{news_text}"

In exactly 2-3 short sentences: 
- What should be verified? 
- How to fact-check it? 

Do not use bullet points or formatting.`}
              </pre>
            </div>

            <h4 className="doc-subsection-title mt-3">Environment Configuration</h4>
            <Table striped bordered className="config-table">
              <thead>
                <tr>
                  <th>Variable</th>
                  <th>Default Value</th>
                  <th>Description</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><code>OLLAMA_BASE_URL</code></td>
                  <td>http://127.0.0.1:11434</td>
                  <td>Ollama service endpoint</td>
                </tr>
                <tr>
                  <td><code>OLLAMA_MODEL</code></td>
                  <td>llama3</td>
                  <td>LLM model to use</td>
                </tr>
                <tr>
                  <td><code>OLLAMA_TIMEOUT</code></td>
                  <td>60</td>
                  <td>Request timeout in seconds</td>
                </tr>
              </tbody>
            </Table>

            <h4 className="doc-subsection-title mt-3">Error Handling</h4>
            <p className="doc-text">
              The system gracefully handles Ollama failures:
            </p>
            <ul className="doc-text">
              <li>Connection errors (service not running)</li>
              <li>Timeout errors (response taking too long)</li>
              <li>Invalid JSON responses</li>
              <li>Empty or malformed responses</li>
            </ul>
            <p className="doc-text">
              When LLM analysis fails, the ML prediction is still displayed, and users are notified 
              that additional insights are unavailable.
            </p>
          </Card.Body>
        </Card>

        {/* Features */}
        <Card className="doc-card">
          <Card.Body>
            <h2 className="doc-section-title">✨ Key Features</h2>
            <Row>
              <Col md={4}>
                <div className="feature-box">
                  <h5>🔍 Check News by Title</h5>
                  <p>Users can input any news headline to get instant ML-based classification and LLM-powered credibility analysis.</p>
                </div>
              </Col>
              <Col md={4}>
                <div className="feature-box">
                  <h5>📰 Live News Monitoring</h5>
                  <p>Real-time news feed from The Guardian API with automatic fake news detection for each article.</p>
                </div>
              </Col>
              <Col md={4}>
                <div className="feature-box">
                  <h5>🎯 News Quiz</h5>
                  <p>Interactive quiz to test users' ability to identify fake news and improve media literacy.</p>
                </div>
              </Col>
            </Row>
            <Row className="mt-3">
              <Col md={4}>
                <div className="feature-box">
                  <h5>🎨 Theme Support</h5>
                  <p>Multiple color themes (Light, Dark, Blue, Purple) with persistent user preferences.</p>
                </div>
              </Col>
              <Col md={4}>
                <div className="feature-box">
                  <h5>🤖 AI-Powered Insights</h5>
                  <p>Detailed analysis using Llama 3 LLM to explain what to verify and how to fact-check.</p>
                </div>
              </Col>
              <Col md={4}>
                <div className="feature-box">
                  <h5>📱 Responsive Design</h5>
                  <p>Mobile-friendly interface that works seamlessly across all device sizes.</p>
                </div>
              </Col>
            </Row>
          </Card.Body>
        </Card>

        {/* Approach & Methodology */}
        <Card className="doc-card">
          <Card.Body>
            <h2 className="doc-section-title">🔬 Approach & Methodology</h2>
            <h4 className="doc-subsection-title">1. Data Preprocessing</h4>
            <ul className="doc-text">
              <li>Text normalization and cleaning</li>
              <li>Tokenization using CountVectorizer</li>
              <li>Feature extraction from news text</li>
            </ul>

            <h4 className="doc-subsection-title mt-3">2. Model Training</h4>
            <ul className="doc-text">
              <li>Algorithm: Multinomial Naive Bayes (suitable for text classification)</li>
              <li>Training on labeled dataset of real and fake news</li>
              <li>Model serialization using pickle for deployment</li>
            </ul>

            <h4 className="doc-subsection-title mt-3">3. Hybrid Prediction System</h4>
            <ul className="doc-text">
              <li><strong>Stage 1:</strong> Classical ML model provides binary classification (Real/Fake)</li>
              <li><strong>Stage 2:</strong> LLM analyzes the content and provides detailed insights</li>
              <li><strong>Output:</strong> Combined result with prediction label + contextual analysis</li>
            </ul>

            <h4 className="doc-subsection-title mt-3">4. Real-time Integration</h4>
            <ul className="doc-text">
              <li>Background thread fetches news from The Guardian API</li>
              <li>Automatic classification of incoming news articles</li>
              <li>Category-based filtering and organization</li>
              <li>Error handling for API rate limits</li>
            </ul>
          </Card.Body>
        </Card>

        {/* Installation & Setup */}
        <Card className="doc-card">
          <Card.Body>
            <h2 className="doc-section-title">⚙️ Installation & Setup</h2>
            <h4 className="doc-subsection-title">Prerequisites</h4>
            <ul className="doc-text">
              <li>Python 3.8+</li>
              <li>Node.js 14+</li>
              <li>Ollama (for LLM features)</li>
            </ul>

            <h4 className="doc-subsection-title mt-3">Backend Setup</h4>
            <div className="code-block">
              <pre>{`cd app/FakeNewsDetectorAPI/
pip install -r requirements.txt
python manage.py migrate
python manage.py quiz_data_loader game_data/game_data.csv
python manage.py runserver`}</pre>
            </div>

            <h4 className="doc-subsection-title mt-3">Frontend Setup</h4>
            <div className="code-block">
              <pre>{`cd app/fake-news-detector-frontend/
npm install
npm start`}</pre>
            </div>

            <h4 className="doc-subsection-title mt-3">Ollama Setup</h4>
            <div className="code-block">
              <pre>{`# Install Ollama from https://ollama.com/download
ollama pull llama3
ollama serve`}</pre>
            </div>
          </Card.Body>
        </Card>

        {/* Future Enhancements */}
        <Card className="doc-card">
          <Card.Body>
            <h2 className="doc-section-title">🚀 Future Enhancements</h2>
            <ul className="doc-text">
              <li>Enhanced ML models with deep learning (BERT, RoBERTa)</li>
              <li>User authentication and profile management</li>
              <li>Bookmark and save news articles</li>
              <li>Social sharing integration</li>
              <li>Multi-language support</li>
              <li>Browser extension for real-time fact-checking</li>
              <li>API for third-party integrations</li>
              <li>Advanced analytics dashboard</li>
              <li>Model retraining pipeline with user feedback</li>
            </ul>
          </Card.Body>
        </Card>

      </Container>
    </>
  );
}

export default Documentation;
