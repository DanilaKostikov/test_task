from fastapi import FastAPI
from sqlalchemy import Column, Integer, String, DateTime, create_engine, MetaData, Table
import databases as databases
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

database = databases.Database(SQLALCHEMY_DATABASE_URL)

metadata = MetaData()

# Создание таблицы сообщений.
messages = Table(
    "messages",
    metadata,
    Column("user", String),
    Column("text", String),
    Column("date", DateTime),
    Column("id", Integer, autoincrement=True, primary_key=True, index=True),
    Column("number_of_messages", Integer),
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


# Класс, который отражает поля, отправляемых на сервер данных.
class MessageInput(BaseModel):
    name: str
    text: str


# Подключение к базе данных при запуске сервера.
@app.on_event("startup")
async def startup():
    await database.connect()


# Отключение от базы данных при отключении сервера.
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# Основная функция api, которая принимает на вход имя пользователя и сообщение.
@app.post("/message/")
async def send_message(message: MessageInput):
    name = message.name
    text = message.text
    date = datetime.now()
    # Отправка запроса, на сбор всех сообщений пользователя из базы данных.
    query = messages.select().where(messages.c.user == name)
    result = await database.fetch_all(query)
    _len = len(result)+1
    # Отправка запроса, на добавление сообщения в базу данных.
    query = messages.insert().values(user=name, text=text, date=date, number_of_messages=_len)
    await database.execute(query)
    # Отправка запроса, на сбор последних 10 сообщений из базы данных.
    query = messages.select().order_by(messages.c.id.desc()).limit(10)
    result = await database.fetch_all(query)
    return result
