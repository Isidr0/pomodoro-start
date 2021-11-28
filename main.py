from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
# WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
WORK_MIN = 1
# SHORT_BREAK_MIN = .01
# LONG_BREAK_MIN = .01
reps = 0
timer = None

# ---------------------------- TIMER RESET ------------------------------- # 
def timer_reset():
    global reps
    reps = 0
    window.after_cancel(timer)
    # timer 00:00
    canvas.itemconfig(timer_text, text="00:00")
    # timer label "Timer"
    timer_label.config(text="Timer", fg=GREEN)
    # reset check marks
    checkmark_label.config(text="")

# ---------------------------- TIMER MECHANISM ------------------------------- #
def timer_start():
    global reps
    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60
    # If it's the 8th rep:
    # count down long break seconds
    if reps % 8 == 0:
        count_down(long_break_sec)
        timer_label.config(text="Break", fg=RED)
    # if it's 2, 4, 6 rep: EVEN
    # count down short break seconds
    elif reps % 2 == 0:
        count_down(short_break_sec)
        timer_label.config(text="Break", fg=PINK)
    # If it's the 1st/3rd/5th/7th rep: ODD
    # count down work seconds
    else:
        count_down(work_sec)
        timer_label.config(text="Work", fg=GREEN)
# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
# a way to work around not being able to use a loop in a GUI
# have a function with window.after that calls itself.
def count_down(count):
    global reps
    count_min = math.floor(count / 60)
    count_sec = count % 60

    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        timer_start()
        work_sessions = reps//2
        marks = ""
        for r in range(work_sessions):
            marks += "🗸"
        checkmark_label.config(text=marks)

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)


canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)




# Timer Label 1, 0
timer_label = Label(text="Timer", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 50, "bold"))
timer_label.grid(column=1, row=0)

# Start Button 0, 2
start_button = Button(text="Start", command=timer_start, font=(FONT_NAME, 10))
start_button.grid(column=0, row=2)

# Checkmark 1, 3
checkmark_label = Label(bg=YELLOW, fg=GREEN, font=(FONT_NAME, 25, "bold"))
checkmark_label.grid(column=1, row=3)

# Reset button 2, 2
start_button = Button(text="Reset", command=timer_reset, font=(FONT_NAME, 10))
start_button.grid(column=2, row=2)

# GUI applications like this are known as event driven. They have their own loop that constantly
# checks for user input. You can't use an additional loop inside the application, because it will break.
window.mainloop()