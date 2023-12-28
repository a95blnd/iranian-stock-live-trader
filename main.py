import tkinter as tk
import customtkinter

from screens.dashboard_screen import DashboardScreen
from screens.screen_manager import ScreenManager
from screens.splash_screen import SplashScreen
from screens.login_screen import LoginScreen

DARK_MODE = "dark"
customtkinter.set_appearance_mode(DARK_MODE)
customtkinter.set_default_color_theme("green")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("اتوتریدر معاملات اختیار")
        self.geometry("1100x700")

        self.screen_manager = ScreenManager(self)
        self.screen_manager.show_screen(SplashScreen)

    def splash_screen(self):
        SplashScreen(self)

    def dashboard_screen(self):
        DashboardScreen(self)

    def login_screen(self):
        LoginScreen(self)

    def clear_all(self):
        for widget in self.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()