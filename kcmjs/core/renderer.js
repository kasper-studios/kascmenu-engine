/**
 * Core rendering engine for CUI framework
 */

export class Style {
    constructor({ fg = null, bg = null, bold = false, italic = false, underline = false } = {}) {
        this.fg = fg;
        this.bg = bg;
        this.bold = bold;
        this.italic = italic;
        this.underline = underline;
    }
}

export class Renderer {
    static COLORS = {
        black: 30, red: 31, green: 32, yellow: 33,
        blue: 34, magenta: 35, cyan: 36, white: 37,
        brightBlack: 90, brightRed: 91, brightGreen: 92,
        brightYellow: 93, brightBlue: 94, brightMagenta: 95,
        brightCyan: 96, brightWhite: 97
    };

    constructor() {
        this.buffer = [];
        const size = this.getTerminalSize();
        this.width = size.columns;
        this.height = size.rows;
    }

    getTerminalSize() {
        return {
            columns: process.stdout.columns || 80,
            rows: process.stdout.rows || 24
        };
    }

    clear() {
        process.stdout.write('\x1b[2J\x1b[H');
    }

    enterAltScreen() {
        process.stdout.write('\x1b[?1049h');
    }

    exitAltScreen() {
        process.stdout.write('\x1b[?1049l');
    }

    styleText(text, style) {
        const codes = [];

        if (style.bold) codes.push('1');
        if (style.italic) codes.push('3');
        if (style.underline) codes.push('4');
        if (style.fg && Renderer.COLORS[style.fg]) {
            codes.push(Renderer.COLORS[style.fg]);
        }
        if (style.bg && Renderer.COLORS[style.bg]) {
            codes.push(Renderer.COLORS[style.bg] + 10);
        }

        if (codes.length > 0) {
            return `\x1b[${codes.join(';')}m${text}\x1b[0m`;
        }
        return text;
    }

    moveCursor(x, y) {
        // Add to buffer instead of writing directly
        this.buffer.push(`\x1b[${y};${x}H`);
    }

    hideCursor() {
        process.stdout.write('\x1b[?25l');
    }

    showCursor() {
        process.stdout.write('\x1b[?25h');
    }

    render() {
        // Flush buffer to screen
        const output = this.buffer.join('');
        process.stdout.write(output);
        this.buffer = [];
    }
}
