# Finlytics Quick Start Guide

Get up and running with Finlytics in 5 minutes!

## Prerequisites

- Python 3.11 or higher
- pip package manager
- Internet connection (for market data)

## Installation

### 1. Clone and Setup

```bash
# Navigate to project directory
cd finlytics

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings (optional for paper trading)
# nano .env
```

**Minimal Configuration for Paper Trading:**
```env
TRADING_MODE=paper
DEFAULT_CAPITAL=100000
```

## Running the System

### Option 1: Run Main Trading System

```bash
# Run the complete trading system
python -m src.main
```

This will:
- Start all trading agents
- Begin collecting market data for AAPL, GOOGL, MSFT, TSLA, AMZN
- Perform technical analysis
- Generate trading signals
- Execute trades in paper trading mode
- Track portfolio performance

The system will run for 5 minutes by default and then stop.

### Option 2: Run Backtesting

```bash
# Test strategies on historical data
python scripts/run_backtest.py
```

This will:
- Generate simulated price data
- Test momentum and trend-following strategies
- Display performance metrics

### Option 3: Monitor System

```bash
# Monitor system status (run in separate terminal while main system is running)
python scripts/monitor_system.py
```

This will display:
- Agent status
- Portfolio value
- Current positions
- Recent trades
- Performance metrics

## Understanding the Output

### Main System Output

```
2026-02-06 10:30:00 | INFO     | Starting Finlytics Trading System
2026-02-06 10:30:00 | INFO     | Trading Mode: PAPER
2026-02-06 10:30:00 | INFO     | Initial Capital: $100,000.00
2026-02-06 10:30:01 | INFO     | Starting agent: MarketDataAgent
2026-02-06 10:30:01 | INFO     | Starting agent: AnalysisAgent
...
2026-02-06 10:30:05 | INFO     | Published market data for AAPL: $150.25
2026-02-06 10:30:10 | INFO     | Technical analysis for AAPL: RSI=65.32
2026-02-06 10:30:15 | INFO     | Generated BUY signal for AAPL (strength: 0.75)
2026-02-06 10:30:16 | INFO     | Order placed: BUY 6.67 AAPL @ $150.25
2026-02-06 10:30:16 | INFO     | Order filled: BUY 6.67 AAPL @ $150.40
2026-02-06 10:30:20 | INFO     | Portfolio: $100,000.00 | P&L: $0.00 (0.00%) | Positions: 1
```

### Key Events to Watch

1. **Market Data Updates**: Real-time price information
2. **Technical Analysis**: Indicator calculations (RSI, MACD, etc.)
3. **Trading Signals**: Buy/Sell recommendations with strength
4. **Order Execution**: Trade confirmations
5. **Portfolio Updates**: Current value and P&L

## Common Use Cases

### 1. Test a Strategy

Edit `src/main.py` to use your preferred symbols:

```python
symbols = ["AAPL", "TSLA"]  # Trade only these symbols
```

### 2. Adjust Risk Parameters

Edit `.env`:

```env
MAX_POSITION_SIZE=0.05      # Max 5% per position
MAX_PORTFOLIO_RISK=0.01     # Max 1% portfolio risk
```

### 3. Change Update Intervals

Edit `.env`:

```env
MARKET_DATA_INTERVAL=5      # Check prices every 5 seconds
ANALYSIS_INTERVAL=10        # Analyze every 10 seconds
SIGNAL_INTERVAL=20          # Generate signals every 20 seconds
```

### 4. Run Indefinitely

```bash
# Run until manually stopped (Ctrl+C)
python -m src.main --continuous
```

## Viewing Results

### Check Logs

```bash
# View main log
tail -f logs/finlytics.log

# View errors only
tail -f logs/errors.log
```

### Check Database

```bash
# Install SQLite browser or use command line
sqlite3 finlytics.db

# View trades
SELECT * FROM trades ORDER BY timestamp DESC LIMIT 10;

# View positions
SELECT * FROM positions WHERE quantity > 0;

# View portfolio snapshots
SELECT * FROM portfolio_snapshots ORDER BY timestamp DESC LIMIT 5;
```

## Troubleshooting

### Issue: "No module named 'src'"

**Solution:** Make sure you're running from the project root directory:
```bash
cd /path/to/finlytics
python -m src.main
```

### Issue: "Failed to fetch market data"

**Solution:** Check your internet connection. The system uses yfinance which requires internet access.

### Issue: "Database locked"

**Solution:** Only one instance can write to the database at a time. Stop other instances:
```bash
pkill -f "python -m src.main"
```

### Issue: Import errors for TA-Lib

**Solution:** TA-Lib requires system libraries. Install them first:

**On Ubuntu/Debian:**
```bash
sudo apt-get install ta-lib
pip install TA-Lib
```

**On Mac:**
```bash
brew install ta-lib
pip install TA-Lib
```

**On Windows:**
Download pre-built wheel from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib

## Next Steps

1. **Read the Architecture**: Check `ARCHITECTURE.md` for system design
2. **Explore Agents**: Look at agent implementations in `src/agents/`
3. **Create Strategies**: Add your own strategies in `src/strategies/`
4. **Run Tests**: Execute `pytest tests/` to verify functionality
5. **Customize**: Modify agents and strategies for your needs

## Safety Reminders

⚠️ **Important:**
- Always start with paper trading mode
- Test strategies thoroughly with backtesting
- Never risk more than you can afford to lose
- This is educational software, not financial advice
- Past performance doesn't guarantee future results

## Getting Help

- Check logs in `logs/` directory
- Review `README.md` for detailed documentation
- Examine `ARCHITECTURE.md` for system design
- Look at test files in `tests/` for examples

## Example Session

```bash
# Terminal 1: Start the trading system
python -m src.main

# Terminal 2: Monitor in real-time
watch -n 5 python scripts/monitor_system.py

# Terminal 3: View logs
tail -f logs/finlytics.log
```

Happy Trading! 🚀📈
