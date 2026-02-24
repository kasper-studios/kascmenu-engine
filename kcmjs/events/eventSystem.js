/**
 * Event system for handling user input and custom events
 */

export const EventType = {
    KEY_PRESS: 'key_press',
    MOUSE_CLICK: 'mouse_click',
    MOUSE_MOVE: 'mouse_move',
    RESIZE: 'resize',
    CUSTOM: 'custom'
};

export class Event {
    constructor(type, data = null) {
        this.type = type;
        this.data = data;
    }
}

export class EventBus {
    constructor() {
        this.listeners = new Map();
    }

    subscribe(eventType, callback) {
        if (!this.listeners.has(eventType)) {
            this.listeners.set(eventType, []);
        }
        this.listeners.get(eventType).push(callback);
    }

    unsubscribe(eventType, callback) {
        if (this.listeners.has(eventType)) {
            const callbacks = this.listeners.get(eventType);
            const index = callbacks.indexOf(callback);
            if (index > -1) {
                callbacks.splice(index, 1);
            }
        }
    }

    emit(event) {
        if (this.listeners.has(event.type)) {
            for (const callback of this.listeners.get(event.type)) {
                callback(event);
            }
        }
    }
}
