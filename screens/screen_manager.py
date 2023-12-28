class ScreenManager:
    def __init__(self, app):
        self.app = app
        self.current_screen = None

    def show_screen(self, new_screen):
        if self.current_screen:
            self.app.clear_all()
        self.current_screen = new_screen(self.app)
