import asyncio
import json
import threading
import tkinter as tk
import customtkinter
from db.user import UserModel
from network.api.connection import get_connection_id_token, send_start_watchlist
from network.ws.signal import connect_to_websocket
from view.scrollable import ScrollableText


class DashboardScreen:
    def __init__(self, app):
        self.app = app
        self.main_container = customtkinter.CTkFrame(self.app, corner_radius=0)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        self.right_side_panel = customtkinter.CTkFrame(self.main_container, width=250, corner_radius=10)
        self.right_side_panel.pack(side=tk.RIGHT, fill=tk.Y, expand=False, padx=5, pady=5)

        self.left_side_panel = customtkinter.CTkFrame(self.main_container, corner_radius=10)
        self.left_side_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.scrollable_text = ScrollableText(master=self.left_side_panel,width=770, height=640, item_list=['Connecting to socket ...'])
        self.scrollable_text.grid(row=0, column=0, padx=15, pady=15, sticky="ns")

        # Use Tkinter's after method to start an asyncio loop task
        self.fetch_captcha_thread = threading.Thread(target=self.start_asyncio_loop())
        self.fetch_captcha_thread.start()


    def start_asyncio_loop(self):
        asyncio.run(self.connect_to_websocket())

    async def connect_to_websocket(self):
        # Create a queue for communication between coroutines
        queue = asyncio.Queue()

        # Provide your id and access_token here
        connection_id, connection_token = get_connection_id_token()
        db_user = UserModel.get_all_users()
        id = connection_token
        access_token = db_user[0].token

        send_start_watchlist(token=access_token, cookie=json.loads(db_user[0].cookie), connection_id=connection_id)

        # Start the WebSocket connection
        asyncio.create_task(connect_to_websocket(id, access_token, queue))


        while True:
            # Check for new messages in the queue
            if not queue.empty():
                # Get and process the received response
                received_response = await queue.get()
                self.scrollable_text.add_item(str(received_response)[:150])
                self.scrollable_text.after(10, self.scrollable_text._parent_canvas.yview_moveto, 1.0) ,
                print(f"Received outside function: {received_response}")

            # Do other processing or tasks here
            # You can add your own logic outside the WebSocket coroutine

            await asyncio.sleep(1 * 10 ** -10)  # Adjust this delay as needed


