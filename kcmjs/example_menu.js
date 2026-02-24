/**
 * Menu example for KCM Framework
 */
import { App, Rect, Menu, MenuItem, StatusIndicator, Component } from './main.js';

// Create root container
const root = new Component(new Rect(1, 1, 80, 25));

// Create status indicator
const status = new StatusIndicator(new Rect(2, 2, 60, 1), 'info', 'Используйте стрелки для навигации');
root.addChild(status);

// Create menu
const menu = new Menu(new Rect(20, 5, 40, 10), {
    title: 'Главное меню',
    items: [
        new MenuItem('Новый проект', () => {
            status.setStatus('success', 'Создан новый проект');
        }, 'n'),
        new MenuItem('Открыть проект', () => {
            status.setStatus('success', 'Открыт проект');
        }, 'o'),
        new MenuItem('Настройки', () => {
            status.setStatus('info', 'Открыты настройки');
        }, 's'),
        new MenuItem('Выход', () => app.stop(), 'q'),
    ]
});
root.addChild(menu);

// Create app
const app = new App(root, { inline: false, animated: false });
app.run();
