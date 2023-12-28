import json

import requests

from db.user import UserModel


def get_api_captcha():
    url = "https://armoon-white.tsetab.ir/api/Captcha/get"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        token = data["response"]["data"]["token"]
        image = data["response"]["data"]["image"]
        return token, image
    else:
        print("Failed to fetch data. Status code:", response.status_code)
        return None, None


def send_login(
        captcha_code:str,
        captcha_token:str,
        username:str,
        password:str
):
    url = 'https://armoon-white.tsetab.ir/api/Accounts/Login'

    # Request body
    payload = {
        "username": username,
        "password": password,
        "captchaToken": captcha_token,
        "captchaResponseCode": captcha_code
    }

    # Convert payload to JSON
    payload_json = json.dumps(payload)

    # Make POST request
    try:
        response = requests.post(url, data=payload_json, headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            new_user = UserModel(username=username, password=password, cookie=response.cookies.get_dict(), token=response.json()['response']['data']['tokenInfo']['token'])
            new_user.save()
        return response
    except requests.RequestException as e:
        raise Exception(e)


def get_profile(token:str, cookie:json):
    url = "https://armoon-delta.tsetab.ir/api/Customers/GetProfile"

    headers = {
        "Authorization":token,
        "Cookie":"; ".join([f"{key}={value}" for key, value in cookie.items()])
    }
    response = requests.get(url, headers=headers)
    return response
