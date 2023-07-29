from tkinter import *
import math


# ---------------------------- CREATE LOG ------------------------------- #
def write_log():
    from datetime import datetime
    with open("pomodoro_log.dat", 'a') as logfile:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M\n")
        log_text = f'Study length: {WORK_MIN} minutes. Study Session time: {dt_string}'
        logfile.write(log_text)



# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_STYLE = "Courier"
WORK_MIN = 1
SHORT_BREAK_MIN = 1
LONG_BREAK_MIN = 1
reps = 0
timer = None


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
    reps += 1
    work_sec = WORK_MIN * 3
    short_break_sec = SHORT_BREAK_MIN * 3
    long_break_sec = LONG_BREAK_MIN * 3

    window.attributes('-topmost', 1)
    if reps % 8 == 0:
        countdown(long_break_sec)
        title_label.config(text="Break", font=(FONT_STYLE, 50), fg=RED, bg=YELLOW)
    elif reps % 2 == 0:
        countdown(short_break_sec)
        title_label.config(text="Break", font=(FONT_STYLE, 50), fg=PINK, bg=YELLOW)
    else:
        countdown(work_sec)
        title_label.config(text="Work", font=(FONT_STYLE, 50), fg=GREEN, bg=YELLOW)

    window.attributes('-topmost', 0)


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
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00.00", fill="white", font=(FONT_STYLE, 35, "bold"))
canvas.grid(column=1, row=1)

start_button = Button(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=2)

check_mark = Label(fg=GREEN, bg=YELLOW, font=(FONT_STYLE, 15, "bold"))
check_mark.grid(column=1, row=3)

window.mainloop()
