"""
Local storage management for Daily Streak Tracker
"""
import json
import os
from pathlib import Path
from models import AppData


class Storage:
    """Handles local file-based storage"""
    
    def __init__(self, data_file: str = "streak_data.json"):
        self.data_dir = Path.home() / ".daily_streak_tracker"
        self.data_file = self.data_dir / data_file
        self._ensure_data_dir()
    
    def _ensure_data_dir(self):
        """Create data directory if it doesn't exist"""
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def save(self, app_data: AppData) -> bool:
        """Save application data to local file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(app_data.to_dict(), f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    def load(self) -> AppData:
        """Load application data from local file"""
        if not self.data_file.exists():
            return AppData()
        
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
            return AppData.from_dict(data)
        except Exception as e:
            print(f"Error loading data: {e}")
            return AppData()
    
    def get_data_path(self) -> str:
        """Get the full path to the data file"""
        return str(self.data_file)
