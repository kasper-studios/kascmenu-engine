"""Event system for handling user input and custom events."""
from enum import Enum
from typing import Callable, Dict, List
from dataclasses import dataclass


class EventType(Enum):
    """Event types supported by the framework."""
    KEY_PRESS = "key_press"
    MOUSE_CLICK = "mouse_click"
    MOUSE_MOVE = "mouse_move"
    RESIZE = "resize"
    CUSTOM = "custom"


@dataclass
class Event:
    """Base event class."""
    type: EventType
    data: dict = None


class EventBus:
    """Central event bus for pub/sub pattern."""
    
    def __init__(self):
        self.listeners: Dict[EventType, List[Callable]] = {}
    
    def subscribe(self, event_type: EventType, callback: Callable):
        """Subscribe to event type."""
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)
    
    def unsubscribe(self, event_type: EventType, callback: Callable):
        """Unsubscribe from event type."""
        if event_type in self.listeners:
            self.listeners[event_type].remove(callback)
    
    def emit(self, event: Event):
        """Emit event to all subscribers."""
        if event.type in self.listeners:
            for callback in self.listeners[event.type]:
                callback(event)
