# secure-user-log-app-model
A full-stack web application deployed on Google Cloud Platform that: Authenticates users via Google OAuth through Identity-Aware Proxy Stores user activity in a private MySQL database Sends notifications through Google Pub/Sub messaging Operates entirely on a private network for maximum security


secure-user-log-app/
├── app.py
├── requirements.txt
├── runtime.txt
├── Procfile
├── .env
├── .gitignore
├── README.md
└── templates/
    ├── dashboard.html
    ├── unauthorized.html
    └── email_form.html

    # Secure User Activity Log App

A Flask web application for user activity logging and notifications.

## Features
- User authentication and authorization
- Activity logging
- Notification system
- Real-time updates

## Live Demo
Access the application at: [Your deployed URL will appear here]

## Local Development
```bash
pip install -r requirements.txt
python app.py




Project name:
Restricted Email Login API (Flask + SQLite)

Description (bullets):

Built a lightweight Flask REST API that validates login requests against a strict allow‑list of corporate emails backed by an SQLite database.​

Implemented database auto‑initialization to create a users table and seed it with approved email IDs, ensuring only predefined users can access the system.​

Designed a clean JSON contract for /login with clear success and failure responses, enabling easy integration with Postman, curl, or frontend clients.​

Versioned the full codebase on GitHub/Bitbucket with a documented architecture and setup guide, improving reproducibility and team onboarding.​

Business value (optional bullets):

Reduced unauthorized access risk by enforcing a controlled email allow‑list at the API layer instead of relying on client-side checks.​

Simplified demos and PoCs by providing a ready‑to‑run, file‑based database that requires no external DB server setup.​

If you share your final GitHub URL and actual deployment platform, this can be further customized with concrete metrics
