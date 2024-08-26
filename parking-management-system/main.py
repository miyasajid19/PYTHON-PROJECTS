from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from datetime import datetime
import smtplib as sp
import webbrowser
import pyttsx3
root = Tk()
root.title("Parking Management System")
root.iconbitmap(r"parking_car_paid_icon_180136.ico")
root.configure(bg="#FFEBB2")
b = "#FFEBB2"
global frame1
frame1 = Frame(root)
frame1.configure(bg=b)
frame1.pack()
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[0].id)


def connection1():
    try:
        connection = mysql.connector.connect(host="localhost", user="root", password="", database="parking")
        if connection.is_connected():
            return connection
    except Exception as e:
        speak(e)
        messagebox.showerror("error", e)
def give():
    global slotid,licenseno
    global casid, recieverid, amount, senderpassword
    global slotid,slotname,slotkey,licenseno,licenses
    sid = casid.get()
    rid = recieverid.get()
    rs = int(amount.get())
    spassword = senderpassword.get()

    try:
        connection = mysql.connector.connect(host="localhost", user="root", password="", database="bankingsystem")
        cursor = connection.cursor()

        # Check if sender and receiver exist
        cursor.execute("SELECT * FROM `users`")
        users = cursor.fetchall()
        user_ids = {user[0] for user in users}

        if sid in user_ids and rid in user_ids:
            # Check sender's balance and perform transaction
            cursor.execute("SELECT amount FROM account WHERE casid = %s AND passs = %s", (sid, spassword))
            sender_balance = cursor.fetchone()
            if sender_balance:
                sender_balance = int(sender_balance[0])
                if sender_balance >= rs:
                    sender_balance -= rs
                    cursor.execute("UPDATE account SET amount = %s WHERE casid = %s", (sender_balance, sid))

                    # Update receiver's balance
                    cursor.execute("SELECT amount FROM account WHERE casid = %s", (rid,))
                    receiver_balance = int(cursor.fetchone()[0])
                    receiver_balance += rs
                    cursor.execute("UPDATE account SET amount = %s WHERE casid = %s", (receiver_balance, rid))
                    
                    connection.commit()
                    messagebox.showinfo("Success", f"{rs} has been paid")
                    connection.close()
                    conn=connection1()
                    mycursor=conn.cursor()
                    sql1=f"delete from  `booked`where uid='{slotid}'"
                    mycursor.execute(sql1)
                    speak(f" Rs. {rs} has been successfully credited to SMPK bank account")
                    conn.commit()
                    conn.close()
                    conn=connection1()
                    mycursor=conn.cursor()
                    sql2=f"UPDATE `slots` SET `status`='vacant' WHERE uid='{slotid}'"
                    mycursor.execute(sql2)
                    
                    conn.commit()
                    conn.close()
                    conn=connection1()
                    mycursor=conn.cursor()
                    sql3=f"delete from  `users`where licenseno='{licenses}'"
                    mycursor.execute(sql3)
                    
                    conn.commit()
                    conn.close()
                    global frame1
                    frame1.destroy()
                    # Declare frame1 as global
                    frame1.pack_forget()  # Use pack_forget() instead of frame1.forget()
                    frame1 = Frame(root)
                    frame1.configure(bg=b)
                    frame1.grid(row=0, column=0, sticky="nsew")
                    main()
                else:
                    speak("Insufficient balance to proceed with the transaction")
                    messagebox.showerror("Error", "Insufficient balance to proceed with the transaction")
            else:
                speak("invalid password")
                messagebox.showerror("Error", "Invalid password")
        else:
            speak("Either sender or receiver does not have a bank account")
            messagebox.showerror("Error", "Either sender or receiver does not have a bank account")
    except mysql.connector.Error as e:
        speak(f"Database error : {e}")
        messagebox.showerror("Error", f"Database error: {e}")
    finally:
        if 'connection' in locals():
            connection.close()
        

