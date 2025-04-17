const express = require("express");
const fs = require("fs");
const path = require("path");

const app = express();
const PORT = 3000;
const USERS_FILE = path.join(__dirname, "users.json");


app.use(express.static("public"));
app.use(express.json());


const loadUsers = () => {
  if (!fs.existsSync(USERS_FILE)) return [];
  const data = fs.readFileSync(USERS_FILE, "utf-8");
  return JSON.parse(data || "[]");
};

const saveUsers = (users) => {
  fs.writeFileSync(USERS_FILE, JSON.stringify(users, null, 2));
};


app.post("/signup", (req, res) => {
  const { email, password } = req.body;
  const users = loadUsers();

  const userExists = users.find((user) => user.email === email);
  if (userExists) {
    return res.status(400).json({ message: "Email already registered!" });
  }

  users.push({ email, password });
  saveUsers(users);
  res.status(200).json({ message: "Signup successful!" });
});


app.post("/login", (req, res) => {
  const { email, password } = req.body;
  const users = loadUsers();

  const user = users.find(
    (user) => user.email === email && user.password === password
  );

  if (user) {
    res.status(200).json({ message: "Login successful!" });
  } else {
    res.status(401).json({ message: "Invalid email or password!" });
  }
});


app.listen(PORT, () => {
  console.log(`🚀 Server running at http://localhost:${PORT}`);
});
