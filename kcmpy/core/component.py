"""Base component system for CUI framework."""
from typing import Optional, List
from dataclasses import dataclass


@dataclass
class Rect:
    """Rectangle bounds for component positioning."""
    x: int
    y: int
    width: int
    height: int


class Component:
    """Base class for all UI components."""
    
    def __init__(self, rect: Rect):
        self.rect = rect
        self.children: List[Component] = []
        self.parent: Optional[Component] = None
        self.visible = True
        self.focused = False
    
    def add_child(self, child: 'Component'):
        """Add child component."""
        child.parent = self
        self.children.append(child)
    
    def remove_child(self, child: 'Component'):
        """Remove child component."""
        if child in self.children:
            child.parent = None
            self.children.remove(child)
    
    def render(self, renderer):
        """Render component to screen. Override in subclasses."""
        # Default implementation: render all children
        for child in self.children:
            child.render(renderer)
    
    def update(self, delta_time: float):
        """Update component state."""
        for child in self.children:
            child.update(delta_time)
    
    def handle_event(self, event):
        """Handle input events."""
        for child in self.children:
            if child.handle_event(event):
                return True
        return False
