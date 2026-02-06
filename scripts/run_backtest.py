"""Script to run backtesting on historical data."""
import asyncio
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.logger import log
from src.strategies.momentum_strategy import MomentumStrategy, TrendFollowingStrategy


class Backtester:
    """Simple backtesting engine."""
    
    def __init__(self, initial_capital: float = 100000):
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.positions = {}
        self.trades = []
        
    def run_backtest(self, prices: list, strategy):
        """Run backtest on historical prices."""
        log.info(f"Starting backtest with ${self.capital:,.2f}")
        
        for i in range(len(prices)):
            if i < 50:  # Need minimum data
                continue
            
            # Get price history up to this point
            price_history = prices[:i+1]
            current_price = prices[i]
            
            # Generate signal
            signal = strategy.generate_signal(price_history)
            
            # Execute trades based on signal
            if signal["signal"] == "BUY" and signal["strength"] > 0.6:
                self._execute_buy(current_price, i)
            elif signal["signal"] == "SELL" and signal["strength"] > 0.6:
                self._execute_sell(current_price, i)
        
        # Close any remaining positions
        if prices:
            final_price = prices[-1]
            if self.positions:
                self._execute_sell(final_price, len(prices) - 1)
        
        return self._calculate_metrics()
    
    def _execute_buy(self, price: float, index: int):
        """Execute buy order."""
        if self.positions:  # Already have position
            return
        
        # Use 90% of capital
        position_value = self.capital * 0.9
        quantity = position_value / price
        
        self.positions = {
            "quantity": quantity,
            "entry_price": price,
            "entry_index": index
        }
        
        self.capital -= position_value
        
        self.trades.append({
            "type": "BUY",
            "price": price,
            "quantity": quantity,
            "index": index
        })
        
        log.info(f"BUY: {quantity:.2f} @ ${price:.2f}")
    
    def _execute_sell(self, price: float, index: int):
        """Execute sell order."""
        if not self.positions:
            return
        
        quantity = self.positions["quantity"]
        entry_price = self.positions["entry_price"]
        
        proceeds = quantity * price
        self.capital += proceeds
        
        pnl = (price - entry_price) * quantity
        pnl_pct = (price - entry_price) / entry_price * 100
        
        self.trades.append({
            "type": "SELL",
            "price": price,
            "quantity": quantity,
            "index": index,
            "pnl": pnl,
            "pnl_pct": pnl_pct
        })
        
        log.info(f"SELL: {quantity:.2f} @ ${price:.2f} | P&L: ${pnl:.2f} ({pnl_pct:.2f}%)")
        
        self.positions = {}
    
    def _calculate_metrics(self):
        """Calculate backtest metrics."""
        final_value = self.capital
        total_return = final_value - self.initial_capital
        total_return_pct = (total_return / self.initial_capital) * 100
        
        num_trades = len([t for t in self.trades if t["type"] == "BUY"])
        winning_trades = len([t for t in self.trades if t["type"] == "SELL" and t.get("pnl", 0) > 0])
        losing_trades = len([t for t in self.trades if t["type"] == "SELL" and t.get("pnl", 0) < 0])
        
        win_rate = (winning_trades / num_trades * 100) if num_trades > 0 else 0
        
        return {
            "initial_capital": self.initial_capital,
            "final_value": final_value,
            "total_return": total_return,
            "total_return_pct": total_return_pct,
            "num_trades": num_trades,
            "winning_trades": winning_trades,
            "losing_trades": losing_trades,
            "win_rate": win_rate
        }


async def main():
    """Main backtest function."""
    log.info("=" * 60)
    log.info("Finlytics Backtesting")
    log.info("=" * 60)
    
    # Generate sample price data (in production, load from database or API)
    import numpy as np
    
    # Simulate price movement
    np.random.seed(42)
    prices = [100]
    for _ in range(500):
        change = np.random.normal(0.001, 0.02)  # Mean return 0.1%, volatility 2%
        prices.append(prices[-1] * (1 + change))
    
    log.info(f"Generated {len(prices)} price points")
    log.info(f"Starting price: ${prices[0]:.2f}")
    log.info(f"Ending price: ${prices[-1]:.2f}")
    
    # Test Momentum Strategy
    log.info("\n" + "=" * 60)
    log.info("Testing Momentum Strategy")
    log.info("=" * 60)
    
    backtester1 = Backtester(initial_capital=100000)
    strategy1 = MomentumStrategy(lookback_period=20, threshold=0.02)
    metrics1 = backtester1.run_backtest(prices, strategy1)
    
    log.info("\nMomentum Strategy Results:")
    log.info(f"Initial Capital: ${metrics1['initial_capital']:,.2f}")
    log.info(f"Final Value: ${metrics1['final_value']:,.2f}")
    log.info(f"Total Return: ${metrics1['total_return']:,.2f} ({metrics1['total_return_pct']:.2f}%)")
    log.info(f"Number of Trades: {metrics1['num_trades']}")
    log.info(f"Win Rate: {metrics1['win_rate']:.2f}%")
    
    # Test Trend Following Strategy
    log.info("\n" + "=" * 60)
    log.info("Testing Trend Following Strategy")
    log.info("=" * 60)
    
    backtester2 = Backtester(initial_capital=100000)
    strategy2 = TrendFollowingStrategy(short_period=20, long_period=50)
    metrics2 = backtester2.run_backtest(prices, strategy2)
    
    log.info("\nTrend Following Strategy Results:")
    log.info(f"Initial Capital: ${metrics2['initial_capital']:,.2f}")
    log.info(f"Final Value: ${metrics2['final_value']:,.2f}")
    log.info(f"Total Return: ${metrics2['total_return']:,.2f} ({metrics2['total_return_pct']:.2f}%)")
    log.info(f"Number of Trades: {metrics2['num_trades']}")
    log.info(f"Win Rate: {metrics2['win_rate']:.2f}%")
    
    log.info("\n" + "=" * 60)
    log.info("Backtesting Complete")
    log.info("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
