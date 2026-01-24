"""
Business logic for streak management
"""
from datetime import datetime, date, timedelta
from typing import Optional
from models import Streak, ActivityLog, RestoreToken


class StreakManager:
    """Manages streak calculations and updates"""
    
    @staticmethod
    def get_today() -> str:
        """Get today's date in YYYY-MM-DD format"""
        return date.today().isoformat()
    
    @staticmethod
    def get_current_month() -> str:
        """Get current month in YYYY-MM format"""
        return date.today().strftime("%Y-%m")
    
    @staticmethod
    def parse_date(date_str: str) -> date:
        """Parse date string to date object"""
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    
    @staticmethod
    def days_between(date1_str: str, date2_str: str) -> int:
        """Calculate days between two dates"""
        d1 = StreakManager.parse_date(date1_str)
        d2 = StreakManager.parse_date(date2_str)
        return abs((d2 - d1).days)
    
    @staticmethod
    def check_streak_status(streak: Streak) -> str:
        """
        Check the status of a streak
        Returns: 'active', 'broken', or 'new'
        """
        if not streak.last_activity_date:
            return 'new'
        
        today = StreakManager.get_today()
        last_date = streak.last_activity_date
        days_diff = StreakManager.days_between(last_date, today)
        
        if days_diff == 0:
            return 'active'  # Activity logged today
        elif days_diff == 1:
            return 'active'  # Can continue today
        else:
            return 'broken'  # Missed more than 1 day
    
    @staticmethod
    def mark_activity(streak: Streak, activity_date: str = None, notes: str = "") -> bool:
        """
        Mark an activity for a streak
        Returns True if activity was successfully logged
        """
        if activity_date is None:
            activity_date = StreakManager.get_today()
        
        # Check if activity already logged for this date
        for log in streak.activity_logs:
            if log.date == activity_date:
                return False  # Already logged
        
        # Add activity log
        log = ActivityLog(date=activity_date, notes=notes)
        streak.activity_logs.append(log)
        
        # Update streak
        if not streak.last_activity_date:
            # First activity
            streak.current_streak = 1
            streak.longest_streak = 1
        else:
            days_diff = StreakManager.days_between(streak.last_activity_date, activity_date)
            if days_diff == 1:
                # Consecutive day
                streak.current_streak += 1
                streak.longest_streak = max(streak.longest_streak, streak.current_streak)
            elif days_diff == 0:
                # Same day (should not happen with check above)
                pass
            else:
                # Streak broken
                streak.current_streak = 1
        
        streak.last_activity_date = activity_date
        return True
    
    @staticmethod
    def restore_streak(streak: Streak, restore_token: RestoreToken) -> bool:
        """
        Restore a broken streak using a restore token
        Returns True if restoration was successful
        """
        status = StreakManager.check_streak_status(streak)
        
        if status != 'broken':
            return False  # Streak is not broken
        
        if not restore_token.can_restore():
            return False  # No tokens available
        
        # Use token
        if not restore_token.use_token():
            return False
        
        # Restore streak by marking yesterday's activity
        today = StreakManager.get_today()
        yesterday = (StreakManager.parse_date(today) - timedelta(days=1)).isoformat()
        
        # Mark activity for yesterday
        return StreakManager.mark_activity(streak, yesterday, "Restored using token")
    
    @staticmethod
    def update_streak_if_broken(streak: Streak) -> None:
        """
        Update streak current count to 0 if it's broken
        """
        status = StreakManager.check_streak_status(streak)
        if status == 'broken':
            streak.current_streak = 0
    
    @staticmethod
    def get_or_create_restore_token(restore_tokens: dict, month: str = None) -> RestoreToken:
        """
        Get or create restore token for a given month
        """
        if month is None:
            month = StreakManager.get_current_month()
        
        if month not in restore_tokens:
            restore_tokens[month] = RestoreToken(month=month)
        
        return restore_tokens[month]
