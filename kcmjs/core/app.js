/**
 * Main application class for CUI framework
 */
import { Renderer } from './renderer.js';
import { EventBus } from '../events/eventSystem.js';

export class App {
    constructor(root, options = {}) {
        this.root = root;
        this.renderer = new Renderer();
        this.eventBus = new EventBus();
        this.running = false;
        this.inline = options.inline !== undefined ? options.inline : true;
        this.animated = options.animated || false;
        this.needsRender = false;
    }

    run() {
        this.running = true;
        
        // Setup input handling
        const stdin = process.stdin;
        stdin.setRawMode(true);
        stdin.resume();
        stdin.setEncoding('utf8');
        
        // Switch to alternate screen buffer (like nano/vim)
        process.stdout.write('\x1b[?1049h');
        
        this.renderer.hideCursor();
        
        // Initial render
        if (this.animated) {
            this._clearScreen();
        }
        this.render();
        
        let lastUpdate = Date.now();

        // Input handler
        stdin.on('data', (key) => {
            if (!this.running) return;
            
            const keyStr = key.toString();
            
            if (keyStr === 'q' || keyStr === '\u0003') { // q or Ctrl+C
                this.stop();
                return;
            }
            
            // Handle key event
            if (this.root.handleKey && this.root.handleKey(keyStr)) {
                this.needsRender = true;
            }
            
            // Render if needed
            if (this.needsRender) {
                if (this.animated) {
                    this._clearScreen();
                }
                this.render();
                this.needsRender = false;
            }
        });

        // Animation/update loop
        const loop = () => {
            if (!this.running) {
                this.renderer.showCursor();
                if (this.animated) {
                    this._clearScreen();
                }
                // Return to normal screen buffer
                process.stdout.write('\x1b[?1049l');
                stdin.setRawMode(false);
                stdin.pause();
                return;
            }

            const currentTime = Date.now();
            const deltaTime = (currentTime - lastUpdate) / 1000;

            // Update animations periodically
            if (deltaTime >= 0.1) { // 10 FPS
                if (this.animated) {
                    const needsRender = this.root.update(deltaTime);
                    // Render if update returns true or undefined (default behavior)
                    if (needsRender !== false) {
                        this._clearScreen();
                        this.render();
                    }
                }
                lastUpdate = currentTime;
            }

            setTimeout(loop, 50);
        };

        loop();
    }

    _clearScreen() {
        // Clear screen and move cursor to home
        process.stdout.write('\x1b[2J\x1b[H');
        // Also clear buffer to avoid artifacts
        this.renderer.buffer = [];
    }

    update(deltaTime) {
        this.root.update(deltaTime);
    }

    render() {
        // Clear buffer before rendering
        this.renderer.buffer = [];
        this.root.render(this.renderer);
        this.renderer.render();
    }

    stop() {
        this.running = false;
    }
}
