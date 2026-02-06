"""Market Data Agent - Collects and streams real-time market data."""
import asyncio
from typing import List, Dict
from datetime import datetime
import yfinance as yf
from src.agents.base_agent import BaseAgent
from src.core.events import EventType
from src.core.config import settings
from src.core.logger import log


class MarketDataAgent(BaseAgent):
    """Agent responsible for collecting and streaming market data."""
    
    def __init__(self, symbols: List[str]):
        super().__init__("MarketDataAgent")
        self.symbols = symbols
        self.last_prices: Dict[str, float] = {}
        self.tickers = {}
        
    async def initialize(self):
        """Initialize market data connections."""
        log.info(f"Initializing market data for symbols: {self.symbols}")
        
        # Initialize yfinance tickers
        for symbol in self.symbols:
            try:
                self.tickers[symbol] = yf.Ticker(symbol)
                log.info(f"Initialized ticker for {symbol}")
            except Exception as e:
                log.error(f"Failed to initialize ticker for {symbol}: {e}")
    
    async def process(self):
        """Fetch and publish market data."""
        for symbol in self.symbols:
            try:
                await self._fetch_and_publish_data(symbol)
            except Exception as e:
                log.error(f"Error fetching data for {symbol}: {e}")
        
        # Send heartbeat every 10 iterations
        if hasattr(self, '_iteration_count'):
            self._iteration_count += 1
        else:
            self._iteration_count = 1
            
        if self._iteration_count % 10 == 0:
            await self.send_heartbeat()
    
    async def _fetch_and_publish_data(self, symbol: str):
        """Fetch and publish data for a single symbol."""
        ticker = self.tickers.get(symbol)
        if not ticker:
            return
        
        # Get current price data
        try:
            # Run blocking yfinance call in executor
            loop = asyncio.get_event_loop()
            info = await loop.run_in_executor(None, lambda: ticker.info)
            
            current_price = info.get('currentPrice') or info.get('regularMarketPrice')
            if not current_price:
                return
            
            # Check if price changed
            last_price = self.last_prices.get(symbol)
            if last_price == current_price:
                return
            
            self.last_prices[symbol] = current_price
            
            # Prepare market data
            market_data = {
                "symbol": symbol,
                "price": current_price,
                "bid": info.get('bid'),
                "ask": info.get('ask'),
                "volume": info.get('volume'),
                "market_cap": info.get('marketCap'),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Publish price update event
            await self.publish_event(
                EventType.PRICE_UPDATE,
                market_data
            )
            
            # Publish general market data update
            await self.publish_event(
                EventType.MARKET_DATA_UPDATE,
                market_data
            )
            
            log.debug(f"Published market data for {symbol}: ${current_price}")
            
        except Exception as e:
            log.error(f"Error fetching data for {symbol}: {e}")
    
    async def cleanup(self):
        """Cleanup resources."""
        log.info(f"Cleaning up {self.name}")
        self.tickers.clear()
    
    def get_interval(self) -> float:
        """Get the data fetch interval."""
        return settings.market_data_interval
    
    async def get_historical_data(self, symbol: str, period: str = "1mo") -> Dict:
        """Get historical data for a symbol."""
        try:
            ticker = self.tickers.get(symbol)
            if not ticker:
                return {}
            
            loop = asyncio.get_event_loop()
            hist = await loop.run_in_executor(
                None,
                lambda: ticker.history(period=period)
            )
            
            return hist.to_dict('records')
        except Exception as e:
            log.error(f"Error fetching historical data for {symbol}: {e}")
            return {}
