import tkinter as tk
from tkinter import ttk
from datetime import datetime

root = tk.Tk()
root.title("Birthday Countdown")
root.configure(background='#FFEBB2')  # Setting background color for the root window

# Create a custom style
style = ttk.Style()

# Configure the style for labels
style.configure('CustomLabel.TLabel', font=('helvetica', 12,'bold'), foreground='#191919', background='#3D3B40')
style.configure('Bold.TLabel', font=('helvetica', 20, 'bold'), foreground='#191919', background='#3D3B40')

# Function to update the current date and time every second
def update_datetime():
    date = datetime.now()
    currentdate.config(text="Current Date: " + date.strftime("%Y-%m-%d"))
    currenttime.config(text="Current Time: " + date.strftime("%I:%M:%S %p"))  # Format with AM/PM
    root.after(1000, update_datetime)

# Function to calculate and display remaining time until the next birthday
def update_remaining_time():
    event="2005-07-23"#replace your event day for instance i have placed the birthdate
    birthdate = datetime.strptime(event, '%Y-%m-%d')
    current_date = datetime.now()

    next_birthday = datetime(current_date.year, birthdate.month, birthdate.day)
    if next_birthday < current_date:
        next_birthday = datetime(current_date.year + 1, birthdate.month, birthdate.day)

    remaining_time = next_birthday - current_date

    # Calculate remaining time in seconds
    total_seconds = remaining_time.total_seconds()

    # Calculate weeks, days, hours, minutes, and seconds
    weeks, remainder = divmod(total_seconds, 604800)  # 1 week = 7 days = 604800 seconds
    days, remainder = divmod(remainder, 86400)         # 1 day = 86400 seconds
    hours, remainder = divmod(remainder, 3600)         # 1 hour = 3600 seconds
    minutes, seconds = divmod(remainder, 60)

    # Update the labels with the remaining time
    remaining_time_label.config(text="Time Until Next Birthday", style='Bold.TLabel')
    weeks_label.config(text="Weeks: " + str(int(weeks)), style='CustomLabel.TLabel')
    days_label.config(text="Days: " + str(int(days)), style='CustomLabel.TLabel')
    hours_label.config(text="Hours: " + str(int(hours)), style='CustomLabel.TLabel')
    minutes_label.config(text="Minutes: " + str(int(minutes)), style='CustomLabel.TLabel')
    seconds_label.config(text="Seconds: " + str(int(seconds)), style='CustomLabel.TLabel')

    # Schedule the update_remaining_time() function to run after 1 second
    root.after(1000, update_remaining_time)

# Labels for current date and time
currentdate = ttk.Label(root, style='CustomLabel.TLabel', background='#FFEBB2')
currentdate.grid(row=0, column=0, padx=20, pady=(30, 5), sticky=tk.W)
currenttime = ttk.Label(root, style='CustomLabel.TLabel', background='#FFEBB2')
currenttime.grid(row=1, column=0, padx=20, pady=5, sticky=tk.W)

# Labels for remaining time
remaining_time_label = ttk.Label(root, style='Bold.TLabel', background='#FFEBB2')
remaining_time_label.grid(row=2, column=0, padx=20, pady=10, columnspan=2, sticky=tk.W)
weeks_label = ttk.Label(root, style='CustomLabel.TLabel', background='#FFEBB2')
weeks_label.grid(row=3, column=0, padx=20, pady=2, sticky=tk.W)
days_label = ttk.Label(root, style='CustomLabel.TLabel', background='#FFEBB2')
days_label.grid(row=4, column=0, padx=20, pady=2, sticky=tk.W)
hours_label = ttk.Label(root, style='CustomLabel.TLabel', background='#FFEBB2')
hours_label.grid(row=5, column=0, padx=20, pady=2, sticky=tk.W)
minutes_label = ttk.Label(root, style='CustomLabel.TLabel', background='#FFEBB2')
minutes_label.grid(row=6, column=0, padx=20, pady=2, sticky=tk.W)
seconds_label = ttk.Label(root, style='CustomLabel.TLabel', background='#FFEBB2')
seconds_label.grid(row=7, column=0, padx=20, pady=2, sticky=tk.W)

# Start updating date, time, and remaining time
update_datetime()
update_remaining_time()

root.mainloop()
