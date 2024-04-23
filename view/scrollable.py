# -*- coding: UTF-8 -*-

import customtkinter
import tkinter as tk

from db.instrument_info import InstrumentInfoModel
from strategy.strategy_conversion import profit_calculator_conversion_strategy
from utils.export import append_to_excel
from view.font import fonts


class ScrollableText(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.text_list = []

    def add_item(self, signal):
        arguments = signal.get('arguments')[0]
        instrument_id = arguments.get('instrumentId')
        instrument_info = InstrumentInfoModel.get_instrument_by_id(instrument_id)
        if signal.get('target') == 'MW' or signal.get('target') == 'MS':
            if arguments.get('data') or arguments.get('it'):
                # print(arguments.get('it'), arguments.get('data'))
                self.main_container = customtkinter.CTkFrame(self, fg_color="black", height=60, width=750)
                self.main_container.grid(row=len(self.text_list), column=0, pady=(0, 10))

                # left side panel ------------------------------------------------------------------------------------
                left_side_panel = customtkinter.CTkFrame(self.main_container, width=250, height=60, fg_color="red",
                                                         corner_radius=0)
                left_side_panel.pack(side=tk.LEFT, expand=False, padx=0, pady=0)

                # center side panel ----------------------------------------------------------------------------------
                center_side_panel = customtkinter.CTkFrame(self.main_container, width=250, height=60, fg_color="green",
                                                           corner_radius=0)
                center_side_panel.pack(side=tk.LEFT, expand=False, padx=0, pady=0)

                # right side panel -----------------------------------------------------------------------------------
                right_side_panel = customtkinter.CTkFrame(self.main_container, width=250, height=90, fg_color="black",
                                                          border_color="white", border_width=1)
                right_side_panel.pack(side=tk.LEFT, expand=False, padx=0, pady=0)

                txt_symbol = customtkinter.CTkLabel(right_side_panel, text=f"نماد:  {instrument_info.lVal18AFC}",
                                                    width=250, height=20, fg_color="transparent",
                                                    font=fonts.get_font(weight="bold"))
                txt_symbol.grid(row=0, column=0, padx=0, pady=0)

                if signal.get('target') == 'MW':
                    it_data = arguments.get('it')
                    if it_data:
                        txt_pclosing = customtkinter.CTkLabel(right_side_panel,
                                                              text=f"قیمت فعلی:  {it_data.get('pDrCotVal') or '-'}     -     قیمت پایانی:  {it_data.get('pClosing') or '-'}",
                                                              width=250, height=20, fg_color="transparent",
                                                              font=fonts.get_font(weight="bold"))
                        txt_pclosing.grid(row=1, column=0, padx=0, pady=0)

                        txt_qTotTran5J_zTotTran = customtkinter.CTkLabel(right_side_panel,
                                                                         text=f"حجم:  {it_data.get('qTotTran5J') or '-'}     -     تعداد:  {it_data.get('zTotTran') or '-'}",
                                                                         width=250, height=20, fg_color="transparent",
                                                                         font=fonts.get_font(weight="bold"))
                        txt_qTotTran5J_zTotTran.grid(row=2, column=0, padx=0, pady=0)

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
                        # sells.reverse()

                        # Buyer ------------------------------------------------------------
                        for index, item in enumerate(buys):
                            if index == 3: break
                            buyers = customtkinter.CTkLabel(center_side_panel,
                                                            text=f"تعداد:  {item.get('count') or '-'}     -     حجم:  {item.get('quantity') or '-'}     -     قیمت:  {item.get('price') or '-'}",
                                                            width=250, height=20, fg_color="transparent",
                                                            font=fonts.get_font(weight="bold"))
                            buyers.grid(row=index, column=0, padx=0, pady=0)

                        # Seller ------------------------------------------------------------
                        for index, item in enumerate(sells):
                            if index == 3: break
                            buyers = customtkinter.CTkLabel(left_side_panel,
                                                            text=f"تعداد:  {item.get('count') or '-'}     -     حجم:  {item.get('quantity') or '-'}     -     قیمت:  {item.get('price') or '-'}",
                                                            width=250, height=20, fg_color="transparent",
                                                            font=fonts.get_font(weight="bold"))
                            buyers.grid(row=index, column=0, padx=0, pady=0)

                    else:
                        txt_symbol = customtkinter.CTkLabel(right_side_panel, text=f"خریدار و فروشنده ندارد", width=250,
                                                            height=20, fg_color="transparent",
                                                            font=fonts.get_font(weight="bold"))
                        txt_symbol.grid(row=0, column=0, padx=0, pady=0)

                self.text_list.append(self.main_container)

    def remove_item(self, item):
        for text in self.text_list:
            if item == text.cget("text"):
                text.destroy()
                self.text_list.remove(text)
                return

    def get_items(self):
        return [text.cget("text") for text in self.text_list if text.get() == 1]


class ConversionStrategyScrollableText(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.text_list = []

    def add_item(
            self,
            strike_price: float,
            best_sell_price_base: float,
            best_buy_price_call_option: float,
            best_sell_price_put_option: float,
            remainder_expire_day: int
    ):
        if (isinstance(best_sell_price_base, float) and isinstance(best_buy_price_call_option, float) and isinstance(best_sell_price_put_option, float)):
            profit = profit_calculator_conversion_strategy(
                strike_price=strike_price,
                best_sell_price_base=best_sell_price_base,
                best_buy_price_call_option=best_buy_price_call_option,
                best_sell_price_put_option=best_sell_price_put_option,
                remainder_expire_day=remainder_expire_day
                )

            append_to_excel(
                "export.xlsx",
                strike_price,
                best_sell_price_base,
                best_buy_price_call_option,
                best_sell_price_put_option,
                remainder_expire_day,
                round(profit,4)
            )
            self.main_container = customtkinter.CTkFrame(self, fg_color="black", height=30, width=750)
            self.main_container.grid(row=len(self.text_list), column=0, pady=(0, 10))

            text = customtkinter.CTkLabel(self.main_container,
                                          text=f"F2={strike_price}   F3={best_sell_price_base}   F4={best_buy_price_call_option}   F5={best_sell_price_put_option}   F6={remainder_expire_day}  -------> Profit={round(profit,4)}",
                                          width=740, height=20, fg_color="transparent", )
            text.grid(row=0, column=0, padx=0, pady=0)

            self.text_list.append(self.main_container)

    def remove_item(self, item):
        for text in self.text_list:
            if item == text.cget("text"):
                text.destroy()
                self.text_list.remove(text)
                return

    def get_items(self):
        return [text.cget("text") for text in self.text_list if text.get() == 1]


class SumMinStrategyScrollableText(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.text_list = []

    def add_item(
            self,
            symbol: str,
            f1: float,
            f2: float,
            f3: float,
            result: float,
    ):
            self.main_container = customtkinter.CTkFrame(self, fg_color="black", height=30, width=750)
            self.main_container.grid(row=len(self.text_list), column=0, pady=(0, 10))

            text = customtkinter.CTkLabel(self.main_container,
                                          text=f"Symbol={symbol}   :   F1={f1}   F2={f2}   F3={f3}   -------> result={result}",
                                          width=740, height=20, fg_color="transparent", )
            text.grid(row=0, column=0, padx=0, pady=0)

            self.text_list.append(self.main_container)

    def remove_item(self, item):
        for text in self.text_list:
            if item == text.cget("text"):
                text.destroy()
                self.text_list.remove(text)
                return

    def get_items(self):
        return [text.cget("text") for text in self.text_list if text.get() == 1]
