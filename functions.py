from config import *

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

def make(source, clr):
	frames = 10
	resolution = (256, 256)
	images = []
	base = source.convert('RGBA').resize(resolution)

	for i in range(frames):
		squeeze = i if i < frames/2 else frames - i
		width = 0.8 + squeeze * 0.02
		height = 0.8 - squeeze * 0.05
		offsetX = (1 - width) * 0.5 + 0.1
		offsetY = (1 - height) - 0.08

		canvas = Image.new('RGBA', size=resolution, color=clr)
		canvas.paste(base.resize((round(width * resolution[0]), round(height * resolution[1]))), (round(offsetX * resolution[0]), round(offsetY * resolution[1])))
		with Image.open(resource_stream(__name__, f"bot/pet/pet{i}.gif")).convert('RGBA').resize(resolution) as pet:
			canvas.paste(pet, mask=pet)
		images.append(canvas)
	bio = BytesIO()
	bio.name = 'result.gif'
	save_transparent_gif(images, durations=20, save_file=bio)
	bio.seek(0)
	return bio

def flood_counter_plus(bot,message):
	floodlist = bot.antiflood['floodlist']
	user_id = message.from_user.id
	msgs = 5 # Messages in
	sec = 3 # Seconds
	ban = 10 # Seconds
	try:
		usr = floodlist[user_id]
		usr["messages"] += 1
	except:
		floodlist[user_id] = {"next_time": int(time.time()) + sec, "messages": 1, "banned": 0}
		usr = floodlist[user_id]
	if usr["banned"] >= int(time.time()):
		return True
	else:
		if usr["next_time"] >= int(time.time()):
			if usr["messages"] >= msgs:
				floodlist[user_id]["banned"] = time.time() + ban
				bot.send_message(message.chat.id, 'Ты в муте клоун, хватит спамить',reply_to_message_id=message.message_id)
				return True
		else:
			floodlist[user_id]["messages"] = 1
			floodlist[user_id]["next_time"] = int(time.time()) + sec
	return False

def img_resize(img,required_w,required_h):
	w,h = img.size
	if w > h and required_w < required_h:
		nh = required_h
		nw = int((required_h/h)*w)
	else:
		nw = required_w
		nh = int((required_w/w)*h)

	if nw < required_w:
		nw = required_w
	if nh < required_h:
		nh = required_h
	img = img.resize((nw, nh),  Image.ANTIALIAS)
	return img

def draw_stroke(draw,font,fillcolor,shadowcolor,text,x,y):
	draw.text((x-2, y), text, font=font, fill=shadowcolor)
	draw.text((x+2, y), text, font=font, fill=shadowcolor)
	draw.text((x, y-2), text, font=font, fill=shadowcolor)
	draw.text((x, y+2), text, font=font, fill=shadowcolor)
	draw.text((x-2, y-2), text, font=font, fill=shadowcolor)
	draw.text((x+2, y-2), text, font=font, fill=shadowcolor)
	draw.text((x-2, y+2), text, font=font, fill=shadowcolor)
	draw.text((x, y), text, font=font, fill=fillcolor)

def create_licension(bot,photo_neko,photo_design,chel,gender,old_licension_time = 0):
	im0 = get_pil(bot,photo_design)
	im0 = img_resize(im0,600,630)
	im1 = Image.new(mode = 'RGB',size = (1120,698))
	copy = im1
	im1.paste(im0.convert('RGB'), (40,34))
	im0 = im1
	with Image.open('bot/licension/lic02.png') as im2:
		im0.paste(im2.convert('RGB'), (0,0), im2)
	im0 = im0.convert('RGBA')
	pixdata = im0.load()
	for y in range(im0.size[1]):
		for x in range(im0.size[0]):
			if pixdata[x,y][0]==255 and pixdata[x,y][1]==0 and pixdata[x,y][2]==0:
				pixdata[x, y] = (255, 255, 255,0)
	if len(chel) > 18:
		chel = (chel[:18] + '..')
	im1 = get_pil(bot,photo_neko)
	im1 = img_resize(im1,600,630)
	im3 = copy
	im3.paste(im1.convert('RGB'), (490,30))
	im1 = im3
	im1.paste(im0.convert('RGB'), (0,0), im0)
	font = ImageFont.truetype('bot/fonts/segoeprint_bold.ttf', size=35)
	draw = ImageDraw.Draw(im1)
	if old_licension_time == 0:
		cur = datetime.fromtimestamp(time.time() + TIMESTAMP)
	else:
		cur = datetime.fromtimestamp(old_licension_time + TIMESTAMP - LICENSION_TIMEOUT)
	old_date = date_string(cur)
	if old_licension_time == 0:
		cur = datetime.fromtimestamp(time.time() + TIMESTAMP + LICENSION_TIMEOUT)    
	else:
		cur = datetime.fromtimestamp(old_licension_time + TIMESTAMP)
	new_date = date_string(cur)
	fillcolor = "#FFFFFF"
	shadowcolor = "#242425"
	text = 'Выдано:  @NekoslaviaBot'
	x, y = 63, 65
	draw_stroke(draw,font,fillcolor,shadowcolor,text,x,y)
	text = f'Кому:  {chel}'
	x, y = 63, 125
	draw_stroke(draw,font,fillcolor,shadowcolor,text,x,y)
	text = f'Дата выдачи:  {old_date}'
	x, y = 63, 185
	draw_stroke(draw,font,fillcolor,shadowcolor,text,x,y)
	text = f'Действует до:  {new_date}'
	x, y = 63, 245
	draw_stroke(draw,font,fillcolor,shadowcolor,text,x,y)
	
	font = ImageFont.truetype('bot/fonts/comicbd.ttf', size=52)
	text = 'ЛИЦЕНЗИЯ НА\nНЕКОДЕВОЧКУ'
	x, y = 95, 500
	if gender == 1:
		text = 'ЛИЦЕНЗИЯ НА\nНЕКОМАЛЬЧИКА'
		x, y = 65, 500
	fillcolor = "#F6B1CB"
	draw_stroke(draw,font,fillcolor,shadowcolor,text,x,y)
	return send_pil(im1)
	
def get_pil(bot,fid):
	file_info = bot.get_file(fid)
	downloaded_file = bot.download_file(file_info.file_path)
	im = Image.open(BytesIO(downloaded_file))
	return im

def send_pil(im):
	bio = BytesIO()
	bio.name = 'result.png'
	im.save(bio, 'PNG')
	bio.seek(0)
	return bio

def poker_init_keyboard(idk):
	keyboard = types.InlineKeyboardMarkup(row_width=2)
	callback_button1 = types.InlineKeyboardButton(text = '➕',callback_data = f'pplus {idk}')
	callback_button2 = types.InlineKeyboardButton(text = '➖',callback_data = f'pminus {idk}')
	callback_button3 = types.InlineKeyboardButton(text = 'Продолжить ✔️',callback_data = f'pcontinue {idk}')
	keyboard.add(callback_button1,callback_button2)
	keyboard.add(callback_button3)
	return keyboard
	
