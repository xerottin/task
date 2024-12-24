const express = require('express');
const cors = require('cors');
const app = express();

// Настройка CORS для Firebase
app.use(cors({
  origin: [
    'https://your-firebase-app.web.app',     // Замените на ваш домен Firebase
    'https://your-firebase-app.firebaseapp.com',
    'http://localhost:3000'  // Для локальной разработки
  ],
  credentials: true
}));

// Остальные middleware
app.use(express.json());

// Пример middleware для проверки Firebase Auth токена
const admin = require('firebase-admin');

admin.initializeApp({
  credential: admin.credential.cert({
    projectId: process.env.FIREBASE_PROJECT_ID,
    clientEmail: process.env.FIREBASE_CLIENT_EMAIL,
    privateKey: process.env.FIREBASE_PRIVATE_KEY.replace(/\\n/g, '\n')
  })
});

// Ваши роуты...

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
}); 