import sqlite3
from sqlitepy import SQLighter
import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import re

#http://rzhunemogu.ru/RandJSON.aspx?CType=? 11/16
bot = Bot(token="1811709778:AAElnKrdZHBXeP6O9970K6pSmPcGzdpRtWY")
dp = Dispatcher(bot)
db = SQLighter("db1.db")
 
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    if(not db.user_exists(message.from_user.id)):
    	db.add_user(message.from_user.id, message.from_user.username)
    else:
        bot.send_message(message.from_user.id, "Ты уже тута")
    await message.reply("Привет!\n у нас тут есть анекдоты и тосты 18+")
    

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")


@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)




if __name__ == '__main__':
    executor.start_polling(dp)