def pay():
    global slotid,slotname,slotkey,licenseno,licenses
    licenses=licenseno.get()
    global frame1,b
    global casid,recieverid,amount,senderpassword
    global cost
    frame1.destroy()  # Destroy the existing frame
    frame1 = Frame(root)  # Recreate the frame
    frame1.configure(bg=b)
    frame1.pack()
    Label(frame1,text='user cas id : ',bg=b,font="helvetica 20 bold").grid(row=3,column=0,sticky=N,padx=10,pady=10)
    casid=Entry(frame1,width=40)
    casid.grid(row=3,column=1,padx=10,pady=10)
    Label(frame1,text='reciever-id : ',bg=b,font="helvetica 20 bold").grid(row=4,column=0,sticky=N,padx=10,pady=10)
    recieverid=Entry(frame1,width=40)
    recieverid.grid(row=4,column=1,padx=10,pady=10)
    recieverid.insert(0,"3365427625")
    recieverid.config(state="disabled")
    Label(frame1,text='amount : ',bg=b,font="helvetica 20 bold").grid(row=5,column=0,sticky=N,padx=10,pady=10)
    amount=Entry(frame1,width=40)
    amount.grid(row=5,column=1,padx=10,pady=10)
    amount.insert(0,cost)
    amount.config(state="disabled")
    Label(frame1,text='sender-password : ',bg=b,font="helvetica 20 bold").grid(row=6,column=0,sticky=N,padx=10,pady=10)
    senderpassword=Entry(frame1,width=20,show='.',font="stencil 15 bold")
    senderpassword.grid(row=6,column=1,padx=10,pady=10)
    Button(frame1,text="pay",command=give,width=40,height=1,border=3,bd=3).grid(row=7,columnspan=2,padx=10,pady=10,sticky=N)

    
    
def proceed():
    
    global slotid1,key1,slotname1,cost
    global slotid,slotname,slotkey
    slotid=slotid1.get()
    slotname=slotname1.get()
    slotkey=key1.get()
    conn=connection1()
    mycursor=conn.cursor()
    sql=f"SELECT `uid`, `sectionname`, `licenseno`, `vehicleno`, `start_time`, `cost` FROM `booked` WHERE uid='{slotid}'"
    mycursor.execute(sql)
    data=mycursor.fetchone()
    sql1=f"SELECT `licenseno`, `vehicleno`, `name`, `age`, `sex`, `contact`, `email` FROM `users` WHERE licenseno='{data[2]}'"
    mycursor.execute(sql1)
    data1=mycursor.fetchone()
    conn.commit()
    conn.close()
    global frame1,b
    global slotarea,licenseno,vehicleno,name,sex,age,contact,email,cost
    frame1.destroy()  # Destroy the existing frame
    frame1 = Frame(root)  # Recreate the frame
    frame1.configure(bg=b)
    frame1.pack()  # Pack the recreated frame
    
    
    Label(frame1,text="License No. :",bg=b,fg="#31363F",font="stencil 24 bold").grid(row=2,column=0,padx=10,pady=10)
    licenseno=Entry(frame1,width=15,fg="#31363F",font="helvetica 24 italic")
    licenseno.grid(row=2,column=1,padx=10,pady=10)
    licenseno.insert(0,data1[0])
    licenseno.config(state="disabled")

    Label(frame1,text="Vehicle No. :",bg=b,fg="#31363F",font="stencil 24 bold").grid(row=2,column=2,padx=10,pady=10)
    vehicleno=Entry(frame1,width=15,fg="#31363F",font="helvetica 24 italic")
    vehicleno.grid(row=2,column=3,padx=10,pady=10)
    vehicleno.insert(0,data1[1])
    vehicleno.config(state="disabled")

    Label(frame1,text="Name :",bg=b,fg="#31363F",font="stencil 24 bold").grid(row=3,column=0,padx=10,pady=10)
    name=Entry(frame1,width=15,fg="#31363F",font="helvetica 24 italic")
    name.grid(row=3,column=1,padx=10,pady=10)
    name.insert(0,data1[2])
    name.config(state="disabled")

    Label(frame1,text="Age :",bg=b,fg="#31363F",font="stencil 24 bold").grid(row=3,column=2,padx=10,pady=10)
    age=Entry(frame1,width=15,fg="#31363F",font="helvetica 24 italic")
    age.grid(row=3,column=3,padx=10,pady=10)
    age.insert(0,data1[3])
    age.config(state="disabled")

    values=['Male','Female','Others']
    sex=StringVar()
    sex.set(data1[4])
    OptionMenu(frame1,sex,*values).grid(row=4,column=1,padx=10,pady=10)
    Label(frame1,text="Sex :",bg=b,fg="#31363F",font="stencil 24 bold",state="disabled").grid(row=4,column=0,padx=10,pady=10)
    #sex=Entry(frame1,width=15,fg="#31363F",font="helvetica 24 italic")
    

    Label(frame1,text="Contact No. :",bg=b,fg="#31363F",font="stencil 24 bold").grid(row=4,column=2,padx=10,pady=10)
    contact=Entry(frame1,width=15,fg="#31363F",font="helvetica 24 italic")
    contact.grid(row=4,column=3,padx=10,pady=10)
    contact.insert(0,data1[5])
    contact.config(state="disabled")

    Label(frame1,text="E-mail :",bg=b,fg="#31363F",font="stencil 24 bold").grid(row=5,column=0,padx=10,pady=10)
    email=Entry(frame1,width=15,fg="#31363F",font="helvetica 24 italic")
    email.grid(row=5,column=1,padx=10,pady=10)
    email.insert(0,data1[6])
    email.config(state="disabled")
    global cost1
    Label(frame1,text="Basic Cost :",bg=b,fg="#31363F",font="stencil 24 bold").grid(row=5,column=2,padx=10,pady=10)
    cost1=Entry(frame1,width=15,fg="#31363F",font="helvetica 24 italic")
    cost1.grid(row=5,column=3,padx=10,pady=10)
    # Parse the string into a datetime object
    datetime_from_database = datetime.strptime(str(data[4]), "%Y-%m-%d %H:%M:%S")

    # Get the current datetime
    current_datetime = datetime.now()
    current_datetime = current_datetime.replace(microsecond=0)
    # Calculate the time difference
    time_difference = current_datetime - datetime_from_database

    # Extract the difference in minutes
    minutes_difference = int(time_difference.total_seconds() / 60)
    global cost
    cost=50+minutes_difference*2
    cost1.insert(0,f"NRS {cost}")
    cost1.config(state=DISABLED)
    Button(frame1,text="Pay",font="stencil 20 bold",width=15,height=1,border=0,bd=1,fg=b,bg="#A7D397",command=pay).grid(row=6,columnspan=4)
    