def date_string(cur):
	dy = cur.day
	if dy < 10:
		dy = f'0{dy}'
	else:
		dy = f'{dy}'
	mn = cur.month
	if mn < 10:
		mn = f'0{mn}'
	else:
		mn = f'{mn}'
	yr = cur.year
	date = f'{dy}.{mn}.{yr}'
	return date
	
def pack(mas):
	data = {"data": mas}
	data = json.dumps(data,ensure_ascii=False)
	return data
	
def unpack(data):
	mas = json.loads(data)
	mas = mas["data"]
	return mas
	
def dominant_color(image):
	width, height = 150,150
	image = image.resize((width, height),resample = 0)
	#Get colors from image object
	pixels = image.getcolors(width * height)
	#Sort them by count number(first element of tuple)
	sorted_pixels = sorted(pixels, key=lambda t: t[0])
	#Get the most frequent color
	dominant_color = sorted_pixels[-1][1]
	return dominant_color
	
def generate_gazeta(bot):
	print(f"Версия: {bot.gazeta['patch_version']}")
	lines = textwrap.wrap(bot.gazeta['patch_text'], width=35)
	ptxt = ''
	for line in lines:
		ptxt += line + '\n'
	with Image.open('bot/for_text/gazetka.png') as im0:
		font = ImageFont.truetype('bot/fonts/times-new-roman.ttf', size=50)
		draw = ImageDraw.Draw(im0)
		draw.text((70, 130), ptxt, font=font, fill=(82, 64, 64))
		w = font.getlength(bot.gazeta['patch_title'])
		draw.text(((924-w)/2,50), bot.gazeta['patch_title'], font=font, fill=(82, 64, 64))
		m = bot.send_photo(ME_CHATID, photo=send_pil(im0))
		bot.gazeta['patch_image'] = m.photo[-1].file_id
	
def generate_papers(bot):
	today_event = random.randint(1,3)
	if today_event == 1:
		bad_prof = [random.choice(prof),random.choice(prof)]
		while bad_prof[0] == bad_prof[1]:
			bad_prof = [random.choice(prof),random.choice(prof)]
		prof_text = ['монтажникам','электрикам','токарям','сварщикам','охранникам']
		p1 = prof_text[prof.index(bad_prof[0])]
		p2 = prof_text[prof.index(bad_prof[1])]
		bot.zavod['today_text'] = f'Cегодня запрещен проход {p1} и {p2}'
	elif today_event == 2:
		bad_prof = [random.choice(prof)]
		prof_text = ['монтажники','электрики','токари','сварщики','охранники']
		p = prof_text[prof.index(bad_prof[0])]
		bot.zavod['today_text'] = f'Cегодня {p} обязаны носить защитные каски'
	elif today_event == 3:
		bad_prof = [random.choice(prof)]
		prof_text = ['монтажники','электрики','токари','сварщики','охранники']
		p = prof_text[prof.index(bad_prof[0])]
		bot.zavod['today_text'] = f'Cегодня {p} должны иметь печать, подтверждающую их квалификацию'
	print(bot.zavod['today_text'])
	for k in range(1,11):
		propusk = random.choice([True,False])
		reason = 0
		if not propusk:
			reason = random.randint(1,5)
		with Image.open('bot/zavod/papers.png') as im0:
			#reason = 2 ДЛЯ ИВЕНТА
			if reason == 1:
				#ФОТОГРАФИЯ
				k2 = random.randint(1,10)
				while k == k2:
					k2 = random.randint(1,10)
				
				filenam = 'bot/zavod/pas'+str(k2)+'.png'
			else:
				filenam = 'bot/zavod/pas'+str(k)+'.png'
			with Image.open(filenam) as im2:
				im0.paste(im2.convert('RGB'), (445,35))
			names = ['Мику', 'Бака', 'Наруто', 'Макима', 'Шмара','Асука','Сакура']
			families = ['Некочановна','Славонековна','Кринжеделовна','Сосалка','Дегенератовна','Антифризовна','Капибаровна']
			draw = ImageDraw.Draw(im0)
			font = ImageFont.truetype('bot/fonts/segoeprint_bold.ttf', size=24)
			text = random.choice(names) + ' ' + random.choice(families)
			draw.text((650, 100), text, font=font,fill="#f0f0f0", stroke_width=2, stroke_fill='#141414')
			font = ImageFont.truetype('bot/fonts/segoeprint_bold.ttf', size=20)
			if reason == 2:
				#ВЫБОР ПРОФЕССИИ
				p = random.choice(bad_prof)
			else:
				p = random.choice(prof)
				if today_event == 1:
					while p in bad_prof:
						p = random.choice(prof)
			text = 'Профессия: ' + p
			draw.text((650, 137), text, font=font, fill="#141414", stroke_width=0, stroke_fill='#141414')
			if today_event == 2 and reason != 2 and p in bad_prof:
				filenam = 'bot/zavod/kask'+str(k)+'.png'
			else:
				filenam = 'bot/zavod/table'+str(k)+'.png'
			with Image.open(filenam) as im2:
				im0.paste(im2.convert('RGB'), (0,0))
			if reason == 3:
				#ДАТА ВЫДАЧИ
				days = random.randint(10,300)
				date = date_string(datetime.fromtimestamp(time.time() + TIMESTAMP + days*3600*24))
			else:
				days = random.randint(20,300)
				date = date_string(datetime.fromtimestamp(time.time() + TIMESTAMP - days*3600*24))
			text = 'Выдано: ' + date
			draw.text((650, 165), text, font=font, fill="#141414", stroke_width=0, stroke_fill='#141414')
			if reason == 4:
				#СРОК ГОДНОСТИ
				days = random.randint(1,15)
				date = date_string(datetime.fromtimestamp(time.time() + TIMESTAMP - days*3600*24))
			else:
				days = random.randint(10,300)
				date = date_string(datetime.fromtimestamp(time.time() + TIMESTAMP + days*3600*24))
			text = 'До: ' + date
			draw.text((650, 193), text, font=font, fill="#141414", stroke_width=0, stroke_fill='#141414')
			if reason == 5:
				#ПЕЧАТЬ
				pechat = random.choice([True,False])
				if pechat:
					with Image.open('bot/zavod/skamik.png') as im2:
						im0.paste(im2.convert('RGB'), (840,110),im2)
			else:
				with Image.open('bot/zavod/slavik.png') as im2:
					im0.paste(im2.convert('RGB'), (840,110),im2)
			if today_event == 3 and reason != 2 and p in bad_prof:
				with Image.open('bot/zavod/ekspertik.png') as im2:
					im0.paste(im2.convert('RGB'), (684,173),im2)
			m = bot.send_photo(ME_CHATID, photo=send_pil(im0))
			img = m.photo[-1].file_id
			bot.zavod['papers_images'].append(f'{img} {propusk} {reason}')
			time.sleep(1)
	
def equ(row):
	if -1 in row:
		return -1
	if 5 not in row:
		if row.count(row[0]) == len(row):
			return row[0]
		else:
			return -1
	for i in range(5):
		rw = row.copy()
		for j in range(len(rw)):
			if rw[j] == 5:
				rw[j] = i
		if rw.count(rw[0]) == len(rw):
			return rw[0]
	return -1
	
