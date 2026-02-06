"""Base agent class for all trading agents."""
import asyncio
from abc import ABC, abstractmethod
from typing import Optional, Set
from datetime import datetime
from src.core.events import Event, EventType
from src.core.message_bus import message_bus
from src.core.logger import log


class BaseAgent(ABC):
    """Abstract base class for all agents in the trading system."""
    
    def __init__(self, name: str):
        self.name = name
        self.running = False
        self._task: Optional[asyncio.Task] = None
        self._subscribed_events: Set[EventType] = set()
        
    async def start(self):
        """Start the agent."""
        if self.running:
            log.warning(f"Agent {self.name} is already running")
            return
        
        self.running = True
        log.info(f"Starting agent: {self.name}")
        
        # Subscribe to events
        await self.subscribe_to_events()
        
        # Publish agent started event
        await self.publish_event(
            EventType.AGENT_STARTED,
            {"agent_name": self.name}
        )
        
        # Start the main loop
        self._task = asyncio.create_task(self._run())
        
    async def stop(self):
        """Stop the agent."""
        if not self.running:
            return
        
        self.running = False
        log.info(f"Stopping agent: {self.name}")
        
        # Cancel the main task
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        
        # Unsubscribe from events
        await self.unsubscribe_from_events()
        
        # Publish agent stopped event
        await self.publish_event(
            EventType.AGENT_STOPPED,
            {"agent_name": self.name}
        )
    
    async def _run(self):
        """Main agent loop."""
        try:
            await self.initialize()
            
            while self.running:
                try:
                    await self.process()
                    await asyncio.sleep(self.get_interval())
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    log.error(f"Error in {self.name} process loop: {e}")
                    await self.handle_error(e)
                    await asyncio.sleep(5)  # Wait before retrying
        except Exception as e:
            log.error(f"Fatal error in {self.name}: {e}")
            await self.publish_event(
                EventType.ERROR_OCCURRED,
                {"agent_name": self.name, "error": str(e)}
            )
        finally:
            await self.cleanup()
    
    @abstractmethod
    async def initialize(self):
        """Initialize the agent. Override in subclasses."""
        pass
    
    @abstractmethod
    async def process(self):
        """Main processing logic. Override in subclasses."""
        pass
    
    @abstractmethod
    async def cleanup(self):
        """Cleanup resources. Override in subclasses."""
        pass
    
    @abstractmethod
    def get_interval(self) -> float:
        """Get the processing interval in seconds. Override in subclasses."""
        return 1.0
    
    async def subscribe_to_events(self):
        """Subscribe to relevant events. Override in subclasses."""
        pass
    
    async def unsubscribe_from_events(self):
        """Unsubscribe from events."""
        for event_type in self._subscribed_events:
            message_bus.unsubscribe(event_type, self.handle_event)
        self._subscribed_events.clear()
    
    def subscribe(self, event_type: EventType):
        """Subscribe to a specific event type."""
        message_bus.subscribe(event_type, self.handle_event)
        self._subscribed_events.add(event_type)
        log.debug(f"{self.name} subscribed to {event_type}")
    
    async def handle_event(self, event: Event):
        """Handle incoming events. Override in subclasses for custom handling."""
        log.debug(f"{self.name} received event: {event.event_type}")
    
    async def publish_event(self, event_type: EventType, data: dict, metadata: dict = None):
        """Publish an event to the message bus."""
        event = Event(
            event_type=event_type,
            source_agent=self.name,
            data=data,
            metadata=metadata or {}
        )
        await message_bus.publish(event)
    
    async def handle_error(self, error: Exception):
        """Handle errors. Can be overridden in subclasses."""
        log.error(f"Error in {self.name}: {error}")
        await self.publish_event(
            EventType.ERROR_OCCURRED,
            {
                "agent_name": self.name,
                "error": str(error),
                "error_type": type(error).__name__
            }
        )
    
    async def send_heartbeat(self):
        """Send heartbeat event."""
        await self.publish_event(
            EventType.HEARTBEAT,
            {
                "agent_name": self.name,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    
    def __repr__(self):
        return f"<{self.__class__.__name__} name={self.name} running={self.running}>"
