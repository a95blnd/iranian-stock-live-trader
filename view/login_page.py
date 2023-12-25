import threading

from PIL import Image, ImageTk
import io, base64
import customtkinter
from api.login import get_api_captcha
import tkinter as tk  # Add this line for 'tk.CENTER'

class LoginPage:
    def __init__(self, login_screen, home_page_ref):
        self.spinner_label = None
        self.login_screen = login_screen
        self.token_captcha = None
        self.login_frame = None
        self.entry_captcha = None
        self.home_page = home_page_ref
        # ... (other attributes that were part of the App class)

        # Create necessary widgets and initiate the process
        self.initialize_login_page()

    def show_spinner(self):
        self.spinner_label.place(x=50, y=230)

    def hide_spinner(self):
        self.spinner_label.place_forget()

    def update_ui_after_captcha(self, image_captcha):
        self.hide_spinner()

        # Process the captcha data if needed
        captcha = Image.open(io.BytesIO(base64.decodebytes(bytes(image_captcha, "utf-8")))).resize((130, 30))
        captcha_img = customtkinter.CTkImage(captcha, size=(130, 30))
        label_captcha = customtkinter.CTkLabel(master=self.login_frame, width=130, height=30, text="", image=captcha_img)
        label_captcha.place(x=50, y=230)

    def fetch_captcha(self):
        self.show_spinner()
        self.token_captcha, image_captcha = get_api_captcha()
        self.update_ui_after_captcha(image_captcha)

    def initialize_login_page(self):
        img1 = customtkinter.CTkImage(Image.open("./assets/pattern.png"))  # Use CTkImage
        l1 = customtkinter.CTkLabel(master=self.login_screen, image=img1)
        l1.pack()

        self.login_frame = customtkinter.CTkFrame(master=l1, width=320, height=360, corner_radius=15)
        self.login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Use 'tk.CENTER'

        # Create a label for the spinner/loader
        self.spinner_label = customtkinter.CTkLabel(master=self.login_frame, text="Loading...",
                                                    font=('Century Gothic', 14))
        self.spinner_label.place(x=50, y=230)
        self.fetch_captcha_thread = threading.Thread(target=self.fetch_captcha)
        self.fetch_captcha_thread.start()

        l2 = customtkinter.CTkLabel(master=self.login_frame, text="Log into your Account", font=('Century Gothic', 20))
        l2.place(x=50, y=45)

        self.entry_username = customtkinter.CTkEntry(master=self.login_frame, width=220, placeholder_text='Username')
        self.entry_username.place(x=50, y=110)
        self.entry_username.insert(index=0, string="0021231354")

        self.entry_password = customtkinter.CTkEntry(master=self.login_frame, width=220, placeholder_text='Password',
                                                     show="*")
        self.entry_password.place(x=50, y=165)
        self.entry_password.insert(index=0, string="eVAhjSNPS4")

        self.entry_captcha = customtkinter.CTkEntry(master=self.login_frame, width=70, height=30,
                                                    placeholder_text='captcha')
        self.entry_captcha.place(x=200, y=230)

        button_login = customtkinter.CTkButton(master=self.login_frame, width=220, text="Login", command=self.home_page,
                                               corner_radius=6)
        button_login.place(x=50, y=290)
