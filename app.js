const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');

const path = require('path');
const app = express();

// Połączenie z bazą danych MongoDB
mongoose.connect('mongodb://0.0.0.0:27017/Bilety', {
  useNewUrlParser: true,
  useUnifiedTopology: true
})
.then(() => {
  console.log('Connected to MongoDB');
})
.catch((err) => {
  console.error(err);
});

// Define user schema and model
const userSchema = new mongoose.Schema({
    name: String,
    email: String,
    password: String
  });
  
  const User = mongoose.model('User', userSchema);
  
  // Define endpoints for CRUD operations on users
  app.get('/users', (req, res) => {
    User.find()
      .then(users => res.json(users))
      .catch(err => res.status(500).json({ error: err.message }));
  });
  
  app.get('/users/:userId', (req, res) => {
    User.findById(req.params.userId)
      .then(user => res.json(user))
      .catch(err => res.status(500).json({ error: err.message }));
  });
  
  app.post('/users', (req, res) => {
    const newUser = new User(req.body);
    newUser.save()
      .then(user => res.json(user))
      .catch(err => res.status(500).json({ error: err.message }));
  });
  
  app.put('/users/:userId', (req, res) => {
    User.findByIdAndUpdate(req.params.userId, req.body)
      .then(user => res.json(user))
      .catch(err => res.status(500).json({ error: err.message }));
  });
  
  app.delete('/users/:userId', (req, res) => {
    User.findByIdAndDelete(req.params.userId)
      .then(user => res.json(user))
      .catch(err => res.status(500).json({ error: err.message }));
  });

// Serve static files from the public directory
app.use(express.static(path.join(__dirname, 'public')));

app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(4000, () => {
  console.log('Server started on port 4000');
});