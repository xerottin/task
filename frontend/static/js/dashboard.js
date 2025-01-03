const API_URL = 'https://your-railway-domain.up.railway.app';

// Проверка авторизации
function checkAuth() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/index.html';
        return null;
    }
    return token;
}

// Получение информации о пользователе
async function getUserInfo() {
    const token = checkAuth();
    if (!token) return;

    try {
        console.log('Getting user info...');
        const response = await fetch(`${API_URL}/auth/test-token`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Accept': 'application/json'
            }
        });

        console.log('Response status:', response.status);
        
        if (!response.ok) {
            const error = await response.json();
            console.error('Error response:', error);
            throw new Error(error.detail || 'Ошибка получения данных');
        }

        const user = await response.json();
        console.log('User info:', user);
        displayUserInfo(user);
    } catch (error) {
        console.error('Error getting user info:', error);
        localStorage.removeItem('token');
        window.location.href = '/index.html';
    }
}

// Получение статистики сообщений
async function getMessageStats() {
    const token = checkAuth();
    if (!token) return;

    try {
        const response = await fetch(`${API_URL}/messages/stats`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Accept': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error('Ошибка получения статистики');
        }

        const stats = await response.json();
        document.getElementById('messageCount').textContent = stats.total_messages;
    } catch (error) {
        console.error('Error getting message stats:', error);
    }
}

// Отображение информации о пользователе
function displayUserInfo(user) {
    document.getElementById('username').textContent = user.username;
    if (user.telegram_id) {
        document.getElementById('telegramId').textContent = user.telegram_id;
        document.getElementById('telegramConnectBlock').style.display = 'none';
    }
}

// Обработка выхода
document.getElementById('logoutBtn').addEventListener('click', () => {
    localStorage.removeItem('token');
    window.location.href = '/index.html';
});

// Подключение Telegram
document.getElementById('connectTelegramBtn').addEventListener('click', async () => {
    const token = checkAuth();
    if (!token) return;

    const code = document.getElementById('telegramCode').value;
    if (!code) {
        alert('Введите код подключения');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/users/connect-telegram`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code: code })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Ошибка подключения Telegram');
        }

        const result = await response.json();
        alert('Telegram успешно подключен!');
        location.reload();
    } catch (error) {
        console.error('Error:', error);
        alert(error.message || 'Ошибка при подключении Telegram');
    }
});

// Загрузка списка пользователей
async function loadUsers() {
    const token = checkAuth();
    if (!token) return;

    try {
        console.log('Loading users...');
        const response = await fetch(`${API_URL}/messages/users`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Ошибка загрузки пользователей');
        }

        const users = await response.json();
        console.log('Loaded users:', users);
        
        const select = document.getElementById('recipientSelect');
        select.innerHTML = '<option value="">Выберите получателя...</option>';
        users.forEach(user => {
            console.log('Adding user to select:', user);
            select.innerHTML += `<option value="${user.id}">${user.username}</option>`;
        });
    } catch (error) {
        console.error('Error loading users:', error);
    }
}

// Обновим обработчик отправки сообщения
document.getElementById('sendBotMessageBtn').addEventListener('click', async () => {
    const token = checkAuth();
    if (!token) return;

    const recipientId = document.getElementById('recipientSelect').value;
    if (!recipientId) {
        alert('Выберите получателя');
        return;
    }

    const messageText = document.getElementById('botMessageInput').value.trim();
    if (!messageText) {
        alert('Введите текст сообщения');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/messages/send-bot-message?message=${encodeURIComponent(messageText)}&recipient_id=${recipientId}`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Ошибка отправки сообщения');
        }

        alert('Сообщение успешно отправлено!');
        document.getElementById('botMessageInput').value = '';
    } catch (error) {
        console.error('Error:', error);
        alert(error.message || 'Ошибка при отправке сообщения');
    }
});

// Инициализация страницы
document.addEventListener('DOMContentLoaded', () => {
    console.log('Dashboard loaded');
    getUserInfo();
    getMessageStats();
    loadUsers();
}); 