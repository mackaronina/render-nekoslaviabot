from config import *
from functions import *

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

def jobupd(bot):
	try:
		cursor = bot.cursor
		db = bot.db
		tim = int(time.time())
		data = cursor.execute(f'SELECT name,id,chat,chel,notifed,kormit FROM neko WHERE kormit < {tim - 4*24*3600}')
		data = data.fetchall()
		for dat in data:
			nam = dat[0]
			idk = dat[1]
			ch = dat[2]
			chel = dat[3]
			notifed = dat[4]
			kormit = int(dat[5] - tim)
			if kormit < -4*24*3600 and not notifed:
				try:
					cursor.execute(f"UPDATE neko SET notifed = TRUE WHERE id = " + str(idk))
					bot.send_message(ch, nam + ' уже не ела четыре дня! <a href="tg://user?id='+str(idk)+'">'+str(chel)+'</a>, ты охуел?')
					bot.send_sticker(ch, 'CAACAgIAAxkBAAEFNvlixtyYbnUoOviqOfiUaIH6jdlPhAACuxMAAsmQWEhravemy77rYSkE')
				except:
					pass
			#if kormit > 5*24*3600:
			#    try:
			#        bot.send_message(ch, nam + ' умерла от голода... <a href="tg://user?id='+str(idk)+'">'+str(chel)+'</a>, её смерть на твоей совести, и ты теперь изгнан из Некославии')
			#        bot.send_sticker(ch, 'CAACAgIAAxkBAAEFNNFixbh5x7lPtkqzBN2g8YO9FAMCLgACjxEAAqg6WEjqQFCw4uPiwikE')
			#    except:
			#        pass
			#    add_to_dead(cursor,nam, 'Смерть от голода')
			#    cursor.execute(f"DELETE FROM neko WHERE id = "+str(idk))
		for key in list(db.keys()):
			struct = unpack(db[key])
			wait = struct['wait']
			gametype = struct['type']
			msg = struct['message']
			ch = struct['chat']
			if wait < int(time.time()):
				try:
					if gametype == 'dungeon':
						bot.edit_message_caption(chat_id=ch, message_id=msg, caption='Твой некочан не выдержал ужасов LGBT мира и сбежал, бросив всё найденное. В следующий раз не заставляй его находиться там так долго')
					elif gametype == 'boss':
						event = struct['event']
						if event == 0:
							bot.edit_message_text(chat_id=ch, message_id=msg, text='Никто не отозвался, ну и пошли они нахуй')
						elif event == 1:
							bot.edit_message_caption(chat_id=ch, message_id=msg, caption='Некочаны заебались ждать и ушли оставив вас одних')
						elif event == 2:
							bot.edit_message_caption(chat_id=ch, message_id=msg, caption='Бой длился слишком долго, в следствии чего некочаны не выдержали напряжения и сбежали поджав хвосты')
					elif gametype == 'battle':
						event = struct['event']
						if event == 0:
							bot.edit_message_text(chat_id=ch, message_id=msg,text="Что ж, на вызов так никто и не ответил..")
						elif event == 2:
							bot.edit_message_caption(chat_id=ch, message_id=msg,caption="Это был затяжной бой, завершившийся ничьёй..")
					elif gametype == 'poker':
						event = struct['event']
						if event == -1:
							bot.edit_message_text(chat_id=ch, message_id=msg,text = 'Никто не отозвался, одно ссыкло в чате')
						else:
							bot.edit_message_caption(chat_id=ch, message_id=msg, caption='Вы заебали уже играть, в следующий раз надо быстрее')
					elif gametype == 'papers':
						bot.edit_message_caption(chat_id=ch, message_id=msg, caption='Рабочий день закончился, в следующий раз будь быстрее')
				except:
					pass
				del db[key]
	except Exception as e:
		bot.send_message(ME_CHATID, e)

def job_delete(bot,chat,mid):
	try:
		bot.delete_message(chat_id=chat, message_id=mid)
		print('Удалено')
	except:
		print('Неудалено')
	return schedule.CancelJob