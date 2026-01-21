#!/usr/bin/env python3
"""
Test script for Daily Streak Tracker core functionality
"""
import sys
import os
from datetime import date, timedelta

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import Streak, ActivityLog, RestoreToken, AppData
from storage import Storage
from streak_logic import StreakManager


def test_streak_creation():
    """Test creating a new streak"""
    print("Test 1: Creating a new streak...")
    streak = Streak(name="GitHub Commits")
    assert streak.name == "GitHub Commits"
    assert streak.current_streak == 0
    assert streak.longest_streak == 0
    assert streak.last_activity_date == ""
    print("✓ Streak creation successful")


def test_mark_activity():
    """Test marking daily activity"""
    print("\nTest 2: Marking daily activity...")
    streak = Streak(name="LeetCode")
    today = date.today().isoformat()
    
    success = StreakManager.mark_activity(streak, today, "Solved problem #1")
    assert success == True
    assert streak.current_streak == 1
    assert streak.longest_streak == 1
    assert streak.last_activity_date == today
    assert len(streak.activity_logs) == 1
    print("✓ Activity marking successful")


def test_consecutive_days():
    """Test consecutive day streaks"""
    print("\nTest 3: Testing consecutive day streaks...")
    streak = Streak(name="Test Streak")
    
    # Day 1
    day1 = (date.today() - timedelta(days=2)).isoformat()
    StreakManager.mark_activity(streak, day1)
    assert streak.current_streak == 1
    
    # Day 2 (consecutive)
    day2 = (date.today() - timedelta(days=1)).isoformat()
    StreakManager.mark_activity(streak, day2)
    assert streak.current_streak == 2
    
    # Day 3 (consecutive)
    day3 = date.today().isoformat()
    StreakManager.mark_activity(streak, day3)
    assert streak.current_streak == 3
    assert streak.longest_streak == 3
    print("✓ Consecutive day tracking successful")


def test_streak_broken():
    """Test broken streak detection"""
    print("\nTest 4: Testing broken streak detection...")
    streak = Streak(name="Test Streak")
    
    # Activity 3 days ago
    old_date = (date.today() - timedelta(days=3)).isoformat()
    StreakManager.mark_activity(streak, old_date)
    
    # Check status - should be broken
    status = StreakManager.check_streak_status(streak)
    assert status == "broken"
    print("✓ Broken streak detection successful")


def test_restore_token():
    """Test restore token functionality"""
    print("\nTest 5: Testing restore token functionality...")
    token = RestoreToken(month="2026-01")
    
    assert token.can_restore() == True
    assert token.remaining_tokens() == 2
    
    # Use first token
    success = token.use_token()
    assert success == True
    assert token.remaining_tokens() == 1
    
    # Use second token
    success = token.use_token()
    assert success == True
    assert token.remaining_tokens() == 0
    
    # Try to use third token (should fail)
    success = token.use_token()
    assert success == False
    assert token.can_restore() == False
    print("✓ Restore token functionality successful")


def test_streak_restore():
    """Test streak restoration"""
    print("\nTest 6: Testing streak restoration...")
    streak = Streak(name="Test Streak")
    token = RestoreToken(month="2026-01")
    
    # Create a broken streak (activity 3 days ago)
    old_date = (date.today() - timedelta(days=3)).isoformat()
    StreakManager.mark_activity(streak, old_date)
    
    # Verify it's broken
    status = StreakManager.check_streak_status(streak)
    assert status == "broken"
    
    # Restore the streak
    success = StreakManager.restore_streak(streak, token)
    assert success == True
    assert token.tokens_used == 1
    print("✓ Streak restoration successful")


def test_storage():
    """Test data storage and loading"""
    print("\nTest 7: Testing data storage...")
    
    # Create test data
    streak1 = Streak(name="GitHub")
    streak2 = Streak(name="LeetCode")
    app_data = AppData(streaks=[streak1, streak2])
    
    # Save to temporary file
    storage = Storage(data_file="test_data.json")
    success = storage.save(app_data)
    assert success == True
    
    # Load data
    loaded_data = storage.load()
    assert len(loaded_data.streaks) == 2
    assert loaded_data.streaks[0].name == "GitHub"
    assert loaded_data.streaks[1].name == "LeetCode"
    
    # Clean up
    if os.path.exists(storage.data_file):
        os.remove(storage.data_file)
    print("✓ Data storage and loading successful")


def test_duplicate_activity():
    """Test preventing duplicate activity logging"""
    print("\nTest 8: Testing duplicate activity prevention...")
    streak = Streak(name="Test Streak")
    today = date.today().isoformat()
    
    # First activity
    success1 = StreakManager.mark_activity(streak, today)
    assert success1 == True
    
    # Try to mark again for same day
    success2 = StreakManager.mark_activity(streak, today)
    assert success2 == False
    assert len(streak.activity_logs) == 1
    print("✓ Duplicate activity prevention successful")


def test_data_serialization():
    """Test data serialization to/from dict"""
    print("\nTest 9: Testing data serialization...")
    
    # Create streak with activity
    streak = Streak(name="Test")
    StreakManager.mark_activity(streak, date.today().isoformat())
    
    # Serialize
    streak_dict = streak.to_dict()
    assert isinstance(streak_dict, dict)
    assert streak_dict["name"] == "Test"
    
    # Deserialize
    restored_streak = Streak.from_dict(streak_dict)
    assert restored_streak.name == streak.name
    assert restored_streak.current_streak == streak.current_streak
    assert len(restored_streak.activity_logs) == len(streak.activity_logs)
    print("✓ Data serialization successful")


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Running Daily Streak Tracker Core Functionality Tests")
    print("=" * 60)
    
    try:
        test_streak_creation()
        test_mark_activity()
        test_consecutive_days()
        test_streak_broken()
        test_restore_token()
        test_streak_restore()
        test_storage()
        test_duplicate_activity()
        test_data_serialization()
        
        print("\n" + "=" * 60)
        print("✅ All tests passed successfully!")
        print("=" * 60)
        return 0
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
