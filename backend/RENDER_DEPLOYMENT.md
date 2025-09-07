# 🚀 RENDER DEPLOYMENT GUIDE - Math Tutor Backend

## ✅ Files Created for Deployment:
- `build.sh` - Installation script for Render
- `start.sh` - Startup command for FastAPI
- `render.yaml` - Render configuration
- `runtime.txt` - Python version specification
- Updated `requirements.txt` with uvicorn
- Updated CORS in `complete_fastapi.py`

## 🎯 STEP-BY-STEP RENDER DEPLOYMENT:

### **Step 1: Create Render Account**
1. Go to https://render.com
2. Sign up with your GitHub account
3. Connect your GitHub account

### **Step 2: Deploy from GitHub**
1. Click **"New +"** → **"Web Service"**
2. Connect your **Math_Tutor** repository
3. Configure the service:
   ```
   Name: math-tutor-backend
   Runtime: Python 3
   Build Command: ./build.sh
   Start Command: ./start.sh
   Root Directory: backend
   ```

### **Step 3: Set Environment Variables**
In Render Dashboard → Environment → Add these:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here  
MONGODB_URI=your_mongodb_atlas_connection_string
PYTHON_VERSION=3.11.7
ENVIRONMENT=production
```

### **Step 4: Deploy!**
- Click **"Create Web Service"**
- Render will automatically build and deploy
- You'll get a URL like: `https://math-tutor-backend.onrender.com`

## 🔧 After Deployment - Update Frontend:

### **Step 5: Update Frontend API URL**
Your frontend will automatically detect the new backend URL!
The current logic in App.js already handles production URLs.

### **Step 6: Test Deployment**
Visit your backend URL:
```
https://your-app-name.onrender.com/health
https://your-app-name.onrender.com/status
```

## 🌟 Environment Variables You Need:

### **Required Variables:**
1. **GEMINI_API_KEY** - Get from Google AI Studio
2. **TAVILY_API_KEY** - Get from Tavily.com (for web search)
3. **MONGODB_URI** - Your MongoDB Atlas connection string

### **Optional Variables:**
- EXA_API_KEY - For alternative web search
- OPENAI_API_KEY - For OpenAI integration
- ANTHROPIC_API_KEY - For Claude integration

## 🔥 Production Features Enabled:
- ✅ Health checks for monitoring
- ✅ CORS configured for GitHub Pages
- ✅ Professional logging
- ✅ Error handling
- ✅ Auto-scaling ready
- ✅ Zero-downtime deployments

## 🎉 Your App Will Be Live At:
- **Backend**: `https://your-app-name.onrender.com`
- **Frontend**: `https://srinikhil2005.github.io/Math_Tutor/` (already working!)

## ⚡ Pro Tips:
- Free tier sleeps after 15 minutes of inactivity
- First request after sleep takes ~30 seconds
- Upgrade to paid tier ($7/month) for always-on service
- Render automatically handles HTTPS and SSL certificates
- Auto-deploys on every GitHub push to main branch

## 🚨 Troubleshooting:
- If build fails, check build logs in Render dashboard
- If app crashes, check runtime logs
- Health check endpoint: `/health`
- Status endpoint: `/status` (shows component status)

---
**Ready to deploy? Just follow the steps above! 🚀**
