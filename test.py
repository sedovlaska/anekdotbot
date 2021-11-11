import requests
import re
import os
import sqlite3
from sqlitepy import SQLighter
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove,ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, callback_query, reply_keyboard
from gtts import gTTS
from config import token

bot = Bot(token=token)
dp = Dispatcher(bot)
db = SQLighter("db1.db")


button1 = InlineKeyboardButton('Анекдот 18+',callback_data='anekdot')
button2 = InlineKeyboardButton('Тост 18+',callback_data='tost')
button3 = InlineKeyboardButton('Сохранить :)', callback_data='save')
button4 = InlineKeyboardButton('Аудиофайл',callback_data='audio')
greet_kb = InlineKeyboardMarkup()
start_kb = InlineKeyboardMarkup()
start_kb.add(button1)
start_kb.add(button2)
greet_kb.add(button1)
greet_kb.add(button2)
greet_kb.add(button4)
greet_kb.add(button3)

@dp.message_handler(commands=['hello'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.from_user.id,"Привет!\n у нас тут есть анекдоты и тосты 18+")
     
@dp.message_handler(commands=['start'])
async def get_start(message:types.Message):
    if(not db.user_exists(message.from_user.id)):
        	db.add_user(message.from_user.id, message.from_user.username)
    await message.answer("Нажми на кнопочку",parse_mode="Markdown",reply_markup=start_kb) 

@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, 'Пока что не понимаю тыкай кнопки :(')  

@dp.callback_query_handler(text='anekdot')
async def anekdotstart(callback_query: types.CallbackQuery):
    r = requests.get('http://rzhunemogu.ru/RandJSON.aspx?CType=11')
    test = r.text
    test = re.sub(r'{"content":"','',test)
    test = re.sub(r'"}','',test)
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text(text=test,reply_markup = greet_kb)

@dp.callback_query_handler(text='tost')
async def toststart(callback_query: types.CallbackQuery):
    r = requests.get('http://rzhunemogu.ru/RandJSON.aspx?CType=16')
    test = r.text
    test = re.sub(r'{"content":"','',test)
    test = re.sub(r'"}','',test)
    #await bot.send_message(query.from_user.id, test,reply_markup=greet_kb)
    bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text(text=test,reply_markup = greet_kb)

@dp.callback_query_handler(text='save')
async def savetext(callback_query: types.CallbackQuery):
    text = callback_query.message.text
    if (not db.check_text(text)):
        db.save_text(text,callback_query.from_user.username)
    await bot.send_message(callback_query.from_user.id, text)
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete() 
    await bot.send_message(callback_query.from_user.id,text="Продолжим ?",parse_mode="Markdown",reply_markup=start_kb) 

@dp.callback_query_handler(text='audio')
async def saveaudio(callback_query: types.CallbackQuery):
    text = callback_query.message.text
    tts = gTTS(text, lang='ru')
    tts.save(str(callback_query.message.message_id)+'.mp3') 
    bot.send_audio(callback_query.from_user.id,audio=open(str(callback_query.message.message_id)+'.mp3','rb'))
    os.remove((str(callback_query.from_user.id)+'.mp3'))
    callback_query.message.delete() 
    bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,text="Продолжим ?",parse_mode="Markdown",reply_markup=start_kb) 
    

if __name__ == '__main__':
    executor.start_polling(dp)