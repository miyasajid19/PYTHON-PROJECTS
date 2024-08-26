from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk
root=Tk()
import random
def again():
    global cnt,rolltimes,imageframe
    cnt=0
    imageframe.destroy()
    imageframe=Frame(root)
    imageframe.pack()
    rolltimes=random.randint(7,32)
    roll()
    
def roll():
    global cnt,rolltimes,imageframe
    images={'1.png','2.png','3.png','4.png','5.png','6.png'}
    images=list(images)
    which=random.choice(images)
    img=Image.open(which).resize((100,100))
    img=ImageTk.PhotoImage(img)
    label=Label(imageframe,image=img)
    label.grid(row=0,column=0)
    label.image=img
    cnt+=1
    if cnt!=rolltimes:
        root.after(50,roll)
        dice=Label(imageframe,text=which[0],font="stencil 30 bold")
        dice.grid(row=2)
    else:
        dice=Label(imageframe,text=which[0],font="stencil 30 bold")
        dice.grid(row=2)
        messagebox.showinfo("info",f"you have got {which[0]}")
        cnt=0
        rolltimes=random.randint(50,100)
        Button(imageframe,text="Roll Again",font="jokerman 12 italic",command=again).grid(row=3)
        
        
rolltimes=random.randint(7,32)
imageframe=Frame(root)
imageframe.pack()
cnt=0
roll()
root.mainloop()