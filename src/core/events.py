"""Event system for agent communication."""
from enum import Enum
from typing import Any, Dict, Optional
from datetime import datetime
from pydantic import BaseModel, Field
import uuid


class EventType(str, Enum):
    """Types of events in the trading system."""
    
    # Market data events
    MARKET_DATA_UPDATE = "market_data_update"
    PRICE_UPDATE = "price_update"
    ORDERBOOK_UPDATE = "orderbook_update"
    
    # Analysis events
    TECHNICAL_ANALYSIS = "technical_analysis"
    FUNDAMENTAL_ANALYSIS = "fundamental_analysis"
    SENTIMENT_ANALYSIS = "sentiment_analysis"
    
    # Signal events
    BUY_SIGNAL = "buy_signal"
    SELL_SIGNAL = "sell_signal"
    HOLD_SIGNAL = "hold_signal"
    
    # Risk events
    RISK_ALERT = "risk_alert"
    POSITION_LIMIT = "position_limit"
    STOP_LOSS_TRIGGER = "stop_loss_trigger"
    
    # Execution events
    ORDER_PLACED = "order_placed"
    ORDER_FILLED = "order_filled"
    ORDER_CANCELLED = "order_cancelled"
    ORDER_REJECTED = "order_rejected"
    
    # Portfolio events
    PORTFOLIO_UPDATE = "portfolio_update"
    REBALANCE_REQUIRED = "rebalance_required"
    
    # System events
    AGENT_STARTED = "agent_started"
    AGENT_STOPPED = "agent_stopped"
    ERROR_OCCURRED = "error_occurred"
    HEARTBEAT = "heartbeat"


class Event(BaseModel):
    """Base event class for all system events."""
    
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: EventType
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    source_agent: str
    data: Dict[str, Any] = Field(default_factory=dict)
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary."""
        return self.model_dump()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Event":
        """Create event from dictionary."""
        return cls(**data)


class MarketDataEvent(Event):
    """Market data specific event."""
    event_type: EventType = EventType.MARKET_DATA_UPDATE


class SignalEvent(Event):
    """Trading signal event."""
    pass


class OrderEvent(Event):
    """Order execution event."""
    pass


class RiskEvent(Event):
    """Risk management event."""
    pass
