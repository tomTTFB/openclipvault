from flask import Flask, request, redirect, url_for, render_template, flash, send_from_directory, session
import os
import json
import uuid
from werkzeug.utils import secure_filename
from auth import register_user, authenticate_user, login_required, load_users

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'webm'}
FILES_DATA_FILE = 'files.json'  # Store file metadata

# Create Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super-secret-key'  # In production, use a proper secret key

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def load_files_data():
    """Load files data from JSON file"""
    if os.path.exists(FILES_DATA_FILE):
        with open(FILES_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_files_data(files_data):
    """Save files data to JSON file"""
    with open(FILES_DATA_FILE, 'w') as f:
        json.dump(files_data, f)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_file_id():
    """Generate a random file ID"""
    return str(uuid.uuid4()).replace('-', '')[:12]

@app.route('/')
def index():
    # List all files in the upload directory
    files_data = load_files_data()
    return render_template('index.html', files=files_data, logged_in='username' in session)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authenticate_user(username, password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    # Check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        # Generate a random ID for the file
        file_id = generate_file_id()
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Store file metadata
        files_data = load_files_data()
        files_data[file_id] = {
            'original_name': filename,
            'uploader': session['username'],
            'id': file_id
        }
        save_files_data(files_data)
        
        flash('File uploaded successfully')
        return redirect(url_for('index'))
    else:
        flash('Invalid file type. Allowed types: png, jpg, jpeg, gif, mp4, mov, webm')
        return redirect(url_for('index'))
@app.route('/uploads/<file_id>')
def uploaded_file(file_id):
    files_data = load_files_data()
    if file_id in files_data:
        filename = files_data[file_id]['original_name']
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    else:
        flash('File not found')
        return redirect(url_for('index'))

@app.route('/f/<file_id>')
def short_file(file_id):
    """Short URL route for file access"""
    files_data = load_files_data()
    if file_id in files_data:
        filename = files_data[file_id]['original_name']
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    else:
        flash('File not found')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)