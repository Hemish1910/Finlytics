# Finlytics

A comprehensive real-time trading agent system built with Python. Finlytics uses multiple specialized agents working together to analyze markets, generate signals, manage risk, and execute trades.

## 🚀 Features

- **Multi-Agent Architecture**: Specialized agents for different trading tasks
- **Real-Time Market Data**: Live price streaming and market data collection
- **Technical Analysis**: Advanced indicators (RSI, MACD, Bollinger Bands, Moving Averages)
- **Signal Generation**: Automated trading signal generation based on multiple strategies
- **Risk Management**: Position sizing, portfolio risk monitoring, and stop-loss management
- **Order Execution**: Paper trading and live trading support
- **Portfolio Tracking**: Real-time portfolio valuation and P&L tracking
- **Sentiment Analysis**: News and social media sentiment analysis
- **Event-Driven Architecture**: Pub/Sub messaging system for agent communication

## 🏗️ Architecture

### Core Components

1. **Message Bus**: Central pub/sub system for inter-agent communication
2. **Event System**: Typed events for different trading activities
3. **Orchestrator**: Manages agent lifecycle and coordination
4. **Database**: SQLite for storing trades, signals, and market data

### Trading Agents

- **MarketDataAgent**: Collects and streams real-time market data
- **AnalysisAgent**: Performs technical analysis on price data
- **SignalAgent**: Generates trading signals based on analysis
- **RiskAgent**: Manages portfolio risk and position sizing
- **ExecutionAgent**: Handles order placement and management
- **PortfolioAgent**: Tracks portfolio state and performance
- **SentimentAgent**: Analyzes market sentiment from various sources

## 📦 Installation

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd finlytics
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## 🎯 Usage

### Basic Usage

Run the trading system with default settings:

```bash
python -m src.main
```

### Configuration

Edit `.env` file to configure:

- **Trading Mode**: `paper` (simulated) or `live` (real trading)
- **Capital**: Initial trading capital
- **Risk Parameters**: Position size limits, portfolio risk limits
- **API Keys**: For market data providers
- **Symbols**: Stocks to trade

### Example Configuration

```env
TRADING_MODE=paper
DEFAULT_CAPITAL=100000
MAX_POSITION_SIZE=0.1
MAX_PORTFOLIO_RISK=0.02
```

## 📊 Trading Strategies

The system includes several built-in strategies:

### 1. Momentum Strategy
Trades based on price momentum over a lookback period.

```python
from src.strategies.momentum_strategy import MomentumStrategy

strategy = MomentumStrategy(lookback_period=20, threshold=0.02)
signal = strategy.generate_signal(prices)
```

### 2. Mean Reversion Strategy
Trades when price deviates significantly from its mean.

```python
from src.strategies.momentum_strategy import MeanReversionStrategy

strategy = MeanReversionStrategy(lookback_period=20, num_std=2.0)
signal = strategy.generate_signal(prices)
```

### 3. Trend Following Strategy
Uses moving average crossovers to identify trends.

```python
from src.strategies.momentum_strategy import TrendFollowingStrategy

strategy = TrendFollowingStrategy(short_period=20, long_period=50)
signal = strategy.generate_signal(prices)
```

## 🔧 Development

### Project Structure

```
finlytics/
├── src/
│   ├── agents/           # Trading agents
│   │   ├── base_agent.py
│   │   ├── market_data_agent.py
│   │   ├── analysis_agent.py
│   │   ├── signal_agent.py
│   │   ├── risk_agent.py
│   │   ├── execution_agent.py
│   │   ├── portfolio_agent.py
│   │   └── sentiment_agent.py
│   ├── core/             # Core system components
│   │   ├── config.py
│   │   ├── logger.py
│   │   ├── events.py
│   │   ├── message_bus.py
│   │   └── orchestrator.py
│   ├── models/           # Database models
│   │   └── database.py
│   ├── strategies/       # Trading strategies
│   │   └── momentum_strategy.py
│   ├── utils/            # Utilities
│   │   └── database_manager.py
│   └── main.py           # Main entry point
├── tests/                # Test files
├── logs/                 # Log files
├── data/                 # Data storage
├── requirements.txt      # Python dependencies
├── .env.example          # Example environment variables
└── README.md
```

### Running Tests

```bash
pytest tests/ -v
```

### Adding a New Agent

1. Create a new agent class inheriting from `BaseAgent`
2. Implement required methods: `initialize()`, `process()`, `cleanup()`, `get_interval()`
3. Subscribe to relevant events in `subscribe_to_events()`
4. Register the agent with the orchestrator in `main.py`

Example:

```python
from src.agents.base_agent import BaseAgent
from src.core.events import EventType

class MyCustomAgent(BaseAgent):
    def __init__(self):
        super().__init__("MyCustomAgent")
    
    async def initialize(self):
        # Setup code
        pass
    
    async def process(self):
        # Main logic
        pass
    
    async def cleanup(self):
        # Cleanup code
        pass
    
    def get_interval(self) -> float:
        return 5.0  # Run every 5 seconds
```

## 📈 Monitoring

### Logs

Logs are stored in the `logs/` directory:
- `finlytics.log`: General application logs
- `errors.log`: Error logs only

### Portfolio Tracking

The system logs portfolio updates including:
- Total portfolio value
- Cash balance
- Position details
- Realized and unrealized P&L
- Number of active positions

## ⚠️ Risk Disclaimer

This software is for educational and research purposes only. Trading financial instruments carries risk. Past performance does not guarantee future results. Always test strategies thoroughly in paper trading mode before considering live trading.

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details

## 🔗 Resources

- [Technical Analysis Library](https://github.com/bukosabino/ta)
- [yfinance Documentation](https://pypi.org/project/yfinance/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [asyncio Documentation](https://docs.python.org/3/library/asyncio.html)

## 📧 Support

For questions or issues, please open an issue on GitHub.

---

**Built with ❤️ for algorithmic trading enthusiasts**
