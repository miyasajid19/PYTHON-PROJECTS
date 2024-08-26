from tkinter import *
from tkinter import messagebox
import sqlite3
from datetime import datetime
import os

DB_FILE = "messenger.db"

def connection1():
    try:
        conn = sqlite3.connect(DB_FILE)
        create_table_if_not_exists(conn)
        return conn
    except Exception as e:
        messagebox.showerror("Error", e)

def create_table_if_not_exists(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                name VARCHAR(255) NOT NULL,
                mail VARCHAR(255) UNIQUE NOT NULL,
                passkey VARCHAR(255)
            )
        """)
        conn.commit()
    except Exception as e:
        messagebox.showerror("Error", e)

def chat(username, friend):
    global frame1
    if frame1 is not None:
        frame1.destroy()

    frame1 = Frame(root, bg=b)
    frame1.pack(fill=BOTH, expand=True)
    
    def refresh():
        update_chat()
        frame1.after(1, refresh)

    chatframe = Frame(frame1)
    chatframe.grid(row=0, column=0, sticky="nsew")

    messageframe = Frame(frame1)
    messageframe.grid(row=1, column=0, sticky="ew")
    
    frame1.grid_rowconfigure(0, weight=1)
    frame1.grid_columnconfigure(0, weight=1)

    chats_folder = "chats"
    if not os.path.exists(chats_folder):
        os.makedirs(chats_folder)

    if username > friend:
        file_path = os.path.join(chats_folder, f"{username}_{friend}.txt")
    else:
        file_path = os.path.join(chats_folder, f"{friend}_{username}.txt")

    scrollbar = Scrollbar(chatframe)
    scrollbar.pack(side=RIGHT, fill=Y)

    text_widget = Text(chatframe, wrap=WORD, yscrollcommand=scrollbar.set)
    text_widget.pack(side=LEFT, fill=BOTH, expand=True)

    scrollbar.config(command=text_widget.yview)

    def update_chat():
        try:
            with open(file_path, "r") as file:
                content = file.read()
                text_widget.config(state=NORMAL)
                text_widget.delete(1.0, END)
                text_widget.insert(END, content)
                text_widget.config(state=DISABLED)
                text_widget.see(END)
        except FileNotFoundError:
            pass
        except Exception as e:
            messagebox.showerror("error",e)

    update_chat()

    def send(event=None):
        msg = f"{username} : {message.get()}\n"
        with open(file_path, "a") as file:
            file.write(msg)
        message.delete(0, END)
        update_chat()
    def end():
        frame1.destroy()
        main()
    message = Entry(messageframe, width=50, font="Helvetica 15 italic",fg=b,bg="#FFD0EC")
    message.grid(row=0, column=0)
    Button(messageframe, text="Send", width=10, command=send,font="jokerman 10 italic",bg=b,fg="#FFD0EC").grid(row=0, column=1)
    Button(messageframe, text="End", width=10, command=end,font="jokerman 10 italic",bg=b,fg="#FFD0EC").grid(row=0, column=2)

    message.bind("<Return>", send)

    refresh()

def chatwith(username):
    global frame1
    frame1.destroy()
    frame1 = Frame(root)
    frame1.pack()
    conn = connection1()
    mycursor = conn.cursor()
    
    try:
        sql = "SELECT name FROM users"
        mycursor.execute(sql)
        data = mycursor.fetchall()
        conn.commit()
    except Exception as e:
        messagebox.showerror("Error", e)
    finally:
        conn.close()

    values = set()
    for i in data:
        values.add(i[0])

    Label(frame1, text="chat with : ", bg=b, font="stencil 20 bold").grid(row=0, column=0)
    friend = StringVar()
    friend.set("choose")
    OptionMenu(frame1, friend, *values).grid(row=0, column=1, padx=3, pady=3)
    
    def go():
        chat(username, friend.get())
        
    Button(frame1, text="start chat", font="helvetica 15 italic", width=20, height=1, border=1, fg=b, bg="#FFD0EC", command=go).grid(row=1, column=0, columnspan=2)

def register():
    global frame1, name, email, password, cpassword
    username = name.get()
    mail = email.get()
    key = password.get()
    ckey = cpassword.get()
    if username == '' or mail == '' or key == '' or ckey == '':
        messagebox.showinfo("info","required")
    else:
        if key != ckey:
            messagebox.showerror("error","passwords didn't match")
        else:
            conn = connection1()
            mycursor = conn.cursor()
            try:
                sql = f"INSERT INTO users(name, mail, passkey) VALUES (?, ?, ?)"
                mycursor.execute(sql, (username, mail, key))
                conn.commit()
                conn.close()
                messagebox.showinfo("info", "registered successfully")
                frame1.destroy()
                main()
            except Exception as e:
                messagebox.showerror("error", e)

def signup():
    global frame1, name, email, password, cpassword
    frame1.destroy()
    frame1 = Frame(root, bg=b)
    frame1.pack()
    Label(frame1, text="name : ", bg=b, fg="#FFD0EC", font="Verdana 20 italic").grid(row=0, column=0)
    name = Entry(frame1, width=40, font="helvetica 12 italic", bg="#FFD0EC", fg=b)
    name.grid(row=0, column=1, padx=10, pady=10, sticky="e")
    Label(frame1, text="Email : ", bg=b, fg="#FFD0EC", font="Verdana 20 italic").grid(row=1, column=0)
    email = Entry(frame1, width=40, font="helvetica 12 italic", bg="#FFD0EC", fg=b)
    email.grid(row=1, column=1, padx=10, pady=10, sticky="e")
    Label(frame1, text="password : ", bg=b, fg="#FFD0EC", font="Verdana 20 italic").grid(row=2, column=0)
    password = Entry(frame1, width=40, font="helvetica 12 italic", bg="#FFD0EC", fg=b, show="*")
    password.grid(row=2, column=1, padx=10, pady=10, sticky="e")
    Label(frame1, text="confirm password : ", bg=b, fg="#FFD0EC", font="Verdana 20 italic").grid(row=3, column=0)
    cpassword = Entry(frame1, width=40, font="helvetica 12 italic", bg="#FFD0EC", fg=b, show="*")
    cpassword.grid(row=3, column=1, padx=10, pady=10, sticky="e")
    Button(frame1, text="Register", font="helvetica 15 italic", width=20, height=1, border=1, fg=b, bg="#FFD0EC", command=register).grid(row=4, column=0, columnspan=2)



def login():
    global email, key
    conn = connection1()
    mycursor = conn.cursor()
    try:
        sql = "SELECT name FROM users WHERE mail = ? AND passkey = ?"
        mycursor.execute(sql, (email.get(), key.get()))
        data = mycursor.fetchone()
        if data:
            chatwith(data[0])
        else:
            messagebox.showerror("Error", "Invalid email or password")
    except Exception as e:
        messagebox.showerror("Error", e)
    finally:
        conn.close()

def main():
    global frame1, email, key
    frame1 = Frame(root, bg=b)
    frame1.pack()

    Label(frame1, text="Email : ", bg=b, fg="#FFD0EC", font="Verdana 20 italic").grid(row=1, column=0)
    email = Entry(frame1, width=40, font="helvetica 12 italic", bg="#FFD0EC", fg=b)
    email.grid(row=1, column=1, padx=10, pady=10, sticky="e")
    Label(frame1, text="Password : ", bg=b, fg="#FFD0EC", font="Verdana 20 italic").grid(row=2, column=0)
    key = Entry(frame1, width=40, font="helvetica 12 italic", bg="#FFD0EC", fg=b, show="*")
    key.grid(row=2, column=1, padx=10, pady=10, sticky="e")
    Button(frame1, text="Log In", font="helvetica 15 italic", width=20, height=1, border=1, fg=b, bg="#FFD0EC", command=login).grid(row=4, column=0, columnspan=2,padx=10,pady=10)
    Label(frame1, text="Don't have account??", font="verdana 15", bg=b, fg="#FFD0EC", justify="center").grid(row=5, column=0, sticky="w",padx=10,pady=10)
    Button(frame1, text="sign up", bg=b, fg="#ECEE81", font="Impact 15 bold", border=0, command=signup).grid(row=5, column=1, sticky="w",padx=10,pady=10)

# Check if database and table exist, if not, create them
if not os.path.exists(DB_FILE):
    with sqlite3.connect(DB_FILE) as conn:
        create_table_if_not_exists(conn)

root = Tk()
root.title("tkinter messaging app")
root.iconbitmap(r"icon.ico")
b = "#865DFF"
root.configure(bg=b)
main()
root.mainloop()
