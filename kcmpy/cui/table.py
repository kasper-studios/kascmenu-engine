"""Table and data display widgets."""
from ..core.component import Component, Rect
from ..core.renderer import Style
from ..events.event_system import Event, EventType
from typing import List, Any
import platform


class Table(Component):
    """Scrollable table with headers."""
    
    def __init__(self, rect: Rect, headers: List[str] = None):
        super().__init__(rect)
        self.headers = headers or []
        self.rows = []
        self.selected_row = 0
        self.scroll_offset = 0
        self.style_header = Style(fg='black', bg='bright_cyan', bold=True)
        self.style_row = Style(fg='white')
        self.style_selected = Style(fg='black', bg='bright_white', bold=True)
        self.style_border = Style(fg='bright_blue')
        self.is_windows = platform.system() == 'Windows'
        self.show_borders = True
        self.column_widths = []
    
    def add_row(self, row: List[Any]):
        """Add a row to the table."""
        self.rows.append([str(cell) for cell in row])
        self._calculate_widths()
    
    def clear_rows(self):
        """Clear all rows."""
        self.rows = []
        self.selected_row = 0
        self.scroll_offset = 0
    
    def _calculate_widths(self):
        """Calculate optimal column widths."""
        if not self.headers:
            return
        
        self.column_widths = [len(h) for h in self.headers]
        
        for row in self.rows:
            for i, cell in enumerate(row):
                if i < len(self.column_widths):
                    self.column_widths[i] = max(self.column_widths[i], len(cell))
    
    def handle_event(self, event: Event) -> bool:
        """Handle navigation."""
        if event.type != EventType.KEY_PRESS:
            return False
        
        key = event.data.get('key', '')
        
        if key == '\x1b[A':  # Up
            if self.selected_row > 0:
                self.selected_row -= 1
                if self.selected_row < self.scroll_offset:
                    self.scroll_offset = self.selected_row
            return True
        elif key == '\x1b[B':  # Down
            if self.selected_row < len(self.rows) - 1:
                self.selected_row += 1
                visible_rows = self.rect.height - 3 if self.show_borders else self.rect.height - 1
                if self.selected_row >= self.scroll_offset + visible_rows:
                    self.scroll_offset = self.selected_row - visible_rows + 1
            return True
        
        return False
    
    def render(self, renderer):
        """Render table."""
        if not self.visible or not self.headers:
            return
        
        y = self.rect.y
        
        # Border characters
        if self.is_windows:
            h_line, v_line, corner = '-', '|', '+'
        else:
            h_line, v_line, corner = '─', '│', '┼'
        
        # Top border
        if self.show_borders:
            renderer.move_cursor(self.rect.x, y)
            border = corner
            for width in self.column_widths:
                border += h_line * (width + 2) + corner
            renderer.buffer.append(renderer.style_text(border[:self.rect.width], self.style_border))
            renderer.buffer.append('\n')
            y += 1
        
        # Headers
        renderer.move_cursor(self.rect.x, y)
        header_line = v_line if self.show_borders else ''
        for i, header in enumerate(self.headers):
            if i < len(self.column_widths):
                header_line += f" {header.ljust(self.column_widths[i])} {v_line}"
        renderer.buffer.append(renderer.style_text(header_line[:self.rect.width], self.style_header))
        renderer.buffer.append('\n')
        y += 1
        
        # Header separator
        if self.show_borders:
            renderer.move_cursor(self.rect.x, y)
            border = corner
            for width in self.column_widths:
                border += h_line * (width + 2) + corner
            renderer.buffer.append(renderer.style_text(border[:self.rect.width], self.style_border))
            renderer.buffer.append('\n')
            y += 1
        
        # Rows
        visible_rows = self.rect.height - y + self.rect.y
        for i in range(self.scroll_offset, min(self.scroll_offset + visible_rows, len(self.rows))):
            renderer.move_cursor(self.rect.x, y)
            
            row = self.rows[i]
            row_line = v_line if self.show_borders else ''
            
            for j, cell in enumerate(row):
                if j < len(self.column_widths):
                    row_line += f" {cell.ljust(self.column_widths[j])} {v_line}"
            
            style = self.style_selected if i == self.selected_row else self.style_row
            renderer.buffer.append(renderer.style_text(row_line[:self.rect.width], style))
            renderer.buffer.append('\n')
            y += 1


