import tkinter as tk
from tkinter import simpledialog, messagebox
from streak_data import load_streaks, save_streaks
from streak_logic import check_in, restore_streak

# Load streaks from file
streaks = load_streaks()

# Create main window
root = tk.Tk()
root.title("Multi Streak Tracker")
root.geometry("500x600")

# Frame to hold streak info
frame = tk.Frame(root)
frame.pack(pady=20)

# Function to dynamically create streaks
def create_streak(streaks, name):
    if name not in streaks:
        streaks[name] = {
            "name": name,
            "count": 0,
            "last_date": None,
            "restores": 0,
            "restore_month": None
        }
        save_streaks(streaks)  # save immediately
        print(f"✅ Streak '{name}' created!")
    else:
        print(f"⚠️ Streak '{name}' already exists.")

# Function to update the display
def update_display():
    for widget in frame.winfo_children():
        widget.destroy()  # clear previous widgets

    for name, streak in streaks.items():
        # Display streak info
        streak_name = streak.get('name', name)
        count = streak.get('count', 0)
        last_date = streak.get('last_date', None)
        label = tk.Label(frame, text=f"{streak_name} - Streak: {count} - Last: {last_date}")
        label.pack(pady=5)

        # Check-in button
        def make_checkin(s=streak):
            def inner():
                from streak_logic import check_in
                success = check_in(s)
                if success:
                    save_streaks(streaks)
                    update_display()
                    tk.messagebox.showinfo("Check-in", f"✅ Checked in! Current streak: {s['count']}")
                else:
                    tk.messagebox.showwarning("Check-in", "⚠️ Already checked in today!")
            return inner

        checkin_btn = tk.Button(frame, text="Check-in", command=make_checkin())
        checkin_btn.pack(pady=2)

        # Restore button
        def make_restore(s=streak):
            def inner():
                from streak_logic import restore_streak
                success, message = restore_streak(s)
                save_streaks(streaks)
                update_display()
                tk.messagebox.showinfo("Restore", message)
            return inner

        restore_btn = tk.Button(frame, text="Restore", command=make_restore())
        restore_btn.pack(pady=2)

def add_new_streak():
    name = simpledialog.askstring("New Streak", "Enter streak name:")
    if name:
        create_streak(streaks, name)
        update_display()
# Button to add streaks
add_button = tk.Button(root, text="Add New Streak", command=add_new_streak)
add_button.pack(pady=10)
# Initial display
update_display()

# Run the GUI
root.mainloop()

