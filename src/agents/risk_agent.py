"""Risk Management Agent - Manages portfolio risk and position sizing."""
from typing import Dict
from src.agents.base_agent import BaseAgent
from src.core.events import Event, EventType
from src.core.config import settings
from src.core.logger import log


class RiskAgent(BaseAgent):
    """Agent responsible for risk management and position sizing."""
    
    def __init__(self, initial_capital: float = None):
        super().__init__("RiskAgent")
        self.capital = initial_capital or settings.default_capital
        self.positions: Dict[str, Dict] = {}
        self.max_position_size = settings.max_position_size
        self.max_portfolio_risk = settings.max_portfolio_risk
        
    async def initialize(self):
        """Initialize the risk agent."""
        log.info(f"Initializing Risk Agent with capital: ${self.capital:,.2f}")
    
    async def subscribe_to_events(self):
        """Subscribe to relevant events."""
        self.subscribe(EventType.BUY_SIGNAL)
        self.subscribe(EventType.SELL_SIGNAL)
        self.subscribe(EventType.ORDER_FILLED)
        self.subscribe(EventType.PORTFOLIO_UPDATE)
    
    async def handle_event(self, event: Event):
        """Handle incoming events."""
        if event.event_type in [EventType.BUY_SIGNAL, EventType.SELL_SIGNAL]:
            await self._evaluate_signal(event)
        elif event.event_type == EventType.ORDER_FILLED:
            await self._update_positions(event)
        elif event.event_type == EventType.PORTFOLIO_UPDATE:
            await self._check_portfolio_risk(event)
    
    async def _evaluate_signal(self, event: Event):
        """Evaluate trading signal for risk."""
        symbol = event.data.get("symbol")
        signal_type = event.data.get("signal_type")
        current_price = event.data.get("current_price")
        stop_loss = event.data.get("stop_loss")
        
        if not all([symbol, signal_type, current_price]):
            return
        
        # Calculate position size
        position_size = await self._calculate_position_size(
            symbol, current_price, stop_loss
        )
        
        if position_size == 0:
            log.warning(f"Risk check failed for {symbol} - position size is 0")
            await self.publish_event(
                EventType.RISK_ALERT,
                {
                    "symbol": symbol,
                    "reason": "Position size too small or risk too high",
                    "signal_type": signal_type
                }
            )
            return
        
        # Check if we can take this position
        if signal_type == "BUY":
            cost = position_size * current_price
            if cost > self.capital * self.max_position_size:
                log.warning(f"Position size exceeds limit for {symbol}")
                await self.publish_event(
                    EventType.POSITION_LIMIT,
                    {
                        "symbol": symbol,
                        "reason": "Position size exceeds maximum allowed",
                        "max_size": self.capital * self.max_position_size,
                        "requested_size": cost
                    }
                )
                return
        
        # Risk check passed - forward to execution
        log.info(f"Risk check passed for {symbol} {signal_type} - size: {position_size}")
    
    async def _calculate_position_size(
        self, symbol: str, price: float, stop_loss: float = None
    ) -> float:
        """Calculate appropriate position size based on risk."""
        try:
            # Use Kelly Criterion or fixed percentage
            max_risk_per_trade = self.capital * self.max_portfolio_risk
            
            if stop_loss and stop_loss > 0:
                # Calculate based on stop loss
                risk_per_share = abs(price - stop_loss)
                if risk_per_share > 0:
                    position_size = max_risk_per_trade / risk_per_share
                else:
                    position_size = 0
            else:
                # Use fixed percentage of capital
                position_value = self.capital * self.max_position_size
                position_size = position_value / price
            
            # Round to reasonable number
            position_size = round(position_size, 2)
            
            return max(0, position_size)
            
        except Exception as e:
            log.error(f"Error calculating position size for {symbol}: {e}")
            return 0
    
    async def _update_positions(self, event: Event):
        """Update position tracking after order fill."""
        symbol = event.data.get("symbol")
        side = event.data.get("side")
        quantity = event.data.get("quantity")
        price = event.data.get("price")
        
        if not all([symbol, side, quantity, price]):
            return
        
        if symbol not in self.positions:
            self.positions[symbol] = {
                "quantity": 0,
                "avg_price": 0,
                "realized_pnl": 0
            }
        
        position = self.positions[symbol]
        
        if side == "BUY":
            # Add to position
            total_cost = position["quantity"] * position["avg_price"] + quantity * price
            position["quantity"] += quantity
            position["avg_price"] = total_cost / position["quantity"] if position["quantity"] > 0 else 0
        elif side == "SELL":
            # Reduce position
            if position["quantity"] >= quantity:
                pnl = (price - position["avg_price"]) * quantity
                position["realized_pnl"] += pnl
                position["quantity"] -= quantity
                
                if position["quantity"] == 0:
                    position["avg_price"] = 0
        
        log.info(f"Updated position for {symbol}: {position}")
    
    async def _check_portfolio_risk(self, event: Event):
        """Check overall portfolio risk."""
        portfolio_value = event.data.get("total_value", self.capital)
        
        # Calculate total exposure
        total_exposure = sum(
            pos["quantity"] * pos["avg_price"]
            for pos in self.positions.values()
        )
        
        exposure_ratio = total_exposure / portfolio_value if portfolio_value > 0 else 0
        
        if exposure_ratio > 0.9:  # More than 90% exposed
            await self.publish_event(
                EventType.RISK_ALERT,
                {
                    "reason": "High portfolio exposure",
                    "exposure_ratio": exposure_ratio,
                    "total_exposure": total_exposure,
                    "portfolio_value": portfolio_value
                }
            )
    
    async def process(self):
        """Periodic risk checks."""
        # Calculate portfolio metrics
        if self.positions:
            total_positions = len([p for p in self.positions.values() if p["quantity"] > 0])
            log.debug(f"Active positions: {total_positions}")
        
        await self.send_heartbeat()
    
    async def cleanup(self):
        """Cleanup resources."""
        log.info(f"Cleaning up {self.name}")
    
    def get_interval(self) -> float:
        """Get the processing interval."""
        return settings.risk_check_interval
