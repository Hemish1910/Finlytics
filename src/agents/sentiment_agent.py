"""Sentiment Agent - Analyzes market sentiment from news and social media."""
import asyncio
from typing import List, Dict
from datetime import datetime, timedelta
from textblob import TextBlob
from src.agents.base_agent import BaseAgent
from src.core.events import EventType
from src.core.logger import log


class SentimentAgent(BaseAgent):
    """Agent responsible for sentiment analysis."""
    
    def __init__(self, symbols: List[str]):
        super().__init__("SentimentAgent")
        self.symbols = symbols
        self.sentiment_scores: Dict[str, float] = {}
        
    async def initialize(self):
        """Initialize the sentiment agent."""
        log.info(f"Initializing Sentiment Agent for symbols: {self.symbols}")
    
    async def process(self):
        """Analyze sentiment for tracked symbols."""
        for symbol in self.symbols:
            try:
                sentiment = await self._analyze_sentiment(symbol)
                if sentiment:
                    self.sentiment_scores[symbol] = sentiment["score"]
                    await self._publish_sentiment(symbol, sentiment)
            except Exception as e:
                log.error(f"Error analyzing sentiment for {symbol}: {e}")
        
        await self.send_heartbeat()
    
    async def _analyze_sentiment(self, symbol: str) -> Dict:
        """Analyze sentiment for a symbol."""
        try:
            # In a real implementation, this would fetch news and social media data
            # For now, we'll simulate sentiment analysis
            
            # Simulate fetching news headlines
            headlines = await self._fetch_news(symbol)
            
            if not headlines:
                return None
            
            # Analyze sentiment of headlines
            sentiments = []
            for headline in headlines:
                blob = TextBlob(headline)
                sentiments.append(blob.sentiment.polarity)
            
            # Calculate average sentiment
            avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
            
            # Classify sentiment
            if avg_sentiment > 0.1:
                classification = "positive"
            elif avg_sentiment < -0.1:
                classification = "negative"
            else:
                classification = "neutral"
            
            return {
                "score": avg_sentiment,
                "classification": classification,
                "num_sources": len(headlines),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            log.error(f"Error in sentiment analysis for {symbol}: {e}")
            return None
    
    async def _fetch_news(self, symbol: str) -> List[str]:
        """Fetch news headlines for a symbol."""
        # Simulate news fetching
        # In real implementation, this would use News API or similar
        
        # Simulated headlines (in production, fetch from API)
        simulated_headlines = [
            f"{symbol} shows strong performance in recent trading",
            f"Analysts upgrade {symbol} rating",
            f"{symbol} announces new product launch",
            f"Market volatility affects {symbol} trading",
            f"{symbol} reports quarterly earnings"
        ]
        
        # Simulate API delay
        await asyncio.sleep(0.1)
        
        return simulated_headlines[:3]  # Return subset
    
    async def _publish_sentiment(self, symbol: str, sentiment: Dict):
        """Publish sentiment analysis results."""
        await self.publish_event(
            EventType.SENTIMENT_ANALYSIS,
            {
                "symbol": symbol,
                "sentiment_score": sentiment["score"],
                "classification": sentiment["classification"],
                "num_sources": sentiment["num_sources"],
                "timestamp": sentiment["timestamp"]
            }
        )
        
        log.info(
            f"Sentiment for {symbol}: {sentiment['classification']} "
            f"(score: {sentiment['score']:.3f})"
        )
    
    async def cleanup(self):
        """Cleanup resources."""
        log.info(f"Cleaning up {self.name}")
        self.sentiment_scores.clear()
    
    def get_interval(self) -> float:
        """Get the processing interval."""
        return 30.0  # Check sentiment every 30 seconds
