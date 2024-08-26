from tkinter import *
root=Tk()
root.title("student registration system")
def update():
    root.destroy()
    import update
def delete():
    root.destroy()
    import delete
def register():
    root.destroy()
    import register
root.configure(bg="#8B93FF",border=1)
Button(root,text="register",anchor="center",fg="white",bg="#419197",font="stencil 20 bold",width=15,bd=1,border=0,command=register).grid(row=1,column=0,columnspan=4,padx=10,pady=10)
Button(root,text="delete",anchor="center",fg="white",bg="#419197",font="stencil 20 bold",width=15,bd=1,border=0,command=delete).grid(row=2,column=0,columnspan=4,padx=10,pady=10)
Button(root,text="check",anchor="center",fg="white",bg="#419197",font="stencil 20 bold",width=15,bd=1,border=0,command=update).grid(row=3,column=0,columnspan=4,padx=10,pady=10)
root.mainloop()