#!/bin/bash

echo "========================================"
echo "  DEEPFAKE DETECTOR - VERCEL DEPLOY"
echo "========================================"
echo ""
echo "This script will deploy your app to Vercel"
echo ""

# Check if vercel is installed
if ! command -v vercel &> /dev/null
then
    echo "❌ Vercel CLI not found!"
    echo ""
    echo "Install it with: npm install -g vercel"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

echo "✅ Vercel CLI found"
echo ""
echo "Deploying to production..."
echo ""

# Deploy to Vercel
vercel --prod

echo ""
echo "🎉 Deployment complete!"
echo ""
read -p "Press Enter to exit..."
