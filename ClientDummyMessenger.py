import random
import asyncio
import requests
import json
import time


# Функция, которая отправляет 100 запросов на сервер.
async def send_request():
    users_array = ['Victor', 'Danya', 'Vika', 'Kate', 'Sam', 'Ivan', 'Anastasiya', 'Daria', 'Nika', 'Vlad']
    messages_array = ['Hello', 'Bye', 'How are you?']
    port_array = ["8000", "8001"]
    for i in range(100):
        # Создание и отправка запроса со случайными параметрами, на один из двух портов.
        user = random.choice(users_array)
        message = random.choice(messages_array)
        request = {
            "name": user,
            "text": message
        }
        port = random.choice(port_array)
        request = json.dumps(request)
        response = requests.post(f"http://127.0.0.1:{port}/message/", data=request, timeout=None)
        print(response.content)
    pass


# Функция, которая создаёт 50 корутин.
async def asynchronous():
    coroutines = [asyncio.ensure_future(send_request()) for i in range(50)]
    await asyncio.wait(coroutines)


if __name__ == '__main__':
    start_time = time.time()
    ioloop = asyncio.get_event_loop()
    ioloop.run_until_complete(asynchronous())
    ioloop.close()
    time = time.time() - start_time
    print(f"Время выполнения {time}")
