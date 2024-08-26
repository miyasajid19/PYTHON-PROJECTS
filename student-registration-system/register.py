from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk
import mysql.connector
def submit():
    try:
        try:
            database="studentregistrationsystem"
            connection=mysql.connector.connect(host="localhost",user="root",password="")
            cursor=connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database} ")
            cursor.execute(f"USE {database}")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS `students` (
                    `student_id` INT ,
                    `first_name` VARCHAR(255),
                    `last_name` VARCHAR(255),
                    `email` VARCHAR(255),
                    `branch` VARCHAR(255),
                    `contact` VARCHAR(20),
                    `hostel` VARCHAR(10),
                    `enrolled_year` INT,
                    PRIMARY KEY (`student_id`)
                )
            """)
            print(f"INSERT INTO `students`(`student_id`, `first_name`, `last_name`, `email`, `branch`, `contact`, `hostel`, `enrolled_year`) VALUES ({regno.get()},{firstname.get()},{lastname.get()},{mail.get()},{branch.get()},{contact.get()},{hostel.get()},{eyear.get()})")
            cursor.execute(f"INSERT INTO `students`(`student_id`, `first_name`, `last_name`, `email`, `branch`, `contact`, `hostel`, `enrolled_year`) VALUES ('{regno.get()}','{firstname.get()}','{lastname.get()}','{mail.get()}','{branch.get()}','{contact.get()}','{hostel.get()}','{eyear.get()}')")
            messagebox.showinfo("Success", "Database and table creation successful.")
            connection.commit()
            cursor.close()
            connection.close()
            root.destroy()
            import main
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed creating database: {err}")
    except Exception as e:
        messagebox.showerror("Error", f"Unknown error: {e}")

root=Tk()
root.title("student registration system")
root.configure(bg="#8B93FF",border=1)
Label(root,text="student registration system",font="stencil 30 bold",fg="white",bg="#8B93FF",anchor="center").grid(row=0,column=0,columnspan=99,sticky=N,padx=10,pady=10)
Label(root,text="First name : ",font="helvetica 15 italic",bg="#8b93ff",anchor="center").grid(row=1,column=0,sticky=N)
firstname=Entry(root,width=20,bg="#FFF7FC",fg="#191717",font="ariel 15 italic")
firstname.grid(row=1,column=1,padx=10,pady=3)
Label(root,text="Last name : ",font="helvetica 15 italic",bg="#8b93ff",anchor="center").grid(row=1,column=2,sticky=N)
lastname=Entry(root,width=20,bg="#FFF7FC",fg="#191717",font="ariel 15 italic")
lastname.grid(row=1,column=3,padx=10,pady=3)

Label(root,text="Reg. No. : ",font="helvetica 15 italic",bg="#8b93ff",anchor="center").grid(row=2,column=0,sticky=N)
regno=Entry(root,width=20,bg="#FFF7FC",fg="#191717",font="ariel 15 italic")
regno.grid(row=2,column=1,padx=10,pady=3)
Label(root,text="official mail : ",font="helvetica 15 italic",bg="#8b93ff",anchor="center").grid(row=2,column=2,sticky=N)
mail=Entry(root,width=20,bg="#FFF7FC",fg="#191717",font="ariel 15 italic")
mail.grid(row=2,column=3,padx=10,pady=3)
branches=["computer science and engineering","electrical engineering","civil engineering","mechanical engineering","chemical engineering","others"]
branch=StringVar()
branch.set("select branch")
Label(root,text="Branch : ",font="helvetica 15 italic",bg="#8b93ff",anchor="center").grid(row=3,column=0,sticky=N)
branch_dropdown = OptionMenu(root, branch, *branches)
branch_dropdown.config(width=20, bg="#FFF7FC", fg="#191717", font="ariel 10 italic")
branch_dropdown.grid(row=3, column=1, padx=10, pady=3)
Label(root,text="Contact No. : ",font="helvetica 15 italic",bg="#8b93ff",anchor="center").grid(row=3,column=2,sticky=N)
contact=Entry(root,width=20,bg="#FFF7FC",fg="#191717",font="ariel 15 italic")
contact.grid(row=3,column=3,padx=10,pady=3)
hostels=["A","B","C","D","E","H","I","J","K","M","N","O","PG"]
hostel=StringVar()
hostel.set("select hostel")
Label(root,text="Hostel : ",font="helvetica 15 italic",bg="#8b93ff",anchor="center").grid(row=4,column=0,sticky=N)
OptionMenu(root,hostel,*hostels).grid(row=4,column=1,padx=10,pady=3)
Label(root,text="Enrolled year : ",font="helvetica 15 italic",bg="#8b93ff",anchor="center").grid(row=4,column=2,sticky=N)
years=[2022,2023,2024,2025,2026,2027]
eyear=StringVar()
eyear.set("select year")
OptionMenu(root,eyear,*years).grid(row=4,column=3,padx=10,pady=3)

Button(root,text="submit",anchor="center",fg="#7D7C7C",bg="#419197",font="stencil 20 bold",width=30,bd=1,border=0,command=submit).grid(row=5,column=1,columnspan=4,padx=10,pady=10)
root.mainloop()