def field_calculate(field,skills,do_stars):
	atack = 0
	blocks = 0
	turns = 0
	stars = 0
	hp = 0
	figures = [0,1,2,3,4]
	if 2 in skills:
		figures.append(2)
	if 3 in skills:
		figures.append(4)
	while True:
		found = False
		for count in [6,5,4]:
			for j in range(6):
				for i in range(7-count):
					a = []
					for k in range(count):
						a.append(field[j*6+i+k])
					res = equ(a)
					if res != -1:
						if (res == 2 and 2 in skills) or (res == 4 and 3 in skills):
							stars += 1
						if res == 0 or res == 1:
							blocks += count - 3
						elif res == 2 or res == 3:
							atack += count - 3
						elif res == 4:
							turns += count - 3
						for k in range(count):
							field[j*6+i+k] = -1
						found = True

					b = []
					for k in range(count):
						b.append(field[(i+k)*6+j])
					res = equ(b)
					if res != -1:
						if (res == 2 and 2 in skills) or (res == 4 and 3 in skills):
							stars += 1
						if res == 0 or res == 1:
							blocks += count - 3
						elif res == 2 or res == 3:
							atack += count - 3
						elif res == 4:
							turns += count - 3
						for k in range(count):
							field[(i+k)*6+j] = -1
						found = True
		if -1 in field and not found:
			found = True
		if not found:
			break
		while True:
			for i in range(36):
				if field[i] == -1:
					if i < 6:
						if stars > 0 and do_stars:
							stars -= 1
							field[i] = 5
						else:
							field[i] = random.choice(figures)
					else:
						field[i] = field[i-6]
						field[i-6] = -1
			if -1 not in field:
				break
				
	if 1 in skills:
		hp += blocks
		blocks = 0
	result = [atack,blocks,turns,hp]
	return result

def combinator(cards):
	numbers = []
	colors = []
	for card in cards:
		a = card[0]
		b = card[1]
		numbers.append(a)
		colors.append(b)
	max_low = sorted(numbers)
	max_low.reverse()
	#Старшая карта
	comb = 0 + max(numbers)/100
	#Пара
	for n in max_low:
		if numbers.count(n) >= 2:
			comb = 1 + n/100
			break
	#Две пары
	p1 = 0
	p2 = 0
	for n in max_low:
		if numbers.count(n) >= 2 and n != p1 and n != p2:
			if p1 == 0:
				p1 = n
			else:
				p2 = n
		if p1 != 0 and p2 != 0:
			comb = 2 + max(p1,p2)/100 + min(p1,p2)/10000
			break
	#Сет
	for n in max_low:
		if numbers.count(n) >= 3:
			comb = 3 + n/100
			break
	#Стрит
	max_l = sorted(list(set(max_low)))
	max_l.reverse()
	for i in range(len(cards)):
		try:
			if max_l[i] == max_l[i+1]+1 and max_l[i+1] == max_l[i+2]+1 and max_l[i+2] == max_l[i+3]+1 and max_l[i+3] == max_l[i+4]+1:
				comb = 4 + max_l[i]/100
				break
		except:
			pass
	#Флеш
	for color in colors:
		if colors.count(color) >= 5:
			crds = cards.copy()
			nums = []
			for c in crds:
				if c[1] != color:
					crds.remove(c)
				else:
					nums.append(c[0])
			comb = 5 + (max(nums))/100
			break
	#Фулл хаус
	two = 0
	three = 0
	for n in max_low:
		if numbers.count(n) >= 3:
			three = n
		elif numbers.count(n) >= 2:
			two = n
		if two != 0  and three != 0:
			comb = 6 + three/100 + two/10000
			break

	#Каре
	for n in max_low:
				if numbers.count(n) >= 4:
					comb = 7 + n/100
					break
	#Стрит флеш
	for j in range(4):
		max_l = []
		for c in cards:
			if c[1] == j + 1:
				max_l.append(c[0])
		max_l = sorted(max_l)
		max_l.reverse()
		for i in range(len(max_l)):
			try:
				if max_l[i] == max_l[i+1]+1 and max_l[i+1] == max_l[i+2]+1 and max_l[i+2] == max_l[i+3]+1 and max_l[i+3] == max_l[i+4]+1:
					if max_l[i] == 14:
						comb = 9 + max_l[i]/100
					else:
						comb = 8 + max_l[i]/100
					break

			except:
				pass
	return comb

def check_all(bot, user_id):
	db = bot.db
	for key in db.keys():
		struct = unpack(db[key])
		gametype = struct['type']
		players = struct['players']
		if key == user_id or user_id in players:
			if gametype == 'dungeon':
				return 'Ты в данже бля'
			elif gametype == 'boss':
				return 'Ты на забиве бля'
			elif gametype == 'battle':
				return 'Ты на арене бля'
			elif gametype == 'poker':
				return 'Ты играешь в покер бля'
			elif gametype == 'papers':
				return 'Ты на заводе бля'
	return None
	
def add_to_dead(cursor,nam,reason):
	if nam == 'Некодевочка' or nam == 'Некомальчик':
		cursor.execute(f"INSERT INTO dead (name,time,reason) VALUES ('Безымянная могила', {int(time.time())}, '{reason}')")
	else:
		cursor.execute(f"INSERT INTO dead (name,time,reason) VALUES (?, {int(time.time())}, '{reason}')", nam)

def kill_neko(cursor,idk,gender,newphot,nam,baza,chat,reason):
	if gender == 0:
		newnam = 'Некодевочка'
	else:
		newnam = 'Некомальчик'
	add_to_dead(cursor,nam,reason)
	kormit = int(time.time() + KORMIT_TIMEOUT + 5400)
	gulat = int(time.time() + GULAT_TIMEOUT + 5400)
	cursor.execute(f"UPDATE neko SET new_phot = NULL, happy = 0, kormit = {kormit}, gulat = {gulat}, name = '{newnam}', gifka = NULL, licension = 0, gladit = 0,photo = '{newphot}',event = 0 WHERE id = {idk}")
		
def get_hp(equipped):
	if (equipped % 100) == 0:
		return 4
	elif equipped > 300:
		return 8
	elif equipped > 200:
		return 6
	elif equipped > 100:
		return 5
		
def minus_durability(equipped):
	if (equipped % 100) == 0:
		return equipped
	else:
		equipped -= 1
		return equipped
		
def map_text(mas):
	ceils = ['◼️','▫️','🟥','🟢','🟩','🟧','❌']
	txt = ''
	for i in range(13):
		for j in range(10):
			txt += ceils[mas[i][j]]
		txt += '\n'
	return txt
	
