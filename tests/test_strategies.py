"""Tests for trading strategies."""
import pytest
from src.strategies.momentum_strategy import (
    MomentumStrategy,
    MeanReversionStrategy,
    TrendFollowingStrategy,
)


def test_momentum_strategy_buy_signal():
    """Test momentum strategy generates buy signal."""
    strategy = MomentumStrategy(lookback_period=10, threshold=0.02)
    
    # Upward trending prices
    prices = [100 + i for i in range(20)]
    signal = strategy.generate_signal(prices)
    
    assert signal["signal"] == "BUY"
    assert signal["strength"] > 0


def test_momentum_strategy_sell_signal():
    """Test momentum strategy generates sell signal."""
    strategy = MomentumStrategy(lookback_period=10, threshold=0.02)
    
    # Downward trending prices
    prices = [100 - i for i in range(20)]
    signal = strategy.generate_signal(prices)
    
    assert signal["signal"] == "SELL"
    assert signal["strength"] > 0


def test_momentum_strategy_hold_signal():
    """Test momentum strategy generates hold signal."""
    strategy = MomentumStrategy(lookback_period=10, threshold=0.02)
    
    # Flat prices
    prices = [100] * 20
    signal = strategy.generate_signal(prices)
    
    assert signal["signal"] == "HOLD"


def test_mean_reversion_strategy():
    """Test mean reversion strategy."""
    strategy = MeanReversionStrategy(lookback_period=20, num_std=2.0)
    
    # Create prices with outlier
    prices = [100] * 30
    prices.append(120)  # Outlier above mean
    
    signal = strategy.generate_signal(prices)
    
    assert signal["signal"] in ["BUY", "SELL", "HOLD"]
    assert "strength" in signal


def test_trend_following_strategy():
    """Test trend following strategy."""
    strategy = TrendFollowingStrategy(short_period=10, long_period=20)
    
    # Create upward trend
    prices = [100 + i * 0.5 for i in range(50)]
    signal = strategy.generate_signal(prices)
    
    assert signal["signal"] in ["BUY", "SELL", "HOLD"]
    assert "strength" in signal


def test_strategy_insufficient_data():
    """Test strategies with insufficient data."""
    strategy = MomentumStrategy(lookback_period=20)
    
    # Not enough data
    prices = [100, 101, 102]
    signal = strategy.generate_signal(prices)
    
    assert signal["signal"] == "HOLD"
    assert "Insufficient data" in signal["reason"]
