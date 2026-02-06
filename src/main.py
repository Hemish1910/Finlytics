"""Main entry point for Finlytics trading system."""
import asyncio
import sys
from src.core.orchestrator import Orchestrator
from src.core.config import settings
from src.core.logger import log
from src.utils.database_manager import db_manager
from src.agents import (
    MarketDataAgent,
    AnalysisAgent,
    SignalAgent,
    RiskAgent,
    ExecutionAgent,
    PortfolioAgent,
    SentimentAgent,
)


async def main():
    """Main function to run the trading system."""
    log.info("=" * 60)
    log.info("Starting Finlytics Trading System")
    log.info("=" * 60)
    log.info(f"Trading Mode: {settings.trading_mode.upper()}")
    log.info(f"Initial Capital: ${settings.default_capital:,.2f}")
    log.info("=" * 60)
    
    # Initialize database
    await db_manager.initialize()
    
    # Define symbols to trade
    symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]
    log.info(f"Trading symbols: {', '.join(symbols)}")
    
    # Create agents
    market_data_agent = MarketDataAgent(symbols=symbols)
    analysis_agent = AnalysisAgent()
    signal_agent = SignalAgent()
    risk_agent = RiskAgent(initial_capital=settings.default_capital)
    execution_agent = ExecutionAgent()
    portfolio_agent = PortfolioAgent(initial_capital=settings.default_capital)
    sentiment_agent = SentimentAgent(symbols=symbols)
    
    # Create orchestrator and register agents
    orchestrator = Orchestrator()
    orchestrator.register_agents([
        market_data_agent,
        analysis_agent,
        signal_agent,
        risk_agent,
        execution_agent,
        portfolio_agent,
        sentiment_agent,
    ])
    
    # Run the system
    try:
        # Run for 5 minutes for testing, or indefinitely if no duration specified
        duration = 300 if len(sys.argv) == 1 else None
        await orchestrator.run(duration=duration)
    except Exception as e:
        log.error(f"Error in main loop: {e}")
    finally:
        # Cleanup
        await db_manager.close()
        log.info("Finlytics Trading System stopped")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("Received keyboard interrupt")
    except Exception as e:
        log.error(f"Fatal error: {e}")
        sys.exit(1)
