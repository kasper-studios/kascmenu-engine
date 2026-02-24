/**
 * Menu widgets for CUI framework
 */
import { Component } from '../core/component.js';
import { Style } from '../core/renderer.js';

export class MenuItem {
    constructor(label, callback, key = null) {
        this.label = label;
        this.callback = callback;
        this.key = key;
    }
}

export class Menu extends Component {
    constructor(rect, { title = '', items = [] } = {}) {
        super(rect);
        this.title = title;
        this.items = items;
        this.selectedIndex = 0;
        this.style = new Style({ fg: 'white' });
        this.selectedStyle = new Style({ fg: 'black', bg: 'cyan', bold: true });
    }

    render(renderer) {
        if (!this.visible) return;

        // Border
        const tl = '┌', tr = '┐', bl = '└', br = '┘', h = '─', v = '│';
        
        // Top border with title
        renderer.moveCursor(this.rect.x, this.rect.y);
        let top = tl + h.repeat(this.rect.width - 2) + tr;
        if (this.title) {
            const titleText = ` ${this.title} `;
            const pos = Math.floor((this.rect.width - titleText.length) / 2);
            top = top.substring(0, pos) + titleText + top.substring(pos + titleText.length);
        }
        renderer.buffer.push(renderer.styleText(top, this.style));

        // Menu items
        let y = this.rect.y + 1;
        for (let i = 0; i < this.items.length; i++) {
            const item = this.items[i];
            const isSelected = i === this.selectedIndex;
            const style = isSelected ? this.selectedStyle : this.style;
            
            renderer.moveCursor(this.rect.x, y);
            renderer.buffer.push(renderer.styleText(v, this.style));
            
            let itemText = ' ';
            if (item.key) {
                itemText += `[${item.key}] `;
            }
            itemText += item.label;
            itemText = itemText.padEnd(this.rect.width - 2);
            
            renderer.buffer.push(renderer.styleText(itemText, style));
            renderer.buffer.push(renderer.styleText(v, this.style));
            y++;
        }

        // Fill empty space
        while (y < this.rect.y + this.rect.height - 1) {
            renderer.moveCursor(this.rect.x, y);
            renderer.buffer.push(renderer.styleText(v + ' '.repeat(this.rect.width - 2) + v, this.style));
            y++;
        }

        // Bottom border
        renderer.moveCursor(this.rect.x, this.rect.y + this.rect.height - 1);
        renderer.buffer.push(renderer.styleText(bl + h.repeat(this.rect.width - 2) + br, this.style));
    }

    handleKey(key) {
        // Arrow keys
        if (key === '\x1b[A') { // Up
            this.selectedIndex = Math.max(0, this.selectedIndex - 1);
            return true;
        } else if (key === '\x1b[B') { // Down
            this.selectedIndex = Math.min(this.items.length - 1, this.selectedIndex + 1);
            return true;
        } else if (key === '\r' || key === '\n') { // Enter
            const item = this.items[this.selectedIndex];
            if (item && item.callback) {
                item.callback();
            }
            return true;
        }

        // Hotkeys
        for (let i = 0; i < this.items.length; i++) {
            const item = this.items[i];
            if (item.key && key === item.key) {
                this.selectedIndex = i;
                if (item.callback) {
                    item.callback();
                }
                return true;
            }
        }

        return false;
    }
}

export class SelectList extends Component {
    constructor(rect, { items = [], multiSelect = false } = {}) {
        super(rect);
        this.items = items;
        this.multiSelect = multiSelect;
        this.selectedIndex = 0;
        this.selectedItems = new Set();
        this.style = new Style({ fg: 'white' });
        this.selectedStyle = new Style({ fg: 'black', bg: 'cyan' });
    }

    render(renderer) {
        if (!this.visible) return;

        let y = this.rect.y;
        for (let i = 0; i < Math.min(this.items.length, this.rect.height); i++) {
            const item = this.items[i];
            const isSelected = i === this.selectedIndex;
            const isChecked = this.selectedItems.has(i);
            const style = isSelected ? this.selectedStyle : this.style;
            
            renderer.moveCursor(this.rect.x, y);
            
            let text = '';
            if (this.multiSelect) {
                text += isChecked ? '[✓] ' : '[ ] ';
            }
            text += item;
            text = text.substring(0, this.rect.width);
            
            renderer.buffer.push(renderer.styleText(text, style));
            y++;
        }
    }

    handleKey(key) {
        if (key === '\x1b[A') { // Up
            this.selectedIndex = Math.max(0, this.selectedIndex - 1);
            return true;
        } else if (key === '\x1b[B') { // Down
            this.selectedIndex = Math.min(this.items.length - 1, this.selectedIndex + 1);
            return true;
        } else if (key === ' ' && this.multiSelect) { // Space
            if (this.selectedItems.has(this.selectedIndex)) {
                this.selectedItems.delete(this.selectedIndex);
            } else {
                this.selectedItems.add(this.selectedIndex);
            }
            return true;
        }
        return false;
    }
}
