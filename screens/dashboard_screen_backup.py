import asyncio
import json
import threading
import tkinter as tk
import customtkinter

from db.instrument_info import InstrumentInfoModel
from db.user import UserModel
from network.api.connection import get_connection_id_token, send_start_watchlist
from network.ws.signal import connect_to_websocket
from utils.date_convertor import days_until_target_date
from view.scrollable import ScrollableText, ConversionStrategyScrollableText


class DashboardScreenBackup:
    def __init__(self, app):
        self.app = app
        self.is_refresh_signal_list = True

        # Conversion Strategy ------------------------------------
        self.strike_price = float(InstrumentInfoModel.get_instrument_by_id("IRO9IKCO2761").strikePrice),
        self.best_sell_price_base = None,
        self.best_buy_price_call_option = None,
        self.best_sell_price_put_option = None,
        self.remainder_expire_day = int(days_until_target_date(InstrumentInfoModel.get_instrument_by_id("IRO9IKCO2761").psDate))

        self.check_best_sell_price_base = None,
        self.check_best_buy_price_call_option = None,
        self.check_best_sell_price_put_option = None,

        self.summin_data = {
              "zspa" : [
                "IRO9SIPA6651",
                "IRO9SIPA6661",
                "IRO9SIPA6671"
              ],
              "zkhpars" : [
                "IROAPKOD2441",
                "IROAPKOD2001",
                "IROAPKOD2011"
              ],
              "zhrm" : [
                "IRO9IKCO2841",
                "IRO9IKCO2851",
                "IRO9IKCO2861"
              ],
              "ztavan" : [
                "IROATVAF0091",
                "IROATVAF0111",
                "IROATVAF0131"
              ]
            }
        self.summin_value = {
              "zspa" : [0,0,0],
              "zkhpars" : [0,0,0],
              "zhrm" : [0,0,0],
              "ztavan" : [0,0,0]
            }
        #---------------------------------------------------------


        self.main_container = customtkinter.CTkFrame(self.app, corner_radius=0)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        self.right_side_panel = customtkinter.CTkFrame(self.main_container, width=250, corner_radius=10)
        self.right_side_panel.pack(side=tk.RIGHT, fill=tk.Y, expand=False, padx=5, pady=5)

        self.left_side_panel = customtkinter.CTkFrame(self.main_container, corner_radius=10)
        self.left_side_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # self.scrollable_text = ScrollableText(master=self.left_side_panel,width=770, height=640)
        # self.scrollable_text.grid(row=0, column=0, padx=15, pady=15, sticky="ns")

        self.scrollable_text = ConversionStrategyScrollableText(master=self.left_side_panel, width=770, height=640)
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

        # Start the WebSocket connection
        asyncio.create_task(connect_to_websocket(id, access_token, queue))


        while True:
            # Check for new messages in the queue
            if not queue.empty():
                # Get and process the received response
                received_response = await queue.get()
                if self.is_refresh_signal_list:
                    send_start_watchlist(token=access_token, cookie=json.loads(db_user[0].cookie),connection_id=connection_id)
                    self.is_refresh_signal_list = False

                for signal in received_response:
                    if signal.get('type') == 1:
                        arguments = signal.get('arguments')[0]
                        if 'instrumentId' in arguments:
                            instrument_id = arguments.get('instrumentId')
                            for signal in received_response:
                                if signal.get('type') == 1:
                                    arguments = signal.get('arguments')[0]
                                    if 'instrumentId' in arguments:
                                        if signal.get('target') == 'MS':
                                            depth_data = arguments.get('data')
                                            if depth_data:
                                                sells = []
                                                buys = []
                                                for i in depth_data:
                                                    if i.get('orderSide') == 'Buy':
                                                        buys.append(i)
                                                    elif i.get('orderSide') == 'Sell':
                                                        sells.append(i)
                                                buys.reverse()

                                                if instrument_id == "IRO1IKCO0001": #Base
                                                    self.best_sell_price_base = float(sells[0].get('price'))
                                                if instrument_id == "IRO9IKCO2761": #Base
                                                    self.best_buy_price_call_option = float(buys[0].get('price'))
                                                if instrument_id == "IROFIKCO3761": #Base
                                                    self.best_sell_price_put_option = float(sells[0].get('price'))

                                        if(self.check_best_sell_price_base != self.best_sell_price_base or
                                           self.check_best_buy_price_call_option != self.check_best_buy_price_call_option or
                                           self.check_best_sell_price_put_option != self.best_sell_price_put_option):

                                                self.scrollable_text.add_item(
                                                    strike_price=self.strike_price[0],
                                                    best_sell_price_base=self.best_sell_price_base,
                                                    best_buy_price_call_option=self.best_buy_price_call_option,
                                                    best_sell_price_put_option=self.best_sell_price_put_option,
                                                    remainder_expire_day=self.remainder_expire_day
                                                )
                                                self.scrollable_text.after(10, self.scrollable_text._parent_canvas.yview_moveto, 1.0) ,

                                                self.check_best_sell_price_base = self.best_sell_price_base
                                                self.check_best_buy_price_call_option = self.check_best_buy_price_call_option
                                                self.check_best_sell_price_put_option = self.best_sell_price_put_option


                            # self.scrollable_text.add_item(signal)
                            # self.scrollable_text.after(10, self.scrollable_text._parent_canvas.yview_moveto, 1.0) ,

            await asyncio.sleep(1 * 10 ** -10)  # Adjust this delay as needed

    def change_value_summin(self, id, best_buy_price, best_sell_price):
        for key, nested_list in self.summin_data.items():
            if id in nested_list:
                index = nested_list.index(id)
                self.summin_value[key][index] = best_buy_price if index == 1 else best_sell_price

