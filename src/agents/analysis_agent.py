"""Analysis Agent - Performs technical and fundamental analysis."""
import asyncio
from typing import Dict, List
import pandas as pd
import numpy as np
from src.agents.base_agent import BaseAgent
from src.core.events import Event, EventType
from src.core.config import settings
from src.core.logger import log


class AnalysisAgent(BaseAgent):
    """Agent responsible for technical and fundamental analysis."""
    
    def __init__(self):
        super().__init__("AnalysisAgent")
        self.price_history: Dict[str, List[float]] = {}
        self.max_history_length = 200
        
    async def initialize(self):
        """Initialize the analysis agent."""
        log.info("Initializing Analysis Agent")
        
    async def subscribe_to_events(self):
        """Subscribe to market data events."""
        self.subscribe(EventType.PRICE_UPDATE)
        self.subscribe(EventType.MARKET_DATA_UPDATE)
    
    async def handle_event(self, event: Event):
        """Handle incoming market data events."""
        if event.event_type == EventType.PRICE_UPDATE:
            await self._update_price_history(event)
        elif event.event_type == EventType.MARKET_DATA_UPDATE:
            await self._analyze_market_data(event)
    
    async def _update_price_history(self, event: Event):
        """Update price history for a symbol."""
        symbol = event.data.get("symbol")
        price = event.data.get("price")
        
        if not symbol or not price:
            return
        
        if symbol not in self.price_history:
            self.price_history[symbol] = []
        
        self.price_history[symbol].append(price)
        
        # Keep only recent history
        if len(self.price_history[symbol]) > self.max_history_length:
            self.price_history[symbol] = self.price_history[symbol][-self.max_history_length:]
    
    async def _analyze_market_data(self, event: Event):
        """Perform analysis on market data."""
        symbol = event.data.get("symbol")
        
        if not symbol or symbol not in self.price_history:
            return
        
        prices = self.price_history[symbol]
        
        if len(prices) < 20:  # Need minimum data for analysis
            return
        
        # Perform technical analysis
        analysis = await self._technical_analysis(symbol, prices)
        
        # Publish analysis results
        await self.publish_event(
            EventType.TECHNICAL_ANALYSIS,
            {
                "symbol": symbol,
                "analysis": analysis,
                "current_price": prices[-1]
            }
        )
    
    async def _technical_analysis(self, symbol: str, prices: List[float]) -> Dict:
        """Perform technical analysis on price data."""
        try:
            df = pd.DataFrame(prices, columns=['close'])
            
            # Calculate indicators
            analysis = {
                "symbol": symbol,
                "indicators": {}
            }
            
            # Simple Moving Averages
            if len(prices) >= 20:
                analysis["indicators"]["sma_20"] = df['close'].rolling(window=20).mean().iloc[-1]
            if len(prices) >= 50:
                analysis["indicators"]["sma_50"] = df['close'].rolling(window=50).mean().iloc[-1]
            
            # Exponential Moving Average
            analysis["indicators"]["ema_12"] = df['close'].ewm(span=12).mean().iloc[-1]
            analysis["indicators"]["ema_26"] = df['close'].ewm(span=26).mean().iloc[-1]
            
            # MACD
            ema_12 = df['close'].ewm(span=12).mean()
            ema_26 = df['close'].ewm(span=26).mean()
            macd = ema_12 - ema_26
            signal = macd.ewm(span=9).mean()
            analysis["indicators"]["macd"] = macd.iloc[-1]
            analysis["indicators"]["macd_signal"] = signal.iloc[-1]
            analysis["indicators"]["macd_histogram"] = (macd - signal).iloc[-1]
            
            # RSI
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            analysis["indicators"]["rsi"] = rsi.iloc[-1]
            
            # Bollinger Bands
            sma_20 = df['close'].rolling(window=20).mean()
            std_20 = df['close'].rolling(window=20).std()
            analysis["indicators"]["bb_upper"] = (sma_20 + 2 * std_20).iloc[-1]
            analysis["indicators"]["bb_middle"] = sma_20.iloc[-1]
            analysis["indicators"]["bb_lower"] = (sma_20 - 2 * std_20).iloc[-1]
            
            # Volatility
            analysis["indicators"]["volatility"] = df['close'].pct_change().std() * np.sqrt(252)
            
            # Trend detection
            current_price = prices[-1]
            if "sma_20" in analysis["indicators"]:
                if current_price > analysis["indicators"]["sma_20"]:
                    analysis["trend"] = "bullish"
                else:
                    analysis["trend"] = "bearish"
            
            # Momentum
            if analysis["indicators"]["rsi"] > 70:
                analysis["momentum"] = "overbought"
            elif analysis["indicators"]["rsi"] < 30:
                analysis["momentum"] = "oversold"
            else:
                analysis["momentum"] = "neutral"
            
            log.debug(f"Technical analysis for {symbol}: RSI={analysis['indicators']['rsi']:.2f}")
            
            return analysis
            
        except Exception as e:
            log.error(f"Error in technical analysis for {symbol}: {e}")
            return {}
    
    async def process(self):
        """Periodic processing."""
        # Send heartbeat
        await self.send_heartbeat()
    
    async def cleanup(self):
        """Cleanup resources."""
        log.info(f"Cleaning up {self.name}")
        self.price_history.clear()
    
    def get_interval(self) -> float:
        """Get the processing interval."""
        return settings.analysis_interval
