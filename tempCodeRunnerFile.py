import logging
from flask import Flask, render_template, request, jsonify, abort, redirect, url_for, flash, session
import sqlite3
import secrets
import openai

# Configure logging
logging.basicConfig(level=logging.INFO)  # Set the logging level to INFO

# Initialize Flask app
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Set your OpenAI API key
api_key = "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"
openai.api_key = api_key

# Route for home page
@app.route('/')
def home():
    return render_template('home.html', title='Home')

# Route to serve the chatbot page
@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

# Route to send message to ChatGPT API
@app.route('/send-message', methods=['POST'])
def send_message():
    if request.method == 'POST':
        message = request.form.get('message')

        if message is None:
            abort(400)

        # Log the message before sending it to ChatGPT
        logging.info(f"Sending message to ChatGPT API: {message}")

        # Send the message to ChatGPT API
        try:
            response = openai.Completion.create(
                engine="davinci",
                prompt=message,
                max_tokens=150
            )

            # Log the response from ChatGPT
            logging.info(f"Response from ChatGPT API: {response}")
        except Exception as e:
            logging.error(f"Error sending message to ChatGPT API: {e}")
            return jsonify({'response': 'Error: Failed to send message to ChatGPT API'})

        return jsonify({'response': response['choices'][0]['text']})

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Placeholder for login logic
        username = request.form['username']
        password = request.form['password']

        # Verify credentials in the database
        with sqlite3.connect('users.db', check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
            user = cursor.fetchone()

        if user:
            flash(f'Welcome, {username}!', 'success')
            session['user_info'] = {
                'id': user[0],
                'username': user[1],
                'name': user[3],
                'email': user[4],
                'college': user[5],
                'class': user[6],
                'roll_no': user[7],
                'blood_group': user[8],
                'phone_number': user[9],
                'address': user[10],
                'date_of_birth': user[11],
                'parent_details': user[12]
            }
            return redirect(url_for('dashboard'))  # Redirect to dashboard page on successful login
        else:
            flash('Invalid login credentials. Please try again.', 'error')

    return render_template('login.html', title='Login')

# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Placeholder for registration logic
        pass

    return render_template('register.html', title='Register')

# Route for user dashboard
@app.route('/dashboard')
def dashboard():
    user_info = session.get('user_info')
    if user_info:
        return render_template('dashboard.html', title='Dashboard', user_info=user_info)
    else:
        flash('You need to login first.', 'error')
        return redirect(url_for('login'))

# Route for editing user profile
@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    user_info = session.get('user_info')
    if user_info:
        if request.method == 'POST':
            # Placeholder for profile editing logic
            pass

        return render_template('edit_profile.html', title='Edit Profile', user_info=user_info)
    else:
        flash('You need to login first.', 'error')
        return redirect(url_for('login'))

# Route for user settings
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    user_info = session.get('user_info')
    if user_info:
        if request.method == 'POST':
            # Placeholder for settings logic
            pass

        return render_template('settings.html', title='Settings', user_info=user_info)
    else:
        flash('You need to login first.', 'error')
        return redirect(url_for('login'))

# Route for user profile
@app.route('/profile')
def profile():
    user_info = session.get('user_info')
    if user_info:
        return render_template('profile.html', title='User Profile', user_info=user_info)
    else:
        flash('You need to login first.', 'error')
        return redirect(url_for('login'))

# Route for user logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

# Your existing routes for static files, etc. go here

if __name__ == '__main__':
    app.run(debug=True)