def leave():
    global frame1
    frame1.destroy()
      # Declare frame1 as global
    frame1.pack_forget()  # Use pack_forget() instead of frame1.forget()
    frame1 = Frame(root)
    frame1.configure(bg=b)
    global slotid1,key1,slotname1
    frame1.grid(row=0, column=0, sticky="nsew")
    Label(frame1,text="Slot Id :",bg=b,fg="#31363F",font="stencil 24 bold").grid(row=0,column=0,padx=10,pady=10)
    slotid1=Entry(frame1,width=15,bg=b,fg="#31363F",font="helvetica 24 italic")
    slotid1.grid(row=0,column=1,padx=10,pady=10)
    
    Label(frame1,text="Slot Name :",bg=b,fg="#31363F",font="stencil 24 bold").grid(row=1,column=0,padx=10,pady=10)
    slotname1=Entry(frame1,width=15,bg=b,fg="#31363F",font="helvetica 24 italic")
    slotname1.grid(row=1,column=1,padx=10,pady=10)
    
    Label(frame1,text="Digital Key :",bg=b,fg="#31363F",font="stencil 24 bold").grid(row=2,column=0,padx=10,pady=10)
    key1=Entry(frame1,width=15,bg=b,fg="#31363F",font="helvetica 24 italic")
    key1.grid(row=2,column=1,padx=10,pady=10)

    Button(frame1,text="Submit",font="stencil 20 bold",width=15,height=1,border=0,bd=1,fg=b,bg="#A7D397",command=proceed).grid(row=3,columnspan=4)
    
def sendmail(name,email,slotid,slotname,slotkey,current):
    server=sp.SMTP('smtp.gmail.com',587)
    server.starttls()
    try:
        server.login("your mail or sender mail","your password")
    except Exception as e:
        messagebox.showinfo("error",f"failed to login due to {e}")
    subjecttext="Regarding issuance of parking slot"
    body=f'''
Dear {name},

I hope this email finds you well. I am writing to inform you about the issuance of parking slot from our SMPK Parking Service.
The details are as follows:

Slot ID: {slotid}
Slot Name: {slotname}
Slot Area: {slotarea}
Digital key : {slotkey}
Entry Date: {current}
Basic Cost/ Service charge : {cost}

Please ensure that the vehicle is disloged in affordable time by the specified due date.
Remember that perminute Rs 2 is charged from allocated time to endtime.
If you have any questions or need further assistance, feel free to reach out to me.

Thank you for your cooperation.

Sincerely,
managing director
sajid miya
SMPK Parking Service
    '''
    message = f"Subject: {subjecttext}\n\n{body}"

    try:
        server.sendmail('your mail or sender mail',email, message)
        speak("successfully booked your slotid,slotname and digital key is sent to mail")
        messagebox.showinfo("info","successfully booked your slotid,slotname and digital key is sent to mail")
    except Exception as e:
        speak(f"error in sending mail due to {e}")
        messagebox.showerror("error",f"error in sending mail due to {e}")

    server.quit()
