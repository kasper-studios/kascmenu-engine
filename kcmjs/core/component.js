/**
 * Base component system for CUI framework
 */

export class Rect {
    constructor(x, y, width, height) {
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
    }
}

export class Component {
    constructor(rect) {
        this.rect = rect;
        this.children = [];
        this.parent = null;
        this.visible = true;
        this.focused = false;
    }

    addChild(child) {
        child.parent = this;
        this.children.push(child);
    }

    removeChild(child) {
        const index = this.children.indexOf(child);
        if (index > -1) {
            child.parent = null;
            this.children.splice(index, 1);
        }
    }

    render(renderer) {
        // Default implementation: render children
        for (const child of this.children) {
            child.render(renderer);
        }
    }

    update(deltaTime) {
        for (const child of this.children) {
            child.update(deltaTime);
        }
    }

    handleKey(key) {
        // Try to handle key in children first
        for (const child of this.children) {
            if (child.handleKey && child.handleKey(key)) {
                return true;
            }
        }
        return false;
    }

    handleEvent(event) {
        for (const child of this.children) {
            if (child.handleEvent(event)) {
                return true;
            }
        }
        return false;
    }
}
