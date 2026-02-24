/**
 * Input widgets for CUI framework
 */
import { Component } from '../core/component.js';
import { Style } from '../core/renderer.js';

export class TextInput extends Component {
    constructor(rect, { label = '', placeholder = '', value = '', maxLength = null } = {}) {
        super(rect);
        this.label = label;
        this.value = value;
        this.placeholder = placeholder;
        this.maxLength = maxLength;
        this.cursorPos = value.length;
        this.labelStyle = new Style({ fg: 'brightWhite', bold: true });
        this.style = new Style({ fg: 'white' });
        this.focusedStyle = new Style({ fg: 'cyan', bold: true });
        this.placeholderStyle = new Style({ fg: 'brightBlack' });
        this.cursorStyle = new Style({ fg: 'black', bg: 'white' });
    }

    render(renderer) {
        if (!this.visible) return;

        let y = this.rect.y;

        // Label
        if (this.label) {
            renderer.moveCursor(this.rect.x, y);
            renderer.buffer.push(renderer.styleText(this.label, this.labelStyle));
            y++;
        }

        // Input field
        renderer.moveCursor(this.rect.x, y);
        
        const displayText = this.value || this.placeholder;
        const style = this.value ? this.style : this.placeholderStyle;
        
        if (this.focused && this.value) {
            const before = this.value.substring(0, this.cursorPos);
            const cursor = this.cursorPos < this.value.length ? this.value[this.cursorPos] : ' ';
            const after = this.value.substring(this.cursorPos + 1);
            
            renderer.buffer.push(renderer.styleText(before, style));
            renderer.buffer.push(renderer.styleText(cursor, this.cursorStyle));
            renderer.buffer.push(renderer.styleText(after, style));
        } else {
            renderer.buffer.push(renderer.styleText(displayText.substring(0, this.rect.width), style));
        }
    }

    handleKey(key) {
        if (!this.focused) return false;

        if (key === '\x7f' || key === '\b') { // Backspace
            if (this.cursorPos > 0) {
                this.value = this.value.slice(0, this.cursorPos - 1) + this.value.slice(this.cursorPos);
                this.cursorPos--;
            }
            return true;
        } else if (key === '\x1b[C') { // Right arrow
            this.cursorPos = Math.min(this.value.length, this.cursorPos + 1);
            return true;
        } else if (key === '\x1b[D') { // Left arrow
            this.cursorPos = Math.max(0, this.cursorPos - 1);
            return true;
        } else if (key.length >= 1 && !key.startsWith('\x1b') && key !== '\r' && key !== '\n' && key !== '\t') {
            // Accept all printable characters including Unicode/Cyrillic
            // Skip control characters (ASCII < 32) except for multi-byte UTF-8
            if (key.length === 1 && key.charCodeAt(0) < 32) {
                return false;
            }
            
            if (!this.maxLength || this.value.length < this.maxLength) {
                this.value = this.value.slice(0, this.cursorPos) + key + this.value.slice(this.cursorPos);
                this.cursorPos++;
            }
            return true;
        }

        return false;
    }
}

export class Checkbox extends Component {
    constructor(rect, { label = '', checked = false, onChange = null } = {}) {
        super(rect);
        this.label = label;
        this.checked = checked;
        this.onChange = onChange;
        this.boxStyle = new Style({ fg: 'brightCyan', bold: true });
        this.labelStyle = new Style({ fg: 'white' });
        this.selectedStyle = new Style({ fg: 'brightWhite', bold: true });
    }

    render(renderer) {
        if (!this.visible) return;

        renderer.moveCursor(this.rect.x, this.rect.y);
        
        // Checkbox - use [X] instead of [✓] to match Python
        const box = this.checked ? '[X]' : '[ ]';
        
        const style = this.focused ? this.selectedStyle : this.boxStyle;
        renderer.buffer.push(renderer.styleText(box, style));
        
        // Label
        const labelStyle = this.focused ? this.selectedStyle : this.labelStyle;
        renderer.buffer.push(renderer.styleText(` ${this.label}`, labelStyle));
    }

    handleKey(key) {
        if (!this.focused) return false;

        if (key === ' ' || key === '\r' || key === '\n') {
            this.checked = !this.checked;
            if (this.onChange) {
                this.onChange(this.checked);
            }
            return true;
        }

        return false;
    }

    toggle() {
        this.checked = !this.checked;
        if (this.onChange) {
            this.onChange(this.checked);
        }
    }
}

export class RadioGroup extends Component {
    constructor(rect, { options = [], selected = 0, onChange = null } = {}) {
        super(rect);
        this.options = options;
        this.selected = selected;
        this.onChange = onChange;
        this.style = new Style({ fg: 'white' });
        this.focusedStyle = new Style({ fg: 'cyan', bold: true });
    }

    render(renderer) {
        if (!this.visible) return;

        let y = this.rect.y;
        for (let i = 0; i < this.options.length; i++) {
            if (y >= this.rect.y + this.rect.height) break;
            
            renderer.moveCursor(this.rect.x, y);
            
            const style = (this.focused && i === this.selected) ? this.focusedStyle : this.style;
            const radio = i === this.selected ? '(•)' : '( )';
            const display = `${radio} ${this.options[i]}`;
            
            renderer.buffer.push(renderer.styleText(display, style));
            y++;
        }
    }

    handleKey(key) {
        if (!this.focused) return false;

        if (key === '\x1b[A') { // Up
            this.selected = Math.max(0, this.selected - 1);
            if (this.onChange) {
                this.onChange(this.selected);
            }
            return true;
        } else if (key === '\x1b[B') { // Down
            this.selected = Math.min(this.options.length - 1, this.selected + 1);
            if (this.onChange) {
                this.onChange(this.selected);
            }
            return true;
        }

        return false;
    }
}

export class Button extends Component {
    constructor(rect, { label = '', onClick = null } = {}) {
        super(rect);
        this.label = label;
        this.onClick = onClick;
        this.normalStyle = new Style({ fg: 'white', bg: 'brightBlue', bold: true });
        this.focusedStyle = new Style({ fg: 'black', bg: 'brightCyan', bold: true });
        this.pressedStyle = new Style({ fg: 'white', bg: 'blue', bold: true });
        this.pressed = false;
    }

    render(renderer) {
        if (!this.visible) return;

        renderer.moveCursor(this.rect.x, this.rect.y);
        
        // Choose style
        let style;
        if (this.pressed) {
            style = this.pressedStyle;
            this.pressed = false;
        } else if (this.focused) {
            style = this.focusedStyle;
        } else {
            style = this.normalStyle;
        }
        
        // Button text with padding
        const buttonText = ` ${this.label} `;
        const padding = Math.floor((this.rect.width - buttonText.length) / 2);
        const fullText = ' '.repeat(padding) + buttonText + ' '.repeat(padding);
        
        renderer.buffer.push(renderer.styleText(fullText, style));
    }

    handleKey(key) {
        if (!this.focused) return false;

        if (key === ' ' || key === '\r' || key === '\n') {
            this.pressed = true;
            if (this.onClick) {
                this.onClick();
            }
            return true;
        }

        return false;
    }

    click() {
        if (this.onClick) {
            this.onClick();
        }
    }
}
