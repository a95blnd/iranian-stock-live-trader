import threading
import tkinter as tk
import customtkinter
from PIL import ImageTk, Image
import io, base64

from api.login import get_api_captcha, send_login


class App:
    def __init__(self):
        self.token_captcha, self.entry_captcha, self.entry_username, self.entry_password = None, None, None, None
        customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

        self.login_screen = customtkinter.CTk()  # creating custom tkinter window
        self.login_screen.geometry("600x440")
        self.login_screen.title('اتوتریدر معاملات اختیار - ورود')

        self.login_page()

    def show_spinner(self):
        self.spinner_label.place(x=50, y=230)

    def hide_spinner(self):
        self.spinner_label.place(x=50, y=230)

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

    def login_page(self):
        img1 = ImageTk.PhotoImage(Image.open("./assets/pattern.png"))
        l1 = customtkinter.CTkLabel(master=self.login_screen, image=img1)
        l1.pack()

        self.login_frame = customtkinter.CTkFrame(master=l1, width=320, height=360, corner_radius=15)
        self.login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Create a label for the spinner/loader
        self.spinner_label = customtkinter.CTkLabel(master=self.login_frame, text="Loading...", font=('Century Gothic', 14))
        self.spinner_label.place(x=50, y=230)
        self.fetch_captcha_thread = threading.Thread(target=self.fetch_captcha)
        self.fetch_captcha_thread.start()

        l2 = customtkinter.CTkLabel(master=self.login_frame, text="Log into your Account", font=('Century Gothic', 20))
        l2.place(x=50, y=45)

        self.entry_username = customtkinter.CTkEntry(master=self.login_frame, width=220, placeholder_text='Username')
        self.entry_username.place(x=50, y=110)
        self.entry_username.insert(index=0, string="0021231354")

        self.entry_password = customtkinter.CTkEntry(master=self.login_frame, width=220, placeholder_text='Password', show="*")
        self.entry_password.place(x=50, y=165)
        self.entry_password.insert(index=0, string="eVAhjSNPS4")

        self.entry_captcha = customtkinter.CTkEntry(master=self.login_frame, width=70, height=30, placeholder_text='captcha')
        self.entry_captcha.place(x=200, y=230)

        button_login = customtkinter.CTkButton(master=self.login_frame, width=220, text="Login", command=self.home_page, corner_radius=6)
        button_login.place(x=50, y=290)

    def home_page(self):
        login = send_login(
            captcha_code=self.entry_captcha.get(),
            captcha_token=self.token_captcha,
            username=self.entry_username.get(),
            password=self.entry_password.get()
        )
        print(login)
        self.login_screen.destroy()
        self.home_screen = customtkinter.CTk()
        self.home_screen.geometry("1280x720")
        self.home_screen.title('اتوتریدر معاملات اختیار')
        l1 = customtkinter.CTkLabel(master=self.home_screen, text="Home Page", font=('Century Gothic', 60))
        l1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.home_screen.mainloop()

    def run(self):
        self.login_screen.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()