def register():
    global slotid,slotname,slotkey,slotarea,licenseno,vehicleno,name,sex,age,contact,email,cost
    slotid=slotid.get()
    slotname=slotname.get()
    slotkey=slotkey.get()
    slotarea=slotarea.get()
    licenseno=licenseno.get()
    vehicleno=vehicleno.get()
    name=name.get()
    sex=sex.get()
    age=age.get()
    contact=contact.get()
    email=email.get()
    cost=cost.get()
    current=datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    try:
        conn=connection1()
        mycursor=conn.cursor()
        sql1=f"INSERT INTO `booked`(`uid`, `sectionname`, `licenseno`, `vehicleno`, `start_time`, `cost`) VALUES ('{slotid}','{slotname}','{licenseno}','{vehicleno}','{current}',50)"
        sql2=f"UPDATE `slots` SET `status`='occupied' WHERE uid='{slotid}'"
        sql3=f"INSERT INTO `users`(`licenseno`, `vehicleno`, `name`, `age`, `sex`, `contact`, `email`) VALUES ('{licenseno}','{vehicleno}','{name}','{age}','{sex}','{contact}','{email}')"
        mycursor.execute(sql1)
        mycursor.execute(sql2)
        mycursor.execute(sql3)
        conn.commit()
        conn.close()
        sendmail(name,email,slotid,slotname,slotkey,current)
        global frame1,b
        frame1.destroy()
        frame1 = Frame(root)  # Recreate the frame
        frame1.configure(bg=b)
        frame1.pack()
        main()
    except Exception as e:
        speak(f"sorry unable to book the slot due to {e}")
        messagebox.showerror("error",f"sorry unable to book the slot due to {e}")
        
