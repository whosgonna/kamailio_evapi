import json
import socket
import sys
import time
import logging

import aiohttp
import asyncio
import pynetstring

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Starting EVAPI service")

attempt = None

async def main():
    KAMAILIO_HOST = "kamailio"
    KAMAILIO_PORT = 8228
    logger.info("In main")

    host = socket.gethostbyname(KAMAILIO_HOST)
    port = KAMAILIO_PORT  # socket server port number

    logger.info(f"Connecting to {host}:{port}")

    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                logger.info("Connected to server")

                while True:
                    data = s.recv(65535) ## Limited to 1024 bytes?

                    if not data:
                        break

                    t1 = time.time()

                    recv = pynetstring.decode(data)[0].decode()

                    logger.info(f"{t1} Received: {recv}")

                    ev_data = json.loads(recv)
                    event = ev_data["event"]

                    logger.info(f"event is {ev_data["event"]}")

                    t2 = time.time()
                    if event == "get_caller_id":
                        elapsed = t2 - t1
                        logger.info(f"{t2} {elapsed} event is get_caller_id")
                        ret_data = get_caller_id(ev_data)

                    t3 = time.time()
                    elapsed = t3 - t1
                    logger.info(f"{t3} {elapsed} calling mock sleep")
                    ## Mock sleep=
                    await async_sleeping(1)

                    t4 = time.time()
                    elapsed = t4 - t1
                    logger.info(f"{t4} {elapsed} after mock sleep");



                    reply = {
                        "tm":   ev_data["tm"],
                        "data": ret_data
                    }

                    reply_json = json.dumps(reply)

                    t5 = time.time()
                    elapsed = t5 - t1

                    logger.info(f"{t5} {elapsed} Trying to send: {reply_json}")
                    attempt = s.send(pynetstring.encode(reply_json))

                    t6 = time.time()
                    elapsed = t6 - t1
                    logger.info(f"{t6} {elapsed} After sending reply")

        except ConnectionRefusedError:
            logger.error("Server not available. Retrying in 5 seconds...")
            time.sleep(5)


def get_caller_id(data):
    fU = data["data"]["fU"]
    logger.info(f"$fU is {fU}")

    ret_data = {
        "caller_name": "kaufman"
    }

    return ret_data

async def async_sleeping(duration):
    time.sleep(duration)

async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
            else:
                return f"Error: {response.status}"



async def main_req():
    url = "http://www/sleep/1";
    data = await fetch_data(url)
    print(data)


#    client_socket = socket.socket()  # instantiate
#    client_socket.connect((host, port))  # connect to the server
#
#    message = input(" -> ")  # take input
#
#    while message.lower().strip() != 'bye':
#        client_socket.send(message.encode())  # send message
#        data = client_socket.recv(1024).decode()  # receive response
#
#        print('Received from server: ' + data)  # show in terminal
#
#        message = input(" -> ")  # again take input
#
#    client_socket.close()  # close the connection


if __name__ == '__main__':
    asyncio.run(main())


