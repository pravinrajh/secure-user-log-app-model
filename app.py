from flask import Flask, render_template, request, session, jsonify
from datetime import datetime
import os
import json
import sqlite3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-for-production')

# SQLite Database Configuration
DB_PATH = 'secure_app.db'

# Configuration
ALLOWED_USERS = [
    'gcptrail0@gmail.com',
    'pravinrajagcp@gmail.com', 
    'parthibank72@gmail.com'
]

def create_database_connection():
    """Create and return SQLite database connection"""
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.row_factory = sqlite3.Row
        logger.info("✅ Connected to SQLite database")
        return connection
    except Exception as e:
        logger.error(f"❌ Error connecting to SQLite: {e}")
        return None

def initialize_database():
    """Initialize database tables and data"""
    connection = create_database_connection()
    if connection:
        try:
            cursor = connection.cursor()
            
            # Create users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create user_activity_logs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_activity_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_email TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    activity_type TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create unauthorized_access_logs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS unauthorized_access_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    reason TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Insert allowed users if they don't exist
            for user_email in ALLOWED_USERS:
                cursor.execute(
                    "INSERT OR IGNORE INTO users (email) VALUES (?)",
                    (user_email,)
                )
            
            connection.commit()
            logger.info("✅ Database tables initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Error initializing database: {e}")
        finally:
            connection.close()

def execute_query(query, params=None, fetch=False):
    """Execute SQL query and return results if fetch=True"""
    connection = create_database_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor()
        cursor.execute(query, params or ())
        
        if fetch:
            result = [dict(row) for row in cursor.fetchall()]
        else:
            connection.commit()
            result = cursor.lastrowid
        
        return result
    except Exception as e:
        logger.error(f"❌ Database query error: {e}")
        return None
    finally:
        connection.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    """Main application page"""
    if request.method == 'POST':
        email = request.form.get('email')
        session['user_email'] = email
        session['user_name'] = email.split('@')[0]
        return f"""
        <script>
            localStorage.setItem('user_email', '{email}');
            localStorage.setItem('user_name', '{email.split('@')[0]}');
            window.location.href = '/';
        </script>
        """
    
    # Check if user is logged in via session or localStorage
    user_email = session.get('user_email')
    if not user_email and request.args.get('email'):
        user_email = request.args.get('email')
        session['user_email'] = user_email
        session['user_name'] = user_email.split('@')[0]
    
    if not user_email:
        return render_template('email_form.html')
    
    user_name = session.get('user_name', user_email.split('@')[0])
    
    # Check if user is authorized in database
    user_exists = execute_query(
        "SELECT id FROM users WHERE email = ?", 
        (user_email,), 
        fetch=True
    )
    
    if not user_exists:
        # Log unauthorized access to database
        execute_query(
            "INSERT INTO unauthorized_access_logs (email, reason) VALUES (?, ?)",
            (user_email, 'User not in allowed list')
        )
        return render_template('unauthorized.html', 
                             user_email=user_email, 
                             user_name=user_name)
    
    # Log page load activity to database
    execute_query(
        "INSERT INTO user_activity_logs (user_email, activity_type) VALUES (?, ?)",
        (user_email, 'Page Load')
    )
    
    # Get recent logs for this user from database
    recent_logs = execute_query(
        "SELECT id, user_email, timestamp, activity_type " 
        "FROM user_activity_logs WHERE user_email = ? "
        "ORDER BY timestamp DESC LIMIT 10",
        (user_email,),
        fetch=True
    )
    
    return render_template('dashboard.html', 
                         user_email=user_email,
                         user_name=user_name,
                         logs=recent_logs or [])

@app.route('/api/logs')
def get_logs_api():
    """API endpoint to get user logs from database"""
    user_email = session.get('user_email') or request.args.get('user_email')
    if not user_email:
        return jsonify({'error': 'Not logged in'}), 401
    
    # Check if user is authorized
    user_exists = execute_query(
        "SELECT id FROM users WHERE email = ?", 
        (user_email,), 
        fetch=True
    )
    
    if not user_exists:
        return jsonify({'error': 'Access denied'}), 403
    
    # Get logs from database
    logs = execute_query(
        "SELECT id, user_email, timestamp, activity_type " 
        "FROM user_activity_logs WHERE user_email = ? "
        "ORDER BY timestamp DESC LIMIT 10",
        (user_email,),
        fetch=True
    )
    
    return jsonify({'logs': logs or []})

@app.route('/api/send-notification', methods=['POST'])
def send_notification():
    """API endpoint to send notification and log to database"""
    user_email = session.get('user_email') or request.json.get('user_email')
    if not user_email:
        return jsonify({'error': 'Not logged in'}), 401
    
    # Check if user is authorized
    user_exists = execute_query(
        "SELECT id FROM users WHERE email = ?", 
        (user_email,), 
        fetch=True
    )
    
    if not user_exists:
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        # Log notification activity to database
        execute_query(
            "INSERT INTO user_activity_logs (user_email, activity_type) VALUES (?, ?)",
            (user_email, 'Notification Sent')
        )
        
        logger.info(f"📧 Notification logged for user: {user_email}")
        
        return jsonify({
            'status': 'Notification sent successfully!',
            'message_id': f"msg-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'user_email': user_email,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"❌ Error sending notification: {e}")
        return jsonify({'error': 'Failed to send notification'}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy', 
        'service': 'Secure User Activity Log App',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/debug')
def debug():
    """Debug information"""
    users = execute_query("SELECT * FROM users", fetch=True) or []
    activity_logs = execute_query("SELECT * FROM user_activity_logs ORDER BY id DESC LIMIT 10", fetch=True) or []
    unauthorized_logs = execute_query("SELECT * FROM unauthorized_access_logs ORDER BY id DESC LIMIT 10", fetch=True) or []
    
    return jsonify({
        'users_count': len(users),
        'activity_logs_count': len(activity_logs),
        'unauthorized_attempts': len(unauthorized_logs),
        'allowed_users': ALLOWED_USERS,
        'recent_activity': activity_logs,
        'session_data': dict(session)
    })

# Initialize database when app starts
initialize_database()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
