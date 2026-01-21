#!/usr/bin/env python3
"""
Demo script for Daily Streak Tracker (CLI version for demonstration)
This shows the core functionality without requiring a GUI
"""
import sys
import os
from datetime import date, timedelta

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import Streak, AppData
from storage import Storage
from streak_logic import StreakManager


def print_separator():
    print("\n" + "=" * 70 + "\n")


def print_streak_details(streak):
    """Print streak details in a nice format"""
    status = StreakManager.check_streak_status(streak)
    status_emoji = {
        'active': '✅',
        'broken': '❌',
        'new': '🆕'
    }
    
    print(f"\n{status_emoji.get(status, '')} {streak.name}")
    print(f"   Status: {status.upper()}")
    print(f"   Current Streak: {streak.current_streak} days")
    print(f"   Longest Streak: {streak.longest_streak} days")
    if streak.last_activity_date:
        print(f"   Last Activity: {streak.last_activity_date}")
    print(f"   Total Activities: {len(streak.activity_logs)}")


def demo_basic_usage():
    """Demonstrate basic usage of the streak tracker"""
    print_separator()
    print("🔥 DAILY STREAK TRACKER - DEMO")
    print_separator()
    
    # Create storage with a demo file
    storage = Storage(data_file="demo_data.json")
    
    print("1️⃣  Creating a new streak tracker app...")
    app_data = AppData()
    
    # Add GitHub streak
    print("\n2️⃣  Adding 'GitHub Commits' streak...")
    github_streak = Streak(name="GitHub Commits")
    app_data.streaks.append(github_streak)
    
    # Add LeetCode streak
    print("   Adding 'LeetCode Problem' streak...")
    leetcode_streak = Streak(name="LeetCode Problem")
    app_data.streaks.append(leetcode_streak)
    
    print("\n3️⃣  Current streaks:")
    for streak in app_data.streaks:
        print_streak_details(streak)
    
    # Simulate activity over several days
    print_separator()
    print("4️⃣  Simulating activity over 5 consecutive days for GitHub...")
    
    for i in range(5):
        activity_date = (date.today() - timedelta(days=4-i)).isoformat()
        StreakManager.mark_activity(github_streak, activity_date, f"Commit on day {i+1}")
        print(f"   Day {i+1}: Marked activity for {activity_date}")
    
    print("\n   GitHub streak after 5 days:")
    print_streak_details(github_streak)
    
    # Simulate activity for LeetCode (3 days)
    print_separator()
    print("5️⃣  Simulating activity for LeetCode (3 days)...")
    
    for i in range(3):
        activity_date = (date.today() - timedelta(days=2-i)).isoformat()
        StreakManager.mark_activity(leetcode_streak, activity_date, f"Problem on day {i+1}")
        print(f"   Day {i+1}: Marked activity for {activity_date}")
    
    print("\n   LeetCode streak after 3 days:")
    print_streak_details(leetcode_streak)
    
    # Simulate missing a day (broken streak)
    print_separator()
    print("6️⃣  Simulating a broken streak scenario...")
    broken_streak = Streak(name="Coding Practice")
    app_data.streaks.append(broken_streak)
    
    # Activity 3 days ago (missed yesterday and day before)
    old_date = (date.today() - timedelta(days=3)).isoformat()
    StreakManager.mark_activity(broken_streak, old_date)
    
    print(f"   Marked activity on {old_date} (3 days ago)")
    print("\n   Coding Practice streak (broken):")
    print_streak_details(broken_streak)
    
    # Demonstrate restore token
    print_separator()
    print("7️⃣  Demonstrating streak restoration with tokens...")
    
    current_month = StreakManager.get_current_month()
    token = StreakManager.get_or_create_restore_token(app_data.restore_tokens, current_month)
    
    print(f"\n   Current month: {current_month}")
    print(f"   Available restore tokens: {token.remaining_tokens()}/{token.max_tokens}")
    
    print(f"\n   Attempting to restore 'Coding Practice' streak...")
    success = StreakManager.restore_streak(broken_streak, token)
    
    if success:
        print("   ✅ Streak restored successfully!")
        print(f"   Tokens remaining: {token.remaining_tokens()}/{token.max_tokens}")
        print("\n   Updated streak:")
        print_streak_details(broken_streak)
    else:
        print("   ❌ Failed to restore streak")
    
    # Save data
    print_separator()
    print("8️⃣  Saving all data to local file...")
    storage.save(app_data)
    print(f"   ✅ Data saved to: {storage.get_data_path()}")
    
    # Load data
    print("\n9️⃣  Loading data from file...")
    loaded_data = storage.load()
    print(f"   ✅ Loaded {len(loaded_data.streaks)} streaks")
    
    print("\n   All streaks:")
    for streak in loaded_data.streaks:
        print_streak_details(streak)
    
    print_separator()
    print("✨ DEMO COMPLETE!")
    print("\nKey Features Demonstrated:")
    print("  ✅ Multiple streak tracking (GitHub, LeetCode, Custom)")
    print("  ✅ Local data storage (JSON file)")
    print("  ✅ Consecutive day tracking")
    print("  ✅ Broken streak detection")
    print("  ✅ Limited restore tokens (2 per month)")
    print("  ✅ Offline functionality (no internet required)")
    print_separator()
    
    # Cleanup demo file
    if os.path.exists(storage.data_file):
        os.remove(storage.data_file)
        print(f"Demo file cleaned up: {storage.data_file}")


if __name__ == "__main__":
    demo_basic_usage()
