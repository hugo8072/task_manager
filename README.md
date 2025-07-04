# 📋 My Tasks App - Task Management System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Complete-brightgreen.svg)]()

> **A secure and user-friendly terminal-based task management system built with Python**

## 🌟 Features

### 🔐 **Security**
- **PBKDF2 + SHA256 encryption** with unique salt per user (new accounts)
- **SHA256 encryption** for existing accounts (backward compatible)
- **Login attempt tracking** with automatic account blocking (5 attempts, 30min block)
- **Password masking** during input
- **Case-insensitive login** system

### 👥 **Multi-User Support**
- **User registration** with username validation
- **Admin accounts** with special privileges
- **User impersonation** for administrators
- **Individual task management** per user

### 📊 **Task Management**
- ✅ **Create, edit, and delete** tasks
- 🎯 **Priority levels** (1=High, 2=Medium, 3=Low)
- 📅 **Deadline tracking** with overdue detection
- 🏷️ **Category organization**
- ✔️ **Task completion** tracking
- 🔍 **Search and filtering** by priority, category, date range

### 📈 **Statistics & Analytics**
- 📊 **Completion rates** per user
- 📋 **Tasks per category** analysis
- 🔥 **Top 3 categories** identification
- ⏰ **Unfinished/overdue tasks** monitoring
- 🌍 **Global statistics** (admin only)

### 🎨 **Terminal Interface**
- 🌈 **Colorful terminal** output
- 📱 **Full-screen menus** with centered display
- 🔄 **Last action display** for feedback
- ⚡ **Clean, organized** menu structure

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Terminal/Command Prompt

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/task_manager.git
cd task_manager
```

2. **Run the application**
```bash
python3 initial_menu.py
```

### First Time Setup

1. **Register a new user** or create an admin account
2. **Start managing** your tasks immediately
3. **Explore statistics** and advanced features

## 🖥️ Usage Examples

### Main Menu
```
╔══════════════════════════════════════════════════════════════╗
║                    Welcome to My_tasks_App!                  ║
║                    Task Management System                    ║
╚══════════════════════════════════════════════════════════════╝

  1. Login
  2. Register  
  3. Create admin
  0. Exit
```

### Task Management
- **Add tasks** with priorities and deadlines
- **Edit existing** tasks with ease
- **Mark tasks** as completed
- **Filter by** priority, category, or date range

### Admin Features
- **View all users** and their tasks
- **Global statistics** across all users
- **User impersonation** for support
- **System-wide** task management

## 📁 Project Structure

```
task_manager/
├── 📄 initial_menu.py      # Main application entry point
├── 🔐 login.py             # User authentication
├── 📝 register.py          # User registration
├── 👤 task_manager_user.py # User task management
├── 👑 task_manager_admin.py# Admin functionality  
├── 📊 statistics_*.py      # Statistics modules
├── 🔍 search_filter.py     # Search and filtering
├── 🛠️ task_utils.py        # Utility functions
├── 🎨 colors.py            # Terminal colors
├── 🖥️ screen_utils.py      # Screen management
├── 💾 loads.py             # Data loading
├── 💾 saves.py             # Data saving
├── 🔑 password_utils.py    # Password utilities
└── 📁 users/               # User data storage
    ├── 👥 users.json       # User metadata
    ├── 🔐 users.env        # Encrypted passwords
    └── 📁 tasks/           # Individual user tasks
```

## 🔧 Technical Features

### Security Implementation
- **PBKDF2-HMAC-SHA256** password hashing
- **100,000 iterations** for brute-force protection
- **Unique salt** per user account
- **Backward compatibility** with existing passwords

### Data Management
- **JSON-based** storage for portability
- **Environment variables** for sensitive data
- **Atomic operations** for data integrity
- **Automatic backup** and recovery

### Error Handling
- **Comprehensive exception** handling
- **User-friendly error** messages
- **Graceful degradation** on failures
- **Input validation** and sanitization

## 🎯 Advanced Features

### Search & Filter System
```python
# Search by priority
🔴 High Priority Tasks    # Priority 1
🟡 Medium Priority Tasks  # Priority 2  
🟢 Low Priority Tasks     # Priority 3

# Filter by date range
📅 Tasks between 2025-01-01 and 2025-01-31

# Category filtering
📚 Work | 🏠 Home | 💼 Personal | 🎯 Projects
```

### Statistics Dashboard
```
📊 Global Statistics
├── 👥 Total Users: 15
├── 📋 Total Tasks: 847
├── ✅ Completed: 623 (73.6%)
├── ⏳ Pending: 187 (22.1%)
└── ⚠️ Overdue: 37 (4.4%)
```



### Development Setup
```bash
# Clone and setup
git clone https://github.com/yourusername/task_manager.git
cd task_manager

# Create development branch
git checkout -b feature/your-feature-name

# Make your changes and test
python3 initial_menu.py

# Commit and push
git add .
git commit -m "Add: your feature description"
git push origin feature/your-feature-name
```




---
