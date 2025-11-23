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
