from config import *
from functions import *
from jobs import *
from command_handlers import *
from message_handlers import *
from callback_handlers import *
from flask_routes import *

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

time.sleep(2)

class ExHandler(telebot.ExceptionHandler):
	def handle(self, exc):
		sio = StringIO(traceback.format_exc())
		sio.name = 'log.txt'
		sio.seek(0)
		bot.send_document(ME_CHATID, sio)
		return True
bot = telebot.TeleBot(TOKEN, threaded=True, num_threads=10, parse_mode='HTML', exception_handler = ExHandler())

cursor = create_engine(f'mysql+pymysql://{USERNAME}:{PASSWORD}@eu-central.connect.psdb.cloud:3306/nekodb', pool_recycle=280, connect_args={'ssl': {'ssl-mode': 'preferred'}})

app = Flask(__name__)
bot.remove_webhook()
bot.set_webhook(url=APP_URL)

random.seed()

gazeta = {
	'patch_version': 1007,
	'patch_title': 'Патчноут',
	'patch_text': 'Произошел геноцид некодевочек. Напишите мне если кто-то хочет их восстановить',
	'patch_image': ''
}

antiflood = {
	'blocked_messages': [],
	'blocked_users': [],
	'floodlist': {}
}

db = {}

setattr(bot,'cursor',cursor)
setattr(bot,'gazeta',gazeta)
setattr(bot,'antiflood',antiflood)
setattr(bot,'db',db)

setattr(app,'cursor',cursor)
setattr(app,'bot',bot)

bot.register_message_handler(msg_start,commands=["start"],pass_bot=True)
bot.register_message_handler(msg_cmd,commands=["cmd"],pass_bot=True)
bot.register_message_handler(msg_delete,commands=["delete"],pass_bot=True)
bot.register_message_handler(msg_report,commands=["report"],pass_bot=True)
bot.register_message_handler(msg_help,commands=["help"],pass_bot=True)
bot.register_message_handler(msg_stat,commands=["stat"],pass_bot=True)

bot.register_message_handler(msg_text,func=lambda message: True,content_types=["text"],pass_bot=True)
bot.register_message_handler(msg_photo,func=lambda message: True,content_types=["photo"],pass_bot=True)

bot.register_callback_query_handler(callback_get,func=lambda call: True,pass_bot=True)

app.add_url_rule('/' + TOKEN, methods=['POST'], view_func = route_token)
app.add_url_rule('/', view_func = route_ok)
app.add_url_rule('/main', view_func = route_main)
app.add_url_rule('/get_data/<user_id>', methods=['POST'], view_func = route_get_data)
app.add_url_rule('/item/<number>', view_func = route_item)
app.add_url_rule('/set_data', methods=['POST'], view_func = route_set_data)
	
def updater():
	while True:
		schedule.run_pending()
		time.sleep(1)
		
def bot_start():
	generate_gazeta(bot)

schedule.every(60).seconds.do(jobupd,bot)
Thread(target=bot_start).start()
Thread(target=updater).start()
app.run(host='0.0.0.0', port=80, threaded = True)
