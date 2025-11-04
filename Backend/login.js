const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(bodyParser.json());

// Dummy user (later connect DB with Prisma)
const USER = { username: "admin", password: "1234" };

app.post("/login", (req, res) => {
  const { username, password } = req.body;

  if (username === USER.username && password === USER.password) {
    res.json({ message: "Login successful ✅" });
  } else {
    res.json({ message: "Invalid credentials ❌" });
  }
});

app.listen(5000, () => console.log("Server running on http://localhost:5000"));
