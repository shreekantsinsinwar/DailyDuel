# Create the DailyDuel Gryffindor-themed productivity app in a single Python file

from tkinter import *
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# App Data File
DATA_FILE = "dailyduel_data.json"

# Default Data
default_data = {
    "streak": 0,
    "last_date": "",
    "house_points": 0,
    "history": []
}

# Load or Initialize Data
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump(default_data, f)

with open(DATA_FILE, "r") as f:
    data = json.load(f)

# Categories & Challenges
challenges = {
    "Focus Quest": [
        "Do a 25-minute deep work session.",
        "Write 100 words without stopping.",
        "Read a technical article and summarize it."
    ],
    "Physical Trial": [
        "Do 10 push-ups.",
        "Stretch for 5 minutes.",
        "Take a 10-minute walk."
    ],
    "Learning Duel": [
        "Watch one educational video.",
        "Revise a concept from yesterday.",
        "Create a mind map of something you learned."
    ],
    "Decluttering Spell": [
        "Delete one unused file/folder.",
        "Clear your desktop.",
        "Organize one directory."
    ],
    "Gratitude Scroll": [
        "Write down one thing you're grateful for.",
        "Send a thank you message to someone.",
        "Smile at yourself in the mirror for 10 seconds."
    ]
}

# Random daily challenge
def get_daily_challenge():
    category = random.choice(list(challenges.keys()))
    task = random.choice(challenges[category])
    return category, task

# GUI App
app = Tk()
app.title("DailyDuel: Gryffindor Quest")
app.geometry("780x600")
app.configure(bg="#7F0909")  # Gryffindor maroon

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", foreground="white", background="#D3A625", font=("Verdana", 10, "bold"))
style.configure("TLabel", background="#7F0909", foreground="white", font=("Verdana", 11))
style.configure("TNotebook", background="#7F0909", foreground="white")
style.configure("TFrame", background="#7F0909")

notebook = ttk.Notebook(app)
notebook.pack(fill='both', expand=True)

# Tabs
challenge_tab = Frame(notebook, bg="#7F0909")
history_tab = Frame(notebook, bg="#7F0909")
analysis_tab = Frame(notebook, bg="#7F0909")
help_tab = Frame(notebook, bg="#7F0909")

notebook.add(challenge_tab, text="🎯 Daily Challenge")
notebook.add(history_tab, text="📜 History")
notebook.add(analysis_tab, text="📊 Analysis")
notebook.add(help_tab, text="❓ How to Use")

# Save Data
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# Daily Challenge Logic
today = datetime.now().strftime("%Y-%m-%d")

if data["last_date"] != today:
    cat, task = get_daily_challenge()
    data["last_category"] = cat
    data["last_task"] = task
    data["last_date"] = today
    save_data()
else:
    cat = data.get("last_category", "")
    task = data.get("last_task", "")

def complete_task():
    if data["last_date"] != today:
        messagebox.showinfo("Oops!", "No challenge for today!")
        return
    data["streak"] += 1
    data["house_points"] += 10
    data["history"].append({
        "date": today,
        "category": cat,
        "task": task,
        "status": "Completed"
    })
    save_data()
    messagebox.showinfo("Bravo!", "10 Points to Gryffindor! 🔥")
    app.destroy()

# Challenge Tab Layout
ttk.Label(challenge_tab, text="Today's Challenge", font=("Georgia", 16, "bold")).pack(pady=20)
ttk.Label(challenge_tab, text=f"Category: {cat}", font=("Georgia", 13)).pack(pady=5)
ttk.Label(challenge_tab, text=f"🧙 Task: {task}", wraplength=600, justify="center", font=("Georgia", 12)).pack(pady=10)
ttk.Button(challenge_tab, text="✅ Mark as Done", command=complete_task).pack(pady=30)

# History Tab Layout
def populate_history():
    for widget in history_tab.winfo_children():
        widget.destroy()

    ttk.Label(history_tab, text="Challenge History", font=("Georgia", 14, "bold")).pack(pady=10)
    for entry in reversed(data["history"][-30:]):
        line = f"{entry['date']} - [{entry['category']}] {entry['task']} ✅"
        ttk.Label(history_tab, text=line, wraplength=700).pack(anchor="w", padx=10)

populate_history()

# Analysis Tab Layout
def generate_chart():
    for widget in analysis_tab.winfo_children():
        widget.destroy()

    categories = [entry["category"] for entry in data["history"]]
    freq = {cat: categories.count(cat) for cat in set(categories)}

    fig, ax = plt.subplots(figsize=(5, 4))
    wedges, texts, autotexts = ax.pie(freq.values(), labels=freq.keys(), autopct='%1.1f%%', startangle=90)
    ax.set_title("Challenges by Category", color="#D3A625")

    canvas = FigureCanvasTkAgg(fig, master=analysis_tab)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=20)

ttk.Button(analysis_tab, text="🎇 Generate Pie Chart", command=generate_chart).pack(pady=20)

# Help Tab Layout
help_text = """
📌 How to Use DailyDuel

1. Open the app daily and check the 'Daily Challenge' tab.
2. Complete the challenge — it could be a physical task, deep work, declutter, etc.
3. Hit ✅ 'Mark as Done' to gain 10 House Points and maintain your Streak!
4. View your challenge history in the 📜 'History' tab.
5. Analyze your efforts with beautiful charts in 📊 'Analysis'.
6. Missing a day breaks your streak — try to keep the 🔥 going!

Make Gryffindor proud with your daily discipline 🦁✨
"""

Label(help_tab, text=help_text, justify=LEFT, wraplength=700, bg="#7F0909", fg="white", font=("Georgia", 12)).pack(pady=20, padx=20)

# Launch App
app.mainloop()