class Chart(Component):
    """Simple ASCII bar chart."""
    
    def __init__(self, rect: Rect, title: str = ""):
        super().__init__(rect)
        self.title = title
        self.data = []  # List of (label, value) tuples
        self.max_value = 100
        self.style_title = Style(fg='bright_yellow', bold=True)
        self.style_label = Style(fg='white')
        self.style_bar = Style(fg='bright_green', bold=True)
        self.is_windows = platform.system() == 'Windows'
    
    def set_data(self, data: List[tuple]):
        """Set chart data as list of (label, value) tuples."""
        self.data = data
        if data:
            self.max_value = max(v for _, v in data)
    
    def add_data(self, label: str, value: float):
        """Add a data point."""
        self.data.append((label, value))
        self.max_value = max(self.max_value, value)
    
    def render(self, renderer):
        """Render bar chart."""
        if not self.visible:
            return
        
        y = self.rect.y
        
        # Title
        if self.title:
            renderer.move_cursor(self.rect.x, y)
            renderer.buffer.append(renderer.style_text(self.title, self.style_title))
            renderer.buffer.append('\n')
            y += 1
        
        # Calculate bar width
        label_width = max(len(label) for label, _ in self.data) if self.data else 10
        bar_width = self.rect.width - label_width - 10
        
        # Bars
        for label, value in self.data[:self.rect.height - (2 if self.title else 1)]:
            renderer.move_cursor(self.rect.x, y)
            
            # Label
            label_text = label.ljust(label_width)
            renderer.buffer.append(renderer.style_text(label_text, self.style_label))
            renderer.buffer.append(' ')
            
            # Bar
            bar_length = int((value / self.max_value) * bar_width) if self.max_value > 0 else 0
            bar_char = '#' if self.is_windows else '█'
            bar = bar_char * bar_length
            renderer.buffer.append(renderer.style_text(bar, self.style_bar))
            
            # Value
            value_text = f" {value:.1f}"
            renderer.buffer.append(renderer.style_text(value_text, self.style_label))
            renderer.buffer.append('\n')
            y += 1


class TreeView(Component):
    """Hierarchical tree view."""
    
    def __init__(self, rect: Rect):
        super().__init__(rect)
        self.root_nodes = []  # List of TreeNode objects
        self.selected_index = 0
        self.style_normal = Style(fg='white')
        self.style_selected = Style(fg='black', bg='bright_white', bold=True)
        self.style_icon = Style(fg='bright_cyan')
        self.is_windows = platform.system() == 'Windows'
    
    def add_node(self, node):
        """Add root node."""
        self.root_nodes.append(node)
    
    def handle_event(self, event: Event) -> bool:
        """Handle navigation and expand/collapse."""
        if event.type != EventType.KEY_PRESS:
            return False
        
        key = event.data.get('key', '')
        flat_list = self._flatten_tree()
        
        if key == '\x1b[A':  # Up
            if self.selected_index > 0:
                self.selected_index -= 1
            return True
        elif key == '\x1b[B':  # Down
            if self.selected_index < len(flat_list) - 1:
                self.selected_index += 1
            return True
        elif key == '\x1b[C' or key == ' ':  # Right or Space - expand
            if self.selected_index < len(flat_list):
                node, _ = flat_list[self.selected_index]
                node.expanded = not node.expanded
            return True
        
        return False
    
    def _flatten_tree(self, nodes=None, level=0):
        """Flatten tree for rendering."""
        if nodes is None:
            nodes = self.root_nodes
        
        result = []
        for node in nodes:
            result.append((node, level))
            if node.expanded and node.children:
                result.extend(self._flatten_tree(node.children, level + 1))
        return result
    
    def render(self, renderer):
        """Render tree view."""
        if not self.visible:
            return
        
        flat_list = self._flatten_tree()
        y = self.rect.y
        
        for i, (node, level) in enumerate(flat_list[:self.rect.height]):
            renderer.move_cursor(self.rect.x, y)
            
            # Indentation
            indent = '  ' * level
            
            # Expand/collapse icon
            if node.children:
                if self.is_windows:
                    icon = '[-]' if node.expanded else '[+]'
                else:
                    icon = '▼' if node.expanded else '▶'
            else:
                icon = ' ' if self.is_windows else '•'
            
            icon_text = renderer.style_text(icon, self.style_icon)
            
            # Node label
            line = f"{indent}{icon_text} {node.label}"
            style = self.style_selected if i == self.selected_index else self.style_normal
            
            renderer.buffer.append(renderer.style_text(line[:self.rect.width], style))
            renderer.buffer.append('\n')
            y += 1


class TreeNode:
    """Node for TreeView."""
    
    def __init__(self, label: str):
        self.label = label
        self.children = []
        self.expanded = False
    
    def add_child(self, child):
        """Add child node."""
        self.children.append(child)
        return child
