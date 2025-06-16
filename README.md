# 🚀 Django REST API with JWT, Celery, Telegram Bot & Render Deployment

> A robust backend project built with **Django REST Framework**, JWT authentication, **Celery with Redis**, and **Telegram Bot integration**, all deployed live on **Render**. Developed on **Ubuntu via WSL** for maximum compatibility and scalability.

---

## 📌 Table of Contents

* [📦 Features](#-features)
* [🛠 Tech Stack](#-tech-stack)
* [🧑‍💻 Setup on Ubuntu (via WSL)](#-setup-on-ubuntu-via-wsl)
* [⚙️ Local Development Setup](#️-local-development-setup)
* [🔐 Environment Variables](#-environment-variables)
* [📬 API Endpoints](#-api-endpoints)
* [🤖 Telegram Bot Integration](#-telegram-bot-integration)
* [🚀 Deployment (Render)](#-deployment-render)
* [📂 Project Structure](#-project-structure)
* [📸 Screenshots](#-screenshots)

---

## 📦 Features

* ✅ Django REST Framework with JWT-based authentication
* ✅ Public and protected API endpoints
* ✅ Django Login for admin panel
* ✅ Celery for background tasks (e.g., sending emails)
* ✅ Redis as Celery broker
* ✅ Telegram Bot integration with webhook support
* ✅ Deployment on Render with secure `.env` support

---

## 🛠 Tech Stack

| Tool              | Purpose                                       |
| ----------------- | --------------------------------------------- |
| Django + DRF      | Backend API Framework                         |
| PostgreSQL/SQLite | Database                                      |
| Celery + Redis    | Background Task Queue                         |
| Telegram API      | Bot integration                               |
| JWT (SimpleJWT)   | Auth system                                   |
| Render.com        | Deployment Platform                           |
| Ubuntu (WSL)      | Dev Environment (Windows Subsystem for Linux) |

---

## 🧑‍💻 Setup on Ubuntu (via WSL)

If you're on **Windows**, follow these to enable Ubuntu setup:

1. ✅ Enable WSL:

   ```powershell
   wsl --install
   ```

2. ✅ Install Ubuntu from Microsoft Store (Ubuntu 22.04 recommended)

3. ✅ Install system dependencies:

   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv redis-server
   ```

4. ✅ Start Redis:

   ```bash
   sudo service redis-server start
   ```

5. ✅ Clone your repo and follow setup instructions below ⬇️

---

## ⚙️ Local Development Setup

```bash
# 1. Clone the repo
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install requirements
pip install -r requirements.txt

# 4. Create .env file
cp .env.example .env  # or create manually using the format below

# 5. Run initial setup
python manage.py migrate
python manage.py createsuperuser  # create admin user
python manage.py runserver
```

---

## 🔐 Environment Variables

Create a `.env` file in your root folder with:

```env
SECRET_KEY=your_django_secret
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
EMAIL_USE_TLS=True

# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token

# Redis/Celery
CELERY_BROKER_URL=redis://localhost:6379/0
```

---

## 📬 API Endpoints

| Endpoint                 | Method | Auth     | Description                       |
| ------------------------ | ------ | -------- | --------------------------------- |
| `/api/public/`           | GET    | ❌ Public | Public message                    |
| `/api/protected/`        | GET    | ✅ JWT    | Protected for authenticated users |
| `/api/register/`         | POST   | ❌ Public | User registration with email task |
| `/api/token/`            | POST   | ❌ Public | Obtain access and refresh tokens  |
| `/api/token/refresh/`    | POST   | ❌ Public | Refresh JWT token                 |
| `/api/telegram-webhook/` | POST   | Telegram | Handles `/start` from Telegram    |

---

## 🤖 Telegram Bot Integration

* Create a bot via [@BotFather](https://t.me/BotFather)
* Get your `TELEGRAM_BOT_TOKEN`
* Set webhook using this command:

```bash
curl -X POST "https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook" \
-d "url=https://your-render-url.onrender.com/api/telegram-webhook/"
```

* Now when users send `/start`, their Telegram details are saved in your database!

---

## 🚀 Deployment (Render)

1. Push code to GitHub
2. Create a **Web Service** on [Render](https://render.com)
3. Set:

   * Build Command: `pip install -r requirements.txt`
   * Start Command: `gunicorn backend.wsgi`
4. Add Environment Variables from `.env`
5. Click **Deploy**
6. Set the Telegram webhook using your live Render URL

---

## 📂 Project Structure

```
backend/
├── backend/               # Django project root
│   └── settings.py        # Environment, REST, Celery configs
├── core/                  # Main app (views, models, tasks)
│   └── views.py           # Public, protected, Telegram webhook
├── manage.py
├── requirements.txt
└── .env                   # Environment variables
```

---

## 📸 Screenshots

### 🔓 Public Endpoint
> `GET /api/public/`

![Public Endpoint](screenshots/public_endpoint.png)

---

### 🔐 Protected Endpoint (JWT Required)
> `GET /api/protected/` (with token)

![Protected Endpoint](screenshots/protected_endpoint.png)

---

### 📬 Email After Registration
> Triggered after `POST /api/register/`

![Registration Email](screenshots/email_sent.png)

---

### 🤖 Telegram /start Integration
> Bot receives `/start` and saves user

![Telegram Start](screenshots/telegram_start.png)

---

### 🛠 Django Admin Panel
> User and TelegramUser models

![Admin Panel](screenshots/admin_panel.png)

---

## 🧠 Pro Tip

If you're on Windows, using **Ubuntu via WSL** avoids issues with Celery multiprocessing. Always run Celery like this:

```bash
celery -A backend worker --loglevel=info --pool=solo
```

---

## 💬 Final Words

This project checks all backend boxes: ✅ API Auth
✅ Background Tasks
✅ Messaging Bot
✅ Docker/Deploy ready

&#x20;💼🔥
