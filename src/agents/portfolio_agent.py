"""Portfolio Agent - Tracks and manages portfolio state."""
from typing import Dict
from datetime import datetime
from src.agents.base_agent import BaseAgent
from src.core.events import Event, EventType
from src.core.config import settings
from src.core.logger import log


class PortfolioAgent(BaseAgent):
    """Agent responsible for portfolio tracking and management."""
    
    def __init__(self, initial_capital: float = None):
        super().__init__("PortfolioAgent")
        self.initial_capital = initial_capital or settings.default_capital
        self.cash = self.initial_capital
        self.positions: Dict[str, Dict] = {}
        self.total_value = self.initial_capital
        self.daily_pnl = 0.0
        self.total_pnl = 0.0
        
    async def initialize(self):
        """Initialize the portfolio agent."""
        log.info(f"Initializing Portfolio Agent with capital: ${self.initial_capital:,.2f}")
    
    async def subscribe_to_events(self):
        """Subscribe to relevant events."""
        self.subscribe(EventType.ORDER_FILLED)
        self.subscribe(EventType.PRICE_UPDATE)
    
    async def handle_event(self, event: Event):
        """Handle incoming events."""
        if event.event_type == EventType.ORDER_FILLED:
            await self._update_portfolio(event)
        elif event.event_type == EventType.PRICE_UPDATE:
            await self._update_positions_value(event)
    
    async def _update_portfolio(self, event: Event):
        """Update portfolio after order fill."""
        symbol = event.data.get("symbol")
        side = event.data.get("side")
        quantity = event.data.get("quantity")
        price = event.data.get("price")
        
        if not all([symbol, side, quantity, price]):
            return
        
        # Initialize position if needed
        if symbol not in self.positions:
            self.positions[symbol] = {
                "quantity": 0,
                "avg_price": 0,
                "current_price": price,
                "market_value": 0,
                "unrealized_pnl": 0,
                "realized_pnl": 0
            }
        
        position = self.positions[symbol]
        
        if side == "BUY":
            # Update cash
            cost = quantity * price
            self.cash -= cost
            
            # Update position
            total_cost = position["quantity"] * position["avg_price"] + cost
            position["quantity"] += quantity
            position["avg_price"] = total_cost / position["quantity"]
            position["current_price"] = price
            
            log.info(f"Bought {quantity} {symbol} @ ${price:.2f} - Cash: ${self.cash:.2f}")
            
        elif side == "SELL":
            # Update cash
            proceeds = quantity * price
            self.cash += proceeds
            
            # Calculate realized P&L
            if position["quantity"] >= quantity:
                cost_basis = position["avg_price"] * quantity
                realized_pnl = proceeds - cost_basis
                position["realized_pnl"] += realized_pnl
                self.total_pnl += realized_pnl
                
                # Update position
                position["quantity"] -= quantity
                position["current_price"] = price
                
                if position["quantity"] == 0:
                    position["avg_price"] = 0
                
                log.info(f"Sold {quantity} {symbol} @ ${price:.2f} - P&L: ${realized_pnl:.2f} - Cash: ${self.cash:.2f}")
        
        # Update position market value
        position["market_value"] = position["quantity"] * position["current_price"]
        position["unrealized_pnl"] = (position["current_price"] - position["avg_price"]) * position["quantity"]
        
        # Calculate total portfolio value
        await self._calculate_portfolio_value()
        
        # Publish portfolio update
        await self._publish_portfolio_update()
    
    async def _update_positions_value(self, event: Event):
        """Update position values based on current prices."""
        symbol = event.data.get("symbol")
        price = event.data.get("price")
        
        if not symbol or not price:
            return
        
        if symbol in self.positions:
            position = self.positions[symbol]
            position["current_price"] = price
            position["market_value"] = position["quantity"] * price
            
            if position["quantity"] > 0:
                position["unrealized_pnl"] = (price - position["avg_price"]) * position["quantity"]
        
        # Recalculate portfolio value
        await self._calculate_portfolio_value()
    
    async def _calculate_portfolio_value(self):
        """Calculate total portfolio value."""
        positions_value = sum(
            pos["market_value"]
            for pos in self.positions.values()
        )
        
        self.total_value = self.cash + positions_value
        self.total_pnl = self.total_value - self.initial_capital
    
    async def _publish_portfolio_update(self):
        """Publish portfolio update event."""
        active_positions = {
            symbol: pos
            for symbol, pos in self.positions.items()
            if pos["quantity"] > 0
        }
        
        await self.publish_event(
            EventType.PORTFOLIO_UPDATE,
            {
                "total_value": self.total_value,
                "cash": self.cash,
                "positions_value": sum(pos["market_value"] for pos in active_positions.values()),
                "total_pnl": self.total_pnl,
                "daily_pnl": self.daily_pnl,
                "num_positions": len(active_positions),
                "positions": active_positions
            }
        )
    
    def get_portfolio_summary(self) -> Dict:
        """Get portfolio summary."""
        active_positions = {
            symbol: pos
            for symbol, pos in self.positions.items()
            if pos["quantity"] > 0
        }
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "total_value": self.total_value,
            "cash": self.cash,
            "initial_capital": self.initial_capital,
            "total_pnl": self.total_pnl,
            "total_pnl_pct": (self.total_pnl / self.initial_capital * 100) if self.initial_capital > 0 else 0,
            "num_positions": len(active_positions),
            "positions": active_positions
        }
    
    async def process(self):
        """Periodic processing."""
        # Publish portfolio update periodically
        await self._publish_portfolio_update()
        
        # Log portfolio summary
        summary = self.get_portfolio_summary()
        log.info(
            f"Portfolio: ${summary['total_value']:,.2f} | "
            f"P&L: ${summary['total_pnl']:,.2f} ({summary['total_pnl_pct']:.2f}%) | "
            f"Positions: {summary['num_positions']}"
        )
        
        await self.send_heartbeat()
    
    async def cleanup(self):
        """Cleanup resources."""
        log.info(f"Cleaning up {self.name}")
        summary = self.get_portfolio_summary()
        log.info(f"Final Portfolio Summary: {summary}")
    
    def get_interval(self) -> float:
        """Get the processing interval."""
        return 10.0
