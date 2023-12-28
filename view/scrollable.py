import customtkinter


class ScrollableText(customtkinter.CTkScrollableFrame):
    def __init__(self, master, item_list, **kwargs):
        super().__init__(master, **kwargs)

        self.text_list = []
        for i, item in enumerate(item_list):
            self.add_item(item)

    def add_item(self, item):
        text = customtkinter.CTkLabel(self, text=item)
        text.grid(row=len(self.text_list), column=0, pady=(0, 10))
        self.text_list.append(text)

    def remove_item(self, item):
        for text in self.text_list:
            if item == text.cget("text"):
                text.destroy()
                self.text_list.remove(text)
                return

    def get_items(self):
        return [text.cget("text") for text in self.text_list if text.get() == 1]