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
