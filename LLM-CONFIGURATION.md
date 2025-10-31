# 🔧 LLM Provider Configuration Guide

## Quick Start

Your Django backend now supports **multiple LLM providers** with automatic fallback!

---

## 📋 Supported Providers

| Provider | Status | Cost | Speed | Quality |
|----------|--------|------|-------|---------|
| **Ollama** (Local/VPS) | ✅ Default | Free (VPS: $6/mo) | Medium | Good |
| **OpenAI** (GPT-3.5/4) | ✅ Ready | ~$0.002/request | Fast | Excellent |
| **Anthropic** (Claude) | ✅ Ready | ~$0.002/request | Fast | Excellent |
| **Hugging Face** | ✅ Ready | Free tier | Slow | Good |
| **None** (Disable LLM) | ✅ Ready | Free | N/A | N/A |

---

## 🚀 Configuration Examples

### Option 1: Self-Hosted Ollama (Default)

**Best for:** Development, privacy-focused deployments

**Render Environment Variables:**
```bash
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://YOUR_VPS_IP:11434
OLLAMA_MODEL=llama3
OLLAMA_TIMEOUT=60
```

**Setup Steps:**
1. Follow `OLLAMA-CLOUD-SETUP.md` to set up Ollama on a VPS
2. Get your VPS IP address
3. Replace `YOUR_VPS_IP` in `OLLAMA_BASE_URL`
4. Deploy to Render

---

### Option 2: OpenAI (Recommended for Production)

**Best for:** Production apps, best quality/reliability

**1. Get API Key:**
- Go to https://platform.openai.com/api-keys
- Create new API key
- Copy the key (starts with `sk-`)

**2. Install Package:**
Add to `requirements.txt`:
```
openai>=1.3.0
```

Or install locally:
```bash
cd app/FakeNewsDetectorAPI
pip install openai
```

**3. Render Environment Variables:**
```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-proj-your-actual-key-here
OPENAI_MODEL=gpt-3.5-turbo
```

**Models:**
- `gpt-3.5-turbo` - Fast, cheap (~$0.002/request)
- `gpt-4` - Best quality, expensive (~$0.02/request)
- `gpt-4-turbo` - Balanced (~$0.01/request)

---

### Option 3: Anthropic Claude

**Best for:** High-quality analysis, privacy-conscious

**1. Get API Key:**
- Go to https://console.anthropic.com/
- Create API key
- Copy the key (starts with `sk-ant-`)

**2. Install Package:**
```bash
pip install anthropic
```

**3. Render Environment Variables:**
```bash
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
ANTHROPIC_MODEL=claude-3-haiku-20240307
```

**Models:**
- `claude-3-haiku-20240307` - Fast, cheap
- `claude-3-sonnet-20240229` - Balanced
- `claude-3-opus-20240229` - Best quality

---

### Option 4: Hugging Face (Free Tier)

**Best for:** MVP, testing, low budget

**1. Get API Key:**
- Go to https://huggingface.co/settings/tokens
- Create new token
- Copy the token (starts with `hf_`)

**2. Render Environment Variables:**
```bash
LLM_PROVIDER=huggingface
HUGGINGFACE_API_KEY=hf_your-actual-token-here
HUGGINGFACE_MODEL=mistralai/Mistral-7B-Instruct-v0.2
```

**Recommended Models:**
- `mistralai/Mistral-7B-Instruct-v0.2` - Good balance
- `google/flan-t5-large` - Faster, smaller
- `meta-llama/Llama-2-7b-chat-hf` - Good quality

**Note:** Free tier has rate limits (30 requests/hour)

---

### Option 5: Disable LLM

**Best for:** Testing ML predictions without LLM overhead

**Render Environment Variables:**
```bash
LLM_PROVIDER=none
```

The app will still work, but won't show LLM analysis.

---

## 📝 Step-by-Step Setup on Render

### For OpenAI (Example):

1. **Go to Render Dashboard** → Your Service → Environment

2. **Add Environment Variables:**
   Click "Add Environment Variable" for each:
   
   | Key | Value |
   |-----|-------|
   | `LLM_PROVIDER` | `openai` |
   | `OPENAI_API_KEY` | Your actual API key |
   | `OPENAI_MODEL` | `gpt-3.5-turbo` |

3. **Update requirements.txt** on GitHub:
   ```bash
   # Locally:
   cd app/FakeNewsDetectorAPI
   echo "openai>=1.3.0" >> requirements.txt
   git add requirements.txt
   git commit -m "Add OpenAI support"
   git push origin main
   ```

4. **Render will auto-deploy** with the new configuration

5. **Test the API:**
   ```bash
   curl -X POST https://your-app.onrender.com/api/usercheckbytitle/ \
     -H "Content-Type: application/json" \
     -d '{"user_news": "Breaking: Mars colony announced"}'
   ```

---

## 🧪 Testing Locally

### Test with Different Providers:

```python
# In Django shell
python manage.py shell

from core.llm import query_llm

# Test with Ollama
success, msg = query_llm("Analyze this news", provider='ollama')
print(f"Ollama: {success} - {msg}")

# Test with OpenAI (if configured)
success, msg = query_llm("Analyze this news", provider='openai')
print(f"OpenAI: {success} - {msg}")

# Test with configured provider
from django.conf import settings
print(f"Current provider: {settings.LLM_PROVIDER}")
```

