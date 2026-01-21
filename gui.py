"""
GUI for Daily Streak Tracker
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import date
from models import Streak, AppData
from storage import Storage
from streak_logic import StreakManager


class StreakTrackerGUI:
    """Main GUI for the Daily Streak Tracker application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Daily Streak Tracker")
        self.root.geometry("800x600")
        
        # Initialize storage and data
        self.storage = Storage()
        self.app_data = self.storage.load()
        self.streak_manager = StreakManager()
        
        # Update broken streaks on startup
        for streak in self.app_data.streaks:
            self.streak_manager.update_streak_if_broken(streak)
        
        # Create GUI
        self.create_menu()
        self.create_widgets()
        self.refresh_streak_list()
    
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save", command=self.save_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
    
    def create_widgets(self):
        """Create main widgets"""
        # Title
        title_label = tk.Label(
            self.root, 
            text="🔥 Daily Streak Tracker", 
            font=("Arial", 20, "bold")
        )
        title_label.pack(pady=10)
        
        # Info panel
        info_frame = tk.Frame(self.root)
        info_frame.pack(pady=5)
        
        today_str = date.today().strftime("%B %d, %Y")
        today_label = tk.Label(info_frame, text=f"Today: {today_str}", font=("Arial", 10))
        today_label.pack(side=tk.LEFT, padx=10)
        
        self.token_label = tk.Label(info_frame, text="", font=("Arial", 10))
        self.token_label.pack(side=tk.LEFT, padx=10)
        self.update_token_display()
        
        # Button frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        add_btn = tk.Button(
            button_frame, 
            text="➕ Add New Streak", 
            command=self.add_streak,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=5
        )
        add_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = tk.Button(
            button_frame,
            text="🔄 Refresh",
            command=self.refresh_streak_list,
            font=("Arial", 10),
            padx=10,
            pady=5
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Streak list frame
        list_frame = tk.Frame(self.root)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Canvas for scrolling
        self.canvas = tk.Canvas(list_frame, yscrollcommand=scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.canvas.yview)
        
        # Frame inside canvas
        self.streak_frame = tk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.streak_frame, anchor="nw")
        
        # Configure scrolling
        self.streak_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Footer
        footer_label = tk.Label(
            self.root,
            text=f"Data saved to: {self.storage.get_data_path()}",
            font=("Arial", 8),
            fg="gray"
        )
        footer_label.pack(pady=5)
    
    def on_frame_configure(self, event=None):
        """Update scroll region when frame size changes"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def on_canvas_configure(self, event):
        """Update canvas window width when canvas is resized"""
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)
    
    def update_token_display(self):
        """Update restore token display"""
        current_month = self.streak_manager.get_current_month()
        token = self.streak_manager.get_or_create_restore_token(
            self.app_data.restore_tokens, 
            current_month
        )
        remaining = token.remaining_tokens()
        self.token_label.config(text=f"🎫 Restore Tokens: {remaining}/{token.max_tokens}")
    
    def refresh_streak_list(self):
        """Refresh the streak list display"""
        # Clear existing widgets
        for widget in self.streak_frame.winfo_children():
            widget.destroy()
        
        if not self.app_data.streaks:
            no_streak_label = tk.Label(
                self.streak_frame,
                text="No streaks yet. Click 'Add New Streak' to get started!",
                font=("Arial", 12),
                fg="gray"
            )
            no_streak_label.pack(pady=50)
            return
        
        # Create streak cards
        for i, streak in enumerate(self.app_data.streaks):
            self.create_streak_card(streak, i)
        
        self.update_token_display()
    
    def create_streak_card(self, streak, index):
        """Create a card widget for a streak"""
        # Main card frame
        card = tk.Frame(
            self.streak_frame,
            relief=tk.RAISED,
            borderwidth=2,
            bg="white"
        )
        card.pack(fill=tk.X, padx=5, pady=5)
        
        # Determine status and color
        status = self.streak_manager.check_streak_status(streak)
        if status == 'active':
            status_color = "#4CAF50"  # Green
            status_text = "✅ Active"
        elif status == 'broken':
            status_color = "#f44336"  # Red
            status_text = "❌ Broken"
        else:
            status_color = "#2196F3"  # Blue
            status_text = "🆕 New"
        
        # Header
        header_frame = tk.Frame(card, bg=status_color)
        header_frame.pack(fill=tk.X)
        
        name_label = tk.Label(
            header_frame,
            text=streak.name,
            font=("Arial", 14, "bold"),
            bg=status_color,
            fg="white"
        )
        name_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        status_label = tk.Label(
            header_frame,
            text=status_text,
            font=("Arial", 10),
            bg=status_color,
            fg="white"
        )
        status_label.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Info frame
        info_frame = tk.Frame(card, bg="white")
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Streak info
        current_label = tk.Label(
            info_frame,
            text=f"Current Streak: {streak.current_streak} days",
            font=("Arial", 11),
            bg="white"
        )
        current_label.pack(anchor=tk.W)
        
        longest_label = tk.Label(
            info_frame,
            text=f"Longest Streak: {streak.longest_streak} days",
            font=("Arial", 11),
            bg="white"
        )
        longest_label.pack(anchor=tk.W)
        
        if streak.last_activity_date:
            last_label = tk.Label(
                info_frame,
                text=f"Last Activity: {streak.last_activity_date}",
                font=("Arial", 10),
                fg="gray",
                bg="white"
            )
            last_label.pack(anchor=tk.W)
        
        # Button frame
        btn_frame = tk.Frame(card, bg="white")
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Mark Activity button
        mark_btn = tk.Button(
            btn_frame,
            text="✓ Mark Today",
            command=lambda s=streak: self.mark_activity(s),
            bg="#2196F3",
            fg="white",
            font=("Arial", 9, "bold")
        )
        mark_btn.pack(side=tk.LEFT, padx=2)
        
        # Restore button (only if broken)
        if status == 'broken':
            restore_btn = tk.Button(
                btn_frame,
                text="🎫 Restore",
                command=lambda s=streak: self.restore_streak(s),
                bg="#FF9800",
                fg="white",
                font=("Arial", 9, "bold")
            )
            restore_btn.pack(side=tk.LEFT, padx=2)
        
        # Delete button
        delete_btn = tk.Button(
            btn_frame,
            text="🗑 Delete",
            command=lambda idx=index: self.delete_streak(idx),
            bg="#f44336",
            fg="white",
            font=("Arial", 9)
        )
        delete_btn.pack(side=tk.RIGHT, padx=2)
    
    def add_streak(self):
        """Open dialog to add a new streak"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Streak")
        dialog.geometry("400x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Name input
        tk.Label(dialog, text="Streak Name:", font=("Arial", 11)).pack(pady=10)
        
        name_entry = tk.Entry(dialog, font=("Arial", 11), width=30)
        name_entry.pack(pady=5)
        name_entry.focus()
        
        # Predefined options
        predefined_frame = tk.Frame(dialog)
        predefined_frame.pack(pady=10)
        
        tk.Label(predefined_frame, text="Quick Add:", font=("Arial", 9)).pack(side=tk.LEFT)
        
        def set_name(name):
            name_entry.delete(0, tk.END)
            name_entry.insert(0, name)
        
        tk.Button(
            predefined_frame, 
            text="GitHub", 
            command=lambda: set_name("GitHub Commits")
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            predefined_frame, 
            text="LeetCode", 
            command=lambda: set_name("LeetCode Problem")
        ).pack(side=tk.LEFT, padx=2)
        
        # Buttons
        def on_add():
            name = name_entry.get().strip()
            if not name:
                messagebox.showwarning("Invalid Input", "Please enter a streak name.")
                return
            
            # Check if streak already exists
            for streak in self.app_data.streaks:
                if streak.name.lower() == name.lower():
                    messagebox.showwarning("Duplicate", f"Streak '{name}' already exists.")
                    return
            
            # Create new streak
            new_streak = Streak(name=name)
            self.app_data.streaks.append(new_streak)
            self.save_data()
            self.refresh_streak_list()
            dialog.destroy()
            messagebox.showinfo("Success", f"Streak '{name}' added successfully!")
        
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=20)
        
        tk.Button(
            btn_frame,
            text="Add",
            command=on_add,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            width=10
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Cancel",
            command=dialog.destroy,
            font=("Arial", 10),
            width=10
        ).pack(side=tk.LEFT, padx=5)
        
        # Enter key binding
        name_entry.bind("<Return>", lambda e: on_add())
    
    def mark_activity(self, streak):
        """Mark activity for today"""
        today = self.streak_manager.get_today()
        
        # Check if already marked
        for log in streak.activity_logs:
            if log.date == today:
                messagebox.showinfo(
                    "Already Logged",
                    f"Activity for '{streak.name}' is already logged for today!"
                )
                return
        
        # Mark activity
        success = self.streak_manager.mark_activity(streak, today, "")
        
        if success:
            self.save_data()
            self.refresh_streak_list()
            messagebox.showinfo(
                "Success",
                f"Activity marked for '{streak.name}'!\nCurrent Streak: {streak.current_streak} days 🔥"
            )
        else:
            messagebox.showerror("Error", "Failed to mark activity.")
    
    def restore_streak(self, streak):
        """Restore a broken streak using a token"""
        current_month = self.streak_manager.get_current_month()
        token = self.streak_manager.get_or_create_restore_token(
            self.app_data.restore_tokens,
            current_month
        )
        
        if not token.can_restore():
            messagebox.showwarning(
                "No Tokens",
                f"You have used all restore tokens for this month.\n"
                f"Tokens reset monthly."
            )
            return
        
        # Confirm restoration
        result = messagebox.askyesno(
            "Restore Streak",
            f"Restore '{streak.name}' streak?\n\n"
            f"This will use 1 restore token.\n"
            f"Remaining tokens: {token.remaining_tokens()}/{token.max_tokens}\n\n"
            f"Continue?"
        )
        
        if not result:
            return
        
        # Restore
        success = self.streak_manager.restore_streak(streak, token)
        
        if success:
            self.save_data()
            self.refresh_streak_list()
            messagebox.showinfo(
                "Success",
                f"Streak '{streak.name}' restored!\n"
                f"Current Streak: {streak.current_streak} days\n"
                f"Remaining tokens: {token.remaining_tokens()}/{token.max_tokens}"
            )
        else:
            messagebox.showerror("Error", "Failed to restore streak.")
    
    def delete_streak(self, index):
        """Delete a streak"""
        streak = self.app_data.streaks[index]
        
        result = messagebox.askyesno(
            "Delete Streak",
            f"Are you sure you want to delete '{streak.name}'?\n\n"
            f"This action cannot be undone."
        )
        
        if result:
            self.app_data.streaks.pop(index)
            self.save_data()
            self.refresh_streak_list()
            messagebox.showinfo("Success", f"Streak '{streak.name}' deleted.")
    
    def save_data(self):
        """Save application data"""
        self.storage.save(self.app_data)
    
    def on_closing(self):
        """Handle window closing"""
        self.save_data()
        self.root.destroy()


def main():
    """Main entry point for GUI"""
    root = tk.Tk()
    app = StreakTrackerGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
