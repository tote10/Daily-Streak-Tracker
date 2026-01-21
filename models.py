"""
Data models for Daily Streak Tracker
"""
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Dict
import json


@dataclass
class ActivityLog:
    """Represents a single activity log entry"""
    date: str  # YYYY-MM-DD format
    notes: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "date": self.date,
            "notes": self.notes
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ActivityLog':
        return cls(
            date=data["date"],
            notes=data.get("notes", "")
        )


@dataclass
class Streak:
    """Represents a streak for a specific activity"""
    name: str
    current_streak: int = 0
    longest_streak: int = 0
    last_activity_date: str = ""  # YYYY-MM-DD format
    activity_logs: List[ActivityLog] = field(default_factory=list)
    created_date: str = field(default_factory=lambda: date.today().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "current_streak": self.current_streak,
            "longest_streak": self.longest_streak,
            "last_activity_date": self.last_activity_date,
            "activity_logs": [log.to_dict() for log in self.activity_logs],
            "created_date": self.created_date
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Streak':
        return cls(
            name=data["name"],
            current_streak=data.get("current_streak", 0),
            longest_streak=data.get("longest_streak", 0),
            last_activity_date=data.get("last_activity_date", ""),
            activity_logs=[ActivityLog.from_dict(log) for log in data.get("activity_logs", [])],
            created_date=data.get("created_date", date.today().isoformat())
        )


@dataclass
class RestoreToken:
    """Manages restore tokens for streak recovery"""
    month: str  # YYYY-MM format
    tokens_used: int = 0
    max_tokens: int = 2  # Maximum tokens per month
    
    def can_restore(self) -> bool:
        return self.tokens_used < self.max_tokens
    
    def use_token(self) -> bool:
        if self.can_restore():
            self.tokens_used += 1
            return True
        return False
    
    def remaining_tokens(self) -> int:
        return max(0, self.max_tokens - self.tokens_used)
    
    def to_dict(self) -> Dict:
        return {
            "month": self.month,
            "tokens_used": self.tokens_used,
            "max_tokens": self.max_tokens
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'RestoreToken':
        return cls(
            month=data["month"],
            tokens_used=data.get("tokens_used", 0),
            max_tokens=data.get("max_tokens", 2)
        )


@dataclass
class AppData:
    """Container for all application data"""
    streaks: List[Streak] = field(default_factory=list)
    restore_tokens: Dict[str, RestoreToken] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "streaks": [streak.to_dict() for streak in self.streaks],
            "restore_tokens": {k: v.to_dict() for k, v in self.restore_tokens.items()}
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'AppData':
        return cls(
            streaks=[Streak.from_dict(s) for s in data.get("streaks", [])],
            restore_tokens={k: RestoreToken.from_dict(v) for k, v in data.get("restore_tokens", {}).items()}
        )
