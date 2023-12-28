import os

import requests
import json

from db.instrument_info import InstrumentInfoModel


def get_all_instrument_in_json():
    api_url = "https://armoon-red.tsetab.ir/api/PublicMessages/GetOptionInstruments"

    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json().get("response", {}).get("data", [])
        file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'constants', 'instrument_data.json')
        print(file_path)
        if data:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            print("Data saved successfully to 'instrument_data.json'")
        else:
            print("No data found in the response.")
    else:
        print("Failed to fetch data from the API.")


def update_contract_info(instrument_id:str):
    url_1 = f"https://armoon-red.tsetab.ir/api/PublicMessages/Instrument?instrumentId={instrument_id}"
    url_2 = f"https://armoon-red.tsetab.ir/api/PublicMessages/GetOptionContractInfo?instrumentId={instrument_id}"

    response_1 = requests.get(url_1)
    response_2 = requests.get(url_2)
    if response_1.status_code == 200 and response_2.status_code == 200:
        data_1 = response_1.json()['response']['data']
        data_2 = response_2.json()['response']['data']

        db_instrument_info_by_id = InstrumentInfoModel.get_instrument_by_id(instrument_id=instrument_id)

        new = InstrumentInfoModel(
                instrumentId=data_1.get('status').get('instrumentId'),
                status=data_1.get('status').get('status'),
                lVal18AFC=data_1.get('lVal18AFC'),
                lVal30=data_1.get('lVal30'),
                cGrValCot=data_1.get('cGrValCot'),
                qPasCotFxeVal=data_1.get('qPasCotFxeVal'),
                qQtTranMarVal=data_1.get('qQtTranMarVal'),
                qTitMinSaiOmProd=data_1.get('qTitMinSaiOmProd'),
                qTitMaxSaiOmProd=data_1.get('qTitMaxSaiOmProd'),
                baseVol=data_1.get('baseVol'),
                insCode=data_1.get('insCode'),
                zTitad=data_1.get('zTitad'),
                ipo=data_1.get('ipo'),
                yVal=data_1.get('yVal'),
                yDeComp=data_1.get('yDeComp'),
                cSecVal=data_1.get('cSecVal'),
                cSoSecVal=data_1.get('cSoSecVal'),
                cComVal=data_1.get('cComVal'),
                flow=data_1.get('flow'),
                marketType=data_1.get('marketType'),
                cIsin=data_1.get('cIsin'),
                cSocCSAC=data_1.get('cSocCSAC'),
                id=data_1.get('status').get('id'),
                lRfintAdfMsg=data_2.get('lRfintAdfMsg'),
                cFon=data_2.get('cFon'),
                op=data_2.get('op'),
                initialMargin=data_2.get('initialMargin'),
                maintenanceMargin=data_2.get('maintenanceMargin'),
                requiredMargin=data_2.get('requiredMargin'),
                strikePrice=data_2.get('strikePrice'),
                cSize=data_2.get('cSize'),
                sDate=data_2.get('sDate'),
                eDate=data_2.get('eDate'),
                csDate=data_2.get('csDate'),
                psDate=data_2.get('psDate'),
                maxCOP=data_2.get('maxCOP'),
                maxCAOP=data_2.get('maxCAOP'),
                maxBOP=data_2.get('maxBOP'),
                maxMOP=data_2.get('maxMOP'),
                maxOrders=data_2.get('maxOrders'),
                uacIsin=data_2.get('uacIsin'),
                cefo=data_2.get('cefo'),
                baseInstrumentId=data_2.get('baseInstrumentId'),
                createdDateTime=data_2.get('createdDateTime'),
                modifiedDateTime=data_2.get('modifiedDateTime')
        )

        if db_instrument_info_by_id is None:
            new.save()

        else:
            db_instrument_info_by_id.delete()
            new.save()