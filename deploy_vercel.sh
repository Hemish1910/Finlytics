#!/bin/bash

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     Finlytics Trading System - Vercel Deployment          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "⚠️  Vercel CLI not found. Installing..."
    npm install -g vercel
    echo "✅ Vercel CLI installed successfully!"
    echo ""
fi

echo "📋 Deployment Configuration:"
echo "   - Runtime: Python 3.11"
echo "   - Framework: FastAPI"
echo "   - Endpoints: 9 API routes"
echo "   - Agents: 6 trading agents"
echo ""

echo "🔍 Verifying configuration files..."

# Check vercel.json
if [ -f "vercel.json" ]; then
    echo "   ✅ vercel.json found"
else
    echo "   ❌ vercel.json missing!"
    exit 1
fi

# Check api/index.py
if [ -f "api/index.py" ]; then
    echo "   ✅ api/index.py found"
else
    echo "   ❌ api/index.py missing!"
    exit 1
fi

# Check requirements.txt
if [ -f "requirements.txt" ]; then
    echo "   ✅ requirements.txt found"
else
    echo "   ❌ requirements.txt missing!"
    exit 1
fi

echo ""
echo "🚀 Starting deployment to Vercel..."
echo ""

# Deploy to Vercel
vercel --prod

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║              🎉 DEPLOYMENT COMPLETE! 🎉                    ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "📊 Your Finlytics Trading System is now live!"
echo ""
echo "🌐 Test your endpoints:"
echo "   • Dashboard:  https://your-app.vercel.app/"
echo "   • Health:     https://your-app.vercel.app/health"
echo "   • API Status: https://your-app.vercel.app/api/status"
echo "   • Portfolio:  https://your-app.vercel.app/api/portfolio"
echo ""
echo "📚 For more information, see VERCEL_DEPLOYMENT_GUIDE.md"
echo ""
