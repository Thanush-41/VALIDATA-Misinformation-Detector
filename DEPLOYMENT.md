# 🚀 VALIDATA Deployment Guide

This guide will help you deploy the VALIDATA Fake News Detector application to production.

## 📋 Prerequisites

Before deploying, ensure you have:
- Git repository with your code (already on GitHub)
- Accounts on:
  - [Render](https://render.com) (for Django backend)
  - [Vercel](https://vercel.com) (for React frontend)
  - [Ollama Cloud](https://ollama.com) or a self-hosted Ollama instance (optional)

## 🎯 Deployment Architecture

```
┌─────────────────┐
│  Vercel (React) │ ──────► Frontend (Static Files)
└────────┬────────┘
         │ API Calls
         ▼
┌─────────────────┐
│ Render (Django) │ ──────► Backend API + ML Model
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Ollama Service  │ ──────► LLM Analysis (Optional)
└─────────────────┘
```

---

## 📦 Part 1: Deploy Django Backend to Render

### Step 1: Prepare Your Repository
Your code is already on GitHub at: `https://github.com/Thanush-41/VALIDATA-Misinformation-Detector`

### Step 2: Create Render Account
1. Go to [https://render.com](https://render.com)
2. Sign up with your GitHub account
3. Authorize Render to access your repositories

### Step 3: Create Web Service on Render
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `VALIDATA-Misinformation-Detector`
3. Configure the service:

   **Basic Settings:**
   - **Name:** `validata-backend`
   - **Region:** Choose closest to your users
   - **Branch:** `main`
   - **Root Directory:** `app/FakeNewsDetectorAPI`
   - **Runtime:** `Python 3`
   - **Build Command:**
     ```bash
     pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --no-input
     ```
   - **Start Command:**
     ```bash
     gunicorn FakeNewsDetectorAPI.wsgi:application
     ```

   **Environment Variables:**
   Add the following environment variables:
   
   | Key | Value | Notes |
   |-----|-------|-------|
   | `PYTHON_VERSION` | `3.11.0` | Python version |
   | `SECRET_KEY` | Generate a random key | Use [Django Secret Key Generator](https://djecrety.ir/) |
   | `DEBUG` | `False` | Disable debug in production |
   | `ALLOWED_HOSTS` | `.onrender.com` | Allow Render domain |
   | `OLLAMA_BASE_URL` | `http://127.0.0.1:11434` | Keep default for now (or use cloud Ollama) |
   | `OLLAMA_MODEL` | `llama3` | LLM model name |
   | `OLLAMA_TIMEOUT` | `60` | Timeout in seconds |

4. Click **"Create Web Service"**
5. Wait for the deployment to complete (5-10 minutes)
6. Copy your backend URL: `https://validata-backend.onrender.com`

### Step 4: Test Backend API
Once deployed, test these endpoints:
- `https://validata-backend.onrender.com/admin/` - Django admin
- `https://validata-backend.onrender.com/api/livenews/` - Live news API
- `https://validata-backend.onrender.com/api/newsquiz/` - News quiz API

---

## 🎨 Part 2: Deploy React Frontend to Vercel

### Step 1: Update API URLs in Frontend
Before deploying, you need to update the API URLs in your React app.

1. Open your terminal and navigate to frontend directory:
   ```bash
   cd app/fake-news-detector-frontend
   ```

2. Create a `.env.production` file:
   ```bash
   REACT_APP_API_URL=https://validata-backend.onrender.com
   ```

3. Update your API calls to use environment variables (if not already done)

### Step 2: Create Vercel Account
1. Go to [https://vercel.com](https://vercel.com)
2. Sign up with your GitHub account
3. Import your repository

### Step 3: Configure Vercel Project
1. Click **"Add New..."** → **"Project"**
2. Import `VALIDATA-Misinformation-Detector` repository
3. Configure the project:

   **Framework Preset:** `Create React App`
   
   **Root Directory:** `app/fake-news-detector-frontend`
   
   **Build Settings:**
   - Build Command: `npm run build`
   - Output Directory: `build`
   - Install Command: `npm install`

   **Environment Variables:**
   
   | Key | Value |
   |-----|-------|
   | `REACT_APP_API_URL` | `https://validata-backend.onrender.com` |

4. Click **"Deploy"**
5. Wait for deployment (3-5 minutes)
6. Your app will be available at: `https://your-app-name.vercel.app`

### Step 4: Configure Custom Domain (Optional)
1. Go to Project Settings → Domains
2. Add your custom domain
3. Update DNS settings as instructed

---

## ⚠️ Important: Ollama Deployment Considerations

### Option 1: Disable Ollama in Production (Simplest)
If you want to deploy without Ollama:

1. Update Django settings to make Ollama optional
2. Handle `analysis` gracefully when Ollama is unavailable
3. The app will still work with ML predictions

### Option 2: Use Cloud-Based LLM (Recommended)
Instead of Ollama, integrate cloud-based LLM services:

- **OpenAI API** (GPT-3.5/4)
- **Anthropic Claude**
- **Google Gemini**
- **Hugging Face Inference API**

Update `core/llm.py` to use these services instead of Ollama.

### Option 3: Self-Host Ollama (Advanced)
Deploy Ollama on a separate server:

1. Rent a VPS (DigitalOcean, AWS EC2, etc.)
2. Install Ollama on the VPS
3. Update `OLLAMA_BASE_URL` to point to your VPS
4. Ensure firewall allows connections

---

## 🔧 Post-Deployment Configuration

### 1. Update CORS Settings
After deployment, update your Django `settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    'https://your-app-name.vercel.app',
    'http://localhost:3001',  # For local development
]
```

### 2. Update ALLOWED_HOSTS
```python
ALLOWED_HOSTS = [
    'validata-backend.onrender.com',
    '.vercel.app',
    'localhost',
]
```

### 3. Set Up Database (Optional)
For production, consider upgrading from SQLite to PostgreSQL:

1. On Render, add a PostgreSQL database
2. Update `DATABASES` in `settings.py` to use environment variables
3. Run migrations again

---

## 🧪 Testing Your Deployment

### Backend Tests
```bash
# Test live news API
curl https://validata-backend.onrender.com/api/livenews/

# Test news quiz API
curl https://validata-backend.onrender.com/api/newsquiz/

# Test user check by title
curl -X POST https://validata-backend.onrender.com/api/usercheckbytitle/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Breaking News: Test Article"}'
```

### Frontend Tests
1. Visit `https://your-app-name.vercel.app`
2. Test all pages:
   - Home (Live News)
   - News Quiz
   - Check News By Title
   - Documentation
3. Test theme switching
4. Test all API integrations

---

## 📊 Monitoring & Maintenance

### Render Dashboard
- Monitor backend logs
- Check resource usage
- View deployment history

### Vercel Analytics
- Enable Web Analytics
- Monitor page views
- Track performance

### Set Up Alerts
Configure alerts for:
- Backend downtime
- High error rates
- Slow response times

---

## 🔄 Continuous Deployment

Both Render and Vercel support auto-deployment from GitHub:

1. **Push to `main` branch** → Automatic deployment
2. **Create PR** → Preview deployment
3. **Merge PR** → Production deployment

---

## 🐛 Troubleshooting

### Backend Issues

**Issue:** `Application failed to start`
- Check Render logs
- Verify all dependencies in `requirements.txt`
- Check environment variables

**Issue:** `500 Internal Server Error`
- Check Django logs
- Verify database migrations
- Check static files collected

**Issue:** `CORS errors`
- Update `CORS_ALLOWED_ORIGINS` in settings
- Verify frontend URL is correct

### Frontend Issues

**Issue:** `API calls failing`
- Verify `REACT_APP_API_URL` is correct
- Check CORS configuration
- Inspect browser console for errors

**Issue:** `Build failed on Vercel`
- Check build logs
- Verify `package.json` scripts
- Check for syntax errors

---

## 💰 Cost Estimates

### Free Tier (Recommended for Testing)
- **Render:** Free tier includes 750 hours/month
- **Vercel:** Free tier includes unlimited deployments
- **Total:** $0/month

### Paid Tier (For Production)
- **Render:** $7/month (Starter plan)
- **Vercel:** $20/month (Pro plan)
- **Ollama VPS:** $5-20/month (DigitalOcean/AWS)
- **Total:** $32-47/month

---

## 🎉 Success Checklist

- [ ] Django backend deployed on Render
- [ ] React frontend deployed on Vercel
- [ ] Environment variables configured
- [ ] CORS settings updated
- [ ] All API endpoints working
- [ ] Frontend connects to backend
- [ ] Theme switching works
- [ ] ML predictions working
- [ ] Custom domain configured (optional)
- [ ] Monitoring set up

---

## 📚 Additional Resources

- [Render Python Deployment Guide](https://render.com/docs/deploy-django)
- [Vercel React Deployment](https://vercel.com/docs/frameworks/create-react-app)
- [Django Production Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [Ollama Documentation](https://github.com/ollama/ollama/blob/main/docs/README.md)

---

## 🆘 Need Help?

If you encounter issues:
1. Check the logs (Render/Vercel dashboards)
2. Review this guide
3. Check GitHub Issues
4. Open a new issue on GitHub

---

**🎊 Congratulations! Your VALIDATA app is now live!**

Share your deployment:
- Frontend: `https://your-app-name.vercel.app`
- Backend API: `https://validata-backend.onrender.com`

Happy detecting! 🕵️‍♂️📰
