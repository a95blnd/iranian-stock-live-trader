import json
import tkinter as tk
import customtkinter
import threading
from network.api.login import get_profile
from db.user import UserModel
from db.instrument_info import InstrumentInfoModel
from screens.dashboard_screen import DashboardScreen
from screens.login_screen import LoginScreen


class SplashScreen:
    def __init__(self, app):
        self.app = app
        self.app.main_container = customtkinter.CTkFrame(self.app, corner_radius=20)
        self.app.main_container.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)
        UserModel.create_table()
        InstrumentInfoModel.create_table()

        self.spinner_label = customtkinter.CTkProgressBar(
            master=self.app.main_container,
            orientation='horizontal',
            mode='indeterminate',
            height=10,
            width=300,
        )

        self.start()

    def show_spinner(self):
        self.spinner_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.spinner_label.set(0)
        self.spinner_label.start()

    def hide_spinner(self):
        self.spinner_label.stop()
        self.spinner_label.place_forget()

    def fetch_profile(self):
        self.show_spinner()
        db_user = UserModel.get_all_users()
        if len(db_user)>0:
            profile = get_profile(token=db_user[0].token, cookie=json.loads(db_user[0].cookie))
            print(profile.status_code)
            self.execute_profile(profile.status_code)
        else:
            self.hide_spinner()
            self.app.screen_manager.show_screen(LoginScreen)

    def execute_profile(self, status_code):
        self.hide_spinner()
        if status_code == 200:
            self.app.screen_manager.show_screen(DashboardScreen)
        else:
            UserModel.delete_all_users()
            self.app.screen_manager.show_screen(LoginScreen)

    def start(self):
        profile_task = threading.Thread(target=self.fetch_profile)
        profile_task.start()
