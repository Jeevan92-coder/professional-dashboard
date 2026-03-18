from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import os
import json
from datetime import datetime, date
import re

app = Flask(__name__)
app.secret_key = 'meher_jeevan_secret_key_2024_ultra_secure'
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

DB_PATH = 'database.db'

# ─── DATABASE SETUP ───────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            dob TEXT NOT NULL,
            mobile_number TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            profile_pic TEXT DEFAULT NULL,
            role TEXT DEFAULT 'User',
            account_status TEXT DEFAULT 'Active',
            login_count INTEGER DEFAULT 0,
            last_login TIMESTAMP DEFAULT NULL,
            account_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS login_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            login_date TEXT,
            login_time TEXT,
            ip_address TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            activity_type TEXT,
            activity_description TEXT,
            activity_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            message TEXT,
            type TEXT DEFAULT 'info',
            is_read INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS security_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            alert_type TEXT,
            alert_message TEXT,
            alert_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS user_preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            language TEXT DEFAULT 'en',
            font_style TEXT DEFAULT 'Inter',
            theme TEXT DEFAULT 'cosmic-purple',
            custom_bg TEXT DEFAULT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    ''')
    conn.commit()
    conn.close()

def log_activity(user_id, activity_type, description):
    conn = get_db()
    conn.execute('INSERT INTO activities (user_id, activity_type, activity_description) VALUES (?,?,?)',
                 (user_id, activity_type, description))
    conn.commit()
    conn.close()

def add_notification(user_id, title, message, notif_type='info'):
    conn = get_db()
    conn.execute('INSERT INTO notifications (user_id, title, message, type) VALUES (?,?,?,?)',
                 (user_id, title, message, notif_type))
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id=?', (user_id,)).fetchone()
    conn.close()
    return user

def get_preferences(user_id):
    conn = get_db()
    prefs = conn.execute('SELECT * FROM user_preferences WHERE user_id=?', (user_id,)).fetchone()
    if not prefs:
        conn.execute('INSERT INTO user_preferences (user_id) VALUES (?)', (user_id,))
        conn.commit()
        prefs = conn.execute('SELECT * FROM user_preferences WHERE user_id=?', (user_id,)).fetchone()
    conn.close()
    return prefs

# ─── AUTH ROUTES ──────────────────────────────────────────────────
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        dob = request.form.get('dob', '').strip()
        mobile = request.form.get('mobile', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        if not all([username, first_name, last_name, dob, mobile, email, password]):
            flash('All fields are required!', 'error')
            return redirect(url_for('register'))

        if password != confirm:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('register'))

        if len(password) < 8:
            flash('Password must be at least 8 characters!', 'error')
            return redirect(url_for('register'))

        if not re.match(r'^\d{10}$', mobile):
            flash('Mobile must be 10 digits!', 'error')
            return redirect(url_for('register'))

        conn = get_db()
        try:
            conn.execute('''INSERT INTO users 
                (username, first_name, last_name, dob, mobile_number, email, password_hash)
                VALUES (?,?,?,?,?,?,?)''',
                (username, first_name, last_name, dob, mobile, email,
                 generate_password_hash(password)))
            conn.commit()
            user = conn.execute('SELECT id FROM users WHERE username=?', (username,)).fetchone()
            conn.execute('INSERT INTO user_preferences (user_id) VALUES (?)', (user['id'],))
            conn.commit()
            log_activity(user['id'], 'Registration', f'New account created for {username}')
            add_notification(user['id'], 'Welcome!', f'Welcome to the platform, {first_name}! Your account is ready.', 'success')
            flash(f'Registration successful! Welcome {first_name}! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError as e:
            if 'username' in str(e):
                flash('Username already exists!', 'error')
            elif 'email' in str(e):
                flash('Email already registered!', 'error')
            elif 'mobile' in str(e):
                flash('Mobile number already registered!', 'error')
            else:
                flash('Registration failed. Please try again.', 'error')
        finally:
            conn.close()

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form.get('login_identifier', '').strip()
        password = request.form.get('password', '')

        conn = get_db()
        user = conn.execute('''SELECT * FROM users WHERE 
            username=? OR email=? OR mobile_number=?''',
            (identifier, identifier.lower(), identifier)).fetchone()

        if user and check_password_hash(user['password_hash'], password):
            if user['account_status'] != 'Active':
                flash('Your account is not active. Please contact support.', 'error')
                conn.close()
                return redirect(url_for('login'))

            now = datetime.now()
            conn.execute('UPDATE users SET login_count=login_count+1, last_login=? WHERE id=?',
                         (now, user['id']))
            conn.execute('INSERT INTO login_history (user_id, login_date, login_time, ip_address) VALUES (?,?,?,?)',
                         (user['id'], now.strftime('%d %b %Y'), now.strftime('%H:%M:%S'),
                          request.remote_addr))
            conn.commit()
            conn.close()

            session['user_id'] = user['id']
            log_activity(user['id'], 'Login', f'Logged in from {request.remote_addr}')
            flash(f'Welcome back, {user["first_name"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            conn.close()
            flash('Invalid credentials. Please check and try again.', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    if 'user_id' in session:
        log_activity(session['user_id'], 'Logout', 'User logged out')
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login'))

# ─── DASHBOARD ────────────────────────────────────────────────────
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    uid = session['user_id']
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id=?', (uid,)).fetchone()

    if user is None:
        conn.close()
        session.clear()
        flash('Session expired. Please login again.', 'error')
        return redirect(url_for('login'))

    activities = conn.execute('SELECT * FROM activities WHERE user_id=? ORDER BY activity_timestamp DESC LIMIT 10', (uid,)).fetchall()
    login_history = conn.execute('SELECT * FROM login_history WHERE user_id=? ORDER BY id DESC LIMIT 8', (uid,)).fetchall()
    notifications = conn.execute('SELECT * FROM notifications WHERE user_id=? ORDER BY created_at DESC LIMIT 10', (uid,)).fetchall()
    notif_count = conn.execute('SELECT COUNT(*) as cnt FROM notifications WHERE user_id=? AND is_read=0', (uid,)).fetchone()['cnt']
    alerts = conn.execute('SELECT * FROM security_alerts WHERE user_id=? ORDER BY alert_timestamp DESC LIMIT 5', (uid,)).fetchall()
    conn.close()

    # Convert last_login string to datetime if needed
    user_dict = dict(user)
    if user_dict.get('last_login') and isinstance(user_dict['last_login'], str):
        try:
            user_dict['last_login'] = datetime.strptime(user_dict['last_login'], '%Y-%m-%d %H:%M:%S.%f')
        except:
            try:
                user_dict['last_login'] = datetime.strptime(user_dict['last_login'], '%Y-%m-%d %H:%M:%S')
            except:
                user_dict['last_login'] = None

    if user_dict.get('account_created') and isinstance(user_dict['account_created'], str):
        try:
            user_dict['account_created'] = datetime.strptime(user_dict['account_created'], '%Y-%m-%d %H:%M:%S.%f')
        except:
            try:
                user_dict['account_created'] = datetime.strptime(user_dict['account_created'], '%Y-%m-%d %H:%M:%S')
            except:
                user_dict['account_created'] = datetime.now()

    # Convert activity timestamps
    acts_processed = []
    for a in activities:
        ad = dict(a)
        if isinstance(ad.get('activity_timestamp'), str):
            try:
                ad['activity_timestamp'] = datetime.strptime(ad['activity_timestamp'], '%Y-%m-%d %H:%M:%S.%f')
            except:
                ad['activity_timestamp'] = datetime.now()
        acts_processed.append(type('obj', (object,), ad)())

    notifs_processed = []
    for n in notifications:
        nd = dict(n)
        if isinstance(nd.get('created_at'), str):
            try:
                nd['created_at'] = datetime.strptime(nd['created_at'], '%Y-%m-%d %H:%M:%S.%f')
            except:
                nd['created_at'] = datetime.now()
        notifs_processed.append(type('obj', (object,), nd)())

    alerts_processed = []
    for al in alerts:
        ald = dict(al)
        if isinstance(ald.get('alert_timestamp'), str):
            try:
                ald['alert_timestamp'] = datetime.strptime(ald['alert_timestamp'], '%Y-%m-%d %H:%M:%S.%f')
            except:
                ald['alert_timestamp'] = datetime.now()
        alerts_processed.append(type('obj', (object,), ald)())

    user_obj = type('obj', (object,), user_dict)()

    return render_template('dashboard.html',
                           user=user_obj,
                           activities=acts_processed,
                           login_history=login_history,
                           notifications=notifs_processed,
                           notif_count=notif_count,
                           alerts=alerts_processed)

@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    uid = session['user_id']
    first_name = request.form.get('first_name', '').strip()
    last_name = request.form.get('last_name', '').strip()
    email = request.form.get('email', '').strip().lower()
    mobile = request.form.get('mobile', '').strip()
    dob = request.form.get('dob', '').strip()

    # Handle profile pic
    profile_pic = None
    if 'profile_pic' in request.files:
        file = request.files['profile_pic']
        if file and file.filename:
            filename = secure_filename(f"user_{uid}_{file.filename}")
            save_path = os.path.join('static', 'uploads', 'profiles', filename)
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            file.save(save_path)
            profile_pic = filename

    conn = get_db()
    try:
        if profile_pic:
            conn.execute('UPDATE users SET first_name=?, last_name=?, email=?, mobile_number=?, dob=?, profile_pic=? WHERE id=?',
                         (first_name, last_name, email, mobile, dob, profile_pic, uid))
        else:
            conn.execute('UPDATE users SET first_name=?, last_name=?, email=?, mobile_number=?, dob=? WHERE id=?',
                         (first_name, last_name, email, mobile, dob, uid))
        conn.commit()
        log_activity(uid, 'Profile Update', 'Profile information updated')
        flash('Profile updated successfully!', 'success')
    except sqlite3.IntegrityError:
        flash('Email or mobile already in use!', 'error')
    finally:
        conn.close()

    return redirect(url_for('dashboard'))

@app.route('/change_password', methods=['POST'])
def change_password():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    uid = session['user_id']
    old_pw = request.form.get('old_password', '')
    new_pw = request.form.get('new_password', '')
    confirm_pw = request.form.get('confirm_password', '')

    if new_pw != confirm_pw:
        flash('New passwords do not match!', 'error')
        return redirect(url_for('dashboard'))

    if len(new_pw) < 8:
        flash('Password must be at least 8 characters!', 'error')
        return redirect(url_for('dashboard'))

    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id=?', (uid,)).fetchone()
    if not check_password_hash(user['password_hash'], old_pw):
        conn.close()
        flash('Current password is incorrect!', 'error')
        return redirect(url_for('dashboard'))

    conn.execute('UPDATE users SET password_hash=? WHERE id=?',
                 (generate_password_hash(new_pw), uid))
    conn.commit()
    conn.close()
    log_activity(uid, 'Password Change', 'Password changed successfully')
    add_notification(uid, 'Security Alert', 'Your password was changed. If this was not you, contact support immediately.', 'warning')
    flash('Password changed successfully!', 'success')
    return redirect(url_for('dashboard'))

# ─── SETTINGS ─────────────────────────────────────────────────────
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    uid = session['user_id']
    prefs = get_preferences(uid)

    if request.method == 'POST':
        language = request.form.get('language', 'en')
        font_style = request.form.get('font_style', 'Inter')
        theme = request.form.get('theme', 'cosmic-purple')

        custom_bg = prefs['custom_bg']
        if 'custom_bg' in request.files:
            file = request.files['custom_bg']
            if file and file.filename:
                filename = secure_filename(f"bg_{uid}_{file.filename}")
                save_path = os.path.join('static', 'uploads', 'backgrounds', filename)
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                file.save(save_path)
                custom_bg = filename

        conn = get_db()
        conn.execute('''INSERT OR REPLACE INTO user_preferences (user_id, language, font_style, theme, custom_bg)
                     VALUES (?,?,?,?,?)''', (uid, language, font_style, theme, custom_bg))
        conn.commit()
        conn.close()
        log_activity(uid, 'Settings Update', f'Theme: {theme}, Language: {language}, Font: {font_style}')
        flash('Settings saved successfully!', 'success')
        return redirect(url_for('settings'))

    prefs_obj = type('obj', (object,), dict(prefs))()
    return render_template('settings.html', preferences=prefs_obj)

@app.route('/mark_notifications_read', methods=['POST'])
def mark_notifications_read():
    if 'user_id' not in session:
        return jsonify({'status': 'error'})
    conn = get_db()
    conn.execute('UPDATE notifications SET is_read=1 WHERE user_id=?', (session['user_id'],))
    conn.commit()
    conn.close()
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    os.makedirs(os.path.join('static', 'uploads', 'profiles'), exist_ok=True)
    os.makedirs(os.path.join('static', 'uploads', 'backgrounds'), exist_ok=True)
    init_db()
    print("\n" + "="*50)
    print("  🚀 Professional Dashboard System")
    print("  © Created by Meher Jeevan")
    print("="*50)
    print("  URL: http://localhost:5000")
    print("="*50 + "\n")
    app.run(debug=True, port=5000)
