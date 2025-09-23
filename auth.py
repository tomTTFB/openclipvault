import hashlib
import os
import json
from functools import wraps
from flask import session, redirect, url_for

# Simple file-based user storage
USERS_FILE = 'users.json'

def load_users():
    """Load users from file, create empty file if it doesn't exist"""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save users to file"""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

def hash_password(password):
    """Hash a password with SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    """Register a new user"""
    users = load_users()
    if username in users:
        return False  # User already exists
    users[username] = hash_password(password)
    save_users(users)
    return True

def authenticate_user(username, password):
    """Authenticate a user"""
    users = load_users()
    if username in users and users[username] == hash_password(password):
        return True
    return False

def login_required(f):
    """Decorator to require login for certain routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function