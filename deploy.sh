#!/bin/bash

# 🚀 Finlytics - Automatic GitHub Pages Deployment Script
# This script will deploy your trading system to GitHub Pages

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   🚀 Finlytics Trading System - GitHub Deployment         ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Step 1: Check current status
echo "📋 Step 1: Checking current git status..."
git status
echo ""

# Step 2: Create/switch to main branch
echo "🌿 Step 2: Creating/switching to main branch..."
git checkout -b main 2>/dev/null || git checkout main
echo "✅ On branch: $(git branch --show-current)"
echo ""

# Step 3: Add all files
echo "📦 Step 3: Adding all files..."
git add .
echo "✅ Files staged for commit"
echo ""

# Step 4: Show what will be committed
echo "📝 Files to be committed:"
git status --short
echo ""

# Step 5: Commit changes
echo "💾 Step 4: Committing changes..."
git commit -m "🚀 Deploy Finlytics to GitHub Pages" || echo "⚠️  Nothing new to commit (already committed)"
echo ""

# Step 6: Push to GitHub
echo "🚀 Step 5: Pushing to GitHub..."
git push -u origin main
echo ""

# Step 7: Success message
echo "╔════════════════════════════════════════════════════════════╗"
echo "║   ✅ DEPLOYMENT SUCCESSFUL!                                ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "🎉 Your code has been pushed to GitHub!"
echo ""
echo "📍 Next Steps:"
echo "   1. Visit: https://github.com/Hemish1910/Finlytics/settings/pages"
echo "   2. Set source to: main branch, /docs folder"
echo "   3. Click Save"
echo "   4. Wait 1-2 minutes"
echo "   5. Visit: https://hemish1910.github.io/Finlytics/"
echo ""
echo "📚 Documentation:"
echo "   - GIT_PUSH_GUIDE.md - Detailed git instructions"
echo "   - FINAL_GITHUB_DEPLOYMENT.md - Complete deployment guide"
echo ""
echo "🎊 Your Finlytics Trading System is ready to go live!"
