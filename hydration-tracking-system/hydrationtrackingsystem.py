from tkinter import *
from datetime import datetime
import os
import pyautogui
import pyttsx3
def main():
    def read_data():
        try:
            with open("log.txt", "r") as file:
                lines = file.readlines()
                if lines:
                    last_entry_date = lines[-1].split()[0]  # Extracting the date from the last entry
                    current_date = datetime.today().strftime('%Y-%m-%d')
                    if last_entry_date != current_date:
                        # Delete the file
                        os.remove("log.txt")
                        # Rewrite the file with current date and 0 cups
                        write_data(0)
                        return 0
                    else:
                        return int(lines[-1].split()[1])
                else:
                    # If file is empty, write current date and 0 cups
                    write_data(0)
                    return 0
        except FileNotFoundError:
            # If file doesn't exist, write current date and 0 cups
            write_data(0)
            return 0

    def write_data(data):
        with open("log.txt", "a") as file:
            today = datetime.today().strftime('%Y-%m-%d')
            file.write("\n{} {}".format(today, data))

    def updatecupandamount():
        try:
            amount = int(entry.get())
            updated_cups = read_data() + amount
            write_data(updated_cups)
            cupsno_label.config(text=str(updated_cups))
            amountno_label.config(text=str(updated_cups * 0.300))
            restart()
        except ValueError:
            said("Please enter a valid number")
            error_label.config(text="Please enter a valid number", fg="red")

    def restart():
        root.destroy()
        main()

    root = Tk()
    root.configure(bg="#31363F")
    root.title("hydration tracking system")
    root.resizable(False,False)
    root.iconbitmap(r"E:\vscode\python\PYTHON FILES\TKINTER PROJECTS\water remainder\1490877846-sport-badges01_82420.ico")
    cupsno = read_data()

    head = Label(root, text="HYDRATION TRACKING SYSTEM", fg="#fbfbfb", bg="#31363F", font="stencil 40 bold", padx=10)
    head.grid(row=0, column=0, columnspan=2)

    ongoing = Label(root, text="On going time: ", fg="#fbfbfb", bg="#31363F", font="stencil 20 bold")
    ongoing.grid(row=1, column=0, columnspan=2)

    Time = Label(root, text="", fg="#fbfbfb", bg="#31363F", font="stencil 20 bold")
    Time.grid(row=2, column=0, columnspan=2)
    Time.config(text=datetime.today().strftime('%H:%M:%S'))

    cups_label = Label(root, text="No. of cups :", fg="#fbfbfb", bg="#31363F", font="stencil 20 bold")
    cups_label.grid(row=3, column=0)

    cupsno_label = Label(root, text=str(cupsno), fg="#fbfbfb", bg="#31363F", font="stencil 20 bold")
    cupsno_label.grid(row=3, column=1)

    amount_label = Label(root, text="amount of water in L :", fg="#fbfbfb", bg="#31363F", font="stencil 20 bold")
    amount_label.grid(row=4, column=0)

    amountno_label = Label(root, text=str(cupsno * 0.3), fg="#fbfbfb", bg="#31363F", font="stencil 20 bold")
    amountno_label.grid(row=4, column=1)

    countdown_label = Label(root, text="next in :", fg="#fbfbfb", bg="#31363F", font="stencil 20 bold")
    countdown_label.grid(row=5, column=0)

    next_time_label = Label(root, text="", fg="#fbfbfb", bg="#31363F", font="stencil 20 bold")
    next_time_label.grid(row=5, column=1)

    global remaining_time
    remaining_time = 3600
    def said(text):
        import pyttsx3

        # Initialize the TTS engine
        engine = pyttsx3.init()

        # Set properties (optional)
        engine.setProperty('rate', 150)  # Speed of speech
        engine.setProperty('volume', 1)  # Volume (0.0 to 1.0)

        # Speak the text
        
        engine.say(text)

        # Wait for speech to finish
        engine.runAndWait()

    def countdown():
        global remaining_time
        if remaining_time > 0:
            remaining_time -= 1
            minutes, seconds = divmod(remaining_time, 60)
            next_time_label.config(text="{:02d}:{:02d}".format(minutes, seconds))
            
            # Update current time
            Time.config(text=datetime.today().strftime('%I:%M:%S %p'))

            
            root.after(1000, countdown)
        else:
            said("its time to drink water sir!!")
            next_time_label.config(text="Time's up!")
            
            entry_label = Label(root, text="How many cups have you drunk?", fg="#fbfbfb", bg="#31363F", font="stencil 20 bold")
            entry_label.grid(row=6, column=0, columnspan=1)
            global entry
            entry = Entry(root)
            entry.grid(row=6, column=1)
            os.system("rundll32.exe user32.dll,LockWorkStation")
            said("you can unlock after drinking water")
            submit_button = Button(root, text="Submit",width=30,bg="#FDA403", font="stencil 14 italic",command=updatecupandamount)
            submit_button.grid(row=7, column=0, columnspan=2)


    countdown()

    error_label = Label(root, text="",bg="#31363F")
    error_label.grid(row=8, column=0, columnspan=2)

    root.mainloop()

main()

