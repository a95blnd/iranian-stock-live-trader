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
        # "InstrumentIds":[
        #     "IRO1IKCO0001",
        #     "IRO9IKCO2761",
        #     "IROFIKCO3761",
        # ]
        # "InstrumentIds":[
        #     'IRO9SIPA6651',
        #     'IRO9SIPA6661',
        #     'IRO9SIPA6671',
        #     'IROAPKOD2441',
        #     'IROAPKOD2001',
        #     'IROAPKOD2011',
        #     'IRO9AHRM6541',
        #     'IRO9AHRM6551',
        #     'IRO9AHRM6561',
        #     'IROATVAF0091',
        #     'IROATVAF0111',
        #     'IROATVAF0131',
        # ]
        "InstrumentIds": [
            "IRO9TAMN8371",
            "IRO9TAMN8381",
            "IRO9TAMN8391",
            "IRO9TAMN8261",
            "IRO9TAMN8271",
            "IRO9TAMN8281",
            "IRO9IKCO20O1",
            "IRO9IKCO20P1",
            "IRO9IKCO20Q1",
            "IROATVAF0091",
            "IROATVAF0111",
            "IROATVAF0131",
            "IRO9AHRM6961",
            "IRO9AHRM6971",
            "IRO9AHRM6981",
            "IRO9AHRM6561",
            "IRO9AHRM6571",
            "IRO9AHRM6581",
            "IRO9AHRM6541",
            "IRO9AHRM6551",
            "IRO9AHRM6561",
            "IRO9SIPA6651",
            "IRO9SIPA6661",
            "IRO9SIPA6671",
            "IRO9SIPA6641",
            "IRO9SIPA6651",
            "IRO9SIPA6661",
            "IRO9SIPA6631",
            "IRO9SIPA6641",
            "IRO9SIPA6651",
            "IROABSMZ2301",
            "IROABSMZ2311",
            "IROABSMZ2321",
            "IROAMOJF0151",
            "IROAMOJF0161",
            "IROAMOJF0171",
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