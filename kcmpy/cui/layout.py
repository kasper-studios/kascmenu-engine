"""Layout managers for automatic widget positioning."""
from ..core.component import Component, Rect
from typing import List


class VBox(Component):
    """Vertical box layout - stacks widgets vertically."""
    
    def __init__(self, rect: Rect, spacing: int = 1):
        super().__init__(rect)
        self.spacing = spacing
        self.items: List[Component] = []
    
    def add(self, widget: Component, height: int = None):
        """Add widget to layout."""
        self.items.append((widget, height))
        self.add_child(widget)
        self._relayout()
    
    def _relayout(self):
        """Recalculate positions of all widgets."""
        if not self.items:
            return
        
        # Calculate total fixed height and count flexible items
        total_fixed = 0
        flexible_count = 0
        
        for widget, height in self.items:
            if height is not None:
                total_fixed += height
            else:
                flexible_count += 1
        
        # Calculate spacing
        total_spacing = self.spacing * (len(self.items) - 1)
        available_height = self.rect.height - total_fixed - total_spacing
        flexible_height = available_height // flexible_count if flexible_count > 0 else 0
        
        # Position widgets
        current_y = self.rect.y
        
        for widget, height in self.items:
            widget_height = height if height is not None else flexible_height
            widget.rect = Rect(
                self.rect.x,
                current_y,
                self.rect.width,
                widget_height
            )
            current_y += widget_height + self.spacing
    
    def render(self, renderer):
        """Render all children."""
        if not self.visible:
            return
        
        for child in self.children:
            child.render(renderer)


class HBox(Component):
    """Horizontal box layout - stacks widgets horizontally."""
    
    def __init__(self, rect: Rect, spacing: int = 2):
        super().__init__(rect)
        self.spacing = spacing
        self.items: List[Component] = []
    
    def add(self, widget: Component, width: int = None):
        """Add widget to layout."""
        self.items.append((widget, width))
        self.add_child(widget)
        self._relayout()
    
    def _relayout(self):
        """Recalculate positions of all widgets."""
        if not self.items:
            return
        
        # Calculate total fixed width and count flexible items
        total_fixed = 0
        flexible_count = 0
        
        for widget, width in self.items:
            if width is not None:
                total_fixed += width
            else:
                flexible_count += 1
        
        # Calculate spacing
        total_spacing = self.spacing * (len(self.items) - 1)
        available_width = self.rect.width - total_fixed - total_spacing
        flexible_width = available_width // flexible_count if flexible_count > 0 else 0
        
        # Position widgets
        current_x = self.rect.x
        
        for widget, width in self.items:
            widget_width = width if width is not None else flexible_width
            widget.rect = Rect(
                current_x,
                self.rect.y,
                widget_width,
                self.rect.height
            )
            current_x += widget_width + self.spacing
    
    def render(self, renderer):
        """Render all children."""
        if not self.visible:
            return
        
        for child in self.children:
            child.render(renderer)


class Grid(Component):
    """Grid layout - arranges widgets in rows and columns."""
    
    def __init__(self, rect: Rect, rows: int, cols: int, spacing: int = 1):
        super().__init__(rect)
        self.rows = rows
        self.cols = cols
        self.spacing = spacing
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
    
    def add(self, widget: Component, row: int, col: int, rowspan: int = 1, colspan: int = 1):
        """Add widget to grid at specified position."""
        if row >= self.rows or col >= self.cols:
            raise ValueError(f"Position ({row}, {col}) out of bounds")
        
        self.grid[row][col] = (widget, rowspan, colspan)
        self.add_child(widget)
        self._relayout()
    
    def _relayout(self):
        """Recalculate positions of all widgets."""
        # Calculate cell dimensions
        total_spacing_h = self.spacing * (self.cols - 1)
        total_spacing_v = self.spacing * (self.rows - 1)
        
        cell_width = (self.rect.width - total_spacing_h) // self.cols
        cell_height = (self.rect.height - total_spacing_v) // self.rows
        
        # Position widgets
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.grid[row][col]
                if cell is None:
                    continue
                
                widget, rowspan, colspan = cell
                
                x = self.rect.x + col * (cell_width + self.spacing)
                y = self.rect.y + row * (cell_height + self.spacing)
                w = cell_width * colspan + self.spacing * (colspan - 1)
                h = cell_height * rowspan + self.spacing * (rowspan - 1)
                
                widget.rect = Rect(x, y, w, h)
    
    def render(self, renderer):
        """Render all children."""
        if not self.visible:
            return
        
        for child in self.children:
            child.render(renderer)


class Stack(Component):
    """Stack layout - overlays widgets on top of each other."""
    
    def __init__(self, rect: Rect):
        super().__init__(rect)
        self.layers: List[Component] = []
    
    def add(self, widget: Component, z_index: int = 0):
        """Add widget to stack with z-index."""
        self.layers.append((widget, z_index))
        self.layers.sort(key=lambda x: x[1])  # Sort by z-index
        self.add_child(widget)
        
        # All widgets occupy full rect
        widget.rect = Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
    
    def render(self, renderer):
        """Render all layers in order."""
        if not self.visible:
            return
        
        for widget, _ in self.layers:
            if widget.visible:
                widget.render(renderer)


class Anchor(Component):
    """Anchor layout - positions widget relative to edges."""
    
    def __init__(self, rect: Rect):
        super().__init__(rect)
        self.anchored_widgets = []
    
    def add(self, widget: Component, anchor: str, offset_x: int = 0, offset_y: int = 0):
        """Add widget with anchor position.
        
        Anchors: 'top-left', 'top-center', 'top-right',
                 'center-left', 'center', 'center-right',
                 'bottom-left', 'bottom-center', 'bottom-right'
        """
        self.anchored_widgets.append((widget, anchor, offset_x, offset_y))
        self.add_child(widget)
        self._position_widget(widget, anchor, offset_x, offset_y)
    
    def _position_widget(self, widget: Component, anchor: str, offset_x: int, offset_y: int):
        """Calculate widget position based on anchor."""
        parts = anchor.split('-')
        v_align = parts[0]  # top, center, bottom
        h_align = parts[1] if len(parts) > 1 else 'center'  # left, center, right
        
        # Vertical position
        if v_align == 'top':
            y = self.rect.y + offset_y
        elif v_align == 'center':
            y = self.rect.y + (self.rect.height - widget.rect.height) // 2 + offset_y
        else:  # bottom
            y = self.rect.y + self.rect.height - widget.rect.height + offset_y
        
        # Horizontal position
        if h_align == 'left':
            x = self.rect.x + offset_x
        elif h_align == 'center':
            x = self.rect.x + (self.rect.width - widget.rect.width) // 2 + offset_x
        else:  # right
            x = self.rect.x + self.rect.width - widget.rect.width + offset_x
        
        widget.rect.x = x
        widget.rect.y = y
    
    def render(self, renderer):
        """Render all anchored widgets."""
        if not self.visible:
            return
        
        for child in self.children:
            child.render(renderer)
