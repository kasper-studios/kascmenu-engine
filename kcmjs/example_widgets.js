/**
 * Widgets example for KCM Framework
 */
import { 
    App, Rect, Box, Text, 
    ProgressBar, Spinner, StatusIndicator,
    TextInput, Checkbox, Button,
    Component, Style
} from './main.js';

// Create root container
const root = new Component(new Rect(1, 1, 80, 30));

// Title
const title = new StatusIndicator(new Rect(2, 2, 60, 1), 'info', '🎨 Демонстрация виджетов');
root.addChild(title);

// Progress bars
const progress1 = new ProgressBar(new Rect(5, 5, 40, 1), { total: 100 });
progress1.setProgress(75);
root.addChild(progress1);

const progress2 = new ProgressBar(new Rect(5, 7, 40, 1), { total: 100 });
progress2.setProgress(45);
root.addChild(progress2);

// Spinner
const spinner = new Spinner(new Rect(5, 9, 30, 1), { style: 'dots', text: 'Загрузка...' });
root.addChild(spinner);

// Status indicators
const success = new StatusIndicator(new Rect(5, 11, 40, 1), 'success', 'Операция успешна');
root.addChild(success);

const error = new StatusIndicator(new Rect(5, 12, 40, 1), 'error', 'Произошла ошибка');
root.addChild(error);

const warning = new StatusIndicator(new Rect(5, 13, 40, 1), 'warning', 'Предупреждение');
root.addChild(warning);

// Text input
const input = new TextInput(new Rect(5, 15, 40, 1), { placeholder: 'Введите текст...' });
root.addChild(input);

// Checkbox
const checkbox = new Checkbox(new Rect(5, 17, 40, 1), { 
    label: 'Согласен с условиями', 
    checked: true 
});
root.addChild(checkbox);

// Button
const button = new Button(new Rect(5, 19, 20, 1), { 
    label: 'Нажми меня',
    onClick: () => {
        title.setStatus('success', '✓ Кнопка нажата!');
    }
});
root.addChild(button);

// Box with text
const box = new Box(new Rect(50, 5, 28, 10), 'Информация', 'rounded');
const boxText = new Text(new Rect(52, 7, 24, 6), 'Это демонстрация\nвиджетов KCM\nFramework.\n\nВсе работает!');
boxText.style = new Style({ fg: 'cyan' });
box.addChild(boxText);
root.addChild(box);

// Override handleKey to handle Tab
root.handleKey = function(key) {
    if (key === '\t') { // Tab
        input.focused = !input.focused;
        return true;
    }
    
    // Try children
    for (const child of this.children) {
        if (child.handleKey && child.handleKey(key)) {
            return true;
        }
    }
    return false;
};

// Create app
const app = new App(root, { inline: false, animated: true });
app.run();
