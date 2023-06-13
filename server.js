const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const dotenv = require('dotenv');
const opn = require('opn');


dotenv.config();
const app = express();
const PORT = process.env.PORT || 3000;

// Connect to the database
const db = new sqlite3.Database('journal_emails.db');

// Create the "users" table if it doesn't exist
db.run(`CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT NOT NULL,
  last_sent_date TEXT NOT NULL,
  start INTEGER NOT NULL,
  end INTEGER NOT NULL,
  interest TEXT NOT NULL
)`);

// Set up the views
app.set('view engine', 'ejs');
app.set('views', 'views');

// Middleware
app.use(express.urlencoded({
  extended: true
}));
app.use('/views', express.static('views'))


// Routes
app.get('/', (req, res) => {
  res.render('index', {
    error: null
  });
});

app.post('/interests', (req, res) => {
  const {
    email
  } = req.body;
  res.render('interests', {
    email
  });
});

app.post('/register', (req, res) => {
  const {
    email,
    interest
  } = req.body;
  const stmt = db.prepare('INSERT INTO users (email, last_sent_date, start, end, interest) VALUES (?, ?, ?, ?, ?)');
  stmt.run(email, new Date().toISOString(), 1, 5, interest);
  stmt.finalize();
  res.render('thankyou', {
    email
  });
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
  opn(`http://localhost:${PORT}`);
});

app.use(express.static('views' + '/public'));
