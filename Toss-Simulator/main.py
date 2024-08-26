
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import pygame
def toss_coin():
    global cnt, imageframe, tossing_sound
    images={'heads.png','tails.png'}
    which=random.choice(list(images))
    print(which)
    img=Image.open(which).resize((200,200))
    img=ImageTk.PhotoImage(img)
    label=Label(imageframe,image=img)
    label.grid(row=0,column=0)
    label.image=img
    cnt+=1
    which=which.split(".")
    if cnt==1:
        pygame.mixer.init()
        tossing_sound=pygame.mixer.Sound(r"Coins Drop Sound Effect (HD) [TubeRipper.com].wav")
        tossing_sound.play()
    if pygame.mixer.get_busy():
        root.after(50,toss_coin)
    else:
        messagebox.showinfo("Result",f"You got {which[0]}")
        Button(imageframe,text="Toss Again",font="jokerman 12 italic",command=reset_game).grid(row=3)

def reset_game():
    global cnt,imageframe
    cnt=0
    imageframe.destroy()
    imageframe=Frame(root)
    imageframe.pack()
    toss_coin()

root=Tk()
root.title("Toss Simulator")
root.iconbitmap(r"coin-of-dollar_icon-icons.com_56195.ico")
root.geometry("400x300+100+100")
imageframe=Frame(root)
imageframe.pack()
cnt=0
toss_coin()
root.mainloop()
