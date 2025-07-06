# WhatsApp Microlearning Coach

**Empowering users with bite-sized learning directly on WhatsApp, powered by AI and a robust full-stack system.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

---

## 🎯 About The Project

The WhatsApp Microlearning Coach is a comprehensive system designed to deliver engaging, bite-sized educational content directly to users via WhatsApp. It combines the power of a Python Flask backend with a MySQL database, a web-based admin interface, and seamless WhatsApp integration through Twilio. This platform is ideal for automating educational content delivery, tracking user progress, and enabling flexible monetization.

### Problem Solved
Small businesses and individual educators often face challenges in delivering engaging, accessible, and trackable learning content. Traditional e-learning platforms can be expensive and complex. This system provides a low-barrier-to-entry solution for delivering structured micro-lessons directly to users' most used communication channel.

### Solution
A robust, scalable platform that automates lesson delivery, tracks user progress, manages subscriptions, and offers an intuitive admin interface, all accessible via WhatsApp. It empowers content creators to monetize their knowledge effectively through various subscription tiers and value-added features.

---

## 📋 Table of Contents
-   [🎯 About The Project](#-about-the-project)
    -   [Problem Solved](#problem-solved)
    -   [Solution](#solution)
-   [✨ Key Features](#-key-features)
    -   [WhatsApp Bot Capabilities](#whatsapp-bot-capabilities)
    -   [Admin Dashboard](#admin-dashboard)
    -   [Monetization Features](#monetization-features)
-   [🛠️ Tech Stack](#️-tech-stack)
-   [🏛️ System Architecture](#️-system-architecture)
    -   [Backend](#backend)
    -   [Frontend](#frontend)
    -   [Database Schema](#database-schema)
-   [💬 WhatsApp Commands](#-whatsapp-commands)
-   [💰 Revenue Streams](#-revenue-streams)
-   [🚀 Getting Started](#-getting-started)
    -   [Prerequisites](#prerequisites)
    -   [Project Structure](#project-structure)
    -   [Installation](#installation)
    -   [Configuration](#configuration)
    -   [Database Setup](#database-setup)
    -   [Running the Application](#running-the-application)
    -   [WhatsApp Webhook Configuration](#whatsapp-webhook-configuration)
-   [🤝 Contributing](#-contributing)
-   [📄 License](#-license)
-   [📞 Contact](#-contact)

---

## ✨ Key Features

### WhatsApp Bot Capabilities:
* **Automated Welcome**: Greets new users upon joining.
* **Personalized Daily Lessons**: Delivers lessons tailored to user progress and preferences.
* **Learning Progress & Streaks**: Tracks user engagement and learning consistency.
* **Subscription Management**: Handles user subscriptions directly via WhatsApp.
* **Interactive Quizzes**: Sends quizzes and collects responses to assess understanding.
* **Certificate Generation**: Automatically generates completion certificates for courses.

### Admin Dashboard:
* **User Management**: Oversee user accounts and activity.
* **Analytics**: Gain insights into user engagement and learning patterns.
* **Lesson Content Management**: Easily add, edit, and organize learning content.
* **Subscription Tracking**: Monitor active subscriptions and revenue.
* **Bulk Messaging**: Send announcements or updates to user segments.

### Monetization Features:
* **Flexible Subscription Tiers**: Supports Daily, Weekly, and Premium plans.
* **Stripe Integration**: Secure and reliable payment processing.
* **Certificate Generation**: Monetize completed courses with digital skill certificates.
* **Progress Tracking & Gamification**: Enhances user engagement, encouraging continued subscription.

---

## 🛠️ Tech Stack

* **Backend**: Python (Flask)
* **WhatsApp Integration**: Twilio API
* **Database**: MySQL
* **Payment Processing**: Stripe
* **Frontend (Admin/Landing)**: HTML, CSS, JavaScript (Bootstrap for responsive design)
* **Certificate Generation**: Custom Python modules (likely Pillow for image manipulation, PDF libraries for PDF generation)

---

## 🏛️ System Architecture

The system is built with a modular design to ensure scalability and ease of expansion.

### Backend
The heart of the system is a Python Flask application. It handles:
* Receiving incoming WhatsApp messages via Twilio webhooks.
* Processing user commands and routing them to appropriate functions.
* Interacting with the MySQL database for data storage and retrieval.
* Scheduling and delivering automated lessons.
* Managing Stripe payments and webhooks.
* Generating certificates dynamically.

### Frontend
A web-based interface provides:
* A public-facing landing page to showcase features and pricing.
* A secure admin dashboard for content creators and administrators to manage users, lessons, and subscriptions.

### Database Schema
The MySQL database is structured to efficiently store and manage all essential data:
* `Users`: User profiles, WhatsApp numbers, subscription status, last active time.
* `Lessons`: Lesson content, categories, sequence.
* `Categories`: Grouping for lessons.
* `Progress Tracking`: Records user's lesson completion, quiz scores, streaks.
* `Subscriptions`: Details of user subscriptions (tier, start/end dates, payment status).
* `Message Logging`: Stores incoming and outgoing messages for analytics and debugging.

---

## 💬 WhatsApp Commands

Users can interact with the bot using the following commands:

* `START` - Begin learning journey and receive the first lesson.
* `LESSON` - Get today's scheduled lesson.
* `PROGRESS` - View personal learning statistics and streaks.
* `SUBSCRIBE` - View available subscription plans and pricing.
* `HELP` - Receive assistance and a list of available commands.

---

## 💰 Revenue Streams

The platform offers multiple avenues for monetization:

* **Subscription Plans**: Ranging from `$2.99/week` to `$29.99/month`.
* **Certificates**: Selling digital skill certificates upon course completion.
* **Premium Features**: Offering add-ons like 1-on-1 coaching sessions or job placement assistance.
* **Partnership**: Collaborating with training institutes to offer their content or services.

---

## 🚀 Getting Started

Follow these steps to get your WhatsApp Microlearning Coach system up and running.

### Prerequisites
Ensure you have the following installed on your system:
* Python 3.8+
* pip (Python package installer)
* MySQL Server
* Git (for cloning the repository)
* A Twilio account with a WhatsApp-enabled phone number.
* A Stripe account for payment processing.

### Project Structure
```
whatsapp-microlearning-coach/
├── scripts/                # Database setup scripts, utility scripts
├── templates/              # HTML templates for admin dashboard and landing page
├── utils/                  # Helper functions (e.g., Twilio API wrappers, Stripe helpers)
├── WhatsappVenv/           # Python virtual environment
├── pycache/            # Python cache files
├── .env                    # Environment variables (copied from .env.example)
├── app.py                  # Main Flask application
├── config.py               # Application configuration
├── requirements.txt        # Python dependencies
└── README.md             # Project documentation

```

---


### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-repo-link/whatsapp-microlearning-coach.git](https://github.com/your-repo-link/whatsapp-microlearning-coach.git)
    cd whatsapp-microlearning-coach
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv WhatsappVenv
    # On Windows:
    .\WhatsappVenv\Scripts\activate
    # On macOS/Linux:
    source WhatsappVenv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1.  **Create `.env` file:**
    Copy the example environment file:
    ```bash
    cp .env.example .env
    ```

2.  **Edit `.env` file:**
    Open the newly created `.env` file and add your credentials for Twilio, Stripe, and MySQL.
    (Example content for `.env.example` would typically be provided with the project)

    ```env
    # Twilio Credentials
    TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    TWILIO_AUTH_TOKEN=your_twilio_auth_token
    TWILIO_WHATSAPP_NUMBER=+1xxxxxxxxxx

    # MySQL Database Credentials
    DB_HOST=localhost
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_NAME=whatsapp_learning

    # Stripe Credentials
    STRIPE_SECRET_KEY=sk_test_xxxxxxxxxxxxxxxxxxxx
    STRIPE_PUBLISHABLE_KEY=pk_test_xxxxxxxxxxxxxxxxxxxx
    STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxxxxxxxxx

    # Flask App Secret Key
    FLASK_SECRET_KEY=your_flask_secret_key_for_sessions
    ```

### Database Setup

1.  **Run the SQL setup script:**
    This script will create the necessary tables in your MySQL database. Ensure your MySQL server is running and you have configured the `DB_USER` and `DB_PASSWORD` in your `.env` correctly.

    ```bash
    mysql -u your_db_user -p your_db_name < database_setup.sql
    ```
    (You will be prompted for your MySQL password)

2.  **Insert sample lessons and categories (Optional):**
    If your `database_setup.sql` doesn't include sample data, you might have separate scripts or an admin interface to add initial content.

### Running the Application

1.  **Start the Flask application:**
    ```bash
    python app.py
    ```
    The application will typically run on `http://127.0.0.1:5000` (or another port if configured).

### WhatsApp Webhook Configuration

1.  **Deploy your application:**
    For Twilio to reach your local server, you'll need to deploy your Flask application to a publicly accessible URL (e.g., using Ngrok for local testing, or a cloud provider like Vercel, Heroku, AWS, etc.).

2.  **Configure Twilio Webhook:**
    In your Twilio console, navigate to your WhatsApp-enabled phone number settings.
    Set the "WHEN A MESSAGE COMES IN" webhook URL to:
    `https://yourdomain.com/webhook`
    Replace `yourdomain.com` with the public URL of your deployed application.

---

## 🤝 Contributing

We welcome contributions! If you'd like to contribute, please fork the repository, create a new branch for your features or bug fixes, and submit a pull request.

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file in the repository (if present) for details.

---

## 📞 Contact

For any inquiries or support, please reach out via:
* **Project Maintainer**: Derrick Karanja 
* **Portfolio**: [My portfolio](https://my-portfolio-project-dk-jr.vercel.app/)

---
