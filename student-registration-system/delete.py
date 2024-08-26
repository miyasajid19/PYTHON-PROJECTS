import mysql.connector
from tkinter import *
from tkinter import messagebox
def delete():
    try:
        connection=mysql.connector.connect(host="localhost",user="root",password="",database="studentregistrationsystem")
        connection.is_connected()
        mycursor=connection.cursor()
        mycursor.execute(f"DELETE FROM `students` where student_id={uid.get()}")
        connection.commit()
        connection.close()
        messagebox.showinfo("info","deleted successfully")
        root.destroy()
        import main
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"MySQL Error: {err}")
    except Exception as e:
        messagebox.showerror("Error", f"Unknown error: {e}")
root=Tk()
root.title("student registration system")
root.configure(bg="#8B93FF",border=1)
Label(root,text="delection section",font="stencil 32 bold",bg="#8B93FF",fg="white",anchor="center").grid(row=0,column=0,columnspan=3,sticky=N,padx=10,pady=10)
Label(root,text="Reg No.",font="SANS  32 italic",bg="#8B93FF",fg="white").grid(row=1,column=0,padx=10,pady=10)
uid=Entry(root,width=20,font="HELVETICA 32 bold",bg="#FFCCFF",fg="white")
uid.grid(row=1,column=1,padx=10,pady=10)
Button(root,text="delete",anchor="center",fg="#7D7C7C",bg="#419197",font="stencil 20 bold",width=15,bd=1,border=0,command=delete).grid(row=5,column=0,columnspan=4,padx=10,pady=10)
root.mainloop()