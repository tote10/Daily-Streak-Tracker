import json
from datetime import datetime, date, timedelta
import tkinter as tk
from tkinter import simpledialog, messagebox

# Load streaks from file
try:
    with open("streaks.json", "r") as f:
        streaks = json.load(f)
except FileNotFoundError:
    streaks = {}

# Save streaks to file
def save_streaks():
    with open("streaks.json", "w") as f:
        json.dump(streaks, f, indent=4)

# Check-in function
def check_in(name):
    today = date.today().isoformat()
    if name not in streaks:
        streaks[name] = {"count": 0, "last_date": None, "restores": 0, "restore_month": None}

    last_date = streaks[name]["last_date"]
    if last_date == today:
        messagebox.showinfo("Check-in", f"You already checked in today for {name}!")
        return

    if last_date:
        last_date_obj = datetime.fromisoformat(last_date).date()
        yesterday = date.today() - timedelta(days=1)
        if last_date_obj < yesterday:
            streaks[name]["count"] = 0

    streaks[name]["count"] += 1
    streaks[name]["last_date"] = today
    save_streaks()
    update_display()
    messagebox.showinfo("Check-in", f"✅ Checked in {name}! Current streak: {streaks[name]['count']}")

# Restore function
def restore_streak(name):
    today_month = date.today().month
    if name not in streaks:
        messagebox.showerror("Error", f"{name} does not exist!")
        return

    if streaks[name]["restore_month"] != today_month:
        streaks[name]["restores"] = 0
        streaks[name]["restore_month"] = today_month

    if streaks[name]["restores"] < 5:
        streaks[name]["count"] += 1
        streaks[name]["restores"] += 1
        save_streaks()
        update_display()
        messagebox.showinfo("Restore", f"✅ {name} streak restored! Current streak: {streaks[name]['count']}")
    else:
        messagebox.showwarning("Restore", f"❌ Maximum restores reached for {name} this month!")

# Tkinter GUI
root = tk.Tk()
root.title("Multi Streak Tracker")
root.geometry("500x600")

frame = tk.Frame(root)
frame.pack(pady=10)

def update_display():
    for widget in frame.winfo_children():
        widget.destroy()
    for name, info in streaks.items():
        tk.Label(frame, text=f"{name} - Streak: {info['count']} - Last: {info['last_date']} - Restores: {info['restores']}", font=("Arial", 12)).pack()
        tk.Button(frame, text=f"Check-in {name}", command=lambda n=name: check_in(n)).pack(pady=2)
        tk.Button(frame, text=f"Restore {name}", command=lambda n=name: restore_streak(n)).pack(pady=2)
        tk.Label(frame, text="----------------------").pack()

def add_streak():
    name = simpledialog.askstring("New Streak", "Enter streak name:")
    if name:
        if name in streaks:
            messagebox.showwarning("Warning", f"{name} already exists!")
            return
        streaks[name] = {"count": 0, "last_date": None, "restores": 0, "restore_month": None}
        save_streaks()
        update_display()

tk.Button(root, text="Add New Streak", command=add_streak, font=("Arial", 12), bg="lightblue").pack(pady=5)
tk.Button(root, text="Exit", command=root.destroy, font=("Arial", 12), bg="lightcoral").pack(pady=5)

update_display()
root.mainloop()
