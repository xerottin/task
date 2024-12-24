const express = require('express');
const app = express();

app.use(express.json());

// Тестовый эндпоинт
app.get('/', (req, res) => {
  res.json({ message: 'Backend is working!' });
});

// Добавим эндпоинт для проверки переменных окружения
app.get('/env-check', (req, res) => {
  res.json({ 
    environment: process.env.NODE_ENV,
    serverTime: new Date().toISOString()
  });
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
  console.log(`Environment: ${process.env.NODE_ENV}`);
}); 