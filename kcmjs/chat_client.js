/**
 * WebSocket chat client with console notifications
 */
import { io } from 'socket.io-client';
import { App } from './core/app.js';
import { Component, Rect } from './core/component.js';
import { Style } from './core/renderer.js';
import { TextInput, Button, Checkbox } from './cui/input.js';
import { StatusIndicator } from './cui/progress.js';
import fs from 'fs';
import os from 'os';
import path from 'path';

// Simple notification manager
class SimpleNotificationManager {
    constructor() {
        this.enabled = true;
        this.notifyMessages = true;
        this.notifyJoins = true;
        this.notifyLeaves = false;
        this.notifications = [];
        this.maxNotifications = 5;
    }

    show(title, message) {
        if (!this.enabled) return;

        const now = new Date();
        const time = now.toTimeString().split(' ')[0];
        const notification = `[${time}] ${title}: ${message}`;
        this.notifications.push(notification);

        if (this.notifications.length > this.maxNotifications) {
            this.notifications.shift();
        }
    }

    notifyNewMessage(username, message) {
        if (this.enabled && this.notifyMessages) {
            const preview = message.length > 30 ? message.substring(0, 30) + '...' : message;
            this.show('💬 Новое сообщение', `${username}: ${preview}`);
        }
    }

    notifyUserJoined(username) {
        if (this.enabled && this.notifyJoins) {
            this.show('👋 Вход', `${username} присоединился`);
        }
    }

    notifyUserLeft(username) {
        if (this.enabled && this.notifyLeaves) {
            this.show('👋 Выход', `${username} покинул чат`);
        }
    }

    getRecentNotifications() {
        return [...this.notifications];
    }
}

// Chat message data
class ChatMessage {
    constructor(username, message, timestamp) {
        this.username = username;
        this.message = message;
        this.timestamp = timestamp;
    }
}

// Config manager
class Config {
    constructor(appName) {
        this.appName = appName;
        const homeDir = os.homedir();
        this.configDir = path.join(homeDir, '.kcm');
        this.configFile = path.join(this.configDir, `${appName}.json`);
        this.data = {};
        this.load();
    }

    load() {
        try {
            if (!fs.existsSync(this.configDir)) {
                fs.mkdirSync(this.configDir, { recursive: true });
            }
            if (fs.existsSync(this.configFile)) {
                const content = fs.readFileSync(this.configFile, 'utf8');
                this.data = JSON.parse(content);
            }
        } catch (err) {
            console.error('Error loading config:', err);
        }
    }

    save() {
        try {
            if (!fs.existsSync(this.configDir)) {
                fs.mkdirSync(this.configDir, { recursive: true });
            }
            fs.writeFileSync(this.configFile, JSON.stringify(this.data, null, 2));
        } catch (err) {
            console.error('Error saving config:', err);
        }
    }

    get(key, defaultValue = null) {
        const keys = key.split('.');
        let value = this.data;
        for (const k of keys) {
            if (value && typeof value === 'object' && k in value) {
                value = value[k];
            } else {
                return defaultValue;
            }
        }
        return value;
    }

    set(key, value) {
        const keys = key.split('.');
        let obj = this.data;
        for (let i = 0; i < keys.length - 1; i++) {
            const k = keys[i];
            if (!(k in obj) || typeof obj[k] !== 'object') {
                obj[k] = {};
            }
            obj = obj[k];
        }
        obj[keys[keys.length - 1]] = value;
    }
}

// Box widget
class Box extends Component {
    constructor(rect, { title = '', borderStyle = 'single' } = {}) {
        super(rect);
        this.title = title;
        this.borderStyle = borderStyle;
        this.style = new Style({ fg: 'white' });
    }

    render(renderer) {
        if (!this.visible) return;

        const borders = this.borderStyle === 'double' 
            ? { tl: '╔', tr: '╗', bl: '╚', br: '╝', h: '═', v: '║' }
            : { tl: '┌', tr: '┐', bl: '└', br: '┘', h: '─', v: '│' };

        // Top border
        renderer.moveCursor(this.rect.x, this.rect.y);
        let top = borders.tl + borders.h.repeat(this.rect.width - 2) + borders.tr;
        if (this.title) {
            const titleText = ` ${this.title} `;
            const pos = Math.floor((this.rect.width - titleText.length) / 2);
            top = top.substring(0, pos) + titleText + top.substring(pos + titleText.length);
        }
        renderer.buffer.push(renderer.styleText(top, this.style));

        // Sides
        for (let y = 1; y < this.rect.height - 1; y++) {
            renderer.moveCursor(this.rect.x, this.rect.y + y);
            renderer.buffer.push(renderer.styleText(borders.v, this.style));
            renderer.moveCursor(this.rect.x + this.rect.width - 1, this.rect.y + y);
            renderer.buffer.push(renderer.styleText(borders.v, this.style));
        }

        // Bottom border
        renderer.moveCursor(this.rect.x, this.rect.y + this.rect.height - 1);
        renderer.buffer.push(renderer.styleText(
            borders.bl + borders.h.repeat(this.rect.width - 2) + borders.br,
            this.style
        ));

        // Render children
        super.render(renderer);
    }
}

// Settings screen
class SettingsScreen extends Component {
    constructor(rect, notificationManager, config, app) {
        super(rect);
        this.notificationManager = notificationManager;
        this.config = config;
        this.app = app;

        // Load saved settings
        const savedUrl = config.get('server.url', 'http://localhost:5000');
        const savedNick = config.get('user.nickname', 'Пользователь');
        const savedNotifyMsg = config.get('notifications.messages', true);
        const savedNotifyJoin = config.get('notifications.joins', true);
        const savedNotifyLeave = config.get('notifications.leaves', false);

        // Container
        this.box = new Box(
            new Rect(rect.x + 10, rect.y + 3, 60, 20),
            { title: 'Настройки подключения', borderStyle: 'double' }
        );
        this.addChild(this.box);

        // Server URL input
        this.urlInput = new TextInput(
            new Rect(this.box.rect.x + 2, this.box.rect.y + 2, 56, 2),
            { label: 'Адрес сервера:', placeholder: 'http://localhost:5000', value: savedUrl }
        );
        this.urlInput.cursorPos = this.urlInput.value.length;
        this.box.addChild(this.urlInput);

        // Nickname input
        this.nickInput = new TextInput(
            new Rect(this.box.rect.x + 2, this.box.rect.y + 6, 56, 2),
            { label: 'Ваш никнейм:', placeholder: 'Аноним', value: savedNick }
        );
        this.nickInput.cursorPos = this.nickInput.value.length;
        this.box.addChild(this.nickInput);

        // Notification settings
        const yOffset = 10;
        this.notifyLabel = new StatusIndicator(
            new Rect(this.box.rect.x + 2, this.box.rect.y + yOffset, 56, 1),
            'info',
            'Настройки уведомлений (консольные):'
        );
        this.box.addChild(this.notifyLabel);

        this.notifyMessagesCheckbox = new Checkbox(
            new Rect(this.box.rect.x + 2, this.box.rect.y + yOffset + 1, 56, 1),
            {
                label: 'Уведомления о новых сообщениях',
                checked: savedNotifyMsg,
                onChange: (checked) => {
                    this.notificationManager.notifyMessages = checked;
                    this.config.set('notifications.messages', checked);
                    this.config.save();
                }
            }
        );
        this.notificationManager.notifyMessages = savedNotifyMsg;
        this.box.addChild(this.notifyMessagesCheckbox);

        this.notifyJoinsCheckbox = new Checkbox(
            new Rect(this.box.rect.x + 2, this.box.rect.y + yOffset + 2, 56, 1),
            {
                label: 'Уведомления о входе пользователей',
                checked: savedNotifyJoin,
                onChange: (checked) => {
                    this.notificationManager.notifyJoins = checked;
                    this.config.set('notifications.joins', checked);
                    this.config.save();
                }
            }
        );
        this.notificationManager.notifyJoins = savedNotifyJoin;
        this.box.addChild(this.notifyJoinsCheckbox);

        this.notifyLeavesCheckbox = new Checkbox(
            new Rect(this.box.rect.x + 2, this.box.rect.y + yOffset + 3, 56, 1),
            {
                label: 'Уведомления о выходе пользователей',
                checked: savedNotifyLeave,
                onChange: (checked) => {
                    this.notificationManager.notifyLeaves = checked;
                    this.config.set('notifications.leaves', checked);
                    this.config.save();
                }
            }
        );
        this.notificationManager.notifyLeaves = savedNotifyLeave;
        this.box.addChild(this.notifyLeavesCheckbox);

        // Connect button
        this.connectBtn = new Button(
            new Rect(this.box.rect.x + 20, this.box.rect.y + 16, 20, 1),
            {
                label: 'Подключиться',
                onClick: () => this.connect()
            }
        );
        this.box.addChild(this.connectBtn);

        // Status
        this.status = new StatusIndicator(
            new Rect(this.box.rect.x + 2, this.box.rect.y + 18, 56, 1),
            'success',
            'Настройки загружены из ~/.kcm/kcm_chat.json'
        );
        this.box.addChild(this.status);

        // Focus management
        this.focusable = [
            this.urlInput,
            this.nickInput,
            this.notifyMessagesCheckbox,
            this.notifyJoinsCheckbox,
            this.notifyLeavesCheckbox,
            this.connectBtn
        ];
        this.focusedIndex = 0;
        this.focusable[0].focused = true;
    }

    connect() {
        const url = this.urlInput.value.trim() || 'http://localhost:5000';
        const nickname = this.nickInput.value.trim() || 'Аноним';

        // Save settings
        this.config.set('server.url', url);
        this.config.set('user.nickname', nickname);
        this.config.save();

        // Switch to chat screen
        if (this.app.chatScreen) {
            this.app.chatScreen.connect(url, nickname);
            this.app.currentScreen = 'chat';
            this.app._clearScreen();
            this.app.needsRender = true;
        }
    }

    handleKey(key) {
        // Tab to switch focus
        if (key === '\t') {
            this.focusable[this.focusedIndex].focused = false;
            this.focusedIndex = (this.focusedIndex + 1) % this.focusable.length;
            this.focusable[this.focusedIndex].focused = true;
            return true;
        }

        // Enter on button
        if ((key === '\r' || key === '\n') && this.focusedIndex === this.focusable.length - 1) {
            this.connect();
            return true;
        }

        return this.focusable[this.focusedIndex].handleKey(key);
    }

    render(renderer) {
        this.box.render(renderer);
    }
}

// Chat screen
class ChatScreen extends Component {
    constructor(rect, notificationManager, app) {
        super(rect);
        this.notificationManager = notificationManager;
        this.app = app;
        this.socket = null;
        this.connected = false;
        this.messages = [];
        this.serverUrl = '';
        this.nickname = '';
        this.scrollOffset = 0;
        this.needsRender = false;

        // Header
        this.header = new StatusIndicator(
            new Rect(2, 2, rect.width - 4, 1),
            'info',
            'Чат KCM - Отключен'
        );
        this.addChild(this.header);

        // Messages box
        this.msgBox = new Box(
            new Rect(2, 4, rect.width - 4, rect.height - 10),
            { title: 'Сообщения', borderStyle: 'single' }
        );
        this.addChild(this.msgBox);

        // Input field (label takes 1 line, so we need space for it)
        this.inputField = new TextInput(
            new Rect(2, rect.height - 5, rect.width - 4, 2),
            { label: 'Сообщение:', placeholder: 'Введите сообщение...' }
        );
        this.inputField.focused = true;
        this.addChild(this.inputField);

        // Status bar
        this.statusBar = new StatusIndicator(
            new Rect(2, rect.height - 1, rect.width - 4, 1),
            'info',
            'Enter - отправить | Esc - настройки | q - выход | 🔔 Консольные уведомления'
        );
        this.addChild(this.statusBar);
    }

    setupSocketIO() {
        this.socket.on('connect', () => {
            this.connected = true;
            this.header.setStatus('success', `Чат KCM - Подключен как ${this.nickname}`);
            this.needsRender = true;
            this.socket.emit('join', { username: this.nickname });
        });

        this.socket.on('disconnect', () => {
            this.connected = false;
            this.header.setStatus('error', 'Чат KCM - Отключен');
            this.needsRender = true;
        });

        this.socket.on('message', (data) => {
            const username = data.username || 'Unknown';
            const message = data.message || '';
            const timestamp = data.timestamp || '';

            const msg = new ChatMessage(username, message, timestamp);
            this.messages.push(msg);

            // Show notification if not from self
            if (username !== this.nickname) {
                this.notificationManager.notifyNewMessage(username, message);
            }

            // Auto-scroll to bottom
            this.scrollOffset = Math.max(0, this.messages.length - this.getVisibleLines());
            this.needsRender = true;
        });

        this.socket.on('user_joined', (data) => {
            const username = data.username || 'Unknown';
            const now = new Date();
            const timestamp = now.toTimeString().split(' ')[0];
            const msg = new ChatMessage('System', `${username} присоединился к чату`, timestamp);
            this.messages.push(msg);

            // Show notification if not self
            if (username !== this.nickname) {
                this.notificationManager.notifyUserJoined(username);
            }

            this.scrollOffset = Math.max(0, this.messages.length - this.getVisibleLines());
            this.needsRender = true;
        });

        this.socket.on('user_left', (data) => {
            const username = data.username || 'Unknown';
            const now = new Date();
            const timestamp = now.toTimeString().split(' ')[0];
            const msg = new ChatMessage('System', `${username} покинул чат`, timestamp);
            this.messages.push(msg);

            // Show notification
            this.notificationManager.notifyUserLeft(username);

            this.scrollOffset = Math.max(0, this.messages.length - this.getVisibleLines());
            this.needsRender = true;
        });

        this.socket.on('history', (data) => {
            const history = data.messages || [];
            for (const msgData of history) {
                const msg = new ChatMessage(
                    msgData.username || 'Unknown',
                    msgData.message || '',
                    msgData.timestamp || ''
                );
                this.messages.push(msg);
            }
            this.scrollOffset = Math.max(0, this.messages.length - this.getVisibleLines());
            this.needsRender = true;
        });
    }

    connect(url, nickname) {
        this.serverUrl = url;
        this.nickname = nickname;
        this.messages = [];

        // Show connecting status
        this.header.setStatus('warning', `Чат KCM - Подключение к ${url}...`);
        this.needsRender = true;

        try {
            this.socket = io(url);
            this.setupSocketIO();
        } catch (err) {
            const now = new Date();
            const timestamp = now.toTimeString().split(' ')[0];
            const msg = new ChatMessage('System', `Ошибка подключения: ${err.message}`, timestamp);
            this.messages.push(msg);
            this.header.setStatus('error', 'Чат KCM - Ошибка подключения');
            this.needsRender = true;
        }
    }

    disconnect() {
        if (this.connected && this.socket) {
            this.socket.disconnect();
        }
    }

    sendMessage() {
        const message = this.inputField.value.trim();
        if (!message || !this.connected) return;

        this.socket.emit('message', { message });
        this.inputField.value = '';
        this.inputField.cursorPos = 0;
        this.needsRender = true;
    }

    update(deltaTime) {
        super.update(deltaTime);
        if (this.needsRender) {
            this.needsRender = false;
            return true; // Tell app to render
        }
        return false;
    }

    getVisibleLines() {
        return this.msgBox.rect.height - 2;
    }

    handleKey(key) {
        // Send message
        if (key === '\r' || key === '\n') {
            this.sendMessage();
            return true;
        }

        // Scroll up
        if (key === '\x1b[A') {
            if (this.scrollOffset > 0) {
                this.scrollOffset--;
            }
            return true;
        }

        // Scroll down
        if (key === '\x1b[B') {
            const maxScroll = Math.max(0, this.messages.length - this.getVisibleLines());
            if (this.scrollOffset < maxScroll) {
                this.scrollOffset++;
            }
            return true;
        }

        // Back to settings
        if (key === '\x1b') {
            this.disconnect();
            this.app.currentScreen = 'settings';
            this.app._clearScreen();
            this.app.needsRender = true;
            return true;
        }

        return this.inputField.handleKey(key);
    }

    render(renderer) {
        // Render header
        this.header.render(renderer);

        // Render message box
        this.msgBox.render(renderer);

        // Render messages
        const visibleLines = this.getVisibleLines();
        const startIdx = this.scrollOffset;
        const endIdx = Math.min(startIdx + visibleLines, this.messages.length);

        let y = this.msgBox.rect.y + 1;
        const maxWidth = this.msgBox.rect.width - 4;

        for (let i = startIdx; i < endIdx; i++) {
            if (y >= this.msgBox.rect.y + this.msgBox.rect.height - 1) break;

            const msg = this.messages[i];
            renderer.moveCursor(this.msgBox.rect.x + 2, y);

            // Format message
            if (msg.username === 'System') {
                const styleSystem = new Style({ fg: 'brightBlack', italic: true });
                let text = `[${msg.timestamp}] ${msg.message}`;
                if (text.length > maxWidth) {
                    text = text.substring(0, maxWidth - 3) + '...';
                }
                renderer.buffer.push(renderer.styleText(text, styleSystem));
            } else {
                const styleTime = new Style({ fg: 'brightBlack' });
                const styleUser = new Style({ fg: 'brightCyan', bold: true });
                const styleMsg = new Style({ fg: 'white' });

                const prefix = `[${msg.timestamp}] ${msg.username}: `;
                const prefixLen = prefix.length;

                let messageText = msg.message;
                const availableWidth = maxWidth - prefixLen;
                if (messageText.length > availableWidth) {
                    messageText = messageText.substring(0, availableWidth - 3) + '...';
                }

                renderer.buffer.push(renderer.styleText(`[${msg.timestamp}] `, styleTime));
                renderer.buffer.push(renderer.styleText(`${msg.username}: `, styleUser));
                renderer.buffer.push(renderer.styleText(messageText, styleMsg));
            }

            y++;
        }

        // Render input field
        this.inputField.render(renderer);

        // Render status bar
        this.statusBar.render(renderer);
    }
}

// Main app
class ChatApp {
    constructor() {
        this.config = new Config('kcm_chat');
        this.notificationManager = new SimpleNotificationManager();
        
        const rect = new Rect(1, 1, 80, 30);
        this.root = new Component(rect);
        this.app = new App(this.root, { inline: false, animated: true });
        
        // Create screens
        this.settingsScreen = new SettingsScreen(rect, this.notificationManager, this.config, this);
        this.chatScreen = new ChatScreen(rect, this.notificationManager, this);
        
        this.currentScreen = 'settings';
        this.app.chatScreen = this.chatScreen;
        
        // Override root render
        this.root.render = (renderer) => {
            if (this.currentScreen === 'settings') {
                this.settingsScreen.render(renderer);
            } else {
                this.chatScreen.render(renderer);
            }
        };
        
        // Override root handleKey
        this.root.handleKey = (key) => {
            if (this.currentScreen === 'settings') {
                return this.settingsScreen.handleKey(key);
            } else {
                return this.chatScreen.handleKey(key);
            }
        };
        
        // Override root update
        this.root.update = (deltaTime) => {
            if (this.currentScreen === 'chat') {
                return this.chatScreen.update(deltaTime);
            }
            return false;
        };
    }

    _clearScreen() {
        this.app._clearScreen();
    }

    run() {
        console.log('='.repeat(70));
        console.log('  KCM Chat Client с консольными уведомлениями');
        console.log('='.repeat(70));
        console.log('\nВозможности:');
        console.log('  • WebSocket подключение к серверу');
        console.log('  • Настройка адреса сервера и никнейма');
        console.log('  • 📝 Консольные уведомления');
        console.log('  • Настройка типов уведомлений');
        console.log('  • Прокрутка истории сообщений');
        console.log('  • 💾 Автосохранение настроек в ~/.kcm/kcm_chat.json');
        console.log('\nНажмите любую клавишу для начала...');
        
        process.stdin.setRawMode(true);
        process.stdin.resume();
        process.stdin.once('data', () => {
            // Clear screen before starting
            process.stdout.write('\x1b[2J\x1b[H');
            this.app.run();
        });
    }
}

// Run
const chatApp = new ChatApp();
chatApp.run();
