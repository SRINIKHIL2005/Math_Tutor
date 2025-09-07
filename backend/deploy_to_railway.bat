@echo off
echo 🚀 DEPLOYING MATH TUTOR BACKEND TO RAILWAY...
echo.

REM Navigate to backend directory
cd /d "f:\Internships\Maths_Pofessor\Real_Math_tutor\backend"

echo ✅ Current directory: %cd%
echo.

echo 📋 Files prepared for deployment:
echo - railway.json (Railway configuration)
echo - Procfile (Process definition)
echo - runtime.txt (Python 3.11)
echo - requirements.txt (Dependencies)
echo - /health endpoint added
echo.

echo 🔧 NEXT STEPS:
echo.
echo 1. Install Railway CLI:
echo    npm install -g @railway/cli
echo    OR download from: https://railway.app/cli
echo.
echo 2. Login to Railway:
echo    railway login
echo.
echo 3. Initialize project:
echo    railway init
echo.
echo 4. Set environment variables in Railway Dashboard:
echo    - GEMINI_API_KEY=AIzaSyD9e8K8lri0b4MlQzn0KtEn6z-nrwBYsdA
echo    - TAVILY_API_KEY=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
echo    - MONGODB_URI=mongodb+srv://mathtutor:password123@mathtutor.mongodb.net/mathtutor?retryWrites=true^&w=majority
echo    - PORT=8000
echo.
echo 5. Deploy:
echo    railway up
echo.
echo 🌐 After deployment, update your frontend App.js with the new Railway URL!
echo.
pause
