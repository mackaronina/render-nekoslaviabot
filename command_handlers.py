from config import *
from functions import *
from jobs import *

from threading import Thread
import random
import schedule
import telebot
from telebot import types
import time
import math
from datetime import datetime
from flask import Flask, request, send_file, jsonify, render_template
from PIL import Image,ImageDraw,ImageFont
import emoji
import textwrap
from petpetgif.saveGif import save_transparent_gif
from pkg_resources import resource_stream
from sqlalchemy import create_engine
import json
from io import StringIO, BytesIO
import html
import traceback
import requests

def msg_cmd(message,bot):
		#text = 'СПИСОК УСТАРЕЛ\n\n<code>Неко</code> - твоя некодевочка\n<code>Вещи</code> - всякий мусор, твой инвентарь\n<code>Покормить</code> - можно кормить раз в 5 часов\n<code>Выгулять</code> - можно выгуливать раз в 8 часов\n<code>Погладить</code> - название говорит само за себя, от 10-ти доверия\n<code>Имя [текст]</code> - дать имя\n<code>Топ</code> - лучшие некодевочки\n<code>Кладбище</code> - недавно умершие некодевочки\n<code>Некобаза</code> - ты здесь живёшь\n<code>Гараж</code> - тут будет стоять твоя машина\n<code>Завод</code> - отработать смену раз в день\n<code>Казино</code> - а здесь можно проебать заработанные деньги\n<code>Донат [N]</code> - перевести деньги ответом на сообщение\n<code>Арена</code> - арена некодевочек, от 20-ти доверия\n<code>Лицензия</code> - получить новую лицензию на некодевочку за 10 💰\n<code>Портал</code> - данж от 50-ти доверия, нужен некомобиль\n<code>Навыки</code> - уникальные боевые способности твоей некодевочки'
		text = help_text[0]
		keyboard = types.InlineKeyboardMarkup(row_width=2)
		callback_button1 = types.InlineKeyboardButton(text = '⬅️',callback_data = f'wikicmd {message.from_user.id} 2')
		callback_button2 = types.InlineKeyboardButton(text = '➡️',callback_data = f'wikicmd {message.from_user.id} 1')
		keyboard.add(callback_button1,callback_button2)
		m = bot.send_message(message.chat.id,text,reply_markup=keyboard)
		schedule.every(DELETE_MINUTES).minutes.do(job_delete,bot,m.chat.id,m.id)

def msg_delete(message,bot):
		cursor = bot.cursor
		data = cursor.execute(f"SELECT id FROM neko WHERE id = {message.from_user.id}")
		data = data.fetchone()
		if data is None:
			bot.send_message(message.chat.id,'У тебя и так нет некодевочки')
			return
		keyboard = types.InlineKeyboardMarkup(row_width=1)
		callback_button1 = types.InlineKeyboardButton(text = '✅ Выкинуть',callback_data = 'delacc ' + str(message.from_user.id))
		callback_button2 = types.InlineKeyboardButton(text = '❌ Да ну нахуй',callback_data = 'dont ' + str(message.from_user.id))
		keyboard.add(callback_button1)
		keyboard.add(callback_button2)
		m = bot.send_message(message.chat.id,'Подумай ещё раз',reply_markup=keyboard)
		schedule.every(DELETE_MINUTES).minutes.do(job_delete,bot,m.chat.id,m.id)
		raise Exception("Проверка")

def msg_report(message,bot):
		if message.reply_to_message is None:
			bot.send_message(message.chat.id, 'Ответом на сообщение даун')
			return
		bot.forward_message(chat_id=SERVICE_CHATID, from_chat_id=message.chat.id, message_id=message.reply_to_message.message_id, protect_content=True)
		bot.send_message(message.chat.id, 'Отправлено')
		
def msg_help(message,bot):
		text = '<b>Некославия</b> - великая держава, а великая держава должна заботиться о своих гражданах, не так ли? Для этого запущена специальная социальная программа - каждому полагается по некодевочке, без очередей и налогов. К счастью, благодаря новейшим разработкам у нас их достаточно. По закону каждый некослав обязан заботиться о своей некодевочке, а её смерть уголовно наказуема. Основой же нашего государственного строя является социальный рейтинг граждан, который напрямую зависит от доверия питомцев к ним\n\nЕсли тебе этого мало, вот ссылка на канал:\n<a href="https://www.youtube.com/channel/UCGGQGNMYzZqNJSCmmLsqEBg">Nekoslavia</a>\nЗадонатить на развитие бота:\n<i>5375 4141 3075 3857</i>'
		text = 'Полезные ссылки:\n\n<a href="https://t.me/nekoslavia">Беседа с ботом</a>\n\n<a href="https://www.youtube.com/channel/UCGGQGNMYzZqNJSCmmLsqEBg">Наш канал на ютубе</a>\n\n<a href="https://send.monobank.ua/jar/86xhtgWqmw">Задонатить на развитие бота</a>\n\nСообщай о багах или предложениях через /report'
		bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQACsNJi4zRDEZJXRw3LDwsaG18kszXm_wACPbsxG6IdGEsJeCDpoaaZxAEAAwIAA3MAAykE',caption = text)

def msg_stat(message,bot):
		text = 'Всего некодевочек:  ' + str(len(photos) + len(elite_photos) + len(ero_photos) + len(arc_photos) + len(trap_photos)) + '\nОбычные:  ' + str(len(photos)) + '\nМагазин:  ' + str(len(elite_photos)) + '\nКазино:  ' + str(len(ero_photos)) + '\nНекоарки:  ' + str(len(arc_photos)) + '\nНекомальчики:  ' + str(len(trap_photos))
		bot.send_message(message.chat.id,text)

def msg_start(message,bot):
		text = 'В этом боте ты получишь настоящую кошкожену, которую можно кормить, гладить и ещё много чего. Напиши <i><u>неко</u></i>" чтобы начать своё приключение в ебанутом мире <b>Некославии</b>'
		bot.send_message(message.chat.id, text)