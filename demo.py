"""Simple demo script to test the trading system."""
import asyncio
from src.core.logger import log
from src.core.message_bus import message_bus
from src.core.events import Event, EventType
from src.agents import MarketDataAgent, AnalysisAgent, SignalAgent


async def event_logger(event: Event):
    """Log all events for demo purposes."""
    log.info(f"📨 Event: {event.event_type.value} from {event.source_agent}")
    if event.data:
        log.info(f"   Data: {event.data}")


async def main():
    """Run a simple demo of the trading system."""
    log.info("=" * 60)
    log.info("Finlytics Demo - Simple Trading System Test")
    log.info("=" * 60)
    
    # Start message bus
    await message_bus.start()
    
    # Subscribe to all events for logging
    for event_type in EventType:
        message_bus.subscribe(event_type, event_logger)
    
    # Create agents
    log.info("\n📦 Creating agents...")
    market_agent = MarketDataAgent(symbols=["AAPL"])
    analysis_agent = AnalysisAgent()
    signal_agent = SignalAgent()
    
    # Start agents
    log.info("\n🚀 Starting agents...")
    await market_agent.start()
    await analysis_agent.start()
    await signal_agent.start()
    
    log.info("\n⏳ Running for 30 seconds...")
    log.info("Watch for: Market Data → Analysis → Signals\n")
    
    # Run for 30 seconds
    await asyncio.sleep(30)
    
    # Stop agents
    log.info("\n🛑 Stopping agents...")
    await market_agent.stop()
    await analysis_agent.stop()
    await signal_agent.stop()
    
    # Stop message bus
    await message_bus.stop()
    
    log.info("\n" + "=" * 60)
    log.info("Demo Complete!")
    log.info("=" * 60)
    log.info("\nNext steps:")
    log.info("1. Run full system: python -m src.main")
    log.info("2. Run backtesting: python scripts/run_backtest.py")
    log.info("3. Monitor system: python scripts/monitor_system.py")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("\n⚠️  Demo interrupted by user")
    except Exception as e:
        log.error(f"\n❌ Error: {e}")
