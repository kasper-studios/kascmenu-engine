/**
 * Progress indicators for CUI framework
 */
import { Component } from '../core/component.js';
import { Style } from '../core/renderer.js';

export class ProgressBar extends Component {
    constructor(rect, { total = 100, showPercent = true, showBar = true } = {}) {
        super(rect);
        this.current = 0;
        this.total = total;
        this.showPercent = showPercent;
        this.showBar = showBar;
        this.style = new Style({ fg: 'cyan' });
        this.barStyle = new Style({ fg: 'green', bold: true });
    }

    setProgress(value) {
        this.current = Math.min(value, this.total);
    }

    render(renderer) {
        if (!this.visible) return;

        const percent = Math.floor((this.current / this.total) * 100);
        
        renderer.moveCursor(this.rect.x, this.rect.y);
        
        if (this.showBar) {
            const barWidth = this.rect.width - (this.showPercent ? 6 : 0);
            const filled = Math.floor((this.current / this.total) * barWidth);
            
            const bar = '█'.repeat(filled) + '░'.repeat(barWidth - filled);
            renderer.buffer.push(renderer.styleText(bar, this.barStyle));
        }
        
        if (this.showPercent) {
            const percentText = ` ${percent}%`;
            renderer.buffer.push(renderer.styleText(percentText, this.style));
        }
    }
}

export class Spinner extends Component {
    static STYLES = {
        dots: ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'],
        line: ['|', '/', '-', '\\'],
        arrow: ['←', '↖', '↑', '↗', '→', '↘', '↓', '↙'],
        bounce: ['⠁', '⠂', '⠄', '⠂'],
        box: ['◰', '◳', '◲', '◱'],
        circle: ['◐', '◓', '◑', '◒'],
        square: ['◰', '◳', '◲', '◱'],
        triangle: ['◢', '◣', '◤', '◥'],
        pulse: ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷'],
        clock: ['🕐', '🕑', '🕒', '🕓', '🕔', '🕕', '🕖', '🕗', '🕘', '🕙', '🕚', '🕛']
    };

    constructor(rect, { style = 'dots', text = '' } = {}) {
        super(rect);
        this.frames = Spinner.STYLES[style] || Spinner.STYLES.dots;
        this.currentFrame = 0;
        this.text = text;
        this.style = new Style({ fg: 'cyan', bold: true });
    }

    update(deltaTime) {
        this.currentFrame = (this.currentFrame + 1) % this.frames.length;
        super.update(deltaTime);
    }

    render(renderer) {
        if (!this.visible) return;

        renderer.moveCursor(this.rect.x, this.rect.y);
        
        const frame = this.frames[this.currentFrame];
        let display = frame;
        if (this.text) {
            display += ' ' + this.text;
        }
        
        renderer.buffer.push(renderer.styleText(display, this.style));
    }
}

export class MultiProgressBar extends Component {
    constructor(rect, { bars = [] } = {}) {
        super(rect);
        this.bars = bars; // Array of {label, current, total}
        this.style = new Style({ fg: 'white' });
        this.barStyle = new Style({ fg: 'green', bold: true });
    }

    render(renderer) {
        if (!this.visible) return;

        let y = this.rect.y;
        for (const bar of this.bars) {
            if (y >= this.rect.y + this.rect.height) break;
            
            renderer.moveCursor(this.rect.x, y);
            
            // Label
            const label = bar.label.substring(0, 15).padEnd(15);
            renderer.buffer.push(renderer.styleText(label + ' ', this.style));
            
            // Progress bar
            const barWidth = this.rect.width - 22;
            const percent = Math.floor((bar.current / bar.total) * 100);
            const filled = Math.floor((bar.current / bar.total) * barWidth);
            
            const barDisplay = '█'.repeat(filled) + '░'.repeat(barWidth - filled);
            renderer.buffer.push(renderer.styleText(barDisplay, this.barStyle));
            
            // Percent
            const percentText = ` ${percent}%`;
            renderer.buffer.push(renderer.styleText(percentText, this.style));
            
            y++;
        }
    }
}

export class StatusIndicator extends Component {
    static ICONS = {
        success: '[OK]',
        error: '[X]',
        warning: '[!]',
        info: '[i]',
        loading: '[~]'
    };

    static COLORS = {
        success: 'brightGreen',
        error: 'brightRed',
        warning: 'brightYellow',
        info: 'brightBlue',
        loading: 'brightCyan'
    };

    constructor(rect, status, text = '') {
        super(rect);
        this.status = status;
        this.text = text;
        this.updateStyle();
    }

    updateStyle() {
        const color = StatusIndicator.COLORS[this.status] || 'white';
        this.iconStyle = new Style({ fg: color, bold: true });
        this.textStyle = new Style({ fg: 'white' });
    }

    setStatus(status, text = null) {
        this.status = status;
        if (text !== null) {
            this.text = text;
        }
        this.updateStyle();
    }

    render(renderer) {
        if (!this.visible) return;

        renderer.moveCursor(this.rect.x, this.rect.y);
        
        const icon = StatusIndicator.ICONS[this.status] || '[•]';
        
        // Render icon and text separately with different styles
        renderer.buffer.push(renderer.styleText(icon, this.iconStyle));
        renderer.buffer.push(renderer.styleText((' ' + this.text).padEnd(this.rect.width - icon.length, ' '), this.textStyle));
    }
}
