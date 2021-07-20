const express = require('express');
const session = require('express-session');
const sqlite3 = require('sqlite3').verbose();

const app = express();
app.use(express.static('static'));
app.use(express.urlencoded({extended: true}));
app.use(express.json());
app.use(session({ secret: process.env.SECRET, saveUninitialized: false, resave: false }));

const user_db = new sqlite3.Database(':memory:');
const location_db = new sqlite3.Database(':memory:');

const port = 3000;

app.post('/api/login', (req, res) => {
  const {username, password} = req.body;
  
  user_db.get(`SELECT username FROM users WHERE username="${username}" AND password="${password}"`, (err, row) => {
    if(err) {
      res.status(400).send({ err: err.message });
    } else if (row && row.username && row.username == 'admin') {
      req.session.loggedIn = true;
      res.redirect("/covid.html");
    } else {
      res.status(403).send({ err: "Incorrect Login" });
    }
  });
});

app.post('/api/locations', (req, res) => {
  if(req.session.loggedIn === undefined || req.session.loggedIn === false) {
    res.sendStatus(403);
    return;
  }
  const {search} = req.body;
    
  location_db.all(`SELECT name, geo, cases FROM locations WHERE name LIKE "${'%' + search + '%'}"`, (err, rows) => {
    if(err) {
      res.status(400).send({ err: err.message });
    } else if (rows) {
      res.json(rows);
    }
  });
})


user_db.serialize(() => {
  user_db.run("CREATE TABLE users(username TEXT, password TEXT)");
  const password = process.env.ADMIN_PASSWORD;
  user_db.run("INSERT INTO users VALUES (?, ?)", "admin", password);
});

location_db.serialize(() => {
  location_db.run("CREATE TABLE locations(name TEXT, geo TEXT, cases INT)");
  location_db.run("CREATE TABLE flag(value TEXT)");
  location_db.run("INSERT INTO locations VALUES (?, ?, ?)", "Bukit Batok", "1.359165737350038, 103.76271107619375", 123);
  location_db.run("INSERT INTO locations VALUES (?, ?, ?)", "NUS", "1.2971374643210083, 103.77635831153047", 43);
  location_db.run("INSERT INTO locations VALUES (?, ?, ?)", "Pasir Ris", "1.37635430359135, 103.94570985251505", 62);
  location_db.run("INSERT INTO locations VALUES (?, ?, ?)", "Changi Airport", "1.3642914894747193, 103.99165954341039", 121);
  location_db.run("INSERT INTO locations VALUES (?, ?, ?)", "Tekong Island", "1.417049237194686, 104.03895113481549", 71);
  
  const flag = process.env.FLAG;
  location_db.run("INSERT INTO flag VALUES (?)", flag); // catch me if you can!
});

app.listen(port, () => {
  console.log(`Listening at port ${3000}`);
})
