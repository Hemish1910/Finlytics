# Finlytics Trading System - Deployment Guide

## 🚀 Deployment Instructions

This guide will help you deploy the Finlytics Trading System to Vercel.

### Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Vercel CLI** (optional): `npm install -g vercel`

### Deployment Methods

#### Method 1: Deploy via Vercel Dashboard (Recommended)

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Finlytics Trading System"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Import to Vercel**:
   - Go to [vercel.com/new](https://vercel.com/new)
   - Click "Import Git Repository"
   - Select your GitHub repository
   - Click "Import"

3. **Configure Project**:
   - Framework Preset: **Other**
   - Root Directory: `./`
   - Build Command: (leave empty)
   - Output Directory: (leave empty)
   - Install Command: `pip install -r requirements.txt`

4. **Deploy**:
   - Click "Deploy"
   - Wait for deployment to complete
   - Your app will be live at: `https://your-project-name.vercel.app`

#### Method 2: Deploy via Vercel CLI

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   cd /vercel/sandbox
   vercel
   ```

4. **Follow the prompts**:
   - Set up and deploy? **Y**
   - Which scope? (select your account)
   - Link to existing project? **N**
   - What's your project's name? **finlytics-trading**
   - In which directory is your code located? **.**
   - Want to override the settings? **N**

5. **Production Deployment**:
   ```bash
   vercel --prod
   ```

### Environment Variables (Optional)

If you want to configure custom settings, add these environment variables in Vercel:

1. Go to your project in Vercel Dashboard
2. Navigate to **Settings** → **Environment Variables**
3. Add the following variables:

```
TRADING_MODE=paper
INITIAL_CAPITAL=100000
MAX_POSITION_SIZE=0.1
STOP_LOSS_PERCENTAGE=0.02
TAKE_PROFIT_PERCENTAGE=0.05
```

### Post-Deployment

After deployment, your trading system will be available at:

```
https://your-project-name.vercel.app
```

#### Available Endpoints:

- **Dashboard**: `https://your-project-name.vercel.app/`
- **API Status**: `https://your-project-name.vercel.app/api/status`
- **Portfolio**: `https://your-project-name.vercel.app/api/portfolio`
- **Trades**: `https://your-project-name.vercel.app/api/trades`
- **Signals**: `https://your-project-name.vercel.app/api/signals`
- **Health Check**: `https://your-project-name.vercel.app/health`

### Features Available in Deployment

✅ **Real-time Dashboard** - Beautiful web interface
✅ **WebSocket Support** - Live data updates
✅ **API Endpoints** - RESTful API for all data
✅ **Portfolio Tracking** - Real-time portfolio monitoring
✅ **Agent Status** - Monitor all 6 trading agents
✅ **Trade History** - View all executed trades
✅ **Signal Monitoring** - Track trading signals

### Limitations on Vercel

⚠️ **Serverless Functions**: Vercel uses serverless functions with a 10-second timeout for Hobby plan
⚠️ **Stateless**: Each request is stateless, so long-running background tasks may not work as expected
⚠️ **Database**: SQLite database will reset on each deployment (use external database for persistence)

### Recommended for Production

For a full production deployment with persistent data and long-running agents:

1. **Database**: Use PostgreSQL (Supabase, Neon, or Railway)
2. **Background Workers**: Deploy agents separately on:
   - Railway
   - Render
   - DigitalOcean App Platform
   - AWS EC2/ECS
3. **Message Queue**: Use Redis Cloud or AWS SQS
4. **Frontend**: Keep on Vercel (it's perfect for the dashboard)

### Troubleshooting

**Issue**: Deployment fails with "Module not found"
- **Solution**: Ensure all dependencies are in `requirements.txt`

**Issue**: WebSocket connection fails
- **Solution**: Vercel supports WebSockets, but check your browser console for errors

**Issue**: Database resets on each deployment
- **Solution**: Use an external database (PostgreSQL, MySQL) instead of SQLite

**Issue**: Timeout errors
- **Solution**: Optimize long-running operations or move them to background workers

### Monitoring

Monitor your deployment:

1. **Vercel Dashboard**: View logs and analytics
2. **Health Endpoint**: `https://your-project-name.vercel.app/health`
3. **System Status**: `https://your-project-name.vercel.app/api/status`

### Support

For issues or questions:
- Check the logs in Vercel Dashboard
- Review the API documentation in README.md
- Check the ARCHITECTURE.md for system design

---

## 🎉 Your Trading System is Live!

Once deployed, share your link:
```
https://your-project-name.vercel.app
```

The dashboard will show:
- Real-time portfolio value
- Active trading agents
- Recent trades and signals
- System status and metrics

**Happy Trading! 📈🚀**