def send_gulat_message(bot,event,nam,baza,chat,gender):
	markup = types.InlineKeyboardMarkup(row_width=3)
	ps = '\n\n<i>Выбери действие</i>'
	if event == 0:
		return
	elif event == 1:
		switch_button1 = types.InlineKeyboardButton(text='Отдать 😔', switch_inline_query_current_chat = "Отдать")
		switch_button2 = types.InlineKeyboardButton(text='Драться 😡', switch_inline_query_current_chat = "Драться")
		markup.add(switch_button1)
		markup.add(switch_button2)
		text = '<b>"Эй, пацан, норм тяночка такая. Одолжишь на пару часиков?"</b> - послышалось сзади. Обернувшись, ты увидел медленно приближающихся гопников. Думать нужно быстро, втсупить в бой или отдать некодевочку?'
		ph = 'AgACAgIAAx0CZQN7rQACLENimg9vCvzViX185G4iP7oGl72XRQACIrwxG0Xf0Eg9-p59YMy7GwEAAwIAA3MAAyQE'
		if gender == 1:
			text = '<b>"Эй, пацан, норм кунчик такой. Одолжишь на пару часиков?"</b> - послышалось сзади. Обернувшись, ты увидел медленно приближающихся гопников. Думать нужно быстро, вступить в бой или отдать некомальчика?'
			ph = 'AgACAgIAAx0CZQN7rQAC1MBjUuUNoGAz-fxdW7ZeYIfUMLbYQQACtNExG0AamErnC56G4DwJHwEAAwIAA3MAAyoE'
	elif event == 2:
		switch_button1 = types.InlineKeyboardButton(text='Открыть ❔', switch_inline_query_current_chat = "Открыть")
		switch_button2 = types.InlineKeyboardButton(text='Уйти 🚶‍♂️', switch_inline_query_current_chat = "Уйти")
		markup.add(switch_button1)
		markup.add(switch_button2)
		text = 'Прогуливаясь, вы заметили странную коробку посреди дороги. ' + nam + ' сразу же предложила открыть её. На самом деле, тебе и самому интересно что там внутри'
		if gender == 1:
			text = 'Прогуливаясь, вы заметили странную коробку посреди дороги. ' + nam + ' сразу же предложил открыть её. На самом деле, тебе и самому интересно что там внутри'
		ph = 'AgACAgIAAx0CZQN7rQACoJpiwc-XmJW9JlazZ9GQkiyni6DQfgACVbsxGxyOEUozV-1wOZ04sAEAAwIAA3MAAykE'
	elif event == 3:
		switch_button1 = types.InlineKeyboardButton(text='Вискас 🍫', switch_inline_query_current_chat = "Вискас")
		switch_button2 = types.InlineKeyboardButton(text='Монстр ⚡️', switch_inline_query_current_chat = "Монстр")
		switch_button3 = types.InlineKeyboardButton(text='Коробка 📦', switch_inline_query_current_chat = "Коробка")
		switch_button4 = types.InlineKeyboardButton(text='Уйти 🚶‍♂️', switch_inline_query_current_chat = "Уйти")
		markup.add(switch_button1,switch_button2,switch_button3)
		markup.add(switch_button4)
		text = '<b>"Whiskas, monster, nekogirls - you want it? Its yours, my friend, as long as you have enough nekogrivnas"</b> - услышали вы, заходя в ничем не примечательный ларёк. Ты с детства знаешь это место, ведь здесь продают бухло без паспорта, но на этот раз вы пришли не за этим\n\nМожно взглянуть на товары:\nВискас  —  25 💰\nМонстр  —  30 💰\nКоробка  —  40 💰'
		ph = 'AgACAgIAAx0CZQN7rQACoh9ixOhAIbV7nzzHybTYBoJOkG2hGAACgb4xGzBhKEomCoej8lEPzgEAAwIAA3MAAykE'
	elif event == 4:
		switch_button1 = types.InlineKeyboardButton(text='Купить 💸', switch_inline_query_current_chat = "Купить")
		switch_button2 = types.InlineKeyboardButton(text='Назад ❌', switch_inline_query_current_chat = "Назад")
		markup.add(switch_button1)
		markup.add(switch_button2)
		text = 'Да это же целый мешок вискаса 🍫! ' + nam + ' облизывается смотря на него. Этого хватит раза на четыре точно\n\nСтоимость:  25 некогривен 💰'
		if baza >= 7:
			text = 'Да это же целый мешок вискаса 🍫! ' + nam + ' облизывается смотря на него. Этого хватит раз на пять точно\n\nСтоимость:  25 некогривен 💰'
		ph = 'AgACAgIAAx0CZQN7rQACoiNixPAzHZnqNOrRhTGCLWbDzhdI8QAChr4xGzBhKErbwYUmB-YY7gEAAwIAA3MAAykE'
	elif event == 5:
		switch_button1 = types.InlineKeyboardButton(text='Купить 💸', switch_inline_query_current_chat = "Купить")
		switch_button2 = types.InlineKeyboardButton(text='Назад ❌', switch_inline_query_current_chat = "Назад")
		markup.add(switch_button1)
		markup.add(switch_button2)
		text = 'Розовые монстры ⚡️ - единственное топливо, подходящее твоему некомобилю 🚘. Ничего не подумай, пить их тоже никто не запрещал\n\nСтоимость:  30 некогривен 💰'
		ph = 'AgACAgIAAx0CZQN7rQACoiVixPeSb0E1O4DOFDnx_KZt2KHongACjr4xGzBhKEr2G-QRjbdbnQEAAwIAA3MAAykE'
	elif event == 6:
		switch_button1 = types.InlineKeyboardButton(text='Купить 💸', switch_inline_query_current_chat = "Купить")
		switch_button2 = types.InlineKeyboardButton(text='Назад ❌', switch_inline_query_current_chat = "Назад")
		markup.add(switch_button1)
		markup.add(switch_button2)
		if gender == 0:
			text = 'Уникальный в своём роде товар, коробка с некодевочкой 🐱. В ней может оказаться кто угодно, но результат точно тебя не разочарует\n\nСтоимость:  40 некогривен 💰'
		else:
			text = 'Уникальный в своём роде товар, коробка с некомальчиком 🐱. В ней может оказаться кто угодно, но результат точно тебя не разочарует\n\nСтоимость:  40 некогривен 💰'
		ph = 'AgACAgIAAx0CZQN7rQACoidixPqDuXC6Re6KtTl1Ma87jDMoPgACkL4xGzBhKEremTk6cCni0AEAAwIAA3MAAykE'
	elif event == 7:
		switch_button1 = types.InlineKeyboardButton(text='Откупиться 💸', switch_inline_query_current_chat = "Откупиться")
		switch_button2 = types.InlineKeyboardButton(text='Показать 👀', switch_inline_query_current_chat = "Показать")
		markup.add(switch_button1)
		markup.add(switch_button2)
		text = '<b>"Молодой человек, будьте любезны, покажите лицензию на некодевочку"</b> - обратились к тебе. Ничего необычного, просто до тебя решили доебаться менты. К счастью, лицензию 🎫 ты не забыл. Но стоит ли её показывать? Можно попытаться предложить 15 некогривен'
		if gender == 1:
			text = '<b>"Молодой человек, будьте любезны, покажите лицензию на некомальчика"</b> - обратились к тебе. Ничего необычного, просто до тебя решили доебаться менты. К счастью, лицензию 🎫 ты не забыл. Но стоит ли её показывать? Можно попытаться предложить 15 некогривен'
		ph = 'AgACAgIAAx0CZQN7rQACy85jH3o2r1Pxxh53bkPNRvxmMXG6TgACvb0xGzWj-UgBumfJ3Ov7wQEAAwIAA3MAAykE'
	elif event == 8:
		switch_button1 = types.InlineKeyboardButton(text='Адреналин 💪', switch_inline_query_current_chat = "Адреналин")
		switch_button2 = types.InlineKeyboardButton(text='Gender changer 🏳️‍🌈', switch_inline_query_current_chat = "Gender changer")
		switch_button4 = types.InlineKeyboardButton(text='Уйти 🚶‍♂️', switch_inline_query_current_chat = "Уйти")
		markup.add(switch_button1,switch_button2)
		markup.add(switch_button4)
		text = 'Зайдя в переулок, вы увидели бездомную некодевочку, роющуюся в мусорном баке. Завидев вас, она подпрыгнула и взволнованно заговорила: <b>"Ня, дайте покушать, а я вам блестяшки, ня"</b>. Похоже, она плохо знает человеческий язык. Некодевочка держит в руках странные вещи, найденные на свалке\n\nМожно взглянуть на товары:\nАдреналин  —  5 🍫\nGender changer  —  10 🍫'
		ph = 'AgACAgIAAx0CZQN7rQAC00ljS2wxdGuJbyZKRPFIhwptU9xbIwACa8AxG7RRWUp-23IUrAnepQEAAwIAA3MAAyoE'
	elif event == 9:
		markup = types.InlineKeyboardMarkup()
		switch_button1 = types.InlineKeyboardButton(text='Купить 💸', switch_inline_query_current_chat = "Купить")
		switch_button2 = types.InlineKeyboardButton(text='Назад ❌', switch_inline_query_current_chat = "Назад")
		markup.add(switch_button1)
		markup.add(switch_button2)
		text = 'Не может быть, это совершенно новая банка АДРЕНАЛИНА! Выпив его, ' + nam + ' определённо сможет стать сильнее\n\nСтоимость:  5 вискаса 🍫'
		ph = 'AgACAgIAAx0CZQN7rQAC00djS1wDLAyjAAESNb1iCMbnFm82jQIAAhHAMRu0UVlKwksUd0cuhScBAAMCAANzAAMqBA'
	elif event == 10:
		switch_button1 = types.InlineKeyboardButton(text='Купить 💸', switch_inline_query_current_chat = "Купить")
		switch_button2 = types.InlineKeyboardButton(text='Назад ❌', switch_inline_query_current_chat = "Назад")
		markup.add(switch_button1)
		markup.add(switch_button2)
		text = 'Кто вообще это выкинул? Не вдаваясь в подробности работы устройства, cкажу лишь, что оно превращает некодевочек в некомальчиков и наоборот. Действительно, удивительная вещь\n\nСтоимость:  10 вискаса 🍫'
		ph = 'AgACAgIAAx0CZQN7rQAC00VjS1vzWZ5Yu_jq-nrUCUZwdZlMZAACEMAxG7RRWUqecoNnqMqp6QEAAwIAA3MAAyoE'
	elif event == 11:       
		switch_button1 = types.InlineKeyboardButton(text='Приложить 🎫', switch_inline_query_current_chat = "Приложить")
		switch_button2 = types.InlineKeyboardButton(text='Уйти 🚶‍♂️', switch_inline_query_current_chat = "Уйти")
		markup.add(switch_button1)
		markup.add(switch_button2)
		text = 'Вы забрели в парк, где возле лавочки стоял подозрительный торговый автомат. Если верить надписи, он выдаёт бесплатный косяк каждому владельцу некодевочки, достаточно просто приложить лицензию 🎫 к сканеру. Почему-то выглядит как наебалово'
		if gender == 1:
			text = 'Вы забрели в парк, где возле лавочки стоял подозрительный торговый автомат. Если верить надписи, он выдаёт бесплатный косяк каждому владельцу некомальчика, достаточно просто приложить лицензию 🎫 к сканеру. Почему-то выглядит как наебалово'
		ph = 'AgACAgIAAx0CZQN7rQABAX7_ZNQ2rFDlxRzvMyobhb1OEfuXC-QAAvnKMRsMUalKaRQHS_543gwBAAMCAANzAAMwBA'
	bot.send_photo(chat,photo = ph,caption = text + ps,reply_markup=markup)
	
def pvp_text(nam1,nam2,maxhp1,maxhp2,hp1,hp2,blocks1,blocks2,skills1,skills2):
	txt = nam1 + '\n[ '
	i = 1
	while i <= maxhp1:
		if (i <= hp1):
			txt = txt + '🟩'
		else:
			txt = txt + '🟥'
		i = i + 1
	txt = txt + ' ]  '
	if blocks1 > 0:
		for i in range(blocks1):
			txt = txt + '🛡 '
	if 8 in skills1:
			txt = txt + '☘️ ☘️ '
	if 88 in skills1:
			txt = txt + '☘️ '
	if 6 in skills1:
			txt = txt + '✝️ '
	txt = txt + '\n\n'
	txt = txt + nam2 + '\n[ '
	i = 1
	while i <= maxhp2:
		if i <= hp2:
			txt = txt + '🟩'
		else:
			txt = txt + '🟥'
		i = i + 1
	txt = txt + ' ]  '
	if blocks2 > 0:
		for i in range(blocks2):
			txt = txt + '🛡 '
	if 8 in skills2:
		txt = txt + '☘️ ☘️ '
	if 88 in skills2:
		txt = txt + '☘️ '
	if 6 in skills2:
		txt = txt + '✝️ '
	txt = txt + '\n\n'
	return txt
	
def pve_text(enemies,nam,hp,maxhp,blocks,skills):
	txt = ''
	for enemy in enemies:
		if enemy['id'] == 0:
			continue
		txt += enemy['name'] + '\n[ '
		i = 1
		while i <= enemy['maxhp']:
			if (i <= enemy['hp']):
				txt += '🟩'
			else:
				txt += '🟥'
			i = i + 1
		txt += ' ]\n'
		
	txt += '\n' + nam + '\n[ '
	i = 1
	while i <= maxhp:
		if i <= hp:
			txt += '🟩'
		else:
			txt += '🟥'
		i = i + 1
	txt += ' ]  '
	if blocks > 0:
		for i in range(blocks):
			txt += '🛡 '
	if 8 in skills:
		txt += '☘️ ☘️ '
	if 88 in skills:
		txt += '☘️ '
	if 6 in skills:
		txt += '✝️ '
	txt += '\n\n'
	return txt

def boss_text(enemies,name,poisoned,hp,maxhp,blocks,skills,player):
	txt = ''
	for enemy in enemies:
		if enemy['id'] == 0:
			continue
		if enemy['maxhp'] == 0:
			txt += enemy['name'] + '\n'
		else:    
			txt += enemy['name'] + '\n[ '
			for j in range(enemy['maxhp']):
				if j < enemy['hp']:
					txt += '🟩'
				else:
					txt += '🟥'
			txt += ' ]\n'
	txt += f'\n<a href="tg://user?id={player}">{name}</a>' + '\n[ '
	if poisoned:
		hpsym = '🟪'
	else:
		hpsym = '🟩'
	for j in range(maxhp):
		if j < hp:
			txt += hpsym
		else:
			txt += '🟥'
	txt += ' ]  '
	for j in range(blocks):
		txt += '🛡 '
	if 8 in skills:
		txt += '☘️ ☘️ '
	if 88 in skills:
		txt += '☘️ '
	if 6 in skills:
		txt += '✝️ '
	txt += '\n\n'
	return txt
   
def hp_bar(nam,maxhp,hp):
	txt = '\n\n' + nam + '\n[ '
	i = 1
	while i <= maxhp:
		if (i <= hp):
			txt = txt + '🟩'
		else:
			txt = txt + '🟥'
		i = i + 1
	txt = txt + ' ] '
	return txt

def boss_hp_bar(all_name,all_hp,all_maxhp):
	txt = ''
	for i in range(len(all_name)):
		txt += hp_bar(all_name[i],all_maxhp[i],all_hp[i])
	return txt  

def poker_text(players,names,bank,turn,pos,money):
	txt = ''
	for i in range(len(players)):
		txt += f"{names[i]}  {bank[i]} 💰 / {money[i]} 💰\n"
	txt += '\nХод <a href="tg://user?id='+str(turn)+'">'+str(names[pos])+'</a>'
	return txt

def poker_join_keyboard(idk):
	keyboard = types.InlineKeyboardMarkup(row_width=2)
	callback_button1 = types.InlineKeyboardButton(text = 'Присоединиться ➕',callback_data = f'pjoin {idk}')
	callback_button2 = types.InlineKeyboardButton(text = 'Старт ✅',callback_data = f'pstart {idk}')
	callback_button3 = types.InlineKeyboardButton(text = 'Отмена ❌',callback_data = f'pend {idk}')
	keyboard.add(callback_button1)
	keyboard.add(callback_button2,callback_button3)
	return keyboard

def poker_image(cards,event):
	with Image.open('bot/poker/table.png') as im1, Image.open('bot/poker/cardback.png') as im2:
		for i in range(5):
			a = cards[i][0]
			b = cards[i][1]
			if i > event:
				im1.paste(im2.convert('RGB'), (82+i*215,203), im2)
			else:
				with Image.open(f"bot/poker/{a}_{b}.png") as crop:
					im1.paste(crop.convert('RGB'), (82+i*215,203), crop)
	return send_pil(im1)
	
def answer_callback_query(bot,call,txt,show = False):
	try:
		bot.answer_callback_query(call.id,text = txt,show_alert = show)
	except:
		if show:
			try:
				bot.send_message(call.from_user.id, text = txt)
			except:
				pass

def generate_field(skills):
	field = []
	b = [0,1,2,3,4]
	if 2 in skills:
		b.append(2)
	if 3 in skills:
		b.append(4)
	for i in range(36):
		s = random.choice(b)
		field.append(s)
	field_calculate(field,skills,False)
	return field

def field_keyboard(keyboard,dat,field,rer1,rer2,skills,selected = -1):
	stack = []
	sym = ['🟥','🟧','🟡','🟢','💙','⭐️','🦴']
	sym_white = ['⬜️','⬜️','⚪️','⚪️','🤍','🌟','☠️']
	for i in range(36):
		if selected == i:
			txt = sym_white[field[i]]
		else:
			txt = sym[field[i]]
		callback_button = types.InlineKeyboardButton(text = txt,callback_data = dat + ' ' + str(i) + ' ' + str(rer1) + ' ' + str(rer2))
		stack.append(callback_button)
		if len(stack) == 6:
			keyboard.add(stack[0],stack[1],stack[2],stack[3],stack[4],stack[5])
			stack = []
	keybd = []
	if skills[0] > 100 and rer1 == 1:
		reroll = types.InlineKeyboardButton(text = skill_names[skills[0]-100],callback_data = dat + ' ' + str(-skills[0]) + ' ' + str(0) + ' ' + str(rer2))
		keybd.append(reroll)
	if skills[1] > 100 and rer2 == 1:
		reroll = types.InlineKeyboardButton(text = skill_names[skills[1]-100],callback_data = dat + ' ' + str(-skills[1]) + ' ' + str(rer1) + ' ' + str(0))
		keybd.append(reroll)
	if len(keybd) > 0:
		keyboard.add(*keybd)
		
def dungeon_keyboard(keyboard,idk):
	callback_button1 = types.InlineKeyboardButton(text = '⬆️',callback_data = 'move ' + str(idk) + ' 1 ')
	callback_button2 = types.InlineKeyboardButton(text = '⬅️',callback_data = 'move ' + str(idk) + ' 4 ')
	callback_button3 = types.InlineKeyboardButton(text = '⏺',callback_data = 'nothing')
	callback_button4 = types.InlineKeyboardButton(text = '➡️',callback_data = 'move ' + str(idk) + ' 2 ')
	callback_button5 = types.InlineKeyboardButton(text = '⬇️',callback_data = 'move ' + str(idk) + ' 3 ')
	callback_button6 = types.InlineKeyboardButton(text = 'Уйти 🔚',callback_data = 'back ' + str(idk))
	keyboard.add(callback_button1,callback_button5,callback_button2,callback_button4)
	keyboard.add(callback_button6)
	
def target_keyboard(keyboard,targ,dat,rer1,rer2):
	if targ == 0:
		target1 = types.InlineKeyboardButton(text = '[Выбрано]',callback_data = 'nothing')
	else:
		target1 = types.InlineKeyboardButton(text = 'Цель 1 ⚔️',callback_data = dat + ' ' + str(-200) + ' ' + str(rer1) + ' ' + str(rer2))
	if targ == 1:
		target2 = types.InlineKeyboardButton(text = '[Выбрано]',callback_data = 'nothing')
	else:
		target2 = types.InlineKeyboardButton(text = 'Цель 2 ⚔️',callback_data = dat + ' ' + str(-201) + ' ' + str(rer1) + ' ' + str(rer2))
	if targ == 2:
		target3 = types.InlineKeyboardButton(text = '[Выбрано]',callback_data = 'nothing')
	else:
		target3 = types.InlineKeyboardButton(text = 'Цель 3 ⚔️',callback_data = dat + ' ' + str(-202) + ' ' + str(rer1) + ' ' + str(rer2))
	keyboard.add(target1,target2,target3)

def poker_keyboard(balance,r,idk,turn,pos,money,bank,islastbet,players,base_bet):
	keyboard = types.InlineKeyboardMarkup(row_width=3)
	if r == 1 and balance:
		callback_button1 = types.InlineKeyboardButton(text = '🆗 Пропуск',callback_data = 'poker ' + str(idk) + ' ' + str(turn) + ' ' + str(pos) + ' 1 ' + str(r))
	else:
		callback_button1 = types.InlineKeyboardButton(text = '🛑 Хуй',callback_data = 'nothing')
	callback_button2 = types.InlineKeyboardButton(text = '❌ Сдаться',callback_data = 'poker ' + str(idk) + ' ' + str(turn) + ' ' + str(pos) + ' 2 ' + str(r))
	if balance:
		minbet = base_bet
		symbol = '⏫'
		action = 4
	else:
		minbet = max(bank) - bank[pos]
		symbol = '⏺'
		action = 3
	#МИН СТАВКА
	if money[pos] < bank[pos] + minbet:
		bet = money[pos] - bank[pos]
		callback_button4 = types.InlineKeyboardButton(text = f'{symbol}  {bet} 💰',callback_data = 'poker ' + str(idk) + ' ' + str(turn) + ' ' + str(pos) + f' {action} ' + str(r) + ' ' + str(bet))
	else:
		callback_button4 = types.InlineKeyboardButton(text = f'{symbol}  {minbet} 💰',callback_data = 'poker ' + str(idk) + ' ' + str(turn) + ' ' + str(pos) + f' {action} ' + str(r) + ' ' + str(minbet))
	#МАКС СТАВКА х2
	if money[pos] <= bank[pos] + minbet or islastbet:
		callback_button5 = types.InlineKeyboardButton(text = '🛑 Хуй',callback_data = 'nothing')
	elif money[pos] < bank[pos] + 2*minbet:
		bet = money[pos] - bank[pos]
		callback_button5 = types.InlineKeyboardButton(text = f'⏫  {bet} 💰',callback_data = 'poker ' + str(idk) + ' ' + str(turn) + ' ' + str(pos) + ' 4 ' + str(r) + ' ' + str(bet))
	else:
		callback_button5 = types.InlineKeyboardButton(text = f'⏫  {2*minbet} 💰',callback_data = 'poker ' + str(idk) + ' ' + str(turn) + ' ' + str(pos) + ' 4 ' + str(r) + ' ' + str(2*minbet))
	#МАКС СТАВКА х3
	if money[pos] <= bank[pos] + 2*minbet or islastbet:
		callback_button6 = types.InlineKeyboardButton(text = '🛑 Хуй',callback_data = 'nothing')
	elif money[pos] < bank[pos] + 4*minbet:
		bet = money[pos] - bank[pos]
		callback_button6 = types.InlineKeyboardButton(text = f'⏫  {bet} 💰',callback_data = 'poker ' + str(idk) + ' ' + str(turn) + ' ' + str(pos) + ' 4 ' + str(r) + ' ' + str(bet))
	else:
		callback_button6 = types.InlineKeyboardButton(text = f'⏫  {4*minbet} 💰',callback_data = 'poker ' + str(idk) + ' ' + str(turn) + ' ' + str(pos) + ' 4 ' + str(r) + ' ' + str(4*minbet))
	callback_button3 = types.InlineKeyboardButton(text = '🃏 Карты в руке',callback_data = 'hand ' + str(idk) + ' ' + str(turn) + ' ' + str(pos))
	keyboard.add(callback_button1,callback_button2)
	keyboard.add(callback_button4,callback_button5,callback_button6)
	keyboard.add(callback_button3)
	return keyboard

def use_skill(bot,ability,selected,call,field):
	turns = 0
	blocks = 0
	atack = 0
	if ability == 101:
		if selected == -1:
			answer_callback_query(bot,call,'Сначала выбери фигуру')
			return [-1,0,0,0]
		if field[selected] == 5:
			answer_callback_query(bot,call,'Это уже звезда')
			return [-1,0,0,0]
		field[selected] = 5
	elif ability == 102:
		if selected == -1:
			answer_callback_query(bot,call,'Сначала выбери фигуру')
			return [-1,0,0,0]
		field[selected] = -1
	elif ability == 103:
		random.shuffle(field)
	elif ability == 104:
		turns = -1
		atack = 1
	elif ability == 105:
		turns = -1
		blocks = 1
	elif ability == 106:
		for x in field:
			if x == 5:
				answer_callback_query(bot,call,'На поле уже есть звезды')
				return [-1,0,0,0]
		a1 = random.randint(0,35)
		a2 = random.randint(0,35)
		while a1 == a2 or field[a1] == 5 or field[a2] == 5:
			a1 = random.randint(0,35)
			a2 = random.randint(0,35)
		field[a1] = 5
		field[a2] = 5
	elif ability == 107:
		if selected == -1:
			answer_callback_query(bot,call,'Сначала выбери фигуру')
			return [-1,0,0,0]
		if field.count(field[selected]) < 11:
			answer_callback_query(bot,call,'Недостаточно фигур')
			return [-1,0,0,0]
		figa = field[selected]
		for i in range(36):
			if field[i] == figa:
				field[i] = -1
		if figa == 0 or figa == 1:
			blocks = 1
		elif figa == 2 or figa == 3:
			atack = 1
		elif figa == 4:
			turns = 1
	elif ability == 108:
		if selected == -1:
			answer_callback_query(bot,call,'Сначала выбери фигуру')
			return [-1,0,0,0]
		res = math.ceil(selected/6 + 0.1)
		for i in range((res-1)*6,res*6):
			field[i] = -1
	elif ability == 109:
		if selected == -1:
			answer_callback_query(bot,call,'Сначала выбери фигуру')
			return [-1,0,0,0]
		if field[selected] != 5:
			answer_callback_query(bot,call,'Это не звезда')
			return [-1,0,0,0]
		field[selected] = -1
		turns = 1
	elif ability == 110:
		if selected == -1:
			answer_callback_query(bot,call,'Сначала выбери фигуру')
			return [-1,0,0,0]
		figa = field[selected]
		if figa == 5:
			answer_callback_query(bot,call,'Со звездами не работает')
			return [-1,0,0,0]
		a1 = random.randint(0,35)
		a2 = random.randint(0,35)
		while a1 == a2 or field[a1] == figa or field[a2] == figa:
			a1 = random.randint(0,35)
			a2 = random.randint(0,35)
		field[a1] = figa
		field[a2] = figa
	answer_callback_query(bot,call,'Использовано')
	return [1,atack,blocks,turns]
	
def change_figures(bot,selected,pos,call,field):
	if selected == -1:
		answer_callback_query(bot,call,'Выбрано')
		selected = pos
		return [-1,selected]
	if selected == pos:
		answer_callback_query(bot,call,'Выбор отменен')
		selected = -1
		return [-1,selected]
	d = selected - pos
	if d != 1 and d != -1 and d != 6 and d != -6:
		answer_callback_query(bot,call,'Выбор изменен')
		selected = pos
		return [-1,selected]
	if field[pos] == field[selected]:
		answer_callback_query(bot,call,'Клетки одинаковые, выбор отменен')
		selected = -1
		return [-1,selected]
	d = field[pos]
	field[pos] = field[selected]
	field[selected] = d
	answer_callback_query(bot,call,'Меняю...')
	return [1]