def proceedbooking(data):
    global frame1,b
    global slotid,slotname,slotkey,slotarea,licenseno,vehicleno,name,sex,age,contact,email,cost
    frame1.destroy()  # Destroy the existing frame
    frame1 = Frame(root)  # Recreate the frame
    frame1.configure(bg=b)
    frame1.pack()  # Pack the recreated frame
    
    Label(frame1,text="Slot Id :",bg=b,fg="#31363F",font="stencil 24 bold").grid(row=0,column=0,padx=10,pady=10)
    slotid=Entry(frame1,width=15,bg=b,fg="#31363F",font="helvetica 24 italic")
    slotid.grid(row=0,column=1,padx=10,pady=10)
    slotid.insert(0,data[0])
    slotid.config(state="disabled")
    Label(frame1,text="Slot Name :",bg=b,fg="#31363F",font="stencil 24 bold").grid(row=0,column=2,padx=10,pady=10)
    slotname=Entry(frame1,width=15,bg=b,fg="#31363F",font="helvetica 24 italic")
    slotname.grid(row=0,column=3,padx=10,pady=10)
    slotname.insert(0,data[1])
    slotname.config(state="disabled")

    Label(frame1,text="Digital Key :",bg=b,fg="#31363F",font="stencil 24 bold").grid(row=1,column=0,padx=10,pady=10)
    slotkey=Entry(frame1,width=15,bg=b,fg="#31363F",font="helvetica 24 italic")
    slotkey.grid(row=1,column=1,padx=10,pady=10)
    slotkey.insert(0,data[2])
    slotkey.config(state="disabled")
    Label(frame1,text="Slot Area :",bg=b,fg="#31363F",font="stencil 24 bold").grid(row=1,column=2,padx=10,pady=10)
    slotarea=Entry(frame1,width=15,bg=b,fg="#31363F",font="helvetica 24 italic")
    slotarea.grid(row=1,column=3,padx=10,pady=10)
    slotarea.insert(0,data[3])
    slotarea.config(state="disabled")
    
    Label(frame1,text="License No. :",bg=b,fg="#31363F",font="stencil 24 bold").grid(row=2,column=0,padx=10,pady=10)
    licenseno=Entry(frame1,width=15,fg="#31363F",font="helvetica 24 italic")
    licenseno.grid(row=2,column=1,padx=10,pady=10)

    Label(frame1,text="Vehicle No. :",bg=b,fg="#31363F",font="stencil 24 bold").grid(row=2,column=2,padx=10,pady=10)
    vehicleno=Entry(frame1,width=15,fg="#31363F",font="helvetica 24 italic")
    vehicleno.grid(row=2,column=3,padx=10,pady=10)
    Label(frame1,text="Name :",bg=b,fg="#31363F",font="stencil 24 bold").grid(row=3,column=0,padx=10,pady=10)
    name=Entry(frame1,width=15,fg="#31363F",font="helvetica 24 italic")
    name.grid(row=3,column=1,padx=10,pady=10)

    Label(frame1,text="Age :",bg=b,fg="#31363F",font="stencil 24 bold").grid(row=3,column=2,padx=10,pady=10)
    age=Entry(frame1,width=15,fg="#31363F",font="helvetica 24 italic")
    age.grid(row=3,column=3,padx=10,pady=10)

    values=['Male','Female','Others']
    sex=StringVar()
    sex.set("Select Gender ")
    OptionMenu(frame1,sex,*values).grid(row=4,column=1,padx=10,pady=10)
    Label(frame1,text="Sex :",bg=b,fg="#31363F",font="stencil 24 bold").grid(row=4,column=0,padx=10,pady=10)
    #sex=Entry(frame1,width=15,fg="#31363F",font="helvetica 24 italic")
    

    Label(frame1,text="Contact No. :",bg=b,fg="#31363F",font="stencil 24 bold").grid(row=4,column=2,padx=10,pady=10)
    contact=Entry(frame1,width=15,fg="#31363F",font="helvetica 24 italic")
    contact.grid(row=4,column=3,padx=10,pady=10)

    Label(frame1,text="E-mail :",bg=b,fg="#31363F",font="stencil 24 bold").grid(row=5,column=0,padx=10,pady=10)
    email=Entry(frame1,width=15,fg="#31363F",font="helvetica 24 italic")
    email.grid(row=5,column=1,padx=10,pady=10)

    Label(frame1,text="Basic Cost :",bg=b,fg="#31363F",font="stencil 24 bold").grid(row=5,column=2,padx=10,pady=10)
    cost=Entry(frame1,width=15,fg="#31363F",font="helvetica 24 italic")
    cost.grid(row=5,column=3,padx=10,pady=10)
    cost.insert(0,"NRS.50")
    cost.config(state=DISABLED)
    Button(frame1,text="Submit",font="stencil 20 bold",width=15,height=1,border=0,bd=1,fg=b,bg="#A7D397",command=register).grid(row=6,columnspan=4)
    

def book():
    # Assuming condition always evaluates to True for now
    if (len(uid.get())>0):
        conn = connection1()
        if conn:
            mycursor = conn.cursor()
            try:
                sql = f"SELECT * FROM `slots` where uid='{uid.get()}'"
                mycursor.execute(sql)
                data1 = mycursor.fetchone()
                if data1:
                    if data1[-1] == 'vacant':
                        proceedbooking(data1)  # Call the proceedbooking function with data1 as argument
                    else:
                        speak("Slot is occupied, please go for advanced booking")
                        messagebox.showinfo("info", "Slot is occupied, please go for advanced booking")
                else:
                    speak("No such slot found")
                    messagebox.showinfo("info", "No such slot found")
            except mysql.connector.Error as e:
                speak(e)
                messagebox.showerror("error", e)
            finally:
                conn.close()
    
