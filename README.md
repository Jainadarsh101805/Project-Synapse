# 🧠 Project Synapse

### 🚀 Overview
**Project Synapse** is a smart, citizen-focused platform designed to simplify access to various **government schemes and services**.  
It helps users explore, understand, and apply for schemes easily — bridging the gap between citizens and technology.

---

### 💡 Features
- 🔍 Easy access to multiple government schemes  
- 👤 User-friendly interface for registration and login  
- 📜 Scheme eligibility check and recommendations  
- 📩 Notifications and updates on applied schemes  
- ☁️ Cloud-based backend with **FastAPI** and **AWS** integration  
- 📊 Admin dashboard for analytics and monitoring  

---

### 🧰 Tech Stack
| Component | Technology Used |
|------------|------------------|
| **Frontend** | HTML, CSS, JavaScript, React, Tailwind, |
| **Backend** | Python, FastAPI, AI Chatbot, LLM |
| **Database** | SQL |
| **Hosting** | AWS / Render / GitHub Pages |
| **Version Control** | Git & GitHub |

---

### ⚙️ Installation & Setup
Follow these steps to run the project locally:

```bash
# Clone this repository
git clone https://github.com/Jainadarsh101805/Project-Synapse.git

# Move into the project folder
cd Project-Synapse

# Backend setup
cd Backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend setup (if applicable)
cd frontend
npm install
npm start
