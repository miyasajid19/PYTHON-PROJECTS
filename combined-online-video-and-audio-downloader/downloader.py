from tkinter import *
from tkinter import messagebox,OptionMenu
import yt_dlp
from PIL import Image,ImageTk
def download1():
    resolution_choice = quality.get().split(":")[0]  # Extract format_id
    ydl_opts['format'] = resolution_choice
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            messagebox.showinfo("info", "Downloaded")
            global frame1
            frame1.destroy()
            frame1 = Frame(root, bg=b)
            frame1.pack()
            main()
        except Exception as p:
            messagebox.showerror("error", p)
def go1():
    global url, quality, ydl_opts
    ydl_opts = {
        "outtmpl": "%(title)s.%(ext)s",  # Output filename template
    }
    url = url.get()
    global frame1
    frame1.destroy()
    frame1=Frame(root,bg=b)
    frame1.pack()
    Label(frame1, text="QUALITY :", bg=b, font="Stencil 20 bold", fg="#FFF3C7").grid(row=0, column=0)
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        formats = info_dict.get("formats", None)
        options = []
        audio_formats = ['m4a', 'mp3', 'opus', 'vorbis', 'aac']
        for f in formats:
            if f['ext'] in audio_formats:
                options.append(f"{f['format_id']}: {f['ext']} ({f.get('format_note', 'Audio')})")
        quality=StringVar()
        quality.set("choose")
        OptionMenu(frame1, quality, *options).grid(row=0, column=1,padx=3,pady=3)
        img=Image.open("360_F_535240482_E2FCPJa9Pw914WrvkV6ipzPjpJVSCBSW.jpg").resize((200,60))
        img=ImageTk.PhotoImage(img)
        btn=Button(frame1,image=img,command=download1)
        btn.image=img
        btn.grid(row=2,column=0,columnspan=5,padx=3,pady=3)
def download():
    resolution_choice = quality.get()
    print(resolution_choice)
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        formats = info_dict.get("formats", None)
    try:
        # Download the video
        ydl.download([url])
        messagebox.showinfo("info","downloaded")
        global frame1
        frame1.destroy()
        frame1=Frame(root,bg=b)
        frame1.pack()
        main()
    except Exception as p:
        messagebox.showerror("error",p)
def go():
    global url,quality,ydl_opts
    ydl_opts = {
        "outtmpl": "%(title)s.%(ext)s",  # Output filename template
    }
    url=url.get()
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        formats = info_dict.get("formats", None)
        options=[]
        for f in formats:
            print(f"{f['format_id']}:\t{f['ext']} ({f.get('format_note', None)}p)")
            options.append(f"{f['format_id']}: {f['ext']} ({f.get('format_note', None)}p)")
        global frame1
        frame1.destroy()
        frame1=Frame(root,bg=b)
        frame1.pack()
        Label(frame1,text="quality",bg=b,fg="#FFF3C7",font="stencil 24 bold").grid(row=0,column=0)
        quality=StringVar()
        quality.set("choose")
        OptionMenu(frame1,quality,*options,).grid(row=0,column=1,padx=3,pady=3)
        img=Image.open("360_F_535240482_E2FCPJa9Pw914WrvkV6ipzPjpJVSCBSW.jpg").resize((200,60))
        img=ImageTk.PhotoImage(img)
        btn=Button(frame1,image=img,command=download)
        btn.image=img
        btn.grid(row=1,column=0,columnspan=5,padx=3,pady=3)
root=Tk()
b="#59B4C3"
root.title("youtube video downloader")
root.iconbitmap("YouTube_23392.ico")
root.configure(bg=b)
img=Image.open("kakashi-hatake-naruto.jpg")
img=ImageTk.PhotoImage(img)
label=Label(root,image=img)
label.image=img
label.pack()
frame1=Frame(root,bg=b)
frame1.pack()
def main():
    global url 
    Label(frame1,text="enter URL :  ",bg=b,font="Stencil 20 bold",fg="#FFF3C7").grid(row=0,column=0)
    url=StringVar()
    Entry(frame1,textvariable=url,width=16,font="comic 15 italic",fg="#BEADFA").grid(row=0,column=1)
    img=Image.open("video-design-china-name.png").resize((200,60))
    img=ImageTk.PhotoImage(img)
    btn=Button(frame1,image=img,command=go)
    btn.image=img
    btn.grid(row=2,column=0,columnspan=5,padx=3,pady=3)
    img=Image.open("images.png").resize((200,60))
    img=ImageTk.PhotoImage(img)
    btn=Button(frame1,image=img,command=go1)
    btn.image=img
    btn.grid(row=3,column=0,columnspan=5,padx=3,pady=3)
main()
root.mainloop()   