def check():
    global frame1,b,uid  # Declare frame1 as global
    frame1.pack_forget()  # Use pack_forget() instead of frame1.forget()
    frame1 = Frame(root)
    frame1.configure(bg=b)
    frame1.grid(row=0, column=0, sticky="nsew")  # Use grid() instead of pack()

    conn = connection1()
    if conn:
        mycursor = conn.cursor()
        sql = "SELECT `uid`, `sectionname`, `area`, `status` FROM `slots`"
        mycursor.execute(sql)
        data = mycursor.fetchall()
        if data:
            # Create Treeview widget
            tree = ttk.Treeview(frame1, columns=("Slot ID", "Location",  "Price", "Status"), show="headings")

            # Define column headings
            tree.heading("Slot ID", text="Slot ID", anchor=CENTER)
            tree.heading("Location", text="Location", anchor=CENTER)
            tree.heading("Price", text="Price", anchor=CENTER)
            tree.heading("Status", text="Status", anchor=CENTER)

            # Configure column width
            tree.column("Slot ID", width=200)
            tree.column("Location", width=200)
            #tree.column("Code", width=200)
            tree.column("Price", width=200)
            tree.column("Status", width=200)

            # Add a scrollbar
            scrollbar = ttk.Scrollbar(frame1, orient="vertical", command=tree.yview)
            scrollbar.grid(row=0, column=2, sticky="ns",padx=10,pady=10)  # Place the scrollbar using grid()
            tree.configure(yscrollcommand=scrollbar.set)

            # Populate the table with data
            for record in data:
                tree.insert("", "end", values=record)
               

            tree.grid(row=0, column=0,columnspan=2, sticky="nsew",padx=10,pady=10)  # Place the Treeview using grid()

            # Set style for column headings and values (rows)
            style = ttk.Style()
            style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), foreground="#E59BE9")
            style.configure("Treeview", font=("helvetica", 12,"italic"),background=b,foreground="#E59BE9")  # Adjust font and color for rows
    conn.close()  # Close the database connection
    frame2=LabelFrame(frame1)
    frame2.grid(row=1,column=0,columnspan=3)
    frame2.configure(bg=b)
    Label(frame2,text="SlotID:",bg=b,fg="#FB5660",font="stencil 20 bold").grid(row=1,column=0,padx=10,pady=10)
    uid=Entry(frame2,width=30)
    uid.grid(row=1,column=1,padx=10,pady=10)
    Button(frame2,text="Book Now",command=book,fg="#BDF2D5",bg=b,border=3,bd=3,width=15,font="stencil 24 bold").grid(row=2,column=0,columnspan=2)

def opengmail():
    email = "miyasajid19@gmail.com"
    webbrowser.open("mailto:" + email)
def Telegram():
    telegram_link = "place your telegram link"
    webbrowser.open(telegram_link)

def main():
    global frame1  # Declare frame1 as global
    Label(frame1, text="Parking Management System", font="stencil 40 bold", fg="white", bg=b).grid(row=0, column=0, columnspan=4)
    img = Image.open("940x600.png")
    img = img.resize((500, 300))  # Resize the image
    img = ImageTk.PhotoImage(img)
    # Keep a reference to the image to prevent garbage collection
    label = Label(frame1, image=img)
    label.image = img
    label.grid(row=1, columnspan=4, sticky=N)
    #############about us###########444444
    Label(frame1,text="""Welcome to our parking facility! We understand that finding a convenient and secure place to park your vehicle is crucial.
 That's why we're dedicated to providing you with a hassle-free parking experience.Our parking facility offers a range of 
amenities to ensure your comfort and peace of mind. Whether you're here for a short visit or need long-term parking solutio
ns, we have you covered.With our state-of-the-art security measures, including surveillance cameras and well-lit surroundin
gs, you can trust that your vehicle is safe with us. Additionally, our attentive staff is always available to assist you wi
th any questions or concerns you may have.We also offer convenient payment options and flexible pricing plans to accommodat
e your needs. Whether you prefer hourly rates or monthly passes, we have options tailored to suit your budget and schedule.
Thank you for choosing our parking facility. We look forward to serving you and providing you with the best parking experience possible.""",font="helvetica 12 italic",bg=b).grid(row=2,column=0,columnspan=4)
    Label(frame1,text="check our facility",bg=b,fg="#CCD3CA",font="stencil 20 bold").grid(row=3,columnspan=4)
    Button(frame1,text="check slots to book now",command=check,bg=b,fg="#836FFF",font="helvetica 20 bold",border=0,bd=0).grid(row=5,column=0,columnspan=2,sticky=N)
    Button(frame1,text="leave now",command=leave,bg=b,fg="#836FFF",font="helvetica 20 bold",border=0,bd=0).grid(row=5,column=2,columnspan=4,sticky=N)
    Label(frame1,text="contact us",bg=b,fg="#CCD3CA",font="stencil 20 bold").grid(row=6,columnspan=4)
    Button(frame1,text="mail",command=opengmail,bg=b,fg="#836FFF",font="helvetica 20 bold",border=0,bd=0).grid(row=7,column=0,columnspan=2)
    Button(frame1,text=" join telegram",command=Telegram,bg=b,fg="#836FFF",font="helvetica 20 bold",border=0,bd=0).grid(row=7,column=2,columnspan=2)

main()

root.mainloop()
