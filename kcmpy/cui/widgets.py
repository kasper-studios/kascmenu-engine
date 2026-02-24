"""Common UI widgets for CUI framework."""
from ..core.component import Component, Rect
from ..core.renderer import Style


class Box(Component):
    """Simple box widget with border."""
    
    BORDERS = {
        'single': ('┌', '┐', '└', '┘', '─', '│'),
        'double': ('╔', '╗', '╚', '╝', '═', '║'),
        'rounded': ('╭', '╮', '╰', '╯', '─', '│'),
    }
    
    def __init__(self, rect: Rect, title: str = "", border_style: str = 'single'):
        super().__init__(rect)
        self.title = title
        self.border_style = border_style
        self.style = Style(fg='white')
    
    def render(self, renderer):
        if not self.visible:
            return
        
        tl, tr, bl, br, h, v = self.BORDERS[self.border_style]
        
        # Top border
        renderer.move_cursor(self.rect.x, self.rect.y)
        top = tl + h * (self.rect.width - 2) + tr
        if self.title:
            title_text = f" {self.title} "
            pos = (self.rect.width - len(title_text)) // 2
            top = top[:pos] + title_text + top[pos + len(title_text):]
        renderer.buffer.append(renderer.style_text(top, self.style))
        
        # Sides
        for i in range(1, self.rect.height - 1):
            renderer.move_cursor(self.rect.x, self.rect.y + i)
            renderer.buffer.append(renderer.style_text(v + ' ' * (self.rect.width - 2) + v, self.style))
        
        # Bottom border
        renderer.move_cursor(self.rect.x, self.rect.y + self.rect.height - 1)
        renderer.buffer.append(renderer.style_text(bl + h * (self.rect.width - 2) + br, self.style))
        
        # Render children
        for child in self.children:
            child.render(renderer)


class Text(Component):
    """Text display widget."""
    
    def __init__(self, rect: Rect, text: str = ""):
        super().__init__(rect)
        self.text = text
        self.style = Style()
    
    def render(self, renderer):
        if not self.visible:
            return
        
        lines = self.text.split('\n')
        for i, line in enumerate(lines[:self.rect.height]):
            if i >= self.rect.height:
                break
            renderer.move_cursor(self.rect.x, self.rect.y + i)
            display_text = line[:self.rect.width]
            renderer.buffer.append(renderer.style_text(display_text, self.style))
