import asyncio
import datetime
import json

import websockets


async def connect_to_websocket(id, access_token, queue):
    url = f'wss://armoon-signal.tsetab.ir/SignalHub/?id={id}&access_token={access_token}'
    async with websockets.connect(url) as websocket:
        signal_text = '{"protocol":"json","version":1}'
        await websocket.send(signal_text)
        print(f"Sent: {signal_text}")

        while True:
            # Put the received response into the queue
            response = await websocket.recv()
            # await queue.put(json.loads(str(response).replace('', '')))
            await queue.put(datetime.datetime.now().strftime('%H:%M:%S') + "  :  " + response)
            # await asyncio.sleep(10)
            #
            # # Sending a keep-alive signal
            # signal_text_keep_connect = '{"type":6}'
            # await websocket.send(signal_text_keep_connect)
            # print(f"Sent: {signal_text_keep_connect}")



