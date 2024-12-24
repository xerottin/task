const API_URL = 'https://your-railway-domain.up.railway.app';

console.log('main.js loaded');

// Функция для переключения между формами
function setupTabSwitching() {
    document.querySelectorAll('.tab-btn').forEach(button => {
        button.addEventListener('click', () => {
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            const formId = button.dataset.tab === 'login' ? 'loginForm' : 'registerForm';
            document.querySelectorAll('.auth-form').forEach(form => form.classList.add('hidden'));
            document.getElementById(formId).classList.remove('hidden');
        });
    });
}

// Функция для обработки входа
async function handleLogin(username, password) {
    try {
        console.log('Attempting login with:', { username });
        
        const formData = `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`;
        console.log('Request body:', formData);
        
        const response = await fetch(`${API_URL}/auth/token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData
        });
        
        console.log('Response status:', response.status);
        const data = await response.json();
        console.log('Response data:', data);
        
        if (!response.ok) {
            throw new Error(data.detail || 'Ошибка входа');
        }

        console.log('Login successful, token:', data.access_token);
        localStorage.setItem('token', data.access_token);
        window.location.href = '/dashboard.html';
    } catch (error) {
        console.error('Login error:', error);
        throw error;
    }
}

// Функция для обработки регистрации
async function handleRegistration(email, username, password) {
    try {
        console.log('Attempting registration for:', username);
        
        const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email,
                username,
                password
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Ошибка регистрации');
        }

        console.log('Registration successful');
        return true;
    } catch (error) {
        console.error('Registration error:', error);
        throw error;
    }
}

// Инициализация форм при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded');
    
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    
    if (!loginForm || !registerForm) {
        console.error('Forms not found!');
        return;
    }

    // Настраиваем переключение вкладок
    setupTabSwitching();

    // Обработчик формы входа
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        console.log('Login form submitted');
        
        const username = document.getElementById('loginUsername').value;
        const password = document.getElementById('loginPassword').value;
        
        try {
            await handleLogin(username, password);
        } catch (error) {
            alert(error.message || 'Ошибка при попытке входа');
        }
    });

    // Обработчик формы регистрации
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        console.log('Register form submitted');
        
        const email = document.getElementById('regEmail').value;
        const username = document.getElementById('regUsername').value;
        const password = document.getElementById('regPassword').value;
        
        try {
            await handleRegistration(email, username, password);
            alert('Регистрация успешна! Теперь вы можете войти.');
            document.querySelector('[data-tab="login"]').click();
        } catch (error) {
            alert(error.message || 'Ошибка при попытке регистрации');
        }
    });
}); 