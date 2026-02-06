"""Message bus for inter-agent communication."""
import asyncio
from typing import Callable, Dict, List, Set
from collections import defaultdict
from src.core.events import Event, EventType
from src.core.logger import log


class MessageBus:
    """Pub/Sub message bus for agent communication."""
    
    def __init__(self):
        self._subscribers: Dict[EventType, Set[Callable]] = defaultdict(set)
        self._event_queue: asyncio.Queue = asyncio.Queue()
        self._running = False
        self._processor_task = None
        
    async def start(self):
        """Start the message bus processor."""
        if self._running:
            return
        
        self._running = True
        self._processor_task = asyncio.create_task(self._process_events())
        log.info("Message bus started")
    
    async def stop(self):
        """Stop the message bus processor."""
        self._running = False
        if self._processor_task:
            self._processor_task.cancel()
            try:
                await self._processor_task
            except asyncio.CancelledError:
                pass
        log.info("Message bus stopped")
    
    def subscribe(self, event_type: EventType, callback: Callable):
        """Subscribe to an event type."""
        self._subscribers[event_type].add(callback)
        log.debug(f"Subscribed to {event_type}: {callback.__name__}")
    
    def unsubscribe(self, event_type: EventType, callback: Callable):
        """Unsubscribe from an event type."""
        self._subscribers[event_type].discard(callback)
        log.debug(f"Unsubscribed from {event_type}: {callback.__name__}")
    
    async def publish(self, event: Event):
        """Publish an event to the bus."""
        await self._event_queue.put(event)
        log.debug(f"Published event: {event.event_type} from {event.source_agent}")
    
    async def _process_events(self):
        """Process events from the queue."""
        while self._running:
            try:
                event = await asyncio.wait_for(
                    self._event_queue.get(),
                    timeout=1.0
                )
                await self._dispatch_event(event)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                log.error(f"Error processing event: {e}")
    
    async def _dispatch_event(self, event: Event):
        """Dispatch event to all subscribers."""
        subscribers = self._subscribers.get(event.event_type, set())
        
        if not subscribers:
            log.debug(f"No subscribers for event type: {event.event_type}")
            return
        
        tasks = []
        for callback in subscribers:
            try:
                if asyncio.iscoroutinefunction(callback):
                    tasks.append(callback(event))
                else:
                    callback(event)
            except Exception as e:
                log.error(f"Error in subscriber {callback.__name__}: {e}")
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)


# Global message bus instance
message_bus = MessageBus()