### Set Environment Variables Locally:

**Windows PowerShell:**
```powershell
$env:LLM_PROVIDER="openai"
$env:OPENAI_API_KEY="sk-your-key"
python manage.py runserver
```

**Linux/Mac:**
```bash
export LLM_PROVIDER=openai
export OPENAI_API_KEY=sk-your-key
python manage.py runserver
```

---

## 💰 Cost Estimation

### For 1000 requests/month:

| Provider | Monthly Cost | Notes |
|----------|-------------|-------|
| Ollama (VPS) | $6 | DigitalOcean basic droplet |
| OpenAI GPT-3.5 | ~$2 | Pay per request |
| OpenAI GPT-4 | ~$20 | Higher quality |
| Anthropic Claude | ~$2-5 | Similar to OpenAI |
| Hugging Face | $0 | Free tier (limited) |

### For 10,000 requests/month:

| Provider | Monthly Cost |
|----------|-------------|
| Ollama (VPS) | $6 |
| OpenAI GPT-3.5 | ~$20 |
| OpenAI GPT-4 | ~$200 |
| Anthropic Claude | ~$20-50 |
| Hugging Face | Need paid plan |

---

## 🔐 Security Best Practices

### 1. Never Commit API Keys

Add to `.gitignore`:
```
.env
.env.local
.env.production
*.key
```

### 2. Use Render's Secret Management

- Store API keys in Render's Environment Variables
- Enable "Secret" checkbox for sensitive values
- Keys are encrypted at rest

### 3. Rotate Keys Regularly

- Change API keys every 90 days
- Use different keys for dev/prod
- Monitor usage for anomalies

### 4. Set Usage Limits

**OpenAI:**
- Set monthly budget limits
- Enable email alerts
- Monitor usage dashboard

**Anthropic:**
- Set organization limits
- Review usage regularly

---

## 🐛 Troubleshooting

### Issue: "Import openai could not be resolved"

**Solution:**
```bash
pip install openai
```

### Issue: "OPENAI_API_KEY not configured"

**Solution:**
1. Check Render Environment Variables
2. Verify key is spelled correctly
3. Ensure no extra spaces in key

### Issue: "Rate limit exceeded"

**Solution:**
- For Hugging Face: Wait or upgrade to paid plan
- For OpenAI: Check billing and increase limits
- Consider switching to Ollama

### Issue: "Connection timeout to Ollama VPS"

**Solution:**
1. Check VPS is running: `systemctl status ollama`
2. Verify firewall: `sudo ufw status`
3. Test from Render: `curl http://YOUR_IP:11434/api/tags`
4. Check OLLAMA_HOST is set to `0.0.0.0:11434`

---

## 🔄 Switching Providers

You can switch providers anytime without code changes!

**Steps:**
1. Go to Render → Environment Variables
2. Change `LLM_PROVIDER` to desired provider
3. Add/update provider-specific keys
4. Save changes
5. Render will auto-redeploy

**Example: Switch from Ollama to OpenAI:**
```
LLM_PROVIDER=openai         (was: ollama)
OPENAI_API_KEY=sk-proj-xxx  (new)
OPENAI_MODEL=gpt-3.5-turbo  (new)
```

---

## 📊 Performance Comparison

| Provider | Avg Response Time | Reliability | Quality Score |
|----------|------------------|-------------|---------------|
| Ollama (Local) | 2-5s | Medium | 7/10 |
| Ollama (VPS) | 3-8s | Medium | 7/10 |
| OpenAI GPT-3.5 | 1-3s | High | 9/10 |
| OpenAI GPT-4 | 3-8s | High | 10/10 |
| Anthropic Claude | 2-4s | High | 9/10 |
| Hugging Face | 5-15s | Low (rate limits) | 6/10 |

---

## 🎯 Recommendations

### For Development:
```bash
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://127.0.0.1:11434
```
Run Ollama locally, free and fast.

### For MVP/Testing:
```bash
LLM_PROVIDER=huggingface
HUGGINGFACE_API_KEY=hf_your_token
```
Free tier, good enough for testing.

### For Production (Small Scale):
```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk_your_key
OPENAI_MODEL=gpt-3.5-turbo
```
Reliable, affordable, excellent quality.

### For Production (Large Scale):
```bash
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://your-dedicated-server:11434
```
Self-hosted for cost efficiency at scale.

### For Privacy-Critical:
```bash
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://your-vps:11434
```
Complete data control.

---

## 📚 Additional Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Anthropic Claude Documentation](https://docs.anthropic.com/)
- [Hugging Face Inference API](https://huggingface.co/docs/api-inference/index)
- [Ollama Documentation](https://github.com/ollama/ollama/blob/main/docs/README.md)

---

**Need help choosing? Consider:**
- Budget → Hugging Face (free) or Ollama (VPS)
- Quality → OpenAI GPT-4 or Anthropic Claude
- Privacy → Ollama self-hosted
- Speed → OpenAI GPT-3.5
- Scale → Ollama cluster or OpenAI

**Still unsure? Start with OpenAI GPT-3.5-turbo - it's the best balance!**
