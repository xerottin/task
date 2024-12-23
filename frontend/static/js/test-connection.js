const API_URL = 'http://localhost:5001';

async function testConnection() {
    try {
        const response = await fetch(`${API_URL}/test/ping`, {
            method: 'GET',
            mode: 'cors',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        console.log('Connection test:', data);
        return true;
    } catch (error) {
        console.error('Connection test error:', error);
        console.error('Error details:', {
            name: error.name,
            message: error.message,
            stack: error.stack
        });
        return false;
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    console.log('Starting connection test...');
    try {
        const isConnected = await testConnection();
        if (!isConnected) {
            console.error('Connection test failed');
            alert('Не удалось подключиться к серверу. Проверьте консоль для деталей.');
        } else {
            console.log('Connection test successful');
        }
    } catch (error) {
        console.error('Error during connection test:', error);
    }
}); 