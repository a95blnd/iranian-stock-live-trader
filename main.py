import tkinter as tk
from datetime import datetime

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




# def days_until_target_date(target_date_str):
#     target_date = datetime.strptime(target_date_str, "%Y-%m-%dT%H:%M:%S")
#     current_date = datetime.now()
#     remaining_time = target_date - current_date
#     days_remaining = remaining_time.days
#     return days_remaining
#
#
# from db.instrument_info import InstrumentInfoModel
#
# psDate = InstrumentInfoModel.get_instrument_by_id("IRO9IKCO2761").psDate
# print(InstrumentInfoModel.get_instrument_by_id("IRO9IKCO2761").strikePrice)
# print(days_until_target_date(psDate))
#
# print("-----------------")
#
# psDate = InstrumentInfoModel.get_instrument_by_id("IROFIKCO3761").psDate
# print(InstrumentInfoModel.get_instrument_by_id("IROFIKCO3761").strikePrice)
# print(days_until_target_date(psDate))