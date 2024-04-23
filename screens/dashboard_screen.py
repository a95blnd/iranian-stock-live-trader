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
from utils.export_summin import append_to_excel_summin
from view.scrollable import ScrollableText, ConversionStrategyScrollableText, SumMinStrategyScrollableText


class DashboardScreen:
    def __init__(self, app):
        self.app = app
        self.is_refresh_signal_list = True

        self.summin_data = {
            "Zspa(1218,1219,1220)": [
                "IRO9SIPA6631",
                "IRO9SIPA6641",
                "IRO9SIPA6651"
            ],
            "Zspa(1219,1220,1221)": [
                "IRO9SIPA6641",
                "IRO9SIPA6651",
                "IRO9SIPA6661"
            ],
            "Zspa(1220,1221,1222)": [
                "IRO9SIPA6651",
                "IRO9SIPA6661",
                "IRO9SIPA6671"
            ],
            "Zhrm(1223,1224,1225)": [
                "IRO9AHRM6541",
                "IRO9AHRM6551",
                "IRO9AHRM6561"
            ],
            "Zhrm(1225,1226,1227)": [
                "IRO9AHRM6561",
                "IRO9AHRM6571",
                "IRO9AHRM6581"
            ],
            "Zhrm(3005,3006,3007)": [
                "IRO9AHRM6961",
                "IRO9AHRM6971",
                "IRO9AHRM6981"
            ],
            "Zhrm(3000,3006,3007)": [
                "IRO9AHRM6911",
                "IRO9AHRM6971",
                "IRO9AHRM6981"
            ],
            "Ztvan(1201,1203,1205)": [
                "IROATVAF0091",
                "IROATVAF0111",
                "IROATVAF0131"
            ],
            "Zkhod(2042,2043,2044)": [
                "IRO9IKCO20O1",
                "IRO9IKCO20P1",
                "IRO9IKCO20Q1"
            ],
            "Zsta(2025,2026,2027)": [
                "IRO9TAMN8261",
                "IRO9TAMN8271",
                "IRO9TAMN8281"
            ],
            "Zsta(3015,3016,3017)": [
                "IRO9TAMN8371",
                "IRO9TAMN8381",
                "IRO9TAMN8391"
            ],
            "Zmoj(405,406,407)": [
                "IROAMOJF0151",
                "IROAMOJF0161",
                "IROAMOJF0171"
            ],
            "zbsama(205,206,207)": [
                "IROABSMZ2301",
                "IROABSMZ2311",
                "IROABSMZ2321"
            ]
        }
        self.summin_value_1 = {
            "Zspa(1218,1219,1220)": [0,0,0],
            "Zspa(1219,1220,1221)": [0,0,0],
            "Zspa(1220,1221,1222)": [0,0,0],
            "Zhrm(1223,1224,1225)": [0,0,0],
            "Zhrm(1225,1226,1227)": [0,0,0],
            "Zhrm(3005,3006,3007)": [0,0,0],
            "Zhrm(3000,3006,3007)": [0,0,0],
            "Ztvan(1201,1203,1205)": [0,0,0],
            "Zkhod(2042,2043,2044)": [0,0,0],
            "Zsta(2025,2026,2027)": [0,0,0],
            "Zsta(3015,3016,3017)": [0,0,0],
            "Zmoj(405,406,407)": [0,0,0],
            "zbsama(205,206,207)": [0,0,0]
        }

        self.summin_value_2 = {
            "Zspa(1218,1219,1220)": [0, 0, 0],
            "Zspa(1219,1220,1221)": [0, 0, 0],
            "Zspa(1220,1221,1222)": [0, 0, 0],
            "Zhrm(1223,1224,1225)": [0, 0, 0],
            "Zhrm(1225,1226,1227)": [0, 0, 0],
            "Zhrm(3005,3006,3007)": [0, 0, 0],
            "Zhrm(3000,3006,3007)": [0, 0, 0],
            "Ztvan(1201,1203,1205)": [0, 0, 0],
            "Zkhod(2042,2043,2044)": [0, 0, 0],
            "Zsta(2025,2026,2027)": [0, 0, 0],
            "Zsta(3015,3016,3017)": [0, 0, 0],
            "Zmoj(405,406,407)": [0, 0, 0],
            "zbsama(205,206,207)": [0, 0, 0]
        }

        self.summin_signal_object = {
            "Zspa(1218,1219,1220)": [{},{},{}],
            "Zspa(1219,1220,1221)": [{},{},{}],
            "Zspa(1220,1221,1222)": [{},{},{}],
            "Zhrm(1223,1224,1225)": [{},{},{}],
            "Zhrm(1225,1226,1227)": [{},{},{}],
            "Zhrm(3005,3006,3007)": [{},{},{}],
            "Zhrm(3000,3006,3007)": [{},{},{}],
            "Ztvan(1201,1203,1205)": [{},{},{}],
            "Zkhod(2042,2043,2044)": [{},{},{}],
            "Zsta(2025,2026,2027)": [{},{},{}],
            "Zsta(3015,3016,3017)": [{},{},{}],
            "Zmoj(405,406,407)": [{},{},{}],
            "zbsama(205,206,207)": [{},{},{}]
        }

        self.summin_value_check_1 = {
            "Zspa(1218,1219,1220)": 0,
            "Zspa(1219,1220,1221)": 0,
            "Zspa(1220,1221,1222)": 0,
            "Zhrm(1223,1224,1225)": 0,
            "Zhrm(1225,1226,1227)": 0,
            "Zhrm(3005,3006,3007)": 0,
            "Zhrm(3000,3006,3007)": 0,
            "Ztvan(1201,1203,1205)": 0,
            "Zkhod(2042,2043,2044)": 0,
            "Zsta(2025,2026,2027)": 0,
            "Zsta(3015,3016,3017)": 0,
            "Zmoj(405,406,407)": 0,
            "zbsama(205,206,207)": 0
        }

        self.summin_value_check_2 = {
            "Zspa(1218,1219,1220)": 0,
            "Zspa(1219,1220,1221)": 0,
            "Zspa(1220,1221,1222)": 0,
            "Zhrm(1223,1224,1225)": 0,
            "Zhrm(1225,1226,1227)": 0,
            "Zhrm(3005,3006,3007)": 0,
            "Zhrm(3000,3006,3007)": 0,
            "Ztvan(1201,1203,1205)": 0,
            "Zkhod(2042,2043,2044)": 0,
            "Zsta(2025,2026,2027)": 0,
            "Zsta(3015,3016,3017)": 0,
            "Zmoj(405,406,407)": 0,
            "zbsama(205,206,207)": 0
        }
        # ---------------------------------------------------------

        self.main_container = customtkinter.CTkFrame(self.app, corner_radius=0)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        self.right_side_panel = customtkinter.CTkFrame(self.main_container, width=250, corner_radius=10)
        self.right_side_panel.pack(side=tk.RIGHT, fill=tk.Y, expand=False, padx=5, pady=5)

        self.left_side_panel = customtkinter.CTkFrame(self.main_container, corner_radius=10)
        self.left_side_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # self.scrollable_text = ScrollableText(master=self.left_side_panel,width=770, height=640)
        # self.scrollable_text.grid(row=0, column=0, padx=15, pady=15, sticky="ns")

        # self.scrollable_text = ConversionStrategyScrollableText(master=self.left_side_panel, width=770, height=640)
        # self.scrollable_text.grid(row=0, column=0, padx=15, pady=15, sticky="ns")

        self.scrollable_text = SumMinStrategyScrollableText(master=self.left_side_panel, width=770, height=640)
        self.scrollable_text.grid(row=0, column=0, padx=15, pady=15, sticky="ns")

        for index, (key, nested_list) in enumerate(self.summin_data.items(), start=1):
            container_name = f"{key}_container"
            text_name1 = f"{key}_text1"
            text_name2 = f"{key}_text2"

            # Dynamically create container attribute
            setattr(self, container_name,
                    customtkinter.CTkFrame(self.scrollable_text, fg_color="black", height=70, width=750))
            container = getattr(self, container_name)
            container.grid(row=index, column=0, pady=(0, 10))

            # Dynamically create text attribute 1
            label_text = f"Symbol={key}   :   F1={nested_list[0]}   F2={nested_list[1]}   F3={nested_list[2]}   -------> result={0}"
            setattr(self, text_name1,
                    customtkinter.CTkLabel(container, text=label_text, width=740, height=20, fg_color="transparent"))
            label = getattr(self, text_name1)
            label.grid(row=0, column=0, padx=0, pady=0)

            # Dynamically create text attribute 1
            label_text = f"Symbol={key}   :   F1={nested_list[0]}   F2={nested_list[1]}   F3={nested_list[2]}   -------> result={0}"
            setattr(self, text_name2,
                    customtkinter.CTkLabel(container, text=label_text, width=740, height=20, fg_color="transparent"))
            label = getattr(self, text_name2)
            label.grid(row=1, column=0, padx=0, pady=0)

        # Use Tkinter's after method to start an asyncio loop task
        self.fetch_captcha_thread = threading.Thread(target=self.start_asyncio_loop())
        self.fetch_captcha_thread.start()

    async def change_value_summin(self, arguments):
        if 'instrumentId' in arguments:
            instrument_id = arguments.get('instrumentId')
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

                for for_key, nested_list in self.summin_data.items():
                    if instrument_id in nested_list:
                        key = for_key
                        index = nested_list.index(instrument_id)

                        self.summin_value_1[key][index] = float(sells[0].get('price') or 0) if index == 0           else float(buys[0].get('price') or 0) if index == 1        else float(sells[0].get('price') or 0)
                        self.summin_value_2[key][index] = float(buys[0].get('price') or 0) if index == 0           else float(sells[0].get('price') or 0) if index == 1        else float(buys[0].get('price') or 0)

                        self.summin_signal_object[key][index] = arguments

                        if not 0 in self.summin_value_1[key] and not 0 in self.summin_value_2[key]:
                            result_1 = 0
                            result_2 = 0

                            if key == "Zhrm(3000,3006,3007)":
                                result_1 = round( (-1 * self.summin_value_1[key][0]) + (4 * self.summin_value_1[key][1]) - (5 * self.summin_value_1[key][2]), 4)
                                result_2 = round( (+1 * self.summin_value_2[key][0]) - (4 * self.summin_value_2[key][1]) + (5 * self.summin_value_2[key][2]), 4)
                            else:
                                result_1 = round( (-1 * self.summin_value_1[key][0]) + (2 * self.summin_value_1[key][1]) - (1 * self.summin_value_1[key][2]), 4)
                                result_2 = round( (+1 * self.summin_value_2[key][0]) - (2 * self.summin_value_2[key][1]) + (1 * self.summin_value_2[key][2]), 4)


                            if result_1 != self.summin_value_check_1[key] or result_2 != self.summin_value_check_2[key]:
                                container_name = f"{key}_container"
                                text_name1 = f"{key}_text1"
                                text_name2 = f"{key}_text2"

                                container = getattr(self, container_name)

                                for widget in container.winfo_children():
                                    widget.destroy()

                                # Dynamically create text attribute 1
                                label_text_1 = f"Symbol={key}   :   F1={self.summin_value_1[key][0]}   F2={self.summin_value_1[key][1]}   F3={self.summin_value_1[key][2]}   -------> result={result_1}"
                                setattr(self, text_name1,
                                        customtkinter.CTkLabel(container, text=label_text_1, width=740, height=20,
                                                               fg_color="transparent"))
                                label_1 = getattr(self, text_name1)
                                label_1.grid(row=0, column=0, padx=0, pady=0)

                                # Dynamically create text attribute 2
                                label_text_2 = f"Symbol={key}   :   F1={self.summin_value_2[key][0]}   F2={self.summin_value_2[key][1]}   F3={self.summin_value_2[key][2]}   -------> result={result_2}"
                                setattr(self, text_name2,
                                        customtkinter.CTkLabel(container, text=label_text_2, width=740, height=20,
                                                               fg_color="transparent"))
                                label_2 = getattr(self, text_name2)
                                label_2.grid(row=1, column=0, padx=0, pady=0)




                                self.summin_value_check_1[key] = result_1
                                self.summin_value_check_2[key] = result_2

                                # append_to_excel_summin(
                                #     path="new_result.xlsx",
                                #     zspa1220=self.summin_value['zspa'][0],
                                #     zspa1221=self.summin_value['zspa'][1],
                                #     zspa1222=self.summin_value['zspa'][2],
                                #     zkhpars1216=self.summin_value['zkhpars'][0],
                                #     zkhpars1200=self.summin_value['zkhpars'][1],
                                #     zkhpars1201=self.summin_value['zkhpars'][2],
                                #     zhrm1223=self.summin_value['zhrm'][0],
                                #     zhrm1224=self.summin_value['zhrm'][1],
                                #     zhrm1225=self.summin_value['zhrm'][2],
                                #     ztavan1201=self.summin_value['ztavan'][0],
                                #     ztavan1203=self.summin_value['ztavan'][1],
                                #     ztavan1205=self.summin_value['ztavan'][2],
                                #     symbol=key,
                                #     result=result,
                                #     signal_zspa1220=self.summin_signal_object['zspa'][0],
                                #     signal_zspa1221=self.summin_signal_object['zspa'][1],
                                #     signal_zspa1222=self.summin_signal_object['zspa'][2],
                                #     signal_zkhpars1216=self.summin_signal_object['zkhpars'][0],
                                #     signal_zkhpars1200=self.summin_signal_object['zkhpars'][1],
                                #     signal_zkhpars1201=self.summin_signal_object['zkhpars'][2],
                                #     signal_zhrm1223=self.summin_signal_object['zhrm'][0],
                                #     signal_zhrm1224=self.summin_signal_object['zhrm'][1],
                                #     signal_zhrm1225=self.summin_signal_object['zhrm'][2],
                                #     signal_ztavan1201=self.summin_signal_object['ztavan'][0],
                                #     signal_ztavan1203=self.summin_signal_object['ztavan'][1],
                                #     signal_ztavan1205=self.summin_signal_object['ztavan'][2],
                                # )

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
                    send_start_watchlist(token=access_token, cookie=json.loads(db_user[0].cookie),
                                         connection_id=connection_id)
                    self.is_refresh_signal_list = False

                for signal in received_response:
                    if signal.get('type') == 1:
                        arguments = signal.get('arguments')[0]
                        if 'instrumentId' in arguments:
                            if signal.get('target') == 'MS':
                                print(arguments)
                                await self.change_value_summin(arguments=arguments)

            await asyncio.sleep(1 * 10 ** -10)  # Adjust this delay as needed
