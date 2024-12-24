const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();

// Настройка CORS
app.use(cors({
  origin: '*', // В продакшене замените на конкретные домены
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true
}));

app.use(express.json());

// Маршрут для регистрации
app.post('/auth/register', (req, res) => {
  try {
    const { email, password } = req.body;
    // Здесь ваша логика регистрации
    res.status(200).json({ 
      message: 'Registration successful',
      user: { email }
    });
  } catch (error) {
    res.status(500).json({ 
      message: 'Registration failed',
      error: error.message 
    });
  }
});

// Обработка OPTIONS запросов
app.options('*', cors());

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
  console.log(`Environment: ${process.env.NODE_ENV}`);
}); 