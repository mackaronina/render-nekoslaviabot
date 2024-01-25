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
from io import BytesIO
import html
import traceback
import requests

def msg_cmd(message,bot):
		text = 'СПИСОК УСТАРЕЛ\n\n<code>Неко</code> - твоя некодевочка\n<code>Вещи</code> - всякий мусор, твой инвентарь\n<code>Покормить</code> - можно кормить раз в 5 часов\n<code>Выгулять</code> - можно выгуливать раз в 8 часов\n<code>Погладить</code> - название говорит само за себя, от 10-ти доверия\n<code>Имя [текст]</code> - дать имя\n<code>Топ</code> - лучшие некодевочки\n<code>Кладбище</code> - недавно умершие некодевочки\n<code>Некобаза</code> - ты здесь живёшь\n<code>Гараж</code> - тут будет стоять твоя машина\n<code>Завод</code> - отработать смену раз в день\n<code>Казино</code> - а здесь можно проебать заработанные деньги\n<code>Донат [N]</code> - перевести деньги ответом на сообщение\n<code>Арена</code> - арена некодевочек, от 20-ти доверия\n<code>Лицензия</code> - получить новую лицензию на некодевочку за 10 💰\n<code>Портал</code> - данж от 50-ти доверия, нужен некомобиль\n<code>Навыки</code> - уникальные боевые способности твоей некодевочки'
		bot.send_message(message.chat.id,text,reply_to_message_id=message.message_id)

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

def msg_report(message,bot):
		print('aboba')
		'''
		cursor = bot.cursor
		args = message.text.split()
		if len(args) < 2:
			bot.send_message(message.chat.id,'После /report нужно написать текст', reply_to_message_id=message.message_id)
			return

		args.pop(0)
		text = ' '.join(args)
		bot.send_message(message.chat.id,'Отправлено', reply_to_message_id=message.message_id)
		m = bot.send_message(SERVICE_CHATID, 'Пришел репорт: '+ text)
		cursor.execute(f"INSERT INTO reports (message,chat,wait,source_message,source_chat) VALUES ({m.id},{m.chat.id},{int(time.time() + REPORT_TIMEOUT)},{message.id},{message.chat.id})")
		'''

def msg_reply(message,bot):
		print('aboba')
		'''
		cursor = bot.cursor
		if message.reply_to_message is None:
			bot.send_message(message.chat.id, 'Ответом на сообщение даун',reply_to_message_id=message.message_id)
			return
		args = message.text.split()
		if len(args) < 2:
			bot.send_message(message.chat.id,'После /reply нужно написать текст', reply_to_message_id=message.message_id)
			return
		args.pop(0)
		text = ' '.join(args)
		data = cursor.execute(f"SELECT source_message,source_chat FROM reports WHERE message = {message.reply_to_message.id} AND chat = {message.reply_to_message.chat.id}")
		data = data.fetchone()
		if data is None:
			bot.send_message(message.chat.id,'Сообщение не найдено',reply_to_message_id=message.message_id)
			return
		source_message = data[0]
		source_chat = data[1]
		bot.send_message(source_chat,'Пришел ответ: ' + text,reply_to_message_id=source_message)
		bot.send_message(message.chat.id,'Отправлено',reply_to_message_id=message.message_id)
		cursor.execute(f"DELETE FROM reports WHERE message = {message.reply_to_message.id} AND chat = {message.reply_to_message.chat.id}")
		'''
		
def msg_help(message,bot):
		text = '<b>Некославия</b> - великая держава, а великая держава должна заботиться о своих гражданах, не так ли? Для этого запуvvщена специальная социальная программа - каждому полагается по некодевочке, без очередей и налогов. К счастью, благодаря новейшим разработкам у нас их достаточно. По закону каждый некослав обязан заботиться о своей некодевочке, а её смерть уголовно наказуема. Основой же нашего государственного строя является социальный рейтинг граждан, который напрямую зависит от доверия питомцев к ним\n\nЕсли тебе этого мало, вот ссылка на канал:\n<a href="https://www.youtube.com/channel/UCGGQGNMYzZqNJSCmmLsqEBg">Nekoslavia</a>\nЗадонатить на развитие бота:\n<i>5375 4141 3075 3857</i>'
		text = 'Полезные ссылки:\n\n<a href="https://t.me/nekoslavia">Беседа с ботом</a>\n\n<a href="https://www.youtube.com/channel/UCGGQGNMYzZqNJSCmmLsqEBg">Наш канал на ютубе</a>\n\n<a href="https://send.monobank.ua/jar/86xhtgWqmw">Задонатить на развитие бота</a>'
		bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQACsNJi4zRDEZJXRw3LDwsaG18kszXm_wACPbsxG6IdGEsJeCDpoaaZxAEAAwIAA3MAAykE',caption = text)

def msg_stat(message,bot):
		text = 'Всего некодевочек:  ' + str(len(photos) + len(elite_photos) + len(ero_photos) + len(arc_photos) + len(trap_photos)) + '\nОбычные:  ' + str(len(photos)) + '\nМагазин:  ' + str(len(elite_photos)) + '\nКазино:  ' + str(len(ero_photos)) + '\nНекоарки:  ' + str(len(arc_photos)) + '\nНекомальчики:  ' + str(len(trap_photos))
		bot.send_message(message.chat.id,text)

def msg_start(message,bot):
		cursor = bot.cursor
		data = cursor.execute(f"SELECT id FROM neko WHERE id = {message.from_user.id}")
		data = data.fetchone()
		if data is None:
			p = random.choice(photos)
			kormit = int(time.time())
			gulat = int(time.time() + GULAT_TIMEOUT)
			licension = int(time.time() + LICENSION_TIMEOUT)
			happy = int(time.time())
			cursor.execute(f"INSERT INTO neko (id,name,gulat,kormit,photo,licension,happy) VALUES ({message.from_user.id},'Некодевочка',{gulat},{kormit},'{p}',{licension}, {happy})")
			bot.send_message(message.chat.id,'Добро пожаловать в Некославию! Каждому гражданину, согласно конституции, полагается некодевочка, держи свою\n\n/cmd - список комманд\n\n/help - полезные ссылки')
			time.sleep(1)
			text = 'Надо бы пояснить тебе наши порядки. <b>Некославия</b> - великая держава, а великая держава должна заботиться о благополучии своих гражданах, не так ли? Для этого запущена специальная социальная программа - каждому полагается по некодевочке, без очередей и налогов. К счастью, благодаря новейшим разработкам у нас их достаточно. По закону каждый некослав обязан заботиться о своей некодевочке, а её смерть уголовно наказуема'
			bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQACsJRi4vTvzOG-zrdVRRS3iQhKUm-K_QAC37oxG6IdGEsIcBwLxnaZgwEAAwIAA3MAAykE',caption = text)
			time.sleep(1)
			text = 'А вот и твоя некодевочка. Вероятно, она проголодалась пока ждала тебя. Напиши "неко" чтобы убедиться в этом, а когда покормишь - не забудь дать ей имя'
			bot.send_photo(message.chat.id, photo = p,caption = text)
			time.sleep(1)
			photo_design = 'AgACAgIAAx0CZQN7rQABAicRZSFoSY43lFLhRbyeeXPlv55ekY8AArbPMRvwnghJbqkwodtNPHcBAAMCAAN5AAMwBA' 
			f = create_licension(bot,p,photo_design,message.from_user.first_name,0)
			m = bot.send_photo(message.chat.id, photo=f,caption = 'И самое главное, держи лицензию 🎫 на свою некодевочку. Нужно будет продлить её через 4 дня, если не хочешь платить штраф, конечно')
			cursor.execute(f"UPDATE neko SET photo_licension = '{m.photo[-1].file_id}' WHERE id = {message.from_user.id}")
		else:
			bot.send_message(message.chat.id,'Ты уже некослав ебанат')