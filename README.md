# NarcoTrace

**NarcoTrace** is a full-stack intelligence platform for tracing illicit narcotics networks, combining a Django-powered AI backend with a React dashboard frontend and a Telegram bot interface. Investigators can upload shipment manifests, run AI-driven analysis (via Transformers models), visualize trends and geospatial data, and receive real-time alerts in Telegram.

---
## Collaborators

- [Aayush Meghal](https://github.com/Assassin2306)  
- [Atharva Dhavale](https://github.com/Atharva-Dhavale)  
- [Harshvardhan Bhosale](https://github.com/Harshbhosale05)  
- [Sarish Sonawane](https://github.com/Sarish05)  
- [Kartik Sirsilla](https://github.com/kartiksirsilla09)  
- [Sakshi Chougule](https://github.com/chougulesakshi1311)


## Table of Contents

- [Key Features](#key-features)  
- [Architecture & Tech Stack](#architecture--tech-stack)  
- [Directory Structure](#directory-structure)  
- [Prerequisites](#prerequisites)  
- [Installation & Setup](#installation--setup)  
  - [Backend](#backend)  
  - [Frontend](#frontend)  
- [Environment Configuration](#environment-configuration)  
- [Database & Migrations](#database--migrations)  
- [Running the Application](#running-the-application)  
- [Security Best Practices](#security-best-practices)  
- [Contributing](#contributing)  

---

## Key Features

- **AI-Driven Analysis**  
  – Leverages Hugging Face Transformers (e.g. RoBERTa) and Torch/TensorFlow pipelines to extract entities, detect anomalous patterns in manifests, and score risk.  
- **Telegram Bot Integration**  
  – Receive real-time alerts and query case summaries via a dedicated TeleBot (using `pyTelegramBotAPI`).  
- **RESTful API**  
  – Backend built on Django 4.2 + Django REST Framework 3.14 for secure, versioned endpoints.  
- **Interactive Dashboard**  
  – React (v18) + MUI for a responsive UI, with Chart.js visualizations (`react-chartjs-2`) and PDF exports (`jspdf`, `jspdf-autotable`).  
- **CORS & Security**  
  – Configured via `django-cors-headers` to allow frontend <> API communication, with environment-driven secrets and debug settings.  

---

## Architecture & Tech Stack

| Layer           | Tech & Libraries                                                                                   |
| --------------- | ------------------------------------------------------------------------------------------------- |
| Backend         | Django==4.2.10, djangorestframework==3.14.0, django-cors-headers==4.3.1                            |
| AI & ML         | transformers==4.36.2, torch==2.1.2, tensorflow==2.15.0.post1                                       |
| Bot Integration | telebot==0.0.5, pyTelegramBotAPI==4.14.0, requests==2.31.0                                          |
| Frontend        | React 18.3.1, MUI v6 (`@mui/material`, `@mui/icons-material`), Emotion, react-router-dom, axios    |
| Charts & Export | chart.js 4.4.4, react-chartjs-2 5.2.0, jspdf 2.5.1, jspdf-autotable 3.8.2                          |
| Database        | SQLite (via `DATABASE_URL=sqlite:///db.sqlite3` by default)                                        |

---

## Directory Structure

```text
NarcoTrace/
├── Backend/               # Django + AI Model + Telegram Bot
│   ├── myproject/         # Project settings & URLs
│   ├── myapp/             # Main application: models, views, serializers, AI routines
│   └── requirements.txt   # Python dependencies
└── Frontend/              # React-based investigative dashboard
    └── my-app/            # Create React App structure
        ├── public/        # Static assets & index.html
        ├── src/           # React components, pages, utils
        └── package.json   # JS dependencies & scripts
```
---

## Prerequisites

- **Python** ≥ 3.9  
- **Node.js** ≥ 18.0 & **npm** ≥ 9.0  
- **Git**  

---

## Installation & Setup

### Backend

1. Clone the repo and enter Backend:
   ```
   git clone https://github.com/Assassin2306/NarcoTrace.git
   cd NarcoTrace/Backend
   
2.Create and activate a venv:
   ```
   python -m venv venv
   source venv/bin/activate       # Windows: venv\Scripts\activate
```

3.Install Python dependencies:
   ```
   pip install -r requirements.txt
```
4.Copy and edit environment variables:
```
   cp .env.example .env
   # Fill in DJANGO_SECRET_KEY, NARCOTRACE_BOT_TOKEN, ROBERTA_MODEL_PATH, etc.
```
### Frontend
1.In another terminal, navigate to the React app:
```
   cd ../Frontend/my-app
```
2.Install JavaScript dependencies:
```
   npm install
```
### Environment Configuration
- Edit Backend/.env with your settings:
- DJANGO_SECRET_KEY=your-secret-key
- DEBUG=False
- ALLOWED_HOSTS=*
- CORS_ALLOWED_ORIGINS=http://localhost:3000
- CORS_ORIGIN_WHITELIST=http://localhost:3000
- NARCOTRACE_BOT_TOKEN=your-telegram-bot-token
- ROBERTA_MODEL_PATH=/absolute/path/to/roberta/model
- API_BASE_URL=http://127.0.0.1:8000
- DATABASE_URL=sqlite:///db.sqlite3

Database & Migrations
From Backend/:
```
   source venv/bin/activate
   python manage.py migrate
```

Running the Application
1.Start the Backend API & Bot
```
      cd Backend
      source venv/bin/activate
      python manage.py runserver
```
Django API: http://127.0.0.1:8000/
Telegram Bot will listen in the same process (ensure valid NARCOTRACE_BOT_TOKEN).

2.Start the Frontend Dashboard
```
   cd ../Frontend/my-app
   npm start
```
Open: http://localhost:3000/

## Security Best Practices
- Never commit real .env files—use .env.example only.

- Rotate DJANGO_SECRET_KEY and NARCOTRACE_BOT_TOKEN regularly.

- Use HTTPS in production and restrict ALLOWED_HOSTS.

- Limit CORS origins to trusted domains.

## Contributing
- Fork the repository

- Create a feature branch (git checkout -b feat/awesome)

- Commit changes (git commit -m "Add awesome feature")

- Push (git push origin feat/awesome)

- Open a Pull Request

Please follow standard best practices and include tests for new functionality.
