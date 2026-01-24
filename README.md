# 🔥 Daily Streak Tracker

A personal **desktop application** built with **Python** to track daily coding streaks such as **GitHub**, **LeetCode**, and any custom activity.

## 🎯 Project Goal

- ✅ Tracks **multiple streaks** (GitHub, LeetCode, etc.)
- ✅ Works **without internet** - fully offline
- ✅ Saves data **locally on your PC**
- ✅ Allows **limited streak restore** when a day is missed (2 tokens per month)
- ✅ Helps maintain consistency in daily coding practice

## 🚀 Features

### Core Features
- **Multiple Streak Tracking**: Track GitHub commits, LeetCode problems, or any custom daily activity
- **Offline First**: No internet connection required - all data stored locally
- **Visual Indicators**: Color-coded streak status (Active/Broken/New)
- **Streak Statistics**: View current streak and longest streak for each activity
- **Daily Activity Logging**: Mark activities for each day with optional notes
- **Restore Tokens**: Get 2 restore tokens per month to recover broken streaks
- **Auto-reset**: Automatically resets streak count if more than 1 day is missed

### User Interface
- Clean and intuitive desktop GUI built with Tkinter
- Easy streak management (Add/Delete/Update)
- Quick actions for marking daily activities
- Visual streak cards with status indicators
- Monthly token tracker

## 📋 Requirements

- **Python 3.7+** (uses only standard library)
- **Tkinter** (usually comes pre-installed with Python)

## 🔧 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/tote10/Daily-Streak-Tracker.git
   cd Daily-Streak-Tracker
   ```

2. **No dependencies to install!** The application uses only Python's standard library.

3. **Verify Python installation**:
   ```bash
   python --version
   # or
   python3 --version
   ```

## 💻 Usage

### Running the Application

**On Linux/Mac**:
```bash
python3 main.py
# or
python main.py
```

**On Windows**:
```bash
python main.py
```

### Using the Application

1. **Add a New Streak**:
   - Click the "➕ Add New Streak" button
   - Enter a custom name or use quick add buttons (GitHub/LeetCode)
   - Click "Add" to create the streak

2. **Mark Daily Activity**:
   - Click "✓ Mark Today" on any streak card
   - This logs your activity for today and updates the streak count

3. **Restore a Broken Streak**:
   - If you miss a day, the streak will be marked as "Broken"
   - Click "🎫 Restore" to use a restore token (if available)
   - You get 2 restore tokens per month

4. **Delete a Streak**:
   - Click "🗑 Delete" on any streak card
   - Confirm the deletion

5. **View Statistics**:
   - Each streak card shows:
     - Current streak count
     - Longest streak achieved
     - Last activity date
     - Status (Active/Broken/New)

## 📁 Data Storage

All data is stored locally in your home directory:
- **Location**: `~/.daily_streak_tracker/streak_data.json`
- **Format**: JSON (human-readable)
- **Backup**: You can manually backup this file to preserve your streaks

### Data Structure
```json
{
  "streaks": [
    {
      "name": "GitHub Commits",
      "current_streak": 15,
      "longest_streak": 30,
      "last_activity_date": "2026-01-21",
      "activity_logs": [...],
      "created_date": "2026-01-01"
    }
  ],
  "restore_tokens": {
    "2026-01": {
      "month": "2026-01",
      "tokens_used": 1,
      "max_tokens": 2
    }
  }
}
```

## 🎫 Restore Token System

- **Monthly Allocation**: 2 tokens per month
- **Reset**: Tokens reset on the 1st of each month
- **Usage**: Use tokens to restore broken streaks (missed >1 day)
- **Limitation**: Cannot restore if already logged activity for today

## 🏗️ Project Structure

```
Daily-Streak-Tracker/
├── main.py           # Application entry point
├── gui.py            # GUI implementation (Tkinter)
├── models.py         # Data models (Streak, ActivityLog, RestoreToken)
├── storage.py        # Local storage management
├── streak_logic.py   # Business logic for streak calculations
├── requirements.txt  # Dependencies (none required)
└── README.md         # This file
```

## 🔒 Privacy & Security

- **100% Local**: All data stays on your computer
- **No Internet**: No data sent to external servers
- **No Accounts**: No login or registration required
- **Open Source**: Full transparency of code

## 🛠️ Development

### Code Architecture

1. **Models** (`models.py`): Data classes for Streak, ActivityLog, RestoreToken, and AppData
2. **Storage** (`storage.py`): JSON-based local file storage
3. **Logic** (`streak_logic.py`): Streak calculation and management
4. **GUI** (`gui.py`): Tkinter-based user interface

### Key Components

- **StreakManager**: Handles all streak-related business logic
- **Storage**: Manages data persistence
- **StreakTrackerGUI**: Main application window and UI components

## 📝 License

This project is open source and available for personal use.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📧 Support

For issues or questions, please open an issue on GitHub.

---

**Happy Coding! Keep your streaks alive! 🔥**
