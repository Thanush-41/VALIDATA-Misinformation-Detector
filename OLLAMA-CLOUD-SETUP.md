# 🌥️ Ollama Cloud Integration Guide

## Overview

Since Render and most PaaS platforms don't support running Ollama natively (it requires significant GPU resources), you have several options for LLM integration in production:

---

## 🎯 Option 1: Self-Hosted Ollama on VPS (Recommended)

### Step 1: Set Up Ollama on a VPS

**Choose a VPS Provider:**
- **DigitalOcean** ($6-12/month for CPU droplet)
- **AWS EC2** (t3.medium or better)
- **Google Cloud Compute Engine**
- **Vultr** ($6-12/month)

**System Requirements:**
- 2GB RAM minimum (4GB recommended)
- 10GB disk space
- Ubuntu 22.04 LTS

### Step 2: Install Ollama on VPS

SSH into your VPS and run:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull your model
ollama pull llama3

# Make Ollama accessible from outside (Important!)
# Edit the service file
sudo systemctl edit ollama.service
```

Add this configuration:

```ini
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
```

Save and restart:

```bash
sudo systemctl daemon-reload
sudo systemctl restart ollama

# Verify it's running
curl http://localhost:11434/api/tags
```

### Step 3: Configure Firewall

```bash
# Allow Ollama port
sudo ufw allow 11434/tcp
sudo ufw enable
```

### Step 4: Update Your Django Backend

On **Render Environment Variables**, set:

```
OLLAMA_BASE_URL = http://YOUR_VPS_IP:11434
OLLAMA_MODEL = llama3
OLLAMA_TIMEOUT = 60
```

Replace `YOUR_VPS_IP` with your VPS IP address (e.g., `http://123.45.67.89:11434`)

### Step 5: Test Connection

```bash
# Test from your local machine
curl http://YOUR_VPS_IP:11434/api/tags
```

---

## 🚀 Option 2: Use Cloud LLM Services (OpenAI, Anthropic, etc.)

This is the **easiest and most reliable option** for production.

### 2A. OpenAI (GPT-3.5/GPT-4)

**Pros:** Reliable, fast, well-documented  
**Cons:** Costs ~$0.002 per request  
**Pricing:** https://openai.com/pricing

#### Installation

```bash
pip install openai
```

#### Update Django Code

I'll create a new LLM service that supports multiple providers.

### 2B. Anthropic Claude

**Pros:** High quality, good for analysis  
**Cons:** Requires API key  
**Pricing:** Similar to OpenAI

### 2C. Google Gemini

**Pros:** Free tier available  
**Cons:** Rate limits  

### 2D. Hugging Face Inference API

**Pros:** Free tier, many models  
**Cons:** Slower response times

---

## 💻 Implementation: Multi-Provider LLM Support

Let me update your Django backend to support multiple LLM providers with a fallback system.

---

## 🔧 Deployment Configuration

### For Render (Environment Variables)

Choose ONE of these configurations:

#### Self-Hosted Ollama:
```
LLM_PROVIDER = ollama
OLLAMA_BASE_URL = http://YOUR_VPS_IP:11434
OLLAMA_MODEL = llama3
OLLAMA_TIMEOUT = 60
```

#### OpenAI:
```
LLM_PROVIDER = openai
OPENAI_API_KEY = sk-proj-xxxxxxxxxxxxx
OPENAI_MODEL = gpt-3.5-turbo
```

#### Anthropic Claude:
```
LLM_PROVIDER = anthropic
ANTHROPIC_API_KEY = sk-ant-xxxxxxxxxxxxx
ANTHROPIC_MODEL = claude-3-haiku-20240307
```

#### Hugging Face:
```
LLM_PROVIDER = huggingface
HUGGINGFACE_API_KEY = hf_xxxxxxxxxxxxx
HUGGINGFACE_MODEL = mistralai/Mistral-7B-Instruct-v0.2
```

