"""Execution Agent - Handles order placement and management."""
import uuid
from datetime import datetime
from typing import Dict
from src.agents.base_agent import BaseAgent
from src.core.events import Event, EventType
from src.core.config import settings
from src.core.logger import log


class ExecutionAgent(BaseAgent):
    """Agent responsible for order execution."""
    
    def __init__(self):
        super().__init__("ExecutionAgent")
        self.pending_orders: Dict[str, Dict] = {}
        self.filled_orders: Dict[str, Dict] = {}
        self.paper_trading = settings.trading_mode == "paper"
        
    async def initialize(self):
        """Initialize the execution agent."""
        mode = "PAPER TRADING" if self.paper_trading else "LIVE TRADING"
        log.info(f"Initializing Execution Agent - Mode: {mode}")
    
    async def subscribe_to_events(self):
        """Subscribe to signal events."""
        self.subscribe(EventType.BUY_SIGNAL)
        self.subscribe(EventType.SELL_SIGNAL)
    
    async def handle_event(self, event: Event):
        """Handle incoming signal events."""
        if event.event_type in [EventType.BUY_SIGNAL, EventType.SELL_SIGNAL]:
            await self._execute_signal(event)
    
    async def _execute_signal(self, event: Event):
        """Execute a trading signal."""
        symbol = event.data.get("symbol")
        signal_type = event.data.get("signal_type")
        current_price = event.data.get("current_price")
        strength = event.data.get("strength", 0)
        
        if not all([symbol, signal_type, current_price]):
            return
        
        # Only execute strong signals
        if strength < 0.6:
            log.debug(f"Signal strength too low for {symbol}: {strength}")
            return
        
        # Create order
        order = await self._create_order(
            symbol=symbol,
            side=signal_type,
            price=current_price,
            quantity=self._calculate_quantity(current_price),
            stop_loss=event.data.get("stop_loss"),
            target_price=event.data.get("target_price")
        )
        
        if order:
            await self._place_order(order)
    
    def _calculate_quantity(self, price: float) -> float:
        """Calculate order quantity (simplified)."""
        # In real implementation, this would come from risk agent
        # For now, use a simple fixed amount
        order_value = 1000  # $1000 per trade
        quantity = order_value / price
        return round(quantity, 2)
    
    async def _create_order(
        self,
        symbol: str,
        side: str,
        price: float,
        quantity: float,
        stop_loss: float = None,
        target_price: float = None
    ) -> Dict:
        """Create an order object."""
        order_id = str(uuid.uuid4())
        
        order = {
            "order_id": order_id,
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            "price": price,
            "stop_loss": stop_loss,
            "target_price": target_price,
            "status": "pending",
            "created_at": datetime.utcnow().isoformat(),
            "filled_at": None
        }
        
        return order
    
    async def _place_order(self, order: Dict):
        """Place an order (paper or live)."""
        order_id = order["order_id"]
        symbol = order["symbol"]
        
        self.pending_orders[order_id] = order
        
        # Publish order placed event
        await self.publish_event(
            EventType.ORDER_PLACED,
            order
        )
        
        log.info(f"Order placed: {order['side']} {order['quantity']} {symbol} @ ${order['price']}")
        
        if self.paper_trading:
            # Simulate immediate fill for paper trading
            await self._simulate_fill(order)
        else:
            # In live trading, this would connect to broker API
            log.warning("Live trading not implemented - use paper trading mode")
    
    async def _simulate_fill(self, order: Dict):
        """Simulate order fill for paper trading."""
        order_id = order["order_id"]
        
        # Simulate small slippage
        slippage = 0.001  # 0.1%
        fill_price = order["price"] * (1 + slippage if order["side"] == "BUY" else 1 - slippage)
        
        # Update order
        order["status"] = "filled"
        order["filled_at"] = datetime.utcnow().isoformat()
        order["fill_price"] = fill_price
        
        # Move to filled orders
        self.filled_orders[order_id] = order
        if order_id in self.pending_orders:
            del self.pending_orders[order_id]
        
        # Publish order filled event
        await self.publish_event(
            EventType.ORDER_FILLED,
            {
                "order_id": order_id,
                "symbol": order["symbol"],
                "side": order["side"],
                "quantity": order["quantity"],
                "price": fill_price,
                "original_price": order["price"],
                "filled_at": order["filled_at"]
            }
        )
        
        log.info(f"Order filled: {order['side']} {order['quantity']} {order['symbol']} @ ${fill_price:.2f}")
    
    async def cancel_order(self, order_id: str):
        """Cancel a pending order."""
        if order_id not in self.pending_orders:
            log.warning(f"Order {order_id} not found in pending orders")
            return
        
        order = self.pending_orders[order_id]
        order["status"] = "cancelled"
        
        del self.pending_orders[order_id]
        
        await self.publish_event(
            EventType.ORDER_CANCELLED,
            {
                "order_id": order_id,
                "symbol": order["symbol"]
            }
        )
        
        log.info(f"Order cancelled: {order_id}")
    
    async def process(self):
        """Periodic processing."""
        # Check for stale orders
        if self.pending_orders:
            log.debug(f"Pending orders: {len(self.pending_orders)}")
        
        await self.send_heartbeat()
    
    async def cleanup(self):
        """Cleanup resources."""
        log.info(f"Cleaning up {self.name}")
        # Cancel all pending orders
        for order_id in list(self.pending_orders.keys()):
            await self.cancel_order(order_id)
    
    def get_interval(self) -> float:
        """Get the processing interval."""
        return 5.0