def change_target(bot,ability,targ,call,enemies):
	newtarg = ability - 200
	if newtarg == targ:
		answer_callback_query(bot,call,'Эта цель уже выбрана')
		return -1
	if enemies[newtarg]['id'] == 0:
		answer_callback_query(bot,call,'На этой позиции никого нет')
		return -1
	answer_callback_query(bot,call,'Меняю цель')
	return newtarg

def bone_atack(field,bone_count):   
	bones = []
	for i in range(bone_count):
		bones.append(random.randint(0,35))
	while True:
		found = False
		for bone in bones:
			if bones.count(bone) > 1 or field[bone] == 6:
				found = True
				break
		if not found:
			break
			
		bones = []
		for i in range(bone_count):
			bones.append(random.randint(0,35))
	
	for bone in bones:
		field[bone] = 6
	field_calculate(field,[],False)
	
def player_atack(enemies,targ,turns,atack,splash):
			if atack <= 0:
				return turns
			for i in range(3):
				if not splash and targ != i:
					continue
				if enemies[i]['dodge']:
					enem_hp = enemies[i]['hp']
					enem_maxhp = enemies[i]['maxhp']
					enem_id = enemies[i]['id']
					enemies[i] = enemy_list[enem_id+1].copy()
					enemies[i]['hp'] = enem_hp
					enemies[i]['maxhp'] = enem_maxhp
				else:
					enemies[i]['hp'] -= atack

				if enemies[i]['hp'] <= 0:
					enem_id = enemies[i]['deathspawn']
					turns += enemies[i]['deathturns']
					enemies[i] = enemy_list[enem_id].copy()
			return turns
			
def change_zero_target(targ,enemies):
	if enemies[targ]['id'] == 0:
		for i in range(3):
			if enemies[i]['id'] != 0:
				targ = i
				break
	return targ
	
def use_player_defence(skills,enemy_atack,blocks,hp,nodef):  
			if enemy_atack <= 0:
				return hp,blocks 
			do_dmg = 5
			if 8 in skills or 88 in skills:
				do_dmg = random.randint(1,5)
			if do_dmg != 1:
				if nodef:
					hp -= enemy_atack
				elif blocks >= enemy_atack:
					blocks -= enemy_atack
				else:
					enemy_atack -= blocks
					blocks = 0
					hp -= enemy_atack
			else:
				if 8 in skills:
					skills.remove(8)
					skills.append(88)
				elif 88 in skills:
					skills.remove(88)
					skills.append(0)        
				  
			if hp <= 0:
				if 6 in skills:
					skills.remove(6)
					skills.append(0)
					hp = 1
					
			return hp,blocks  

def sum_enemies_hp(enemies):
	sumhp = 0
	for enemy in enemies:
		if enemy['maxhp'] != 0 and enemy['id'] != 0:
			sumhp += enemy['hp']
	return sumhp
	
def get_player_turns(skills,hpbal,turns):
	if 7 in skills:
		turns = 4
		skills.remove(7)
		skills.append(0)
	if 9 in skills and hpbal:
		turns += 1
	return turns  

def get_player_damage(skills,hp,maxhp,atack,turns,blocks):
	if 5 in skills and hp == maxhp and atack != 0:
		atack += 1
	if 4 in skills and hp <= 2 and atack != 0:
		atack += 1
	if 10 in skills and turns == 0 and atack != 0 and blocks == 0:
		atack += 1
	return atack
	
def zakup_buy_keyboard(keyboard,idk):
	callback_button1 = types.InlineKeyboardButton(text = '🧃',callback_data = f'buy {idk} 0')
	callback_button2 = types.InlineKeyboardButton(text = '🍕',callback_data = f'buy {idk} 1')
	#callback_button3 = types.InlineKeyboardButton(text = '🧨',callback_data = f'buy {idk} 2')
	callback_button4 = types.InlineKeyboardButton(text = 'Продолжить ⏩',callback_data = f'bcontinue {idk}')
	#callback_button5 = types.InlineKeyboardButton(text = 'Куплено ☑️',callback_data = f'nothing')
	keyboard.add(callback_button1,callback_button2)
	keyboard.add(callback_button4)

def all_cards_text(cards):
	if len(cards) == 0:
		return ''
	colors = ['♦️','♥️','♠️','♣️']
	numbers = ['J','Q','K','A']
	txt = "Карты на столе:\n"
	for x in cards:
		a = x[0]
		b = x[1]
		if a > 10:
			a = numbers[a-11]
		txt += colors[b-1] + str(a) + '   '
	txt += '\n'
	return txt	

def card_text(hand):
	txt = ''
	colors = ['♦️','♥️','♠️','♣️']
	numbers = ['J','Q','K','A']
	a = hand[0][0]
	b = hand[0][1]
	if a > 10:
		a = numbers[a-11]
	txt += colors[b-1] + str(a) + '   '
	a = hand [1][0]
	b = hand [1][1]
	if a > 10:
		a = numbers[a-11]
	txt += colors[b-1] + str(a) + '\n'
	return txt
	
def boss_choose_player(pindex,all_hp):
				pindex += 1
				while pindex != len(all_hp) and (all_hp[pindex] <= 0):
					pindex += 1
				if pindex == len(all_hp):
					pindex = -1
				return pindex
				
def zakup_use_keyboard(keyboard,zakup,dat,rer1,rer2,item_use):
	if len(zakup) == 0 or item_use == 0:
		return
	callback_button1 = types.InlineKeyboardButton(text = 'Растш 🧃',callback_data = dat + ' ' + str(-300) + ' ' + str(rer1) + ' ' + str(rer2))
	callback_button2 = types.InlineKeyboardButton(text = 'Питса 🍕',callback_data = dat + ' ' + str(-301) + ' ' + str(rer1) + ' ' + str(rer2))
	callback_button3 = types.InlineKeyboardButton(text = 'Корср 🧨',callback_data = dat + ' ' + str(-302) + ' ' + str(rer1) + ' ' + str(rer2))
	keybd = []
	butlist = [callback_button1,callback_button2,callback_button3]
	for z in zakup:
		keybd.append(butlist[z])
	keyboard.add(*keybd)
		
def check_alive(all_hp):
				found = False
				for hp in all_hp:
					if hp > 0:
						found = True
						break
				return found
			   
def enemies_turn(enemies,i):
				if enemies[i]['id'] == 0:
					return 0
				enemy_atack = enemies[i]['damage']
				if enemies[i]['turnchange'] is not None:
					enem_hp = enemies[i]['hp']
					enem_maxhp = enemies[i]['maxhp']
					turnchange = enemies[i]['turnchange']
					enemies[i] = enemy_list[turnchange].copy()
					enemies[i]['hp'] = enem_hp
					enemies[i]['maxhp'] = enem_maxhp
				return enemy_atack      

def get_happiness_level(happy,baza):
	h = 16
	if baza >= 3:
		h = 22 
	if happy <= h*3600:
		return 0
	elif happy <= h*2*3600:
		return 1
	elif happy <= h*3*3600:
		return 2
	elif happy <= h*4*3600:
		return 3
	else:
		return 4
