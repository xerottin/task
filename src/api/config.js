const API_URL = process.env.NODE_ENV === 'production' 
  ? 'https://your-railway-app.railway.app'  // URL вашего Railway приложения
  : 'http://localhost:3000';                // Локальный адрес для разработки

export default API_URL; 