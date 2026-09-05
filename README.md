# 🌱 Carbon Intelligence Platform

A web-based **Environmental Intelligence and Carbon Accounting Platform** that helps organizations calculate, monitor, and analyze their carbon emissions.

## ✨ Features

- 🔐 Login interface
- 📊 Executive emissions dashboard
- 🌍 Scope 1, Scope 2 and Scope 3 tracking
- 🧮 Emission factor based CO₂e calculations
- 📈 Emissions visualization using charts
- 🤖 Rule-based anomaly detection
- 🌱 Carbon reduction what-if scenarios
- 🎯 Reduction target and progress tracking
- 🤝 Supplier engagement and carbon scoring
- ✅ Data quality and audit status

## 🛠️ Technology Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, FastAPI
- **Database:** SQLite with SQLAlchemy
- **Charts:** Chart.js
- **Development:** VS Code, Git, GitHub

📁 Project Structure
carbon-intelligence/
│
├── static/
│   ├── index.html
│   ├── login.html
│   ├── script.js
│   └── style.css
│
├── database.py
├── main.py
├── requirements.txt
└── .gitignore


🚀 How to Run in VS Code
1. Clone the repository
git clone https://github.com/sidhi-narlawar/carbon-intelligence.git
cd carbon-intelligence

2. Create a virtual environment
python -m venv venv

3. Activate the virtual environment
macOS / Linux:
source venv/bin/activate
Windows:
venv\Scripts\activate

4. Install dependencies:
pip install -r requirements.txt
Or install manually:
pip install fastapi uvicorn sqlalchemy

5. Start the FastAPI server
uvicorn main:app --reload

6. Open the Login Page
http://127.0.0.1:8000/static/login.html
Demo Login
Email: admin@nexgile.com
Password: admin123
The application will run at:
http://127.0.0.1:8000

