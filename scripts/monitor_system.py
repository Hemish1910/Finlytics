"""Script to monitor the trading system status."""
import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.logger import log
from src.utils.database_manager import db_manager
from src.models.database import AgentStatus, Trade, Position, PortfolioSnapshot
from sqlalchemy import select, func


async def monitor_agents():
    """Monitor agent status."""
    log.info("=" * 60)
    log.info("Agent Status")
    log.info("=" * 60)
    
    async with db_manager.get_session() as session:
        result = await session.execute(select(AgentStatus))
        agents = result.scalars().all()
        
        if not agents:
            log.info("No agents found in database")
            return
        
        for agent in agents:
            status_emoji = "✅" if agent.status == "running" else "❌"
            log.info(f"{status_emoji} {agent.agent_name}: {agent.status}")
            log.info(f"   Last Heartbeat: {agent.last_heartbeat}")
            log.info(f"   Events Processed: {agent.events_processed}")
            log.info(f"   Errors: {agent.errors_count}")


async def monitor_portfolio():
    """Monitor portfolio status."""
    log.info("\n" + "=" * 60)
    log.info("Portfolio Status")
    log.info("=" * 60)
    
    async with db_manager.get_session() as session:
        # Get latest portfolio snapshot
        result = await session.execute(
            select(PortfolioSnapshot)
            .order_by(PortfolioSnapshot.timestamp.desc())
            .limit(1)
        )
        snapshot = result.scalar_one_or_none()
        
        if snapshot:
            log.info(f"Total Value: ${snapshot.total_value:,.2f}")
            log.info(f"Cash: ${snapshot.cash:,.2f}")
            log.info(f"Positions Value: ${snapshot.positions_value:,.2f}")
            log.info(f"Total P&L: ${snapshot.total_pnl:,.2f}")
            log.info(f"Active Positions: {snapshot.num_positions}")
        else:
            log.info("No portfolio data available")


async def monitor_positions():
    """Monitor current positions."""
    log.info("\n" + "=" * 60)
    log.info("Current Positions")
    log.info("=" * 60)
    
    async with db_manager.get_session() as session:
        result = await session.execute(
            select(Position).where(Position.quantity > 0)
        )
        positions = result.scalars().all()
        
        if not positions:
            log.info("No open positions")
            return
        
        for pos in positions:
            pnl_emoji = "📈" if pos.unrealized_pnl > 0 else "📉"
            log.info(f"{pnl_emoji} {pos.symbol}:")
            log.info(f"   Quantity: {pos.quantity}")
            log.info(f"   Avg Entry: ${pos.avg_price:.2f}")
            log.info(f"   Current: ${pos.current_price:.2f}")
            log.info(f"   Unrealized P&L: ${pos.unrealized_pnl:.2f}")


async def monitor_trades():
    """Monitor recent trades."""
    log.info("\n" + "=" * 60)
    log.info("Recent Trades (Last 10)")
    log.info("=" * 60)
    
    async with db_manager.get_session() as session:
        result = await session.execute(
            select(Trade)
            .order_by(Trade.timestamp.desc())
            .limit(10)
        )
        trades = result.scalars().all()
        
        if not trades:
            log.info("No trades found")
            return
        
        for trade in trades:
            side_emoji = "🟢" if trade.side == "BUY" else "🔴"
            log.info(
                f"{side_emoji} {trade.timestamp.strftime('%Y-%m-%d %H:%M:%S')} | "
                f"{trade.symbol} | {trade.side} | "
                f"{trade.quantity} @ ${trade.price:.2f} | "
                f"Status: {trade.status}"
            )


async def monitor_performance():
    """Monitor trading performance metrics."""
    log.info("\n" + "=" * 60)
    log.info("Performance Metrics")
    log.info("=" * 60)
    
    async with db_manager.get_session() as session:
        # Count total trades
        result = await session.execute(
            select(func.count(Trade.id)).where(Trade.status == "filled")
        )
        total_trades = result.scalar()
        
        # Count by side
        result = await session.execute(
            select(func.count(Trade.id))
            .where(Trade.side == "BUY", Trade.status == "filled")
        )
        buy_trades = result.scalar()
        
        result = await session.execute(
            select(func.count(Trade.id))
            .where(Trade.side == "SELL", Trade.status == "filled")
        )
        sell_trades = result.scalar()
        
        log.info(f"Total Trades: {total_trades}")
        log.info(f"Buy Trades: {buy_trades}")
        log.info(f"Sell Trades: {sell_trades}")


async def main():
    """Main monitoring function."""
    log.info("=" * 60)
    log.info("Finlytics System Monitor")
    log.info(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.info("=" * 60)
    
    await db_manager.initialize()
    
    try:
        await monitor_agents()
        await monitor_portfolio()
        await monitor_positions()
        await monitor_trades()
        await monitor_performance()
    finally:
        await db_manager.close()
    
    log.info("\n" + "=" * 60)
    log.info("Monitoring Complete")
    log.info("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
