from tkinter import *
import random
from tkinter import messagebox
root = Tk()

root.title("Maths Quiz")

score_label = LabelFrame(root, text="SCORE")
current = 0
score_display = Label(score_label, text=f"Score : {current}",font="stencil 50 bold",fg="light pink",bg="light blue")
score_display.grid(row=0, column=0,columnspan=2)
score_label.grid(row=0, column=0,columnspan=2)

question_frame = LabelFrame(root, text="Question")
question_frame.grid(row=1, column=0,columnspan=2)

answer_frame = LabelFrame(root, text="Answer")
answer_frame.grid(row=2, column=0)

x, y, op = 0, 0, ''
answer, wrong_answer1, wrong_answer2 = 0, 0, 0

def questions():
    global x, y, op
    operators = ('+', '-', '*', '/')
    p = True
    while p == True:
        op = random.choice(operators)
        x = random.randint(100, 1000)
        y = random.randint(10, 100)
        if x % y == 0:
            break
    num1 = Label(question_frame, text=x,font="stencil 50 bold",fg="light pink",bg="light blue")
    num1.grid(row=0, column=0)
    operator = Label(question_frame, text=op,font="stencil 50 bold",fg="light pink",bg="light blue")
    operator.grid(row=0, column=1)
    num2 = Label(question_frame, text=y,font="stencil 50 bold",fg="light pink",bg="light blue")
    num2.grid(row=0, column=2)
    answers()

def check(a):
    global current
    if a == answer:
        current += 1
        score_display.config(text=f"Score : {current}")
        questions()
    else:
        for btn in answer_frame.winfo_children():
            btn.config(state="disabled")
        messagebox.showinfo("Result", f" wrong answer\n SCORE : {current}")
def answers():
    global answer, wrong_answer1, wrong_answer2
    if op == '+':
        answer = x + y
    elif op == '-':
        answer = x - y
    elif op == '*':
        answer = x * y
    else:
        answer = x / y
    p=True
    while p==True:
        answer = int(answer)
        wrong_answer1 = random.randrange(answer - 10, answer + 10)
        wrong_answer2 = random.randrange(answer - 10, answer + 10)
        if answer!=wrong_answer1 and answer!=wrong_answer2:
            break
    
    buttons = {Button(answer_frame, text=answer,padx=40,pady=10, command=lambda: check(answer)),
               Button(answer_frame, text=wrong_answer1,padx=40,pady=10, command=lambda: check(wrong_answer1)),
               Button(answer_frame, text=wrong_answer2,padx=40,pady=10, command=lambda: check(wrong_answer2))}
    buttons=list(buttons)
    for btn in buttons:
        
        btn.grid(row=0, column=buttons.index(btn))

questions()

root.mainloop()
