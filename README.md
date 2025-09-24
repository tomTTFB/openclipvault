# OpenClipVault

## Description

OpenClipVault is a lightweight, self-hosted file sharing application built with Python and Flask. It enables authenticated users to upload, store, and share media files (images and videos) via unique short URLs. Files are stored securely on the server, with metadata managed in a JSON file for easy access and listing.

This project serves as a simple alternative to cloud-based file sharing services, giving users full control over their data.

## Features

- **User Authentication**: Login system with hashed passwords stored in a JSON file. (Note: User registration functionality is implemented in the backend but lacks a frontend route; you can add a `/register` route if needed.)
- **File Upload**: Supports images (PNG, JPG, JPEG, GIF) and videos (MP4, MOV, WebM). Files are saved with secure filenames in an `uploads` directory.
- **File Listing**: View all uploaded files on the index page, including metadata like uploader and original name.
- **Short URL Sharing**: Access files via short URLs like `/f/<file_id>` for easy sharing.
- **Direct Download**: Files can be downloaded or streamed directly from the server.
- **Session Management**: Flask sessions for maintaining user login state.
- **Simple Storage**: No database required; uses JSON files for users and file metadata.

## Prerequisites

- Python 3.6+
- pip (for installing dependencies)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/openclipvault.git
   cd openclipvault
   ```

2. Install required dependencies:
   ```
   pip install flask werkzeug
   ```

3. Create necessary directories (optional, as the app does it automatically):
   ```
   mkdir uploads
   ```

4. Run the application:
   ```
   python app.py
   ```

5. Open your browser and navigate to `http://localhost:5000`.

The app runs in debug mode by default. For production, set `debug=False` and use a proper secret key.

## Usage

1. **Login**:
   - Visit `http://localhost:5000/login`.
   - Since no users exist initially, you'll need to manually add a user to `users.json` or implement the registration route.
   - Example `users.json` entry:
     ```
     {
       "admin": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
     }
     ```
     (This is the SHA-256 hash of the password "password". Use the `hash_password` function in `auth.py` to generate hashes.)

2. **Upload Files**:
   - After logging in, go to the index page (`/`).
   - Select a file and upload. Supported formats will be validated.
   - Uploaded files appear in the list with their metadata.

3. **Share Files**:
   - Each upload generates a unique 12-character ID.
   - Share the URL: `http://localhost:5000/f/<file_id>` (e.g., `/f/abc123def456`).
   - Anyone with the link can access the file directly (no auth required for downloads).

4. **Logout**:
   - Click the logout link to end the session.

## File Structure

- `app.py`: Main Flask application with routes for index, login, upload, and file serving.
- `auth.py`: Authentication utilities, including password hashing and login decorator.
- `templates/`: HTML templates.
  - `index.html`: File listing and upload form.
  - `login.html`: Login form.
- `uploads/`: Directory for stored files (created automatically).
- `files.json`: Stores file metadata (ID, name, uploader).
- `users.json`: Stores user credentials (auto-created).

## Security Notes

- **Development Only**: This is a basic implementation. Do not use in production without enhancements:
  - Use environment variables for the secret key.
  - Implement proper user registration.
  - Add file size limits and virus scanning.
  - Use HTTPS and rate limiting.
  - Consider a real database (e.g., SQLite) for scalability.
- Passwords are hashed with SHA-256, but for production, use a stronger method like bcrypt.
- File IDs are random but predictable in length; for higher security, use longer UUIDs.

## Contributing

Feel free to fork the repo, create issues, or submit pull requests for improvements like adding registration, better UI, or database support.

## License

This project is open-source. (Add your preferred license, e.g., MIT, here.)

## Contact

For questions, open an issue on GitHub.