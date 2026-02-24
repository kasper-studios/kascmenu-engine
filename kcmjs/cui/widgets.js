/**
 * Common UI widgets for CUI framework
 */
import { Component } from '../core/component.js';
import { Style } from '../core/renderer.js';

export class Box extends Component {
    static BORDERS = {
        single: ['┌', '┐', '└', '┘', '─', '│'],
        double: ['╔', '╗', '╚', '╝', '═', '║'],
        rounded: ['╭', '╮', '╰', '╯', '─', '│']
    };

    constructor(rect, title = '', borderStyle = 'single') {
        super(rect);
        this.title = title;
        this.borderStyle = borderStyle;
        this.style = new Style({ fg: 'white' });
    }

    render(renderer) {
        if (!this.visible) return;

        const [tl, tr, bl, br, h, v] = Box.BORDERS[this.borderStyle];

        // Top border
        renderer.moveCursor(this.rect.x, this.rect.y);
        let top = tl + h.repeat(this.rect.width - 2) + tr;
        if (this.title) {
            const titleText = ` ${this.title} `;
            const pos = Math.floor((this.rect.width - titleText.length) / 2);
            top = top.substring(0, pos) + titleText + top.substring(pos + titleText.length);
        }
        renderer.buffer.push(renderer.styleText(top, this.style));

        // Sides
        for (let i = 1; i < this.rect.height - 1; i++) {
            renderer.moveCursor(this.rect.x, this.rect.y + i);
            renderer.buffer.push(renderer.styleText(v + ' '.repeat(this.rect.width - 2) + v, this.style));
        }

        // Bottom border
        renderer.moveCursor(this.rect.x, this.rect.y + this.rect.height - 1);
        renderer.buffer.push(renderer.styleText(bl + h.repeat(this.rect.width - 2) + br, this.style));

        // Render children
        for (const child of this.children) {
            child.render(renderer);
        }
    }
}

export class Text extends Component {
    constructor(rect, text = '') {
        super(rect);
        this.text = text;
        this.style = new Style();
    }

    render(renderer) {
        if (!this.visible) return;

        const lines = this.text.split('\n');
        for (let i = 0; i < Math.min(lines.length, this.rect.height); i++) {
            renderer.moveCursor(this.rect.x, this.rect.y + i);
            const displayText = lines[i].substring(0, this.rect.width);
            renderer.buffer.push(renderer.styleText(displayText, this.style));
        }
    }
}
