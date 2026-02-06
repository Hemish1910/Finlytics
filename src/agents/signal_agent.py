"""Signal Agent - Generates trading signals based on analysis."""
from typing import Dict
from src.agents.base_agent import BaseAgent
from src.core.events import Event, EventType
from src.core.config import settings
from src.core.logger import log


class SignalAgent(BaseAgent):
    """Agent responsible for generating trading signals."""
    
    def __init__(self):
        super().__init__("SignalAgent")
        self.latest_analysis: Dict[str, Dict] = {}
        self.latest_prices: Dict[str, float] = {}
        
    async def initialize(self):
        """Initialize the signal agent."""
        log.info("Initializing Signal Agent")
    
    async def subscribe_to_events(self):
        """Subscribe to analysis events."""
        self.subscribe(EventType.TECHNICAL_ANALYSIS)
        self.subscribe(EventType.PRICE_UPDATE)
    
    async def handle_event(self, event: Event):
        """Handle incoming events."""
        if event.event_type == EventType.TECHNICAL_ANALYSIS:
            await self._process_analysis(event)
        elif event.event_type == EventType.PRICE_UPDATE:
            symbol = event.data.get("symbol")
            price = event.data.get("price")
            if symbol and price:
                self.latest_prices[symbol] = price
    
    async def _process_analysis(self, event: Event):
        """Process technical analysis and generate signals."""
        symbol = event.data.get("symbol")
        analysis = event.data.get("analysis", {})
        
        if not symbol or not analysis:
            return
        
        self.latest_analysis[symbol] = analysis
        
        # Generate trading signal
        signal = await self._generate_signal(symbol, analysis)
        
        if signal:
            await self._publish_signal(symbol, signal)
    
    async def _generate_signal(self, symbol: str, analysis: Dict) -> Dict:
        """Generate trading signal based on analysis."""
        try:
            indicators = analysis.get("indicators", {})
            
            if not indicators:
                return None
            
            # Initialize signal
            signal = {
                "type": "HOLD",
                "strength": 0.0,
                "reasons": []
            }
            
            score = 0
            max_score = 0
            
            # RSI-based signals
            rsi = indicators.get("rsi")
            if rsi is not None:
                max_score += 2
                if rsi < 30:
                    score += 2
                    signal["reasons"].append(f"RSI oversold ({rsi:.2f})")
                elif rsi > 70:
                    score -= 2
                    signal["reasons"].append(f"RSI overbought ({rsi:.2f})")
            
            # MACD-based signals
            macd = indicators.get("macd")
            macd_signal = indicators.get("macd_signal")
            if macd is not None and macd_signal is not None:
                max_score += 1
                if macd > macd_signal:
                    score += 1
                    signal["reasons"].append("MACD bullish crossover")
                else:
                    score -= 1
                    signal["reasons"].append("MACD bearish crossover")
            
            # Moving average trend
            current_price = self.latest_prices.get(symbol)
            sma_20 = indicators.get("sma_20")
            sma_50 = indicators.get("sma_50")
            
            if current_price and sma_20:
                max_score += 1
                if current_price > sma_20:
                    score += 1
                    signal["reasons"].append("Price above SMA20")
                else:
                    score -= 1
                    signal["reasons"].append("Price below SMA20")
            
            if sma_20 and sma_50:
                max_score += 1
                if sma_20 > sma_50:
                    score += 1
                    signal["reasons"].append("Golden cross (SMA20 > SMA50)")
                else:
                    score -= 1
                    signal["reasons"].append("Death cross (SMA20 < SMA50)")
            
            # Bollinger Bands
            bb_upper = indicators.get("bb_upper")
            bb_lower = indicators.get("bb_lower")
            if current_price and bb_upper and bb_lower:
                max_score += 1
                if current_price < bb_lower:
                    score += 1
                    signal["reasons"].append("Price below lower Bollinger Band")
                elif current_price > bb_upper:
                    score -= 1
                    signal["reasons"].append("Price above upper Bollinger Band")
            
            # Determine signal type and strength
            if max_score > 0:
                signal["strength"] = abs(score) / max_score
            
            if score >= 3:
                signal["type"] = "BUY"
            elif score <= -3:
                signal["type"] = "SELL"
            else:
                signal["type"] = "HOLD"
            
            # Calculate target and stop loss
            if current_price:
                volatility = indicators.get("volatility", 0.02)
                if signal["type"] == "BUY":
                    signal["target_price"] = current_price * (1 + volatility * 2)
                    signal["stop_loss"] = current_price * (1 - volatility)
                elif signal["type"] == "SELL":
                    signal["target_price"] = current_price * (1 - volatility * 2)
                    signal["stop_loss"] = current_price * (1 + volatility)
            
            return signal
            
        except Exception as e:
            log.error(f"Error generating signal for {symbol}: {e}")
            return None
    
    async def _publish_signal(self, symbol: str, signal: Dict):
        """Publish trading signal."""
        signal_type = signal.get("type")
        
        if signal_type == "HOLD":
            return  # Don't publish hold signals
        
        event_type = EventType.BUY_SIGNAL if signal_type == "BUY" else EventType.SELL_SIGNAL
        
        await self.publish_event(
            event_type,
            {
                "symbol": symbol,
                "signal_type": signal_type,
                "strength": signal.get("strength", 0),
                "reasons": signal.get("reasons", []),
                "target_price": signal.get("target_price"),
                "stop_loss": signal.get("stop_loss"),
                "current_price": self.latest_prices.get(symbol)
            }
        )
        
        log.info(f"Generated {signal_type} signal for {symbol} (strength: {signal['strength']:.2f})")
    
    async def process(self):
        """Periodic processing."""
        await self.send_heartbeat()
    
    async def cleanup(self):
        """Cleanup resources."""
        log.info(f"Cleaning up {self.name}")
        self.latest_analysis.clear()
        self.latest_prices.clear()
    
    def get_interval(self) -> float:
        """Get the processing interval."""
        return settings.signal_interval
