import pygetwindow as gw
import pyautogui
import time
import keyboard
import random
import string
import customtkinter
import webbrowser
import json
import os

from tkinter import messagebox
from pynput.mouse import Button, Controller
from threading import Thread, Event
from PIL import Image

mouse = Controller()

def main():
    save_name = 'data.json'

    # Checking for json data
    if os.path.exists(save_name):
        with open(save_name, 'r') as fl:
            info = json.load(fl)
    else:
        info = {'first': True}

        with open(save_name, 'w') as file:
            json.dump(info, file, indent=2)


    if info['first']:
        license_win = customtkinter.CTk()

        gilroy = customtkinter.CTkFont('Gilroy-Semibold', 25)
        detail_font = customtkinter.CTkFont('Gilroy-Semibold', 14)

        license_win.geometry(f"400x550")
        license_win.protocol("WM_DELETE_WINDOW", lambda: license_win.quit())
        license_win.resizable(False, False)
        license_win.title("Terms of the license")

        license_content = customtkinter.CTkScrollableFrame(license_win,
                                                           width=350,
                                                           height=370,
                                                           label_text='Terms of the license',
                                                           label_font=detail_font)
        
        license_text = customtkinter.CTkLabel(license_content, 
                                              wraplength=300, 
                                              justify='left',
                                              text="""Copyright (c) 2024 MDEV Software

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to use,
publish, distribute, and share the Software, subject to the following conditions:

1. The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

2. The Software is not open source, and the source code cannot be accessed, obtained, or modified in any way.

3. Modification, merging, sublicensing, and/or selling copies of the Software are strictly prohibited.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.""")

        continue_btn = customtkinter.CTkButton(license_win, 
                                               width=100, 
                                               height=30,
                                               text='Continue',
                                               state='disabled',
                                               command=lambda: on_continue_agree_clicked(license_win, info))

        agreement_checkbox = customtkinter.CTkCheckBox(license_win,
                                                       width=50,
                                                       height=50, 
                                                       text='I have carefully read and agree to the terms of the license.',
                                                       command=lambda: continue_btn.configure(state='normal'))
        
        license_text.pack(anchor='c')
        license_content.pack(anchor='c')
        agreement_checkbox.pack(anchor='s')
        continue_btn.place(x=350//2 - 25, y=490)

        license_win.mainloop()

    else:
        draw_ui(info)

def draw_ui(info):
    accuracy_index = [40]  # Default to Easy, using a list to make it mutable

    WIDTH, HEIGHT = 400, 200
    VERSION = "1.0.2"


    window = customtkinter.CTk()

    gilroy = customtkinter.CTkFont('Gilroy-Semibold', 25)
    detail_font = customtkinter.CTkFont('Gilroy-Semibold', 14)

    # Main window settings
    window.iconbitmap('images/bloomer_ico.ico')
    window.title("Bloomer")
    window.geometry(f"{WIDTH}x{HEIGHT}")
    window.resizable(False, False)

    customtkinter.set_appearance_mode('dark')

    app_title = customtkinter.CTkLabel(window, text='Bloomer', font=gilroy, height=80)
    version_title = customtkinter.CTkLabel(window, text=VERSION, font=detail_font)

    hotkey_title = customtkinter.CTkLabel(window, text='Start key', font=detail_font)
    
    hot_key = customtkinter.CTkComboBox(window, 
                                        width=90, 
                                        height=15,
                                        values=[word for word in string.ascii_lowercase],
                                        state='readonly',
                                        button_color='#c849eb',
                                        border_width=1,
                                        dropdown_font=detail_font,
                                        font=detail_font)
    hot_key.set('s')

    accuracy_title = customtkinter.CTkLabel(window, text='Accuracy', font=detail_font)
    accuracy = customtkinter.CTkComboBox(window, 
                                        width=90, 
                                        height=15,
                                        values=["Easy", "Medium", "Extreme"],
                                        state='readonly',
                                        button_color='#c849eb',
                                        border_width=1,
                                        dropdown_font=detail_font,
                                        font=detail_font,
                                        command=lambda selection: on_accuracy_changed(selection, accuracy_index))
    accuracy.set('Easy')

    info_text = customtkinter.CTkLabel(window, text="")

    patreon = customtkinter.CTkButton(window,
                                    width=10,
                                    height=10,
                                    image=customtkinter.CTkImage(dark_image=Image.open("images/patreon-link_1_0_2.png"), size=(30, 30)),
                                    text="",
                                    fg_color="#242424",
                                    bg_color="#242424",
                                    hover_color="#242424",
                                    command=on_patreon_clicked)
    
    telegram = customtkinter.CTkButton(window,
                                    width=10,
                                    height=10,
                                    image=customtkinter.CTkImage(dark_image=Image.open("images/telegram-link_1_0_2.png"), size=(30, 30)),
                                    fg_color="#242424",
                                    bg_color="#242424",
                                    hover_color="#242424",
                                    text="",
                                    command=on_telegram_clicked)
    
    app_title.pack(anchor=customtkinter.CENTER)
    version_title.place(x=WIDTH - 44, y=HEIGHT // 2 + 65)
    patreon.place(x=WIDTH // 2 - 190, y=HEIGHT//2 + 50)
    telegram.place(x=WIDTH // 2 - 150, y=HEIGHT // 2 + 50)

    info_text.place(x=WIDTH // 2, y=HEIGHT // 2 + 70, anchor='c')
    hot_key.place(x=WIDTH // 2 + 5, y=HEIGHT // 2, anchor='c')
    hotkey_title.place(x=WIDTH // 2 - 77, y=HEIGHT // 2, anchor='c')

    accuracy.place(x=WIDTH // 2 + 5, y=HEIGHT // 2 + 30, anchor='c')
    accuracy_title.place(x=WIDTH // 2 - 77, y=HEIGHT // 2 + 30, anchor='c')

    stop_event = Event()
    clicker_thread = Thread(target=clicker_process, args=(hot_key, info_text, window, accuracy_index, stop_event, info))
    clicker_thread.start()

    window.protocol("WM_DELETE_WINDOW", lambda: on_closing(window, stop_event))
    window.mainloop()
def on_closing(window, stop_event):
    stop_event.set()
    window.quit()

def on_continue_agree_clicked(window, info):
    window.destroy()
    draw_ui(info)

    info['first'] = False
    with open('data.json', 'w') as fr:
        json.dump({"first": False}, fr)


def on_telegram_clicked():
    webbrowser.open_new_tab("https://t.me/mdevsoftware")

def on_patreon_clicked():
    webbrowser.open_new_tab("https://www.patreon.com/MDEVSoftware")

def on_accuracy_changed(selection, index):
    if selection == "Easy":
        index[0] = 40
    elif selection == "Medium":
        index[0] = 25
    elif selection == "Extreme":
        index[0] = 23


def clicker_process(hot_key, info, window, index, stop_event, _license):

    try:
        telegram = gw.getWindowsWithTitle("TelegramDesktop")[0]
    except Exception:
        messagebox.showerror(title='An error occurred', message='Unable to detect Bloom. Please, open Bloom and re-open program to start farm!')
        window.quit()
    
    paused = True
    while not stop_event.is_set():

        if keyboard.is_pressed(hot_key.get()):
            paused = not paused
            info.configure(text=f"Clicker paused" if paused else "Clicker continue")
            time.sleep(0.2)

        if paused:
            time.sleep(0.1)
            continue

        try:
            win_rect = (telegram.left, telegram.top, telegram.width, telegram.height)
        except Exception:
            messagebox.showerror(title="An error occurred", message="Unable to use clicker when Bloom closed. Please, open Bloom and re-open program again")
            break

        try:
            if not telegram.isActive:
                telegram.activate()
        except Exception:
            messagebox.showerror(title="An error occurred", message="Unable to restore Telegram Window")
            break

        screen = pyautogui.screenshot(region=win_rect)
        
        width, height = screen.size

        pixel_found = False

        for x in range(0, width, index[0]):
            for y in range(0, height, index[0]):
                r, g, b = screen.getpixel((x, y))
                # Default diapasons
                # if 102 <= r <= 199
                # if 200 <= g <= 254
                # if 0 <= b <= 124
                # 253, 1, 201 (for pink)
                # 110-220, 140-220, 140-220 (for black)
                if 200 <= r <= 253 and 0 <= g <= 70 and 145 <= b <= 200:
                    scrn_x, scrn_y = win_rect[0] + x, win_rect[1] + y
                    click(scrn_x + 4, scrn_y)
                    time.sleep(0.001)
                    pixel_found = True
                    break
                elif 200 <= r <= 253 and 0 <= g <= 70 and 145 <= b <= 200:
                    scrn_x, scrn_y = win_rect[0] + x, win_rect[1] + y
                    click(scrn_x + 4, scrn_y)
                    time.sleep(0.001)
                    pixel_found = True
                    break

            if pixel_found:
                break

def click(x, y):
    mouse.position = (x, y + random.randint(1, 3))
    mouse.press(Button.left)
    mouse.release(Button.left)

if __name__ == "__main__":
    main()
