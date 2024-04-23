def profit_calculator_conversion_strategy(
        *,
        strike_price : float,
        best_sell_price_base : float,
        best_buy_price_call_option : float,
        best_sell_price_put_option : float,
        remainder_expire_day: int
):
    return ((0.9945 * strike_price / (1.003712 * best_sell_price_base - 0.99897 * best_buy_price_call_option + 1.00113 * best_sell_price_put_option)) ** (365 / remainder_expire_day) - 1) * 100

