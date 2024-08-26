import mysql.connector
from tkinter import *
from tkinter import messagebox
def update():
    try:
        connection=mysql.connector.connect(host="localhost",user="root",password="",database="studentregistrationsystem")
        connection.is_connected()
        mycursor=connection.cursor()
        sql=f"UPDATE `students` SET `first_name`='{firstname.get()}',`last_name`='{lastname.get()}',`email`='{mail.get()}',`branch`='{branch.get()}',`contact`='{contact.get()}',`hostel`='{hostel.get()}',`enrolled_year`='{eyear.get()}' WHERE student_id={regno.get()}"
        mycursor.execute(sql)
        connection.commit()
        connection.close()
        messagebox.showinfo("info","updated successfully")
        root.destroy()
        import main
    except Exception as e:
        print(e)
def updatewindow(root,data):
    print(data)
    global firstname, lastname,mail,regno,contact,branch,hostel,eyear
    root=Toplevel(root)
    root.configure(bg="#8b93ff")
    Label(root,text="student registration system",font="stencil 30 bold",fg="white",bg="#8B93FF",anchor="center").grid(row=0,column=0,columnspan=99,sticky=N,padx=10,pady=10)
    Label(root,text="First name : ",font="helvetica 15 italic",bg="#8b93ff",anchor="center").grid(row=1,column=0,sticky=N)
    firstname=Entry(root,width=20,bg="#FFF7FC",fg="#191717",font="ariel 15 italic")
    firstname.grid(row=1,column=1,padx=10,pady=3)
    firstname.insert(0,data[1])
    Label(root,text="Last name : ",font="helvetica 15 italic",bg="#8b93ff",anchor="center").grid(row=1,column=2,sticky=N)
    lastname=Entry(root,width=20,bg="#FFF7FC",fg="#191717",font="ariel 15 italic")
    lastname.grid(row=1,column=3,padx=10,pady=3)
    lastname.insert(0,data[2])
    Label(root,text="Reg. No. : ",font="helvetica 15 italic",bg="#8b93ff",anchor="center").grid(row=2,column=0,sticky=N)
    regno=Entry(root,width=20,bg="#FFF7FC",fg="#191717",font="ariel 15 italic")
    regno.grid(row=2,column=1,padx=10,pady=3)
    regno.insert(0,data[0])
    regno.config(state="disabled")
    Label(root,text="official mail : ",font="helvetica 15 italic",bg="#8b93ff",anchor="center").grid(row=2,column=2,sticky=N)
    mail=Entry(root,width=20,bg="#FFF7FC",fg="#191717",font="ariel 15 italic")
    mail.grid(row=2,column=3,padx=10,pady=3)
    mail.insert(0,data[3])
    branches=["computer science and engineering","electrical engineering","civil engineering","mechanical engineering","chemical engineering","others"]
    branch=StringVar()
    branch.set(data[4])
    Label(root,text="Branch : ",font="helvetica 15 italic",bg="#8b93ff",anchor="center").grid(row=3,column=0,sticky=N)
    branch_dropdown = OptionMenu(root, branch, *branches)
    branch_dropdown.config(width=20, bg="#FFF7FC", fg="#191717", font="ariel 10 italic")
    branch_dropdown.grid(row=3, column=1, padx=10, pady=3)
    Label(root,text="Contact No. : ",font="helvetica 15 italic",bg="#8b93ff",anchor="center").grid(row=3,column=2,sticky=N)
    contact=Entry(root,width=20,bg="#FFF7FC",fg="#191717",font="ariel 15 italic")
    contact.grid(row=3,column=3,padx=10,pady=3)
    contact.insert(0,data[5])
    hostels=["A","B","C","D","E","H","I","J","K","M","N","O","PG"]
    hostel=StringVar()
    hostel.set(data[-2])
    Label(root,text="Hostel : ",font="helvetica 15 italic",bg="#8b93ff",anchor="center").grid(row=4,column=0,sticky=N)
    OptionMenu(root,hostel,*hostels).grid(row=4,column=1,padx=10,pady=3)
    Label(root,text="Enrolled year : ",font="helvetica 15 italic",bg="#8b93ff",anchor="center").grid(row=4,column=2,sticky=N)
    years=[2022,2023,2024,2025,2026,2027]
    eyear=StringVar()
    eyear.set(data[-1])
    OptionMenu(root,eyear,*years).grid(row=4,column=3,padx=10,pady=3)

    Button(root,text="submit",anchor="center",fg="#7D7C7C",bg="#419197",font="stencil 20 bold",width=30,bd=1,border=0,command=update).grid(row=5,column=1,columnspan=4,padx=10,pady=10)
    root.mainloop()

def toupdate():
    try:
        connection=mysql.connector.connect(host="localhost",user="root",password="",database="studentregistrationsystem")
        connection.is_connected()
        sql=f"SELECT * FROM `students` WHERE student_id={uid.get()}"
        mycursor=connection.cursor()
        mycursor.execute(sql)
        updatewindow(root,mycursor.fetchone())
    except Exception as e:
        messagebox.showerror("error",e)

root=Tk()
root.title("student registration system")
root.configure(bg="#8B93FF",border=1)
Label(root,text="update section",font="stencil 32 bold",bg="#8B93FF",fg="white",anchor="center").grid(row=0,column=0,columnspan=3,sticky=N,padx=10,pady=10)
Label(root,text="Reg No.",font="SANS  32 italic",bg="#8B93FF",fg="white").grid(row=1,column=0,padx=10,pady=10)
uid=Entry(root,width=20,font="HELVETICA 32 bold",bg="#FFCCFF",fg="white")
uid.grid(row=1,column=1,padx=10,pady=10)
Button(root,text="go to update",anchor="center",fg="#7D7C7C",bg="#419197",font="stencil 20 bold",width=15,bd=1,border=0,command=toupdate).grid(row=5,column=0,columnspan=4,padx=10,pady=10)
root.mainloop()