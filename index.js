const express = require('express');
const app = express();

app.use(express.json());

// Тестовый эндпоинт
app.get('/', (req, res) => {
  res.json({ message: 'Backend is working!' });
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
}); 