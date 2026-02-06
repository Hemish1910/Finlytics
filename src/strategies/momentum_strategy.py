"""Momentum trading strategy."""
from typing import Dict, List
import pandas as pd
import numpy as np


class MomentumStrategy:
    """Simple momentum-based trading strategy."""
    
    def __init__(self, lookback_period: int = 20, threshold: float = 0.02):
        self.lookback_period = lookback_period
        self.threshold = threshold
        
    def generate_signal(self, prices: List[float]) -> Dict:
        """Generate trading signal based on momentum."""
        if len(prices) < self.lookback_period:
            return {"signal": "HOLD", "strength": 0.0, "reason": "Insufficient data"}
        
        df = pd.DataFrame(prices, columns=['price'])
        
        # Calculate momentum
        momentum = (df['price'].iloc[-1] - df['price'].iloc[-self.lookback_period]) / df['price'].iloc[-self.lookback_period]
        
        # Generate signal
        if momentum > self.threshold:
            return {
                "signal": "BUY",
                "strength": min(abs(momentum) / (self.threshold * 2), 1.0),
                "reason": f"Positive momentum: {momentum:.2%}"
            }
        elif momentum < -self.threshold:
            return {
                "signal": "SELL",
                "strength": min(abs(momentum) / (self.threshold * 2), 1.0),
                "reason": f"Negative momentum: {momentum:.2%}"
            }
        else:
            return {
                "signal": "HOLD",
                "strength": 0.0,
                "reason": f"Weak momentum: {momentum:.2%}"
            }


class MeanReversionStrategy:
    """Mean reversion trading strategy."""
    
    def __init__(self, lookback_period: int = 20, num_std: float = 2.0):
        self.lookback_period = lookback_period
        self.num_std = num_std
        
    def generate_signal(self, prices: List[float]) -> Dict:
        """Generate trading signal based on mean reversion."""
        if len(prices) < self.lookback_period:
            return {"signal": "HOLD", "strength": 0.0, "reason": "Insufficient data"}
        
        df = pd.DataFrame(prices, columns=['price'])
        
        # Calculate mean and standard deviation
        mean = df['price'].rolling(window=self.lookback_period).mean().iloc[-1]
        std = df['price'].rolling(window=self.lookback_period).std().iloc[-1]
        current_price = df['price'].iloc[-1]
        
        # Calculate z-score
        z_score = (current_price - mean) / std if std > 0 else 0
        
        # Generate signal
        if z_score < -self.num_std:
            return {
                "signal": "BUY",
                "strength": min(abs(z_score) / (self.num_std * 2), 1.0),
                "reason": f"Price below mean by {abs(z_score):.2f} std devs"
            }
        elif z_score > self.num_std:
            return {
                "signal": "SELL",
                "strength": min(abs(z_score) / (self.num_std * 2), 1.0),
                "reason": f"Price above mean by {z_score:.2f} std devs"
            }
        else:
            return {
                "signal": "HOLD",
                "strength": 0.0,
                "reason": f"Price within normal range (z-score: {z_score:.2f})"
            }


class TrendFollowingStrategy:
    """Trend following strategy using moving averages."""
    
    def __init__(self, short_period: int = 20, long_period: int = 50):
        self.short_period = short_period
        self.long_period = long_period
        
    def generate_signal(self, prices: List[float]) -> Dict:
        """Generate trading signal based on trend following."""
        if len(prices) < self.long_period:
            return {"signal": "HOLD", "strength": 0.0, "reason": "Insufficient data"}
        
        df = pd.DataFrame(prices, columns=['price'])
        
        # Calculate moving averages
        short_ma = df['price'].rolling(window=self.short_period).mean().iloc[-1]
        long_ma = df['price'].rolling(window=self.long_period).mean().iloc[-1]
        
        # Calculate difference
        ma_diff = (short_ma - long_ma) / long_ma if long_ma > 0 else 0
        
        # Generate signal
        if short_ma > long_ma:
            return {
                "signal": "BUY",
                "strength": min(abs(ma_diff) * 10, 1.0),
                "reason": f"Golden cross: Short MA ({short_ma:.2f}) > Long MA ({long_ma:.2f})"
            }
        elif short_ma < long_ma:
            return {
                "signal": "SELL",
                "strength": min(abs(ma_diff) * 10, 1.0),
                "reason": f"Death cross: Short MA ({short_ma:.2f}) < Long MA ({long_ma:.2f})"
            }
        else:
            return {
                "signal": "HOLD",
                "strength": 0.0,
                "reason": "Moving averages aligned"
            }
