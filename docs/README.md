# Finlytics - Real-Time Trading Agent System

🚀 **Live Demo**: [https://hemish1910.github.io/Finlytics/](https://hemish1910.github.io/Finlytics/)

## Overview

Finlytics is a complete real-time multi-agent trading system built with Python. This is the web dashboard interface that provides real-time monitoring and control of the trading system.

## Features

### 🤖 Multi-Agent Architecture
- **Market Data Agent**: Real-time data collection and streaming
- **Analysis Agent**: Technical analysis with 10+ indicators
- **Signal Agent**: Trading signal generation with confidence scoring
- **Risk Agent**: Position sizing and risk management
- **Execution Agent**: Order placement and management
- **Portfolio Agent**: Portfolio tracking and P&L calculation

### 📊 Dashboard Features
- Real-time portfolio overview
- Trading statistics and performance metrics
- Agent status monitoring
- Recent trades table
- Active trading signals
- Live market data stream
- System controls and logs

### 🎨 Modern UI/UX
- Beautiful gradient design
- Responsive layout (mobile-friendly)
- Real-time data updates
- Interactive charts and visualizations
- Dark theme optimized for trading

## Technology Stack

### Frontend (This Dashboard)
- **HTML5/CSS3**: Modern, responsive design
- **JavaScript (Vanilla)**: No framework dependencies
- **GitHub Pages**: Free static hosting

### Backend (Python System)
- **Python 3.11+**: Core language
- **FastAPI**: REST API framework
- **SQLAlchemy**: Database ORM
- **pandas/numpy**: Data analysis
- **asyncio**: Asynchronous operations
- **WebSockets**: Real-time communication

## Quick Start

### View Live Dashboard
Simply visit: [https://hemish1910.github.io/Finlytics/](https://hemish1910.github.io/Finlytics/)

The dashboard runs in **demo mode** with simulated data for demonstration purposes.

### Run Full System Locally

To run the complete trading system with Python backend:

```bash
# Clone the repository
git clone https://github.com/Hemish1910/Finlytics.git
cd Finlytics

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the trading system
python src/main.py
```

### Configuration

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Edit `.env` with your settings:
- API keys for market data providers
- Database configuration
- Trading parameters
- Risk limits

## Architecture

### Event-Driven Design
```
Market Data → Analysis → Signals → Risk Check → Execution → Portfolio Update
     ↓           ↓          ↓           ↓            ↓            ↓
  Event Bus ←────────────────────────────────────────────────────┘
```

### Agent Communication
- Pub/Sub messaging pattern
- Event-driven architecture
- Asynchronous processing
- Real-time data streaming

### Database Schema
- **Trades**: Trade history and execution details
- **Positions**: Current open positions
- **Signals**: Trading signals with confidence scores
- **MarketData**: Historical price data
- **Portfolio**: Portfolio snapshots over time
- **RiskMetrics**: Risk calculations and limits
- **AgentStatus**: Agent health monitoring

## Trading Strategies

### Built-in Strategies
1. **Momentum Strategy**: Follows price momentum with trend confirmation
2. **Mean Reversion Strategy**: Trades oversold/overbought conditions
3. **Trend Following Strategy**: Identifies and follows market trends

### Custom Strategies
Create your own strategies by extending the base strategy class:

```python
from src.strategies.base_strategy import BaseStrategy

class MyStrategy(BaseStrategy):
    def generate_signals(self, market_data):
        # Your strategy logic here
        pass
```

## Safety Features

⚠️ **Important Safety Measures**:
- ✅ Paper trading mode enabled by default
- ✅ Risk limits enforced on all positions
- ✅ Position size controls
- ✅ Stop-loss protection
- ✅ Portfolio exposure limits
- ✅ Maximum drawdown protection

## API Endpoints

When running the Python backend, the following endpoints are available:

- `GET /api/status` - System status
- `GET /api/portfolio` - Portfolio data
- `GET /api/trades` - Trade history
- `GET /api/signals` - Active signals
- `GET /api/positions` - Current positions
- `GET /api/logs` - System logs
- `GET /api/report` - Download report
- `GET /health` - Health check
- `WS /ws` - WebSocket real-time stream

## Development

### Project Structure
```
Finlytics/
├── docs/                  # GitHub Pages dashboard
│   ├── index.html        # Main dashboard
│   ├── assets/
│   │   ├── css/          # Stylesheets
│   │   └── js/           # JavaScript
│   └── README.md         # This file
├── src/                   # Python source code
│   ├── agents/           # Trading agents
│   ├── core/             # Core infrastructure
│   ├── models/           # Database models
│   ├── strategies/       # Trading strategies
│   └── utils/            # Utilities
├── tests/                # Test suite
├── scripts/              # Utility scripts
└── requirements.txt      # Python dependencies
```

### Running Tests
```bash
pytest tests/ -v
```

### Backtesting
```bash
python scripts/run_backtest.py --strategy momentum --start 2024-01-01 --end 2024-12-31
```

### Monitoring
```bash
python scripts/monitor_system.py
```

## Deployment

### GitHub Pages (Frontend Only)
The dashboard is automatically deployed to GitHub Pages on every push to main/master branch.

### Python Backend Deployment Options

#### Option 1: PythonAnywhere (Free)
1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload your code
3. Install dependencies
4. Configure web app

#### Option 2: Heroku (Free Tier)
```bash
heroku create finlytics-trading
git push heroku main
```

#### Option 3: Railway (Free Tier)
1. Connect GitHub repository
2. Deploy automatically

#### Option 4: Local/VPS
Run on your own server or VPS for full control.

## Documentation

- **QUICKSTART.md**: 5-minute setup guide
- **ARCHITECTURE.md**: System design and architecture
- **PROJECT_SUMMARY.md**: Complete project overview
- **DEPLOYMENT.md**: Deployment instructions

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Disclaimer

⚠️ **IMPORTANT**: This software is for educational and research purposes only. 

- NOT financial advice
- NOT guaranteed to be profitable
- Trading involves substantial risk
- Past performance does not guarantee future results
- Always test thoroughly before live trading
- Use paper trading mode for testing
- Consult a financial advisor before trading

## Support

- **Issues**: [GitHub Issues](https://github.com/Hemish1910/Finlytics/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Hemish1910/Finlytics/discussions)
- **Documentation**: See docs/ folder

## Roadmap

- [ ] Machine learning signal generation
- [ ] Advanced charting and visualization
- [ ] Multi-exchange support
- [ ] Options trading strategies
- [ ] Portfolio optimization
- [ ] Sentiment analysis integration
- [ ] Mobile app

## Acknowledgments

Built with modern Python technologies and best practices for algorithmic trading.

---

**Made with ❤️ for algorithmic traders**

🌟 Star this repo if you find it useful!
