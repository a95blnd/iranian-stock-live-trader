import json
import requests


def get_connection_id_token():
    url = "https://armoon-signal.tsetab.ir/SignalHub/negotiate?negotiateVersion=1"

    response = requests.post(url)

    if response.status_code == 200:
        data = response.json()
        id = data['connectionId']
        token = data['connectionToken']
        return id, token
    else:
        print("Failed to fetch data. Status code:", response.status_code)
        return None, None


def send_start_watchlist(token:str, cookie:json, connection_id:str):
    print(connection_id)
    url = "https://armoon-signal.tsetab.ir/api/Portfolios/Start"
    headers = {
        "Authorization": token,
        "Cookie": "; ".join([f"{key}={value}" for key, value in cookie.items()]),
        "Content-Type": "application/json"
    }
    payloads = {
        "ConnectionId":connection_id,
        "InstrumentIds":[
            "IRO9ZOBI2781","IROFZOBI3781","IRO9ZOBI2791","IROFZOBI3791","IRO9ZOBI2801","IROFZOBI3801","IRO9ZOBI2811","IROFZOBI3811","IRO9ZOBI2821","IROFZOBI3821","IRO9ZOBI2831","IROFZOBI3831","IRO9ZOBI2841","IROFZOBI3841","IRO9ZOBI2851","IROFZOBI3851","IRO9ZOBI2861","IROFZOBI3861","IRO9ZOBI2871","IROFZOBI3871","IRO9ZOBI2881","IROFZOBI3881","IRO9ZOBI4011","IROFZOBI5011","IRO9ZOBI4021","IROFZOBI5021"
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(payloads))

    url2 = "https://armoon-signal.tsetab.ir/api/Subscribes/SubscribeInstrument"
    response2 = requests.post(url2, headers=headers, data=json.dumps(payloads))

    if response.status_code == 200:
        data = response.json()
        print(data)
    if response2.status_code == 200:
        data2 = response2.json()
        print(data2)
    else:
        print("Failed to fetch data. Status code:", response.status_code)
        return None, None