#### Disable LLM (fallback):
```
LLM_PROVIDER = none
```

---

## 📊 Cost Comparison

| Provider | Cost per 1000 requests | Setup Difficulty | Reliability |
|----------|----------------------|------------------|-------------|
| Self-hosted Ollama | $6-12/month (VPS) | Medium | Medium |
| OpenAI GPT-3.5 | ~$2 | Easy | High |
| OpenAI GPT-4 | ~$20 | Easy | High |
| Anthropic Claude | ~$2-5 | Easy | High |
| Hugging Face | Free (rate limited) | Easy | Medium |
| Google Gemini | Free tier available | Easy | Medium |

---

## 🔒 Security Best Practices

### 1. Never Commit API Keys
Add to `.gitignore`:
```
.env
.env.local
.env.production
```

### 2. Use Environment Variables
Store all sensitive data in Render's Environment Variables section.

### 3. Secure Ollama VPS
```bash
# Only allow connections from Render IPs
# Or use a VPN/private network
sudo ufw allow from RENDER_IP to any port 11434
```

### 4. Use HTTPS for Ollama
Set up nginx reverse proxy with SSL:
```bash
sudo apt install nginx certbot python3-certbot-nginx
```

---

## 🧪 Testing Your Setup

### Test Ollama VPS
```bash
curl -X POST http://YOUR_VPS_IP:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3",
    "prompt": "Is this news article real or fake: Tesla announces flying cars",
    "stream": false
  }'
```

### Test from Django
```python
# In Django shell
python manage.py shell

from core.llm import query_llm
result = query_llm("Test news title", "Test news body")
print(result)
```

---

## 🆘 Troubleshooting

### Issue: Connection Refused to Ollama VPS

**Solutions:**
1. Check firewall: `sudo ufw status`
2. Verify Ollama is running: `sudo systemctl status ollama`
3. Check if bound to 0.0.0.0: `sudo netstat -tlnp | grep 11434`

### Issue: Slow Response Times

**Solutions:**
1. Use smaller models (llama3.2 instead of llama3)
2. Increase timeout in Django settings
3. Consider switching to cloud LLM

### Issue: API Key Not Working

**Solutions:**
1. Verify key in environment variables
2. Check API key permissions
3. Verify billing is active (for paid services)

---

## 📈 Scaling Considerations

### Small Scale (< 1000 users)
- Self-hosted Ollama on small VPS
- Or use free tier of Hugging Face/Gemini

### Medium Scale (1000-10000 users)
- OpenAI GPT-3.5 or Anthropic Claude
- Load-balanced Ollama instances

### Large Scale (10000+ users)
- Dedicated LLM infrastructure
- Caching layer for common queries
- Queue system for async processing

---

## 🎯 Recommended Setup

**For Development/Testing:**
- Local Ollama (free)

**For Production (Low Budget):**
- Self-hosted Ollama on DigitalOcean ($6/month)
- Or Hugging Face free tier

**For Production (Best Performance):**
- OpenAI GPT-3.5-turbo (~$2 per 1000 requests)
- Reliable, fast, no maintenance

**For Production (Privacy-Focused):**
- Self-hosted Ollama on dedicated server
- Full data control

---

## 🔄 Migration Path

1. **Start:** Local Ollama (development)
2. **Deploy:** Hugging Face free tier (MVP)
3. **Scale:** OpenAI GPT-3.5 (production)
4. **Optimize:** Self-hosted Ollama cluster (if cost-effective)

---

## 📚 Resources

- [Ollama Documentation](https://github.com/ollama/ollama/blob/main/docs/README.md)
- [OpenAI API Docs](https://platform.openai.com/docs/api-reference)
- [Anthropic Claude Docs](https://docs.anthropic.com/)
- [Hugging Face Inference](https://huggingface.co/docs/api-inference/index)
- [DigitalOcean VPS Setup](https://www.digitalocean.com/community/tutorials)

---

**Need help choosing? Let me know your budget and expected traffic!**
