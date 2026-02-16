@echo off
echo ========================================
echo   DEEPFAKE DETECTOR - VERCEL DEPLOY
echo ========================================
echo.
echo This script will deploy your app to Vercel
echo.

REM Check if vercel is installed
where vercel >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Vercel CLI not found!
    echo.
    echo Install it with: npm install -g vercel
    echo.
    pause
    exit /b 1
)

echo ✅ Vercel CLI found
echo.
echo Deploying to production...
echo.

REM Deploy to Vercel
vercel --prod

echo.
echo 🎉 Deployment complete!
echo.
pause
