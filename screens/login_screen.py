import threading
import tkinter as tk
import customtkinter
from PIL import Image
import io, base64

from network.api.login import get_api_captcha, send_login
from screens.dashboard_screen import DashboardScreen


class LoginScreen:
    def __init__(self, app):
        self.spinner_label = None
        self.app = app
        self.app.clear_all()

        self.login_page()

    def show_spinner(self):
        self.spinner_label = customtkinter.CTkProgressBar(
            master=self.login_frame,
            orientation='horizontal',
            mode='indeterminate',
            height=30,
            width=130,
        )
        self.spinner_label.place(x=50, y=230)
        self.spinner_label.set(0)
        self.spinner_label.start()

    def hide_spinner(self):
        self.spinner_label.stop()
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

    def send_login(self):
        self.show_spinner()
        login = send_login(
            captcha_code=self.entry_captcha.get(),
            captcha_token=self.token_captcha,
            username=self.entry_username.get(),
            password=self.entry_password.get()
        )
        self.execute_login(login)

    def send_login_task(self):
        task = threading.Thread(target=self.send_login)
        task.start()

    def execute_login(self, response):
        self.hide_spinner()
        if response.status_code == 200:
            self.app.screen_manager.show_screen(DashboardScreen)

    def login_page(self):
        background_img = customtkinter.CTkImage(Image.open("./assets/pattern.png"), size=(1100,700))
        background = customtkinter.CTkLabel(master=self.app, image=background_img)
        background.pack()

        self.login_frame = customtkinter.CTkFrame(master=background, width=320, height=360, corner_radius=15)
        self.login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.fetch_captcha_thread = threading.Thread(target=self.fetch_captcha)
        self.fetch_captcha_thread.start()

        self.label = customtkinter.CTkLabel(master=self.login_frame, text="Log into your Account", font=('Century Gothic', 20))
        self.label.place(x=50, y=45)

        self.entry_username = customtkinter.CTkEntry(master=self.login_frame, width=220, placeholder_text='Username')
        self.entry_username.place(x=50, y=110)
        self.entry_username.insert(index=0, string="0021231354")

        self.entry_password = customtkinter.CTkEntry(master=self.login_frame, width=220, placeholder_text='Password', show="*")
        self.entry_password.place(x=50, y=165)
        self.entry_password.insert(index=0, string="eVAhjSNPS4")

        self.entry_captcha = customtkinter.CTkEntry(master=self.login_frame, width=70, height=30, placeholder_text='captcha')
        self.entry_captcha.place(x=200, y=230)

        self.btn_login = customtkinter.CTkButton(master=self.login_frame, width=220, text="Login", command=self.send_login_task, corner_radius=6)
        self.btn_login.place(x=50, y=290)