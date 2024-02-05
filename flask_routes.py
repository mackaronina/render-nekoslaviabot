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
from flask import Flask, request, send_file, jsonify, render_template, current_app
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

def route_token():
	bot = current_app.bot
	json_string = request.get_data().decode('utf-8')
	update = telebot.types.Update.de_json(json_string)
	bot.process_new_updates([update])
	return 'ok', 200

def route_ok():
	return 'ok', 200
	
def route_main():
	return render_template("index.html")
	
def route_get_data(user_id):
	bot = current_app.bot
	cursor = current_app.cursor
	data = cursor.execute(f'SELECT photo, item_one, item_two FROM neko WHERE id = {user_id}')
	data = data.fetchone()     
	if data is None: 
		return jsonify({"success": False})
	phot = data[0]
	item1 = data[1]
	item2 = data[2]
	if item1 == 0 and item2 == 0:
		return jsonify({"success": False})
	return jsonify({"success": True, "phot": bot.get_file_url(phot), "item1": item1, "item2": item2})
	
def route_item(number):
	return send_file(f'bot/items/{number}.png', mimetype='image/png')

def route_set_data():
		bot = current_app.bot
		cursor = current_app.cursor
		content = request.get_json()
		user_id = content['user_id']
		dis1 = content['dis1']
		dis2 = content['dis2']
		rot1 = content['rot1']
		rot2 = content['rot2']
		x1 = content['x1']
		y1 = content['y1']
		x2 = content['x2']
		y2 = content['y2']
		h1 = content['h1']
		h2 = content['h2']
		z1 = int(content['z1'])
		z2 = int(content['z2'])
		data = cursor.execute(f'SELECT item_one, item_two, photo, chat FROM neko WHERE id = {user_id}')
		data = data.fetchone()     
		if data is None: 
			return '!', 200
		item1 = data[0]
		item2 = data[1]
		phot = data[2]
		chat = data[3]
		im0 = get_pil(bot,phot)
		with Image.open("bot/items/"+str(item1)+".png") as im1, Image.open("bot/items/"+str(item2)+".png") as im2:
			if dis1 != 'none' and item1 != 0:
				if x1 == '':
					x1 = 0
				else:
					x1 = x1.replace('px','') 
					x1 = float(x1)
				if y1 == '':
					y1 = 0
				else:
					y1 = y1.replace('px','') 
					y1 = float(y1)              
				x1 = round(x1)    
				y1 = round(y1)
				h1 = round(h1)
				im1 = im1.resize((h1, h1),  Image.ANTIALIAS)
				im1 = im1.rotate(-rot1)
			if dis2 != 'none' and item2 != 0:
				if x2 == '':
					x2 = 0
				else:
					x2 = x2.replace('px','') 
					x2 = float(x2)
				if y2 == '':
					y2 = 0
				else:
					y2 = y2.replace('px','') 
					y2 = float(y2)
				x2 = round(x2) 
				y2 = round(y2)
				h2 = round(h2)
				im2 = im2.resize((h2, h2),  Image.ANTIALIAS)
				im2 = im2.rotate(-rot2)
			if z1 > z2:
				if dis2 != 'none' and item2 != 0:
					im0.paste(im2.convert('RGB'), (x2,y2),im2)
				if dis1 != 'none' and item1 != 0:
					im0.paste(im1.convert('RGB'), (x1,y1),im1)
			else:
				if dis1 != 'none' and item1 != 0:
					im0.paste(im1.convert('RGB'), (x1,y1),im1)
				if dis2 != 'none' and item2 != 0:
					im0.paste(im2.convert('RGB'), (x2,y2),im2)
		keyboard = types.InlineKeyboardMarkup(row_width=2)
		callback_button1 = types.InlineKeyboardButton(text = 'Норм ✅',callback_data = 'wear ' + str(user_id))
		keyboard.add(callback_button1)
		callback_button2 = types.InlineKeyboardButton(text = 'Хуита ❌',callback_data = 'dont ' + str(user_id))
		keyboard.add(callback_button2)
		m = bot.send_photo(chat, photo=send_pil(im0), reply_markup=keyboard)
		schedule.every(DELETE_MINUTES).minutes.do(job_delete,bot,m.chat.id,m.id)
		return '!', 200
