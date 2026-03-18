# 🚀 Professional Dashboard System
## © Created by Meher Jeevan

---

## ⚡ Quick Start (3 Steps)

### Step 1: Install Python Requirements
```bash
pip install -r requirements.txt
```

### Step 2: Run the App
```bash
python app.py
```

### Step 3: Open in Browser
```
http://localhost:5000
```

---

## 📁 Project Structure

```
app/
├── app.py                  ← Main Flask application
├── database.db             ← SQLite database (auto-created)
├── requirements.txt        ← Python dependencies
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── settings.html
└── static/
    ├── css/
    │   ├── style.css       ← Login/Register styles
    │   ├── dashboard.css
    │   └── settings.css
    ├── js/
    │   ├── login.js
    │   ├── register.js
    │   ├── dashboard.js
    │   └── settings.js
    └── uploads/
        ├── profiles/       ← Profile pictures stored here
        └── backgrounds/    ← Custom background images
```

---

## 🔗 All Routes

| Route | Description |
|-------|-------------|
| `/` | Redirects to login/dashboard |
| `/register` | User registration |
| `/login` | User login |
| `/logout` | Logout |
| `/dashboard` | Main dashboard |
| `/update_profile` | Update profile info |
| `/change_password` | Change password |
| `/settings` | Theme & preferences |

---

## 🗄️ Database Tables

- **users** — User accounts
- **login_history** — Login records with IP & time
- **activities** — User activity log
- **notifications** — In-app notifications
- **security_alerts** — Security events
- **user_preferences** — Theme, language, font settings

---

## 🌟 Features

- ✅ Register / Login / Logout
- ✅ Login with Username OR Email OR Mobile
- ✅ Password toggle visibility
- ✅ Profile update (name, email, mobile, DOB)
- ✅ Profile picture upload
- ✅ Change password with validation
- ✅ Login history tracking
- ✅ Activity timeline
- ✅ Notifications system
- ✅ Security alerts
- ✅ Theme selection (8+ themes)
- ✅ Font selector (50+ fonts)
- ✅ Language preferences
- ✅ Custom background upload
- ✅ Live chat support widget
- ✅ Dark mode toggle
- ✅ Fully responsive design
- ✅ SQLite database (no external DB needed)
- ✅ Flash messages (success/error alerts)
