"""Simple WebSocket chat server using Flask-SocketIO."""
from datetime import datetime
from flask import Flask, render_template_string, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kcm-chat-secret'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store connected users
users = {}
messages = []

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>KCM Chat Server</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }
        h1 { color: #00bcd4; }
        .stats { background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0; }
        .message { padding: 10px; margin: 5px 0; background: #e3f2fd; border-radius: 5px; }
        .user { color: #1976d2; font-weight: bold; }
        .time { color: #666; font-size: 0.9em; }
    </style>
</head>
<body>
    <h1>🚀 KCM Chat Server</h1>
    <div class="stats">
        <p><strong>Status:</strong> Running</p>
        <p><strong>Connected users:</strong> <span id="userCount">0</span></p>
        <p><strong>Total messages:</strong> <span id="msgCount">0</span></p>
    </div>
    <h2>Recent Messages</h2>
    <div id="messages"></div>
    
    <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
    <script>
        const socket = io();
        
        socket.on('user_joined', (data) => {
            document.getElementById('userCount').textContent = data.user_count;
        });
        
        socket.on('user_left', (data) => {
            document.getElementById('userCount').textContent = data.user_count;
        });
        
        socket.on('message', (data) => {
            const msgDiv = document.createElement('div');
            msgDiv.className = 'message';
            msgDiv.innerHTML = `
                <span class="user">${data.username}:</span> ${data.message}
                <span class="time">${data.timestamp}</span>
            `;
            document.getElementById('messages').prepend(msgDiv);
            document.getElementById('msgCount').textContent = parseInt(document.getElementById('msgCount').textContent) + 1;
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Web interface."""
    return render_template_string(HTML_TEMPLATE)

@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    print(f'Client connected: {request.sid}')

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    sid = request.sid
    if sid in users:
        username = users[sid]
        del users[sid]
        emit('user_left', {
            'username': username,
            'user_count': len(users)
        }, broadcast=True)
        print(f'User disconnected: {username}')

@socketio.on('join')
def handle_join(data):
    """Handle user joining."""
    username = data.get('username', 'Anonymous')
    users[request.sid] = username
    
    emit('user_joined', {
        'username': username,
        'user_count': len(users)
    }, broadcast=True)
    
    # Send recent messages to new user
    emit('history', {'messages': messages[-50:]})
    
    print(f'User joined: {username}')

@socketio.on('message')
def handle_message(data):
    """Handle incoming message."""
    username = users.get(request.sid, 'Anonymous')
    message = data.get('message', '')
    
    if not message.strip():
        return
    
    msg_data = {
        'username': username,
        'message': message,
        'timestamp': datetime.now().strftime('%H:%M:%S')
    }
    
    messages.append(msg_data)
    if len(messages) > 100:
        messages.pop(0)
    
    emit('message', msg_data, broadcast=True)
    print(f'{username}: {message}')

if __name__ == '__main__':
    print('=' * 60)
    print('  KCM Chat Server')
    print('=' * 60)
    print('\nServer starting...')
    print('Web interface: http://localhost:5000')
    print('WebSocket: ws://localhost:5000')
    print('\nPress Ctrl+C to stop\n')
    
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
