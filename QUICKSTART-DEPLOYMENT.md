# 🚀 Quick Deployment Guide

## ✅ Your Repository is Ready for Deployment!

All deployment configuration files have been created and pushed to GitHub.

---

## 📋 Quick Start (5 Minutes)

### 1️⃣ Deploy Backend (Django on Render)

**Go to:** https://render.com

1. **Sign up** with your GitHub account
2. Click **"New +"** → **"Web Service"**
3. Select repository: `VALIDATA-Misinformation-Detector`
4. **Configure:**
   - Name: `validata-backend`
   - Root Directory: `app/FakeNewsDetectorAPI`
   - Build Command: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --no-input`
   - Start Command: `gunicorn FakeNewsDetectorAPI.wsgi:application`
   
5. **Add Environment Variables:**
   ```
   SECRET_KEY = <generate at https://djecrety.ir/>
   DEBUG = False
   ALLOWED_HOSTS = .onrender.com
   OLLAMA_BASE_URL = http://127.0.0.1:11434
   OLLAMA_MODEL = llama3
   OLLAMA_TIMEOUT = 60
   ```

6. Click **"Create Web Service"**
7. Wait 5-10 minutes for deployment
8. **Copy your backend URL:** `https://validata-backend.onrender.com`

---

### 2️⃣ Deploy Frontend (React on Vercel)

**Go to:** https://vercel.com

1. **Sign up** with your GitHub account
2. Click **"Add New..."** → **"Project"**
3. Import: `VALIDATA-Misinformation-Detector`
4. **Configure:**
   - Framework: `Create React App`
   - Root Directory: `app/fake-news-detector-frontend`
   - Build Command: `npm run build`
   - Output Directory: `build`

5. **Add Environment Variable:**
   ```
   REACT_APP_API_URL = https://validata-backend.onrender.com
   ```
   (Use the URL you copied from step 1)

6. Click **"Deploy"**
7. Wait 3-5 minutes
8. **Your app is live!** `https://your-app-name.vercel.app`

---

## 🎉 That's It!

Your VALIDATA Fake News Detector is now deployed and accessible worldwide!

### 🔗 Important Links

- **Frontend:** https://your-app-name.vercel.app
- **Backend API:** https://validata-backend.onrender.com
- **GitHub Repo:** https://github.com/Thanush-41/VALIDATA-Misinformation-Detector

---

## 📝 Post-Deployment Tasks

### Update CORS Settings (Important!)

After getting your Vercel URL, update Django CORS settings:

1. Go to Render Dashboard → your service → Environment
2. Add/Update:
   ```
   ALLOWED_HOSTS = .onrender.com,.vercel.app
   ```

### Test Your Deployment

Visit your Vercel URL and test:
- ✅ Home page loads
- ✅ Live news displays
- ✅ News Quiz works
- ✅ Check News By Title works
- ✅ Documentation page shows
- ✅ Theme switching works
- ✅ All themes (dark, light, blue, purple)

---

## 🆘 Troubleshooting

### Backend Issues
- **Check Render Logs:** Dashboard → Logs
- **Common issue:** SECRET_KEY not set
- **Fix:** Add SECRET_KEY in environment variables

### Frontend Issues
- **Check Vercel Logs:** Deployments → View Function Logs
- **Common issue:** API calls failing (CORS)
- **Fix:** Update CORS settings in Django

### API Not Working
- Verify `REACT_APP_API_URL` is correct
- Check CORS settings on backend
- Check browser console for errors

---

## 💰 Free Tier Limits

- **Render:** 750 hours/month (free)
- **Vercel:** Unlimited deployments (free)
- **Cost:** $0/month for testing!

---

## 📚 Need More Help?

- Read full guide: `DEPLOYMENT.md`
- Run deployment check: `.\deploy-check.ps1`
- Check GitHub issues
- Review logs in Render/Vercel dashboards

---

**Happy Deploying! 🎊**
