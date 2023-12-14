import tkinter as tk
import pyautogui
from tkinter import ttk
import datetime
import numpy as np
import math
import pywhatkit
import threading
def send():
    time_string = time_entry.get()
    t = datetime.datetime.strptime(time_string, '%H:%M')
    pywhatkit.sendwhatmsg(f'phone_entry',f'm_entry',t.hour, t.minute)
    pyautogui.hotkey('enter')
    print(t.hour, t.minute)
    print("message sanded")
    #not sure should it close the browser or not
    #pyautogui.hotkey('alt', "f4")

def update_clock():
    user_time = time_entry.get()
    error_label['text'] = ''  # Clear previous error messages
    if user_time:  # Check if the entry is not empty
        try:
            # Parse the user input
            hours, minutes = map(int, user_time.split(':'))
            # Validate the hours and minutes
            if hours < 0 or hours > 23 or minutes < 0 or minutes > 59:
                raise ValueError
            # Calculate the angle of the hands
            hour_angle = (hours % 12 + minutes / 60) * 30
            minute_angle = minutes * 6
            # Redraw the clock hands
            draw_clock(hour_angle, minute_angle)
        except ValueError:
            error_label['text'] = "Please enter time in HH:MM format."
    # Schedule the update_clock function to be called after 1000ms (1 second)
    w.after(1000, update_clock)

# Function to draw the clock face
def draw_clock_face():
    canvas.delete('clock_face')  # Clear the previous clock face
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    center_x = width // 2
    center_y = height // 2
    clock_radius = min(center_x, center_y) - 10

    # Draw the clock face
    canvas.create_oval(center_x - clock_radius, center_y - clock_radius,
                       center_x + clock_radius, center_y + clock_radius, tags='clock_face')

    # Draw the numbers
    for number in range(1, 13):
        angle = math.radians(number * 30 - 90)
        x = center_x + clock_radius * 0.8 * math.cos(angle)
        y = center_y + clock_radius * 0.8 * math.sin(angle)
        canvas.create_text(x, y, text=str(number), font=('Arial', 12, 'bold'), tags='clock_face')

    # Draw the minute ticks
    for tick in range(60):
        angle = math.radians(tick * 6 - 90)
        x_start = center_x + clock_radius * 0.95 * math.cos(angle)
        y_start = center_y + clock_radius * 0.95 * math.sin(angle)
        x_end = center_x + clock_radius * (0.85 if tick % 5 == 0 else 0.9) * math.cos(angle)
        y_end = center_y + clock_radius * (0.85 if tick % 5 == 0 else 0.9) * math.sin(angle)
        canvas.create_line(x_start, y_start, x_end, y_end, tags='clock_face')

# Function to draw the clock hands
def draw_clock(hour_angle, minute_angle):
    # Clear the canvas
    canvas.delete('hands')

    # Get the center of the canvas
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    center_x = width // 2
    center_y = height // 2
    clock_radius = min(center_x, center_y) - 10

    # Calculate the hand coordinates using numpy
    hour_length = clock_radius * 0.5
    hour_x = center_x + hour_length * np.sin(np.radians(hour_angle))
    hour_y = center_y - hour_length * np.cos(np.radians(hour_angle))
    canvas.create_line(center_x, center_y, hour_x, hour_y, width=8, fill='blue', tags='hands')

    minute_length = clock_radius * 0.8
    minute_x = center_x + minute_length * np.sin(np.radians(minute_angle))
    minute_y = center_y - minute_length * np.cos(np.radians(minute_angle))
    canvas.create_line(center_x, center_y, minute_x, minute_y, width=6, fill='green', tags='hands')



w = tk.Tk()
w.title("Whatsapp timer")
w.geometry('300x500')

# Add a label and entry field for the phone number
phone_label = tk.Label(w, text="Phone Number:with +852")
phone_label.pack()
phone_entry = tk.Entry(w)
phone_entry.pack()
# Add a label and entry field for the time
time_label = tk.Label(w, text="Time (24-hour format)with :")
time_label.pack()
time_entry = tk.Entry(w)
time_entry.pack()
#add message field
m_label = tk.Label(w,text="your message here")
m_label.pack()
m_entry = tk.Entry(w)
m_entry.pack()
error_label = tk.Label(w, text='', fg='red')
error_label.pack()

# Add a button to send the message
send_button = tk.Button(w, text="Send",command =threading.Thread(target=send).start)
send_button.pack()
canvas = tk.Canvas(w, width=200, height=200, bg='white')
canvas.pack(expand=True, fill='both')

# Call the clock face drawing function when the canvas is resized to ensure it fits properly
def on_resize(event):
    draw_clock_face()
    update_clock()

canvas.bind('<Configure>', on_resize)

# Initial call to update the clock
update_clock()
# Run the GUI event loop
w.mainloop()

