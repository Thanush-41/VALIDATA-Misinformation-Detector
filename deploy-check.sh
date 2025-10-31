#!/bin/bash

# VALIDATA Deployment Helper Script
# This script helps prepare your application for deployment

echo "🚀 VALIDATA Deployment Helper"
echo "=============================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "README.md" ]; then
    echo -e "${RED}❌ Error: Please run this script from the project root directory${NC}"
    exit 1
fi

echo -e "${YELLOW}📋 Pre-deployment Checklist${NC}"
echo ""

# 1. Check Git status
echo "1️⃣  Checking Git status..."
if git diff-index --quiet HEAD --; then
    echo -e "${GREEN}✅ No uncommitted changes${NC}"
else
    echo -e "${YELLOW}⚠️  You have uncommitted changes. Commit them before deploying.${NC}"
    git status --short
fi
echo ""

# 2. Check if on main branch
BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "2️⃣  Current branch: $BRANCH"
if [ "$BRANCH" != "main" ]; then
    echo -e "${YELLOW}⚠️  You're not on the main branch. Consider switching to main.${NC}"
fi
echo ""

# 3. Check Python dependencies
echo "3️⃣  Checking Python dependencies..."
if [ -f "app/FakeNewsDetectorAPI/requirements.txt" ]; then
    echo -e "${GREEN}✅ requirements.txt found${NC}"
    echo "   Dependencies:"
    cat app/FakeNewsDetectorAPI/requirements.txt | grep -v "^#" | grep -v "^$"
else
    echo -e "${RED}❌ requirements.txt not found${NC}"
fi
echo ""

# 4. Check Node dependencies
echo "4️⃣  Checking Node dependencies..."
if [ -f "app/fake-news-detector-frontend/package.json" ]; then
    echo -e "${GREEN}✅ package.json found${NC}"
else
    echo -e "${RED}❌ package.json not found${NC}"
fi
echo ""

# 5. Check deployment files
echo "5️⃣  Checking deployment configuration files..."
files=(
    "app/FakeNewsDetectorAPI/Procfile"
    "app/FakeNewsDetectorAPI/runtime.txt"
    "app/FakeNewsDetectorAPI/render.yaml"
    "app/fake-news-detector-frontend/vercel.json"
    "DEPLOYMENT.md"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✅ $file${NC}"
    else
        echo -e "${RED}❌ $file (missing)${NC}"
    fi
done
echo ""

# 6. Check environment variables
echo "6️⃣  Checking environment setup..."
if [ -f "app/fake-news-detector-frontend/.env.example" ]; then
    echo -e "${GREEN}✅ .env.example found${NC}"
    echo "   Remember to set these variables in Vercel:"
    cat app/fake-news-detector-frontend/.env.example
else
    echo -e "${YELLOW}⚠️  .env.example not found${NC}"
fi
echo ""

# 7. Check models directory
echo "7️⃣  Checking ML models..."
if [ -d "app/FakeNewsDetectorAPI/models" ]; then
    echo -e "${GREEN}✅ models directory found${NC}"
    ls -lh app/FakeNewsDetectorAPI/models/
else
    echo -e "${RED}❌ models directory not found${NC}"
fi
echo ""

# Summary
echo ""
echo "=============================="
echo -e "${GREEN}📝 Next Steps:${NC}"
echo ""
echo "1. 🔐 Generate a Django SECRET_KEY:"
echo "   Visit: https://djecrety.ir/"
echo ""
echo "2. 🌐 Deploy Backend to Render:"
echo "   a. Go to https://render.com"
echo "   b. Create new Web Service"
echo "   c. Connect GitHub repo: Thanush-41/VALIDATA-Misinformation-Detector"
echo "   d. Set root directory: app/FakeNewsDetectorAPI"
echo "   e. Add environment variables (see DEPLOYMENT.md)"
echo ""
echo "3. 🎨 Deploy Frontend to Vercel:"
echo "   a. Go to https://vercel.com"
echo "   b. Import GitHub repo"
echo "   c. Set root directory: app/fake-news-detector-frontend"
echo "   d. Add REACT_APP_API_URL environment variable"
echo ""
echo "4. 📖 Read full deployment guide:"
echo "   cat DEPLOYMENT.md"
echo ""
echo -e "${GREEN}🎉 Good luck with your deployment!${NC}"
echo ""
