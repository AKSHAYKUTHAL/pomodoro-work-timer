import sys
from tkinter import *
import math
import os

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
BLUE = "#2874A6"
FONT_STYLE = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None
break_total = 0
work_total = 0


# check_count = 1


# ---------------------------- TIMER RESET ------------------------------- #

def reset_timer():
    window.after_cancel(timer)

    title_label.config(text="Timer")
    check_mark.config(text="")
    canvas.itemconfig(timer_text, text="00.00")
    global reps
    reps = 0


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps
    global break_total
    global work_total
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    # if reps == 9:
    #     reset_timer()

    if reps % 8 == 0:
        countdown(long_break_sec)
        title_label.config(text="Break", fg=RED)
        break_total = break_total + LONG_BREAK_MIN
    elif reps % 2 == 0:
        countdown(short_break_sec)
        title_label.config(text="Break", fg=PINK)
        work_total = work_total + WORK_MIN

    elif reps % 2 != 0:
        countdown(work_sec)
        title_label.config(text="Work", fg=GREEN)

    if reps % 2 != 0 and reps != 1:
        break_total = break_total + SHORT_BREAK_MIN
        # break_total = ((reps*5)/2 )- 2.5

    total_work_time.config(text=f"{work_total} minutes work")
    total_break_time.config(text=f"{break_total} minutes break")


# ---------------------------- RESOURCE PATH TO ADD THE IMAGE TO EXE ------------------------------- #


def resource_path(relative_path):
    pass
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def countdown(count):
    # global check_count
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        window.attributes('-topmost', 0)
        global timer
        timer = window.after(1000, countdown, count - 1)

    else:
        window.attributes('-topmost', 1)
        window.bell()
        start_timer()
        marks = ""
        work_session = math.floor(reps / 2)
        for i in range(work_session):
            marks += "✔"
        check_mark.config(text=marks)

        # if reps % 2 == 0 and reps < 8:
        #     check_mark.config(text="✔"*check_count)
        #     check_count += 1


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

title_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_STYLE, 40, "bold"))
title_label.grid(column=1, row=0)

canvas = Canvas(width=205, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file=resource_path("tomato.png"))
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00.00", fill="white", font=(FONT_STYLE, 35, "bold"))
canvas.grid(column=1, row=1)

start_button = Button(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=2)

check_mark = Label(fg=GREEN, bg=YELLOW, font=(FONT_STYLE, 15, "bold"))
check_mark.grid(column=1, row=3)

total_break_time = Label(text=f"{reps * 5} minutes break", fg=BLUE, bg=YELLOW, font=(FONT_STYLE, 20, "bold"))
total_break_time.grid(column=0, row=0)

total_work_time = Label(text=f"{reps} minutes work", fg=BLUE, bg=YELLOW, font=(FONT_STYLE, 20, "bold"))
total_work_time.grid(column=2, row=0)

window.mainloop()
