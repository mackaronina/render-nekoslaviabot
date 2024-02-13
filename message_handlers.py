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

def msg_text(message,bot):
		cursor = bot.cursor
		db = bot.db
		patch_version = bot.gazeta['patch_version']
		
		message.text = message.text.replace('@NekoslaviaBot','').strip()
		cmd = message.text.lower()
		words = cmd.split()
		first_word = words[0]
		
		if cmd not in cmd_noarg and first_word not in cmd_arg:
			return  
		if flood_counter_plus(bot,message):
			return
			
		data = cursor.execute(f"SELECT * FROM neko WHERE id = {message.from_user.id}")
		data = data.fetchone()
		if data is None:
			if cmd == 'неко':
				p = random.choice(photos)
				kormit = int(time.time())
				gulat = int(time.time() + GULAT_TIMEOUT)
				licension = 0
				happy = int(time.time())
				cursor.execute(f"INSERT INTO neko (id,name,gulat,kormit,photo,licension,happy,photo_licension) VALUES ({message.from_user.id},'Некодевочка',{gulat},{kormit},'{p}',{licension}, {happy}, NULL)")
				
				text = "<b>Некославия</b> - социалистическое государство, которое достигло небывалого развития благодаря мудрому правлению <b>некокинга</b>. Особого прогреса удалось достичь в генной инженерии, был выведен гибрид кошки и человека - некодевочка. Это позволило запустить специальную социальную программу, каждому гражданину полагается своя кошкожена, без очередей и налогов"
				bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQACsJRi4vTvzOG-zrdVRRS3iQhKUm-K_QAC37oxG6IdGEsIcBwLxnaZgwEAAwIAA3MAAykE',caption = text)
				time.sleep(1)
				text = "Твоя заявка на гражданство Некославии была одобрена и, как гражданину, мы выдаём тебе личную кошкожену. Напиши <i><u>неко</u></i> чтобы взглянуть на неё. Помни, что ключ к хорошим отношениям с твоей некодевочкой это <b>доверие 💞</b>. Его можно повысить многими способами, для начала попробуй дать некодевочке поесть командой <i><u>покормить</u></i>, скорее всего она проголодалась пока ехала к тебе. После этого советую придумать ей какую-нибудь пиздатую кличку командой <i><u>имя [текст]</u></i>"
				bot.send_message(message.chat.id, text)
				#bot.send_message(message.chat.id,'Добро пожаловать в Некославию! Каждому гражданину, согласно конституции, полагается некодевочка, держи свою\n\n/cmd - список комманд\n\n/help - полезные ссылки')
				#time.sleep(1)
				#text = 'Надо бы пояснить тебе наши порядки. <b>Некославия</b> - великая держава, а великая держава должна заботиться о благополучии своих гражданах, не так ли? Для этого запущена специальная социальная программа - каждому полагается по некодевочке, без очередей и налогов. К счастью, благодаря новейшим разработкам у нас их достаточно. По закону каждый некослав обязан заботиться о своей некодевочке, а её смерть уголовно наказуема'
				#bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQACsJRi4vTvzOG-zrdVRRS3iQhKUm-K_QAC37oxG6IdGEsIcBwLxnaZgwEAAwIAA3MAAykE',caption = text)
				#time.sleep(1)
				#text = 'А вот и твоя некодевочка. Вероятно, она проголодалась пока ждала тебя. Напиши "неко" чтобы убедиться в этом, а когда покормишь - не забудь дать ей имя'
				#bot.send_photo(message.chat.id, photo = p,caption = text)
				#time.sleep(1)
				#photo_design = 'AgACAgIAAx0CZQN7rQABAicRZSFoSY43lFLhRbyeeXPlv55ekY8AArbPMRvwnghJbqkwodtNPHcBAAMCAAN5AAMwBA' 
				#f = create_licension(bot,p,photo_design,message.from_user.first_name,0)
				#m = bot.send_photo(message.chat.id, photo=f,caption = 'И самое главное, держи лицензию 🎫 на свою некодевочку. Нужно будет продлить её через 4 дня, если не хочешь платить штраф, конечно')
				#cursor.execute(f"UPDATE neko SET photo_licension = '{m.photo[-1].file_id}' WHERE id = {message.from_user.id}")
				return
			else:
				bot.send_message(message.chat.id,'Ты не один из нас, напиши /start чтобы стать некославом ')
				return
		nam = data[1]
		rep = data[2]
		gulat = int(data[3] - time.time())
		kormit = int(data[4] - time.time())
		phot = data[5]
		bolnitsa = int(data[6] - time.time())
		zavod = data[7]
		baza = data[8]
		car = data[9]
		event = data[10]
		coins = data[11]
		ch = data[12]
		gladit = data[13]
		wins = data[14]
		chel = data[15]
		arena_kd = int(data[16] - time.time())
		photo_base = data[17] 
		photo_mobile = data[18]
		dungeon_kd = int(data[19] - time.time())
		debil = data[20]
		photo_debil = data[21]
		automate = data[22]
		licension = int(data[23] - time.time())
		photo_licension = data[24]
		photo_design = data[25]
		version = data[26]
		skill1 = data[27]
		skill2 = data[28]
		gifka = data[29]
		gender = data[30]
		item_one = data[31]
		item_two = data[32]
		new_phot = data[33]
		if new_phot is not None:
			phot = new_phot
		notifed = data[34]
		days = data[35]
		inventory = unpack(data[36])
		bone_automate = data[37]
		equipped = data[38]
		dungeon_raids = data[39]
		base_buy = data[40]
		mobile_buy = data[41]
		licension_buy = data[42]
		boss_raids = data[43]
		boss_kd = int(data[44] - time.time())
		happy = int(time.time() - data[45])
		gladit_kd = int(data[46] - time.time())
		intro_level = data[47]
		
		if ch != message.chat.id:
			ch = message.chat.id
			cursor.execute(f'UPDATE neko SET chat = {ch} WHERE id = {message.from_user.id}')
		if message.from_user.first_name != html.unescape(chel):
			chel = html.escape(message.from_user.first_name, quote = True)
			cursor.execute(f"UPDATE neko SET chel = %s WHERE id = {message.from_user.id}", str(chel))
		if bolnitsa > 0 and cmd not in cmd_allowed_bolnitsa:
			b = math.ceil(bolnitsa/3600)
			bot.send_message(message.chat.id, f'Ты в больнице дебил\n\n<i>Осталось лечиться {b} часов, используй антипохмелин чтобы выйти досрочно</i>')
			bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEKbkNlGcyWsw1T1RXhFZGTgaGzubYD_AACIA8AAg7tWEjVrCd9QwTr1jAE')
			return
		if check_all(bot, message.from_user.id) is not None and cmd not in cmd_allowed_bolnitsa:
			bot.send_message(message.chat.id, f'{check_all(bot, message.from_user.id)}\n\n<i>Эта хуйня закончится автоматически в течении часа или раньше</i>')
			bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEKbkNlGcyWsw1T1RXhFZGTgaGzubYD_AACIA8AAg7tWEjVrCd9QwTr1jAE')
			return
		if event > 0 and cmd not in cmd_allowed_gulat:
			bot.send_message(message.chat.id, 'Ты гуляешь ебанат\n\n<i>Напиши </i><code>повтор</code><i> чтобы повторить сообщение с выбором если ты его проебал</i>')
			bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEKbkNlGcyWsw1T1RXhFZGTgaGzubYD_AACIA8AAg7tWEjVrCd9QwTr1jAE')
			return
		if cmd_events.get(cmd) is not None and event not in cmd_events.get(cmd):
			if event > 0:
				bot.send_message(message.chat.id, 'Такого действия нет\n\n<i>Напиши </i><code>повтор</code><i> чтобы повторить сообщение с выбором если ты его проебал</i>')
				bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEKbkNlGcyWsw1T1RXhFZGTgaGzubYD_AACIA8AAg7tWEjVrCd9QwTr1jAE')
			else:
				bot.send_message(message.chat.id, 'Хуйню сморозил')
			return
		if cmd in blocked_cmd.get(intro_level):
			bot.send_message(message.chat.id, 'Команда недоступна на текущем уровне обучения\n\n<i>Письма приходят только когда ты кормишь некодевочку</i>')
			bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEKbkNlGcyWsw1T1RXhFZGTgaGzubYD_AACIA8AAg7tWEjVrCd9QwTr1jAE')
			return	
		if cmd == 'неко':
			markup = types.InlineKeyboardMarkup()
			switch_button1 = types.InlineKeyboardButton(text='Покормить 🐟', switch_inline_query_current_chat = "Покормить")
			switch_button2 = types.InlineKeyboardButton(text='Выгулять 🚶‍♀️', switch_inline_query_current_chat = "Выгулять")
			switch_button3 = types.InlineKeyboardButton(text='Погладить 🖐', switch_inline_query_current_chat = "Погладить")
			markup.add(switch_button1,switch_button2)
			markup.add(switch_button3) 
			smiles = ['🥰','😊','😐','😠','🤬']
			text = 'Что ж, это твоя личная некодевочка, чем не повод для гордости?\n\n'
			if gender == 1:
				text = 'Что ж, это твой личный некомальчик, чем не повод для гордости?\n\n'
			
			if nam == 'Некодевочка' or nam == 'Некомальчик':
				if gender == 0:
					text += 'У неё нет имени'
				else:
					text += 'У него нет имени'
			else:
				if gender == 0:
					text += 'Её зовут ' + nam
				else:
					text += 'Его зовут ' + nam
			
			if kormit > 0:
				text += '\nПока не хочет есть ❌\n'
			else:
				text += '\nНе откажется от вискаса ✅\n'
			
			if gulat > 0:
				text += 'Пока не хочет гулять ❌\n'
			else:
				if gender == 0:
					text += 'Хотела бы прогуляться ✅\n'
				else:
					text += 'Хотел бы прогуляться ✅\n'
  
			text += f'Доверие 💞:  {rep}\n'
			text += f'Настроение {smiles[get_happiness_level(happy,baza)]}\n'
			if equipped == 0:
				if gender == 0:
					text += 'Голая 👙\n'
				else:
					text += 'Голый 👙\n'
			else:
				item_names = ['👖 Штаны за 40 гривень','👗 Костюм горничной','🦺 Куртку санса']
				item = int(equipped/100) - 1
				durability = equipped%100
				if gender == 0:
					text += f'Одета в {item_names[item]}\nПрочность [{durability}/10]\n'
				else:
					text += f'Одет в {item_names[item]}\nПрочность [{durability}/10]\n'
		   
			s = [skill1,skill2].count(0)
			if s == 2:
				text += 'Лох без навыков 💪\n'
			elif s == 1:
				text += 'Владеет одним навыком 💪\n'
			elif s == 0:
				text += 'Владеет двумя навыками 💪\n'  
			bot.send_photo(message.chat.id,photo=phot,caption=text,reply_markup=markup)
		elif cmd == 'вещи':
			text = 'Это твой инвентарь. Надеюсь, ты сможешь найти всему этому применение\n'
			text += f'\n💰 Некогривны × {coins}'
			if inventory['whiskas'] > 0:
				text += f"\n🍫 Вискас × {inventory['whiskas']}"
			if inventory['monster'] > 0:
				text += f"\n⚡️ Монстр × {inventory['monster']}"
			if inventory['antipohmelin'] > 0:
				text += f"\n🍼 Антипохмелин × {inventory['antipohmelin']}"
			if inventory['bone'] > 0:
				text += f"\n🦴 Кость санса × {inventory['bone']}"
			if inventory['neko_box'] > 0:
				text += f"\n🎁 Коробка с неко × {inventory['neko_box']}"
			if inventory['horny_neko_box'] > 0:
				text += f"\n🎁 Коробка с хорни неко × {inventory['horny_neko_box']}"
			if inventory['loot_box'] > 0:
				text += f"\n🎁 Коробка с украшениями × {inventory['loot_box']}"
			if inventory['gender_changer'] > 0:
				text += f"\n🪚 Gender changer × {inventory['gender_changer']}"
			if inventory['adrenalin'] > 0:
				text += f"\n🗡 Адреналин × {inventory['adrenalin']}"
			if inventory['carton'] > 0:
				text += f"\n📦 Картон × {inventory['carton']}"
			if inventory['armor1'] > 0:
				text += f"\n👖 Штаны за 40 гривень × {inventory['armor1']}"
			if inventory['armor2'] > 0:
				text += f"\n👗 Костюм горничной × {inventory['armor2']}"
			if inventory['armor3'] > 0:
				text += f"\n🦺 Куртка санса × {inventory['armor3']}"
			text = text + '\n\n<code>Использовать [назв]</code><i> - юзнуть указанный предмет. Кости и вискас используются автоматически, данной командой можно отключить это</i>\n\n<code>Донат [назв] [колво]</code><i> - ответом на сообщение передать предметы</i>'
			bot.send_photo(message.chat.id,photo='AgACAgIAAx0CZQN7rQACrNBi2OxzrdcKU1c1LOxqBdGsjRxKDAACn70xG-8HyUoUEuWNwlQYIgEAAwIAA3MAAykE',caption = text)
		elif cmd == 'навыки':
			if skill1 > 100:
				sktxt1 = active_skill_list[skill1-100]
			else:
				sktxt1 = passive_skill_list[skill1]
			if skill2 > 100:
				sktxt2 = active_skill_list[skill2-100]
			else:
				sktxt2 = passive_skill_list[skill2]
			text = 'Это навыки и черты характера, которыми обладает твоя некодевочка. Удивительно, но некодевочки обычно не такие слабые, какими кажутся на первый взгляд, а их когти острее бритвы\n\n' + sktxt1 + '\n' + sktxt2
			if gender == 1:
				text = 'Это навыки и черты характера, которыми обладает твой некомальчик. Удивительно, но некомальчики обычно не такие слабые, какими кажутся на первый взгляд, а их когти острее бритвы\n\n' + sktxt1 + '\n' + sktxt2
			bot.send_photo(message.chat.id,photo='AgACAgIAAx0CZQN7rQACzrBjRJTTrokWxq7HNUPeZWB8hwhOAwACy8AxGzDSKUp1KOI5xNQ4_gEAAwIAA3MAAyoE',caption = text)
		elif cmd == 'гардероб':
			txt = 'В гардеробе хранятся все украшения, которая твоя некодевочка с удовольствием будет носить. Они нихуя не дают, зато прикольно выглядят. Список украшений:\n\n' + item_list[item_one][0] + '\n\n' + item_list[item_two][0]
			if gender == 1:
				txt = 'В гардеробе хранятся все украшения, которая твой некомальчик с удовольствием будет носить. Они нихуя не дают, зато прикольно выглядят. Список украшений:\n\n' + item_list[item_one][0] + '\n\n' + item_list[item_two][0]
			phot = 'AgACAgIAAx0CZQN7rQABAWdRZMl6876A8ERGzlFYkJ-bVOWwFCgAAvHJMRvvxlFK9St6KqJTAn4BAAMCAANzAAMvBA'   
			markup = types.InlineKeyboardMarkup()
			button1 = types.InlineKeyboardButton("Изменить вид ✨", url='http://t.me/NekoslaviaBot/nekoapp')
			markup.add(button1)
			bot.send_photo(message.chat.id,photo=phot,caption = txt, reply_markup=markup)
		elif cmd == 'руководство':
			txt = 'В этом руководстве описаны требования, которым должны соответствовать документы некочанов, чтобы они могли пройти:\n\n<b>1. Фото совпадает с внешностью некочана\n2. Дата выдачи не позже текущей даты\n3. Лицензия не является просроченной (поле "До")\n4. На лицензии стоит печать с надписью "НЕКОСЛАВИЯ"</b>\n\nТакже, в зависимости от обстановки на заводе, могут действовать особые условия пропуска'
			phot = 'AgACAgIAAx0CZQN7rQABAZt2ZOHZT9gKuVk9t_5vb3jnQ37hkcUAAtTKMRsabhFLyhnWQuJEa6IBAAMCAANzAAMwBA'   
			bot.send_photo(message.chat.id,photo=phot,caption = txt)
		elif cmd == 'топ':
			text = 'Питомцы лучших граждан нашей родины, Некославии. Нет, числа это не цена за час, даже не думай об этом\n\n'
			data = cursor.execute(f'SELECT name,rep,wins FROM neko ORDER BY rep DESC LIMIT 10')
			data = data.fetchall()
			i = 0
			if data is not None:
				for d in data:
					n = d[0]
					if n == 'Некодевочка' or n == 'Некомальчик':
						n = 'Безымянная шмара'
					if i == 0:
						text += f'🏆 <b>{n}</b>  {d[1]} 💞\n'
					else:
						text += f'{i+1}.  {n}  {d[1]} 💞\n'
					i += 1
			bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQACn9piwJArenxX-o-B5a2xO7AhvSCTlAAC4LUxG5j7EUkOukwyvavLgQEAAwIAA3MAAykE',caption = text)
		elif cmd == 'топ деньги': 
			text = 'Это некодевочки и некомальчики богатейших граждан Некославии. Когда-нибудь ты станешь одним из них, если, конечно, не будешь проёбывать все деньги в казино\n\n'
			data = cursor.execute(f'SELECT name,coins FROM neko ORDER BY coins DESC LIMIT 10')
			data = data.fetchall()
			i = 0
			if data is not None:
				for d in data:
					n = d[0]
					if n == 'Некодевочка' or n == 'Некомальчик':
						n = 'Безымянная шмара'
					if i == 0:
						text += f'🏆 <b>{n}</b>  {d[1]} 💰\n'
					else:
						text += f'{i+1}.  {n}  {d[1]} 💰\n'
					i += 1
			bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQACw-di9rxFH9TpOzq-NFDEthztPu5QdAACprwxG81SuUuSxydRTDvpogEAAwIAA3MAAykE',caption = text)
		elif cmd == 'погладить':
			if gladit_kd > 0:
				gkd = math.ceil(gladit_kd/3600)
				txt = f'{nam} пока не хочет чтобы её гладили\n\n<i>Осталось ждать {gkd} часов</i>'
				if gender == 1:
					txt = f'{nam} пока не хочет чтобы его гладили\n\n<i>Осталось ждать {gkd} часов</i>'
				bot.send_message(message.chat.id, txt)
				bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW1iwHwF7vKClo5usceHHPCXG_sHxwACKxAAAnazWEhhnVRbfrQa8ikE')
				return
			d = random.randint(1,6)
			if d == 1:
				gkd = random.randint(4*3600,6*3600)
				g = int(time.time() + gkd)
				gkd = math.ceil(gkd/3600)
				text = f'Охуеть, {nam} не дала себя погладить и откусила тебе палец. Да уж, некодевочки крайне непредсказуемые создания. Лучше подождать некоторое время и дать ей успокоиться, попробуй снова через {gkd} часов'
				if gender == 1:
					text = f'Охуеть, {nam} не дал себя погладить и откусил тебе палец. Да уж, некомальчики крайне непредсказуемые создания. Лучше подождать некоторое время и дать ему успокоиться, попробуй снова через {gkd} часов'
				bot.send_message(message.chat.id, text)
				bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEKas5lF0IAAafJ9SOEnwXYQMhHM2_II-gAAqgPAAJBv1BIUARxSpQ5VdIwBA')
				cursor.execute(f'UPDATE neko SET gladit_kd = {g} WHERE id = {message.from_user.id}')
			else:
				text = 'Ты погладил некодевочку, и она довольно помурчала в ответ. Удивительно, но ' + nam + ' уже была поглажена ' + str(gladit + 1) + ' раз'
				if gender == 1:
					text = 'Ты погладил некомальчика, и он довольно помурчал в ответ. Удивительно, но ' + nam + ' уже был поглажен ' + str(gladit + 1) + ' раз'
				if get_happiness_level(happy,baza) != 0:
					text += '\n\nНастроение повышено 🥰'
					happy = int(time.time())
					cursor.execute(f"UPDATE neko SET happy = {happy}  WHERE id = {message.from_user.id}")
				if gifka is None:
					im0 = get_pil(bot,phot)
					w,h = im0.size
					if w > h:
						n = h
					else:
						n = w
					area = (0, 0, n, n)
					im0 = im0.crop(area)
					mean = dominant_color(im0)
					f = make(im0, mean)
					m = bot.send_animation(message.chat.id,f,caption = text)
					gifka = m.animation.file_id
				else:
					bot.send_animation(message.chat.id,gifka,caption = text)
				cursor.execute(f"UPDATE neko SET gladit = gladit + 1, gifka = '{gifka}'  WHERE id = {message.from_user.id}")
		elif cmd == 'покормить':
			if kormit > 0:
				k = math.ceil(kormit/3600)
				bot.send_message(message.chat.id, f'{nam} пока не хочет есть\n\n<i>Осталось ждать {k} часов </i>')
				bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW1iwHwF7vKClo5usceHHPCXG_sHxwACKxAAAnazWEhhnVRbfrQa8ikE')
			else:
				if inventory['whiskas']  > 0 and automate :
					rep = rep + 2
					inventory['whiskas'] -= 1
					if get_happiness_level(happy,baza) == 0:
						text = 'Ты покормил некодевочку её любимым вискасом. Уверен, ей это понравилось гараздо больше обычной еды\n\n+ 2 Доверия 💞\n– 1 Вискас 🍫'
						if gender == 1:
							text = 'Ты покормил некомальчика его любимым вискасом. Уверен, ему это понравилось гараздо больше обычной еды\n\n+ 2 Доверия 💞\n– 1 Вискас 🍫'
					else:
						text = 'Ты покормил некодевочку её любимым вискасом. Ей это действительно понравилось, и в знак благодарности она предложила погладить себя\n\n+ 2 Доверия 💞\n– 1 Вискас 🍫'
						if gender == 1:
							text = 'Ты покормил некомальчика его любимым вискасом. Ему это действительно понравилось, и в знак благодарности он предложил погладить себя\n\n+ 2 Доверия 💞\n– 1 Вискас 🍫'
				else:
					rep = rep + 1
					if get_happiness_level(happy,baza) == 0:
						text = 'Ты покормил некодевочку, продолжай в том же духе и сможешь завоевать её доверие\n\n+ 1 Доверия 💞'
						if gender == 1:
							text = 'Ты покормил некомальчика, продолжай в том же духе и сможешь завоевать его доверие\n\n+ 1 Доверия 💞'
					else:
						text = 'Ты покормил некодевочку, и в знак благодарности она предложила погладить себя. Не советую отказываться\n\n+ 1 Доверия 💞'
						if gender == 1:
							text = 'Ты покормил некомальчика, и в знак благодарности он предложил погладить себя. Не советую отказываться\n\n+ 1 Доверия 💞'
				kormit = int(time.time() + KORMIT_TIMEOUT + HAPPY_TIMEOUT[get_happiness_level(happy,baza)])
				bot.send_message(message.chat.id,text)
				bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLXFiwHwWe1jhzAgMe071rTZ4ureX3AACJRAAAhQoWEiDQZVvpXK9GikE')
				cursor.execute(f"UPDATE neko SET notifed = FALSE, rep = {rep},inventory = '{pack(inventory)}', kormit = {kormit} WHERE id = {message.from_user.id}")
				if intro_level == 0 or intro_level == 1:
					keyboard = types.InlineKeyboardMarkup()
					callback_button1 = types.InlineKeyboardButton(text = 'Читать 👀',callback_data = f'letter {message.from_user.id} {intro_level}')
					keyboard.add(callback_button1)
					txt = 'Тебе письмо ебать'
					m = bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQAC1PhjVwdShxawIYgm_OAkJPMXuOBWiQAClsgxG1hTuEqsn8YQrmq_egEAAwIAA3MAAyoE',caption = txt,reply_markup=keyboard)
					schedule.every(DELETE_MINUTES).minutes.do(job_delete,bot,m.chat.id,m.id)
					cursor.execute(f"UPDATE neko SET intro_level = intro_level + 1 WHERE id = {message.from_user.id}")
					if intro_level == 1:
						licension = int(time.time() + LICENSION_TIMEOUT)
						f = create_licension(bot,phot,photo_design,message.from_user.first_name,gender)
						m = bot.send_photo(ME_CHATID, photo=f)
						cursor.execute(f"UPDATE neko SET licension = {licension}, photo_licension = '{m.photo[-1].file_id}' WHERE id = {message.from_user.id}")
		elif cmd == 'выгулять':
			if gulat > 0:
				g = math.ceil(gulat/3600)
				bot.send_message(message.chat.id, f'{nam} пока не хочет гулять\n\n<i>Осталось ждать {g} часов </i>')
				bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLW1iwHwF7vKClo5usceHHPCXG_sHxwACKxAAAnazWEhhnVRbfrQa8ikE')
			else:
				d = random.randint(1,7)
				if inventory['carton'] > 0:
					d = random.randint(1,8)
				gulat = int(time.time() + GULAT_TIMEOUT + HAPPY_TIMEOUT[get_happiness_level(happy,baza)])
				active_event = 0
				if d == 1:
						cost = random.randint(1,10)
						k = random.randint(1,2)
						if coins < 10:
							k = 2
						if k == 1:
							coins = coins - cost
							text = f'Взор некодевочки упал на старую колоду карт. Было решено сыграть в дурака, и ты проебал деньги. Если не обращать на это внимания, {nam} весело провела время\n\n– {cost} Некогривен 💰'
							if gender == 1:
								text = f'Взор некомальчика упал на старую колоду карт. Было решено сыграть в дурака, и ты проебал деньги. Если не обращать на это внимания, {nam} весело провёл время\n\n– {cost} Некогривен 💰'
							bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQACrPVi2TUAAV6ak7zuL9k5SIEEHAYXdUkAAmO_MRt-YclKhliUv3FMpYABAAMCAANzAAMpBA',caption = text)
						elif k == 2:
							coins = coins + cost
							text = f'Взор некодевочки упал на старую колоду карт. Было решено сыграть в дурака, и ты выиграл немного денег. Повезло, повезло. Если не обращать на это внимания, {nam} весело провела время\n\n+ {cost} Некогривен 💰'
							if gender == 1:
								text = f'Взор некомальчка упал на старую колоду карт. Было решено сыграть в дурака, и ты выиграл немного денег. Повезло, повезло. Если не обращать на это внимания, {nam} весело провёл время\n\n+ {cost} Некогривен 💰'
							bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQACrPdi2TsB9fVbCZY53iP83RMkWyfu2wACUbsxG35h0UpbeK76av4qSgEAAwIAA3MAAykE',caption = text)
						cursor.execute(f'UPDATE neko SET coins = {coins} WHERE id = {message.from_user.id}')
				elif d == 2:
					k = random.randint(1,2)
					if baza >= 5:
						k = 2
					if k == 1:
						rep = rep - 1
						text = 'Ты проснулся в луже блевоты с дичайшим похмельем. Последнее воспоминание - вы заходите в Сильпо и видите Капитана Моргана по скидке. Вчерашние события, к сожалению, остаются тайной. ' + nam + ' теперь тебе доверяет меньше как их следствие\n\n– 1 Доверия 💞'
						bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQACNE1imy-Ri_WnMfD3yi2ud0IAAToM38oAAuy7MRuYt9lIMfj5yYi-9gEBAAMCAANzAAMkBA',caption = text)
					elif k == 2:
						rep = rep + 1
						text = 'Ты проснулся в луже блевоты с дичайшим похмельем. Последнее воспоминание - вы заходите в Сильпо и видите Капитана Моргана по скидке. Вчерашние события, к сожалению, остаются тайной. ' + nam + ' теперь тебе доверяет больше как их следствие\n\n+ 1 Доверия 💞'
						bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQACNE1imy-Ri_WnMfD3yi2ud0IAAToM38oAAuy7MRuYt9lIMfj5yYi-9gEBAAMCAANzAAMkBA',caption = text)
					cursor.execute(f'UPDATE neko SET rep = {rep} WHERE id = {message.from_user.id}')
				elif d == 3:
					k = random.randint(1,2)
					if k == 1:
						active_event = 1
					elif k == 2:
						active_event = 7
				elif d == 4:
					active_event = 2
				elif d == 5:
					active_event = 3
				elif d == 6:
					active_event = 8
				elif d == 7:
					active_event = 11
				elif d == 8:
					active_event = 12
				send_gulat_message(bot,active_event,nam,baza,message.chat.id,gender)
				cursor.execute(f'UPDATE neko SET event = {active_event}, gulat = {gulat} WHERE id = {message.from_user.id}')
		elif cmd == 'повтор':
			if event == 0:
				bot.send_message(message.chat.id, 'Ты не гуляешь')
				return
			send_gulat_message(bot,event,nam,baza,message.chat.id,gender)
		elif first_word == 'имя':
				args = words
				if len(args) < 2:
					bot.send_message(message.chat.id, 'После имя нужно написать само имя еблан')
					return
				first = message.text.split()[0]
				nam = message.text.replace(first,'').strip()
				nam = nam.replace('\n','')
				if len(nam) > 20 or len(nam) < 3:
					bot.send_message(message.chat.id, 'Имя от 3 до 20 символов')
					return
				if emoji.emoji_count(nam) > 0 or message.entities is not None or 'ᅠ' in nam or '­' in nam:
					bot.send_message(message.chat.id, 'Имя не должно содержать эмодзи и пидорских символов')
					return
				if nam.lower() == 'некодевочка' or nam.lower() == 'некомальчик':
					bot.send_message(message.chat.id, 'Нормальное имя придумай блять')
					return
				nam = html.escape(nam, quote = True)
				text = 'Ты дал имя некодевочке. Без сомнений, она быстро к нему привыкнет'
				if gender == 1:
					text = 'Ты дал имя некомальчику. Без сомнений, он быстро к нему привыкнет'
				cursor.execute(f"UPDATE neko SET name = %s WHERE id = {message.from_user.id}", str(nam))
				bot.send_message(message.chat.id, text)
				bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLaRiwIk4DRbw0Lap34MSyMpU-1-3KQACSQ8AAt46WUgVZwAB2AjTbT8pBA')
		elif cmd == 'кладбище':
			text = 'Здесь покоятся все некочаны, за которыми, к сожалению, мы не доглядели. '
			data = cursor.execute(f'SELECT * FROM dead ORDER BY time DESC LIMIT 5')
			data = data.fetchall()
			text += 'Последние умершие некодевочки и некомальчики:\n\n'
			i = 1
			if data is not None:
				for dat in data:
					#cur = datetime.fromtimestamp(dat[1] + TIMESTAMP)
					#death_date = date_string(cur)
					text += f'{i}.  {dat[0]}  ☠️\n'
					text += f'<i>Причина: {dat[2]}</i>\n'
					i += 1
			bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQACn-JiwJJAUjK0Czuxv3RBKiKJJ61u_wACjrwxG0oRCEoxH0CUJepbQQEAAwIAA3MAAykE',caption = text)
		elif cmd == 'отдать':
				if gender == 0:
					text = '<b>"Еба, все б такие умные были"</b> - сказали гопники, уводя твою некодевочку в неизвестном направлении ☠️. Грустно, конечно, но может оно и к лучшему?\n\n– 3 Доверия 💞'
					bot.send_message(message.chat.id, text)
					bot.send_message(message.chat.id, 'Видимо, придётся выдать тебе новую некодевочку')
					photka = random.choice(photos)
					while phot == photka:
						photka = random.choice(photos)
				else:
					text = '<b>"Еба, все б такие умные были"</b> - сказали гопники, уводя твоего некомальчика в неизвестном направлении ☠️. Грустно, конечно, но может оно и к лучшему?\n\n– 3 Доверия 💞'
					bot.send_message(message.chat.id, text)
					bot.send_message(message.chat.id, 'Видимо, придётся выдать тебе нового некомальчика')
					photka = random.choice(trap_photos)
					while phot == photka:
						photka = random.choice(trap_photos)     

				rep -= 3
				if rep < 0:
					rep = 0
				cursor.execute(f'UPDATE neko SET rep = {rep} WHERE id = {message.from_user.id}')
				kill_neko(cursor,message.from_user.id,gender,photka,nam,baza,message.chat.id,'Гопники пустили по кругу')
		elif cmd == 'драться':  
			biba = random.randint(8*3600,10*3600)
			b = int(time.time() + biba)
			biba = math.ceil(biba/3600)
			text =  "Твоя некодевочка прибежала и, заливаясь слезами, рассказала мне что случилось. Хоть ты и напал первым, но численное преимущество оказалось на стороне гопников. Сожалею, но ближайшие " + str(biba) + " часов прийдётся провести в больнице 💊. Во всяком случае, "+ nam  + " не забудет как ты заступился за неё"
			if gender == 1:
				text =  "Твой некомальчик прибежал и, заливаясь слезами, рассказал мне что случилось. Хоть ты и напал первым, но численное преимущество оказалось на стороне гопников. Сожалею, но ближайшие " + str(biba) + " часов прийдётся провести в больнице 💊. Во всяком случае, "+ nam  + " не забудет как ты заступился за него"
			bot.send_message(message.chat.id, text)
			cursor.execute(f'UPDATE neko SET bolnitsa  = {b}, event = 0 WHERE id = {message.from_user.id}')
		elif cmd == 'показать':
			if licension < 0:
				biba = random.randint(36000,46800)
				b = int(time.time() + biba)
				biba = math.ceil(biba/3600)
				text = 'Мент пристально посмотрел сначала на лицензию, а потом на некодевочку. <b>"А лицензия-то недействительна. Будьте добры пройти с нами в отделение"</b> - было сказано как итог. Пару часов тебя избивали дубинками в отделении, требуя признания в краже некодевочки. В конце-концов, вас отпустили, и ' + nam + ' помогла доковылять тебе до ближайшей больницы, где ты проведёшь ' + str(biba) + ' часов 💊'
				if gender == 1:
					text = 'Мент пристально посмотрел сначала на лицензию, а потом на некомальчика. <b>"А лицензия-то недействительна. Будьте добры пройти с нами в отделение"</b> - было сказано как итог. Пару часов тебя избивали дубинками в отделении, требуя признания в краже некодевочки. В конце-концов, вас отпустили, и ' + nam + ' помог доковылять тебе до ближайшей больницы, где ты проведёшь ' + str(biba) + ' часов 💊'
				bot.send_message(message.chat.id, text)
				cursor.execute(f'UPDATE neko SET bolnitsa  = {b},event = 0 WHERE id = {message.from_user.id}')
			else:
				text = 'Мент пристально посмотрел сначала на лицензию, а потом на некодевочку. <b>"Ладно, всё в полном порядке. Извините за беспокойство"</b> - было сказано с некоторым разочарованием. ' + nam + ' весь оставшийся день расспрашивала тебя что такое лицензия и зачем она нужна, а ты с радостью отвечал на ёё вопросы'
				if gender == 1:
					text = 'Мент пристально посмотрел сначала на лицензию, а потом на некомальчика. <b>"Ладно, всё в полном порядке. Извините за беспокойство"</b> - было сказано с некоторым разочарованием. ' + nam + ' весь оставшийся день расспрашивал тебя что такое лицензия и зачем она нужна, а ты с радостью отвечал на его вопросы'
				bot.send_message(message.chat.id, text)
				cursor.execute(f'UPDATE neko SET event = 0 WHERE id = {message.from_user.id}')
		elif cmd == 'приложить':
			if licension < 0:
				biba = random.randint(36000,46800)
				b = int(time.time() + biba)
				biba = math.ceil(biba/3600)
				text = '<b>"ЛИЦЕНЗИЯ НЕДЕЙСТВИТЕЛЬНА"</b> - проговорил автомат монотонным роботическим голосом. Мгновение спустя он отрастил несколько металлических конечностей, и замахнулся одной из них на некодевочку. К счастью, в последний момент тебе удалось прикрыть её своим телом. После этого ты очнулся уже в больнице, где пролежишь ' + str(biba) + ' часов 💊'
				if gender == 1:
					text = '<b>"ЛИЦЕНЗИЯ НЕДЕЙСТВИТЕЛЬНА"</b> - проговорил автомат монотонным роботическим голосом. Мгновение спустя он отрастил несколько металлических конечностей, и замахнулся одной из них на некомальчика. К счастью, в последний момент тебе удалось прикрыть его своим телом. После этого ты очнулся уже в больнице, где пролежишь ' + str(biba) + ' часов 💊'
				bot.send_photo(message.chat.id,photo = 'AgACAgIAAx0CZQN7rQABAX8DZNQ2te3sum1sc1vUfGclygEEMUAAAvvKMRsMUalKFocMBpcUKx8BAAMCAANzAAMwBA',caption = text)
				cursor.execute(f'UPDATE neko SET bolnitsa  = {b},event = 0 WHERE id = {message.from_user.id}')
			else:
				d = random.randint(1,3)
				if d != 3:
					text = 'Невообразимо, но торговый автомат действительно выдал косяк. Вы с кайфом раскумарились, а потом [ДАННЫЕ УДАЛЕНЫ]. ' + nam + ' определённо стала доверять тебе больше после этого дня\n\n+ 1 Доверия 💞\nНастроение повышено 🥰'
					if gender == 1:
						text = 'Невообразимо, но торговый автомат действительно выдал косяк. Вы с кайфом раскумарились, а потом [ДАННЫЕ УДАЛЕНЫ]. ' + nam + ' определённо стал доверять тебе больше после этого дня\n\n+ 1 Доверия 💞\nНастроение повышено 🥰'
					rep += 1
					ph = 'AgACAgIAAx0CZQN7rQABAX8BZNQ2sQgg0OsW20FrnyZ6TMDWkDAAAvrKMRsMUalKQmYJa7rBXvMBAAMCAANzAAMwBA'
				else:
					text = 'Автомат сломался и выдал вам банку розового монстра ⚡️. Вы пизданули ногами его пару раз, но заветного косяка так и не увидели. Видимо, всё таки это наебалово\n\n+ 1 Монстр ⚡️'
					inventory['monster'] += 1
					ph = 'AgACAgIAAx0CZQN7rQABAX8FZNQ2udaVwx6S9pkFzB4cUUadxR0AAv3KMRsMUalKDxh0u4EeO6sBAAMCAANzAAMwBA'
				bot.send_photo(message.chat.id,photo = ph,caption = text)
				cursor.execute(f"UPDATE neko SET event = 0, happy = {int(time.time())}, rep = {rep}, inventory = '{pack(inventory)}' WHERE id = {message.from_user.id}")
		elif cmd == 'откупиться':
			cost = 15
			if coins < cost:
				bot.send_message(message.chat.id, 'А деньги где')
				return
			coins = coins - cost
			text = '<b>"Хорошего вам дня, молодой человек"</b> - ответили тебе менты с насмешливыми улыбками на их лицах. Как можно было догадаться, этот день хорошим уже не будет\n\n– 15 Некогривен 💰'
			bot.send_message(message.chat.id, text)
			cursor.execute(f'UPDATE neko SET coins  = {coins},event = 0 WHERE id = {message.from_user.id}')
		elif cmd == 'завод':
			cur = datetime.fromtimestamp(time.time() + TIMESTAMP)
			d = int(cur.day)
			h = int(cur.hour)
			if h >= 5 and h < 9:
				pic = 'AgACAgIAAx0CZQN7rQAC1cRjWHHPqKY27zwSInf6YS46TjgN3wAC3r4xG2_iyEpm4U7RaB2iRQEAAwIAA3MAAyoE'
			else:
				pic = 'AgACAgIAAx0CZQN7rQACn_1iwNZlro5zQzmVqnbvJMQSzhuaCQACLr0xG0oRCEphls-j33z4fQEAAwIAA3MAAykE'
			if zavod == d:
				bot.send_message(message.chat.id, 'Сегодня ты уже работал')
				return
			days += 1
			cursor.execute(f"UPDATE neko SET days = {days},zavod = {d} WHERE id = {message.from_user.id}")
			if days < 4:
				c = 15
				coins = coins + c
				if days == 3:
					txt = 'Что ж, самое время идти на завод ебашить за копейки.\n\nЗа эту смену тебе удалось заработать ' + str(c) + ' некогривен 💰. Уверен, у тебя получится всё не пропить\n\nК сожалению, станком тебе отхерачило последний палец, поэтому тебя переводят на новую должность. С завтрашнего дня ты будешь работать на одном из контрольно-пропускных пунктов завода. Можешь считать это повышением'
				else:
					txt = 'Что ж, самое время идти на завод ебашить за копейки.\n\nЗа эту смену тебе удалось заработать ' + str(c) + ' некогривен 💰. Уверен, у тебя получится всё не пропить'
				bot.send_photo(message.chat.id, photo = pic,caption = txt)
				if version != patch_version:
					keyboard = types.InlineKeyboardMarkup()
					callback_button1 = types.InlineKeyboardButton(text = 'Читать 👀',callback_data = 'read ' + str(message.from_user.id))
					keyboard.add(callback_button1)
					callback_button2 = types.InlineKeyboardButton(text = 'Не читать ❌',callback_data = 'dont ' + str(message.from_user.id))
					keyboard.add(callback_button2)
					m = bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQACznBjQgABiPsE5FE7am8mfAOKiXsSOEsAAju9MRuS1hFKlyErHhjWQfcBAAMCAANzAAMqBA',caption = 'Возвращаясь с работы, ты заметил свежую газету, торчащую из твоего почтового ящика. Прочитать её?',reply_markup=keyboard)
					schedule.every(DELETE_MINUTES).minutes.do(job_delete,bot,m.chat.id,m.id)
				cursor.execute(f"UPDATE neko SET coins = {coins} ,version = {patch_version} WHERE id = {message.from_user.id}")
			else:
				if days == 4:
					txt = 'Поздравляем с первым днем на новой должности! В твои обязанности входит проверять документы некочанов и либо пропускать их, либо слать нахуй. Подробнее можно прочитать в руководстве 📕. Помни, твоя зарплата зависит от количества правильных решений'
				else:
					txt = 'Ты пришел на рабочее место и готов принимать первых некочанов. Старая работа за станком определённо была лучше этой хуйни'
				keyboard = types.InlineKeyboardMarkup(row_width=2)
				callback_button1 = types.InlineKeyboardButton(text = 'Начать ▶️',callback_data = 'paper ' + str(message.from_user.id) + ' ' + str(True) + ' '  + str(True) + ' 0 1')
				switch_button1 = types.InlineKeyboardButton(text='Руководство 📕', switch_inline_query_current_chat = "Руководство")
				keyboard.add(callback_button1)
				keyboard.add(switch_button1)
				m = bot.send_photo(message.chat.id, photo=pic, caption=txt)
				res = generate_papers(bot)
				struct = struct_papers.copy()
				struct['players'] = [message.from_user.id]
				struct['today_text'] = res[0]
				struct['images'] = res[1]
				struct['wait'] = int(time.time() + 600)
				struct['chat'] = message.chat.id
				struct['message'] = m.id
				db[message.from_user.id] = pack(struct)
				bot.edit_message_caption(caption=txt, chat_id=m.chat.id, message_id=m.id, reply_markup=keyboard)
		elif cmd == 'выгнать дебилов':
			if debil:
				bot.send_message(message.chat.id, 'Дебилы уже ушли')
				return
			cursor.execute(f'UPDATE neko SET debil = TRUE WHERE id = {message.from_user.id}')
			bot.send_message(message.chat.id, 'Дебилы ушли от тебя, но будут рады вернуться в любой момент')
			bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFi19i9rLE0Zk7bicpKmus0JujKOHZGwACDxEAAoIqUUg7LMMbW4WU6SkE')
			return
		elif cmd == 'вернуть дебилов':
			if not debil:
				bot.send_message(message.chat.id, 'Дебилы никуда не уходили')
				return
			cursor.execute(f'UPDATE neko SET debil = FALSE WHERE id = {message.from_user.id}')
			bot.send_message(message.chat.id, 'Дебилы наконец-то вернулись к тебе')
			bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFi19i9rLE0Zk7bicpKmus0JujKOHZGwACDxEAAoIqUUg7LMMbW4WU6SkE')
			return
		elif cmd == 'некобаза':
			gtxt = ' со своей некодевочкой '
			if gender == 1:
				gtxt = ' со своим некомальчиком '
			markup = types.InlineKeyboardMarkup()
			switch_button1 = types.InlineKeyboardButton(text='Улучшить ⏫', switch_inline_query_current_chat = "Улучшить")
			switch_button2 = types.InlineKeyboardButton(text='Покрасить 🌈', switch_inline_query_current_chat = "Покрасить базу")
			switch_button3 = types.InlineKeyboardButton(text='Выгнать дебилов 🙁', switch_inline_query_current_chat = "Выгнать дебилов")
			switch_button4 = types.InlineKeyboardButton(text='Вернуть дебилов 🙂', switch_inline_query_current_chat = "Вернуть дебилов")
			switch_button5 = types.InlineKeyboardButton(text='Верстак 🛠', switch_inline_query_current_chat = "Верстак")
			debil_base_photos = ['AgACAgIAAx0CZQN7rQABAR1-ZKXYxvflJZskUzvklW6Z45Qrxi4AAi7MMRsoDDFJFdKS2jFfgXcBAAMCAANzAAMvBA',
			'AgACAgIAAx0CZQN7rQABAR2AZKXYzP_0FFnWmNCbXlxTbsFcg5kAAjDMMRsoDDFJs3ld-LV1u1QBAAMCAANzAAMvBA',
			'AgACAgIAAx0CZQN7rQABAR2CZKXY0aLctjwpeiLDTx70wUEEfR8AAjHMMRsoDDFJdHtcBBa1tIEBAAMCAANzAAMvBA',
			'AgACAgIAAx0CZQN7rQABAR2EZKXY14u5l38cpRiFj-Vv3DWtLvUAAjLMMRsoDDFJMnFHQx3YZWwBAAMCAANzAAMvBA',
			'AgACAgIAAx0CZQN7rQABAR2GZKXY3M6f4JPX1RLWqHVhFWizR-AAAjPMMRsoDDFJCO2YBY_FeoMBAAMCAANzAAMvBA',
			'AgACAgIAAx0CZQN7rQABAR2KZKXY5z3iLBpqGJACaUV6-W4dGAsAAjXMMRsoDDFJ63NSfS5_wX0BAAMCAANzAAMvBA',
			'AgACAgIAAx0CZQN7rQABAR2OZKXY89iHb9k9FkzEJAbVHbrmXI0AAjfMMRsoDDFJFpXViPtsKEsBAAMCAANzAAMvBA',
			'AgACAgIAAx0CZQN7rQABAR2SZKXY_TyYfJ1VXsureTNkxM5sHHcAAj3LMRsoDDFJEK6_dlr2I8wBAAMCAANzAAMvBA'
			]
			neko_base_photos = ['AgACAgIAAx0CZQN7rQABAR1-ZKXYxvflJZskUzvklW6Z45Qrxi4AAi7MMRsoDDFJFdKS2jFfgXcBAAMCAANzAAMvBA',
			'AgACAgIAAx0CZQN7rQABAR2AZKXYzP_0FFnWmNCbXlxTbsFcg5kAAjDMMRsoDDFJs3ld-LV1u1QBAAMCAANzAAMvBA',
			'AgACAgIAAx0CZQN7rQABAR2CZKXY0aLctjwpeiLDTx70wUEEfR8AAjHMMRsoDDFJdHtcBBa1tIEBAAMCAANzAAMvBA',
			'AgACAgIAAx0CZQN7rQABAR2EZKXY14u5l38cpRiFj-Vv3DWtLvUAAjLMMRsoDDFJMnFHQx3YZWwBAAMCAANzAAMvBA',
			'AgACAgIAAx0CZQN7rQABAj_iZSvz7VIAAckYG9JYwx-HE8cSi89EAALn1jEbBWphScfFFvlzZKMGAQADAgADeQADMAQ',
			'AgACAgIAAx0CZQN7rQABAj_kZSvz81EDpBw1D9fRmBPW5lNl-HcAAujWMRsFamFJSk6qlezq-f0BAAMCAAN5AAMwBA',
			'AgACAgIAAx0CZQN7rQABAj_oZSvz_pB4jDksSkJvgEpE6E9uH8YAAuvWMRsFamFJ2gGu3wV1JtUBAAMCAAN5AAMwBA',
			'AgACAgIAAx0CZQN7rQABAj_qZSv0DyzIv1KuPa8RJRhJZpWxHBcAAuzWMRsFamFJrzhZtnvW4JkBAAMCAAN5AAMwBA'
			]
			base_text = ['\n\n<b>Улучшить</b>  —  10 💰\nНемного интерьера 🏠\nЭффект:  +2 доверия 💞',
			'\n\n<b>Улучшить</b>  —  30 💰\nВысокотехнологичный верстак 🏠\nЭффект:  Позволяет создавать предметы 🛠',
			'\n\n<b>Улучшить</b>  —  50 💰\nНемного искусства 🏠\nЭффект:  Настроение падает медленнее 😺',
			'\n\n<b>Улучшить</b>  —  70 💰\nТелевизор со встроенным флексаиром 🏠\nЭффект:  +4 доверия 💞',
			'\n\n<b>Улучшить</b>  —  90 💰\nСтол с бухлом 🏠\nЭффект:  Событие с Капитаном Морганом всегда даёт плюс доверие 💞',
			'\n\n<b>Улучшить</b>  —  120 💰\nВсратый туалет 🏠\nЭффект:  +6 доверия 💞',
			'\n\n<b>Улучшить</b>  —  150 💰\nНе менее всратая кухня 🏠\nЭффект:  +1 к получаемому вискасу 🍫',
			'\n\n<b>Покрасить базу</b>  —  100 💰\nТы можешь изменить цвет стен если он тебя заебал'
			]
			text = 'Вау, да это же твоя собственная база. В этом замечательном месте ты живёшь вместе' + gtxt + base_text[baza]
			butlist = []

			if baza < 7:
				if not debil:
					p = debil_base_photos[baza]
				else:
					p = neko_base_photos[baza]
				butlist.append(switch_button1)
			else:
				if not debil:
					p = photo_base
				else:
					p = photo_debil
				butlist.append(switch_button2)

			if baza > 1:
				butlist.append(switch_button5)

			if baza > 3:
				if not debil:
					butlist.append(switch_button3)
				else:
					butlist.append(switch_button4)

			if len(butlist) != 3:
				for b in butlist:
					markup.add(b)
			else:
				markup.add(butlist[0], butlist[1])
				markup.add(butlist[2])
			bot.send_photo(message.chat.id,photo = p,caption = text,reply_markup=markup)
		elif cmd == 'улучшить':
			base_cost = [10,30, 50, 70, 90, 120, 150]
			base_rep = [0,2,0,0,4,0,6,0]
			if baza < 7:
				cost = base_cost[baza]
			else:
				bot.send_message(message.chat.id, 'У тебя база максимального уровня ебанат')
				return
			if coins < cost:
				bot.send_message(message.chat.id, 'А деньги где')
				return
			text = nam + ' не очень понимает что это и зачем оно нужно, но ей понравилось'
			if gender == 1:
				text = nam + ' не очень понимает что это и зачем оно нужно, но ему понравилось'
			bot.send_message(message.chat.id, text)
			bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLYxiwIeP83zV6whMtLqyTygKqGALagAChBAAAh_9WEh3vpYnO2kD1ikE')
			coins -= cost
			baza += 1
			rep += base_rep[baza]
			cursor.execute(f"UPDATE neko SET base = {baza}, rep = {rep}, coins = {coins} WHERE id = {message.from_user.id}")
		elif cmd == 'уйти':
			if event == 2:
				text = "Вы ушли, так и не узнав что находилось внутри загадочной коробки. Могу сказать что это было разумным решением"
			elif event == 3:
				text = '<b>"Sorry, nekoslav, I cant give credit! Come back when youre a little...mmmm...richer"</b> - после этих слов окошко ларька закрылось. Мда уж, видимо, ты сильно разочаровал продавщицу'
			elif event == 8:
				text = 'Вы вежливо отказались, и некодевочка с некоторой грустью молча вернулась к своему занятию. Видимо, ей не впервой слышать подобные слова'
			elif event == 11:
				text = "Вы ушли, так и не узнав пытались ли вас наебать. На следующий день автомата уже не было на прежнем месте"
			bot.send_message(message.chat.id,text)
			cursor.execute(f'UPDATE neko SET event = 0 WHERE id = {message.from_user.id}')
		elif cmd == 'съебать':
			text = "Ебака отвлеклась на кучу картона когда вы пробегали мимо стройки, благодаря чему тебе с некодевочкой удалось оторваться"
			if gender == 1:
				text = "Ебака отвлеклась на кучу картона когда вы пробегали мимо стройки, благодаря чему тебе с некомальчиком удалось оторваться"
			bot.send_message(message.chat.id,text)
			cursor.execute(f'UPDATE neko SET event = 0 WHERE id = {message.from_user.id}')
		elif cmd == 'купить':
			if event == 4:
				cost = 25
				if coins < cost:
					bot.send_message(message.chat.id, 'А деньги где')
					return
				coins = coins - cost
				plus = 4
				if baza >= 7:
					plus = 5
				text = f'Потраченных денег немного жаль, но {nam} выглядит счастливой, а это главное, не так ли?\n\n– 25 Некогривен 💰\n+ {plus} Вискаса 🍫'
				if gender == 1:
					text = f'Потраченных денег немного жаль, но {nam} выглядит счастливым, а это главное, не так ли?\n\n– 25 Некогривен 💰\n+ {plus} Вискаса 🍫'
				inventory['whiskas'] += plus
				bot.send_message(message.chat.id, text)
			elif event == 5:
				cost = 30
				if coins < cost:
					bot.send_message(message.chat.id, 'А деньги где')
					return
				coins = coins - cost
				text = 'Вам конечно хотелось выпить содержимое банок, но заправить некомобиль важнее. Надеюсь, ты не жалеешь о потраченных деньгах\n\n– 30 Некогривен 💰\n+ 1 Монстр ⚡️'
				inventory['monster'] += 1
				bot.send_message(message.chat.id, text)
			elif event == 6:
				cost = 40
				if coins < cost:
					bot.send_message(message.chat.id, 'А деньги где')
					return
				coins = coins - cost
				inventory['neko_box'] += 1
				text = 'Из коробки слышались шкрябание и мольбы о помощи, но после того как продавец пару раз пнул коробку ногой звуки затихли\n\n– 40 Некогривен 💰\n+ 1 Коробка с неко 🎁'
				bot.send_message(message.chat.id, text) 
			elif event == 9:
				cost = 5
				if inventory['whiskas'] < cost:
					bot.send_message(message.chat.id, 'А вискас где')
					return
				inventory['whiskas'] = inventory['whiskas'] - cost
				text = '<b>"Ня, спасибо"</b> - поблагодарила некодевочка и поспешила скрыться, будто боясь, что ты передумаешь. Интересно, адреналин вкуснее монстра?\n\n– 5 Вискаса 🍫\n+ 1 Адреналин 🗡'
				bot.send_message(message.chat.id,text)
				inventory['adrenalin'] += 1
			elif event == 10:
				cost = 10
				if inventory['whiskas'] < cost:
					bot.send_message(message.chat.id, 'А вискас где')
					return
				inventory['whiskas'] = inventory['whiskas'] - cost
				text = f'<b>"Ня, спасибо"</b> - поблагодарила некодевочка и поспешила скрыться, будто боясь, что ты передумаешь. К счастью, {nam} пока не догадывается о назначении этого устройства\n\n– 10 Вискаса 🍫\n+ 1 Gender changer 🪚'
				bot.send_message(message.chat.id,text)
				inventory['gender_changer'] += 1
			cursor.execute(f"UPDATE neko SET coins = {coins}, inventory = '{pack(inventory)}',event = 0 WHERE id = {message.from_user.id}")
		elif cmd == 'открыть':
			d = random.randint(1,2)
			if d == 1:
				text = 'Внутри оказалась бездомная некодевочка. Как только ты открыл коробку, она моментально набросилась на твою, издавая шипящие звуки. К сожалению, ушло время чтобы их разнять. ' + nam + ' обиделась на тебя за это\n\n– 2 Доверия 💞'
				if gender == 1:
					text = 'Внутри оказалась бездомная некодевочка. Как только ты открыл коробку, она моментально набросилась на твоего некомальчика, издавая шипящие звуки. К сожалению, ушло время чтобы их разнять. ' + nam + ' обиделся на тебя за это\n\n– 2 Доверия 💞'
				rep = rep - 2
				bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQACohNixNKGV5unSWPowKZ7Go5lj9An_wACfr4xGzBhKEochCEOh_LDpwEAAwIAA3MAAykE',caption = text)
			if d == 2:
				text = 'Вам повезло, коробка оказалась полностью заполнена вискасом! Этого должно хватить на три раза, если не больше\n\n+ 3 Вискаса 🍫'
				inventory['whiskas'] += 3
				if baza >= 7:
					inventory['whiskas'] += 1
					text = 'Вам повезло, коробка оказалась полностью заполнена вискасом! Этого должно хватить на четыре раза, если не больше\n\n+ 4 Вискаса 🍫'
				bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQACoKJiweU_aU7g1olT0b065v9A9dDVXwACqLsxGxyOEUodvpN4YkjBswEAAwIAA3MAAykE',caption = text)
			cursor.execute(f"UPDATE neko SET inventory = '{pack(inventory)}', rep = {rep},event = 0 WHERE id = {message.from_user.id}")
		elif cmd == 'атаковать':
			d = random.randint(1,2)
			if d == 1:
				inventory['carton'] -= 1
				text = f'Во время боя существу удалось зайти к тебе за спину и достать кусок картона из твоего рюкзака, после чего с ним в зубах оно убежало в неизвестном направлении\n\n– 1 Картон 📦'
			elif d == 2:
				inventory['adrenalin'] += 1
				text = f'Пока {nam} пиздилась с картоноедом, тебе удалось незаметно подкрасться и достать недопитый энергетик с его кармана. Это можно считать победой?\n\n+ 1 Адреналин 🗡'
				if gender == 1:
					text = f'Пока {nam} пиздился с картоноедом, тебе удалось незаметно подкрасться и достать недопитый энергетик с его кармана. Это можно считать победой?\n\n+ 1 Адреналин 🗡'
			bot.send_message(message.chat.id,text)
			cursor.execute(f"UPDATE neko SET inventory = '{pack(inventory)}', event = 0 WHERE id = {message.from_user.id}")
		elif cmd == 'вискас':
				send_gulat_message(bot,4,nam,baza,message.chat.id,gender)
				cursor.execute(f'UPDATE neko SET event = 4 WHERE id = {message.from_user.id}')
		elif cmd == 'монстр':
			send_gulat_message(bot,5,nam,baza,message.chat.id,gender)
			cursor.execute(f'UPDATE neko SET event = 5 WHERE id = {message.from_user.id}')
		elif cmd == 'адреналин':
			send_gulat_message(bot,9,nam,baza,message.chat.id,gender)
			cursor.execute(f'UPDATE neko SET event = 9 WHERE id = {message.from_user.id}')
		elif cmd == 'gender changer':
			send_gulat_message(bot,10,nam,baza,message.chat.id,gender)
			cursor.execute(f'UPDATE neko SET event = 10 WHERE id = {message.from_user.id}')
		elif cmd == 'коробка':
			send_gulat_message(bot,6,nam,baza,message.chat.id,gender)
			cursor.execute(f'UPDATE neko SET event = 6 WHERE id = {message.from_user.id}')
		elif cmd == 'назад':
			if event == 4 or event == 5 or event == 6:
				send_gulat_message(bot,3,nam,baza,message.chat.id,gender)
				cursor.execute(f'UPDATE neko SET event = 3 WHERE id = {message.from_user.id}')
			else:
				send_gulat_message(bot,8,nam,baza,message.chat.id,gender)
				cursor.execute(f'UPDATE neko SET event = 8 WHERE id = {message.from_user.id}')
		elif cmd == 'гараж':
			if not car:
				markup = types.InlineKeyboardMarkup()
				switch_button1 = types.InlineKeyboardButton(text='Купить машину 💸', switch_inline_query_current_chat = "Купить машину")
				markup.add(switch_button1)
				text = 'Это твой гараж, но как-то здесь пустовато, ты так не думаешь?\n\n<b>Купить машину</b>  —  100 💰\nСамое время купить себе некомобиль!'
				bot.send_photo(message.chat.id,photo = 'AgACAgIAAx0CZQN7rQACoV5iw21fDMZ4Yb_e1BZ3uIL-IT1xVwACFrwxG-RaGEpQPC9bR_1lwQEAAwIAA3MAAykE',caption = text,reply_markup=markup)
			else:
				markup = types.InlineKeyboardMarkup()
				switch_button4 = types.InlineKeyboardButton(text='Данж 🏳️‍🌈', switch_inline_query_current_chat = "Данж")
				switch_button3 = types.InlineKeyboardButton(text='Босс ☠️', switch_inline_query_current_chat = "Босс")
				switch_button2 = types.InlineKeyboardButton(text='Покрасить 🌈', switch_inline_query_current_chat = "Покрасить машину")
				markup.add(switch_button4,switch_button3)
				markup.add(switch_button2)
				text = f'Это твой собственный некомобиль, разве он не прекрасен? Что ж, выбирай куда ехать\n<b>Монстров ⚡️:</b>  {inventory["monster"]}\n\n<b>Данж 🏳️‍🌈</b>\nОт 60 доверия. Отправься к загадочному порталу в LGBT мир\n<b>Босс ☠️</b>\nОт 120 доверия. Отпизди неведомую хуйню сам или с друзьями\n\n<b>Покрасить машину</b>  —  100 💰\nТы можешь изменить цвет некомобиля если он тебя заебал'
				bot.send_photo(message.chat.id,photo = photo_mobile,caption = text,reply_markup=markup)
		elif cmd == 'купить машину':  
			if car:
				bot.send_message(message.chat.id, 'У тебя уже есть некомобиль ебанько')
				return
			cost = 100
			if coins < cost:
				bot.send_message(message.chat.id, 'А деньги где')
				return
			bot.send_message(message.chat.id, 'Поздравляю с покупкой! Если машина сломается в течении года, мы вернём 1 некогривну на кэшбек счёт')
			bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLYxiwIeP83zV6whMtLqyTygKqGALagAChBAAAh_9WEh3vpYnO2kD1ikE')
			coins = coins - cost
			cursor.execute(f"UPDATE neko SET car = TRUE, coins = {coins} WHERE id = {message.from_user.id}")
		elif first_word == 'использовать':
				args = words
				if len(args) < 2:
					bot.send_message(message.chat.id,'Еблана ты кусок, после использовать нужно писать название предмета')
					return
				args.pop(0)
				item_name = ' '.join(args)
				if item_name == 'антипохмелин' and inventory['antipohmelin'] > 0:
					if message.reply_to_message is None:
						if bolnitsa <= 0:
							bot.send_message(message.chat.id, 'Дебил, ты должен быть в больнице чтобы использовать антипохмелин')
							return
						bolnitsa = 0
						inventory['antipohmelin'] -= 1
						cursor.execute(f"UPDATE neko SET bolnitsa = {bolnitsa} WHERE id = {message.from_user.id}")
						bot.send_message(message.chat.id, 'Ты вылетел(а) из больницы на жопной тяге')
						bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFhGti8zHsovf2QjnACCIhNm-mGDTNfgACJhUAAm8UmEppPj8WKn_J6ikE')
					else:
						idk = message.reply_to_message.from_user.id
						if idk == message.from_user.id:
							bot.send_message(message.chat.id, 'Чет я не понял')
							return
						data = cursor.execute(f"SELECT bolnitsa,chel FROM neko WHERE id = {idk}")
						data = data.fetchone()
						if data is None:
							bot.send_message(message.chat.id,'У этого лоха нет некодевочки')
							return
						b2 = int(data[0] - time.time())
						chel = data[1]
						if b2 <= 0:
							bot.send_message(message.chat.id,'Этот лох не в больнице')
							return
						inventory['antipohmelin'] -= 1
						b2 = 0
						cursor.execute(f"UPDATE neko SET bolnitsa = {b2} WHERE id = {idk}")
						bot.send_message(message.chat.id, '<a href="tg://user?id='+str(idk)+'">'+str(chel)+'</a> вылетел(а) из больницы на жопной тяге')
						bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFhGti8zHsovf2QjnACCIhNm-mGDTNfgACJhUAAm8UmEppPj8WKn_J6ikE')
				elif item_name == 'вискас' and inventory['whiskas'] > 0:
					if automate:
						text = 'Ты больше не кормишь свою некодевочку вискасом 🍫, жестоко'
						if gender == 1:
							text = 'Ты больше не кормишь своего некомальчика вискасом 🍫, жестоко'
						bot.send_message(message.chat.id, text)
						bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEGHaljTQMPtoJuC9PyYV2e5g0lGX77-wACIA8AAg7tWEjVrCd9QwTr1ioE')
						cursor.execute(f"UPDATE neko SET automate = FALSE WHERE id = {message.from_user.id}")
					else:
						automate = 1
						bot.send_message(message.chat.id, 'Ура, ' + nam + ' снова может есть свой любимый вискас 🍫')
						bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEGHbFjTQM_ocljKc2-O9GAUVL7Nb60TgACSQ8AAt46WUgVZwAB2AjTbT8qBA')
						cursor.execute(f"UPDATE neko SET automate = TRUE WHERE id = {message.from_user.id}")
				elif item_name == 'кость санса' and inventory['bone'] > 0:
					if bone_automate:
						text = 'Твоя некодевочка больше не пиздит врагов костями 🦴'
						if gender == 1:
							text = 'Твой некомальчик больше не пиздит врагов костями 🦴'
						bot.send_message(message.chat.id, text)
						bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEGHaljTQMPtoJuC9PyYV2e5g0lGX77-wACIA8AAg7tWEjVrCd9QwTr1ioE')
						cursor.execute(f"UPDATE neko SET bone_automate = FALSE WHERE id = {message.from_user.id}")
					else:
						text = nam + ' определённо полюбит новое оружие 🦴'
						bot.send_message(message.chat.id, text)
						bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEGHbFjTQM_ocljKc2-O9GAUVL7Nb60TgACSQ8AAt46WUgVZwAB2AjTbT8qBA')
						cursor.execute(f"UPDATE neko SET bone_automate = TRUE WHERE id = {message.from_user.id}")
				elif item_name == 'адреналин' and inventory['adrenalin'] > 0:
					inventory['adrenalin'] -= 1
					a = random.choice([True,False])
					if a:
						skill = random.randint(1,10)
					else:
						skill = random.randint(101,110)

					while skill == skill1 or skill == skill2:
						a = random.choice([True,False])
						if a:
							skill = random.randint(1,10)
						else:
							skill = random.randint(101,110)

					if skill1 > 100:
						sktxt1 = active_skill_list[skill1-100]
					else:
						sktxt1 = passive_skill_list[skill1]
					if skill2 > 100:
						sktxt2 = active_skill_list[skill2-100]
					else:
						sktxt2 = passive_skill_list[skill2]

					keyboard = types.InlineKeyboardMarkup(row_width=3)
					callback_button1 = types.InlineKeyboardButton(text = 'Замена 1️⃣',callback_data = 'skill ' + str(message.from_user.id) + ' 1 ' + str(skill))
					callback_button2 = types.InlineKeyboardButton(text = 'Замена 2️⃣',callback_data = 'skill ' + str(message.from_user.id) + ' 2 ' + str(skill))
					keyboard.add(callback_button1,callback_button2)
					callback_button3 = types.InlineKeyboardButton(text = 'Не менять 🆗',callback_data = 'dont ' + str(message.from_user.id))
					keyboard.add(callback_button3)
					text = nam + ', выпив содержимое банки, почуствовала в себе силу, способную свернуть горы. У неё появилось новое умение, выбери какой навык заменить на случайный:\n\n' + sktxt1 + '\n' + sktxt2
					if gender == 1:
						text = nam + ', выпив содержимое банки, почуствовал в себе силу, способную свернуть горы. У него появилось новое умение, выбери какой навык заменить на случайный:\n\n' + sktxt1 + '\n' + sktxt2
					m = bot.send_message(message.chat.id,text,reply_markup=keyboard)
					schedule.every(DELETE_MINUTES).minutes.do(job_delete,bot,m.chat.id,m.id)
				elif item_name == 'gender changer' and inventory['gender_changer'] > 0:
					inventory['gender_changer'] -= 1
					text = nam + ' чувствует себя странно...'
					bot.send_message(message.chat.id,text)
					if gender == 0:
						photka = random.choice(trap_photos)
						while True:
							if phot != photka:
								break
							else:
								photka = random.choice(trap_photos)
						gender = 1
					else:
						photka = random.choice(photos)
						while True:
							if phot != photka:
								break
							else:
								photka = random.choice(photos)
						gender = 0
					cursor.execute(f"UPDATE neko SET new_phot = NULL gender = {gender}, gifka = NULL, licension = 0, photo = '{photka}' WHERE id = {message.from_user.id}")
				elif item_name == 'коробка с неко' and inventory['neko_box'] > 0:
					inventory['neko_box'] -= 1
					if gender == 0:
						photka = random.choice(elite_photos)
						while True:
							if phot != photka:
								break
							else:
								photka = random.choice(elite_photos)
					else:
						photka = random.choice(trap_photos)
						while True:
							if phot != photka:
								break
							else:
								photka = random.choice(trap_photos)
					keyboard = types.InlineKeyboardMarkup(row_width=3)
					callback_button1 = types.InlineKeyboardButton(text = 'Взять ✅',callback_data = 'get ' + str(message.from_user.id))
					keyboard.add(callback_button1)
					callback_button2 = types.InlineKeyboardButton(text = 'Не брать ❌',callback_data = 'dont ' + str(message.from_user.id))
					keyboard.add(callback_button2)
					m = bot.send_photo(message.chat.id, photo=photka,reply_markup=keyboard)
					schedule.every(DELETE_MINUTES).minutes.do(job_delete,bot,m.chat.id,m.id)
				elif item_name == 'коробка с хорни неко' and inventory['horny_neko_box'] > 0:
					inventory['horny_neko_box'] -= 1
					if gender == 0:
						photka = random.choice(ero_photos)
						while True:
							if phot != photka:
								break
							else:
								photka = random.choice(ero_photos)
					else:
						photka = random.choice(trap_photos)
						while True:
							if phot != photka:
								break
							else:
								photka = random.choice(trap_photos)
					keyboard = types.InlineKeyboardMarkup(row_width=3)
					callback_button1 = types.InlineKeyboardButton(text = 'Взять ✅',callback_data = 'get ' + str(message.from_user.id))
					keyboard.add(callback_button1)
					callback_button2 = types.InlineKeyboardButton(text = 'Не брать ❌',callback_data = 'dont ' + str(message.from_user.id))
					keyboard.add(callback_button2)
					m = bot.send_photo(message.chat.id, photo=photka,reply_markup=keyboard)
					schedule.every(DELETE_MINUTES).minutes.do(job_delete,bot,m.chat.id,m.id)
				elif item_name == 'штаны за 40 гривень' and inventory['armor1'] > 0:
					inventory['armor1'] -= 1
					equipped = 110
					cursor.execute(f"UPDATE neko SET equipped = {equipped} WHERE id = {message.from_user.id}")
					text = nam + ' с удовольствием будет носить эти обноски с ближайшей помойки'
					bot.send_message(message.chat.id, text)
					bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEGHbFjTQM_ocljKc2-O9GAUVL7Nb60TgACSQ8AAt46WUgVZwAB2AjTbT8qBA')
				elif item_name == 'костюм горничной' and inventory['armor2'] > 0:
					inventory['armor2'] -= 1
					equipped = 210
					cursor.execute(f"UPDATE neko SET equipped = {equipped} WHERE id = {message.from_user.id}")
					text = nam + ' с удовольствием будет носить эти обноски с ближайшей помойки'
					bot.send_message(message.chat.id, text)
					bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEGHbFjTQM_ocljKc2-O9GAUVL7Nb60TgACSQ8AAt46WUgVZwAB2AjTbT8qBA')
				elif item_name == 'куртка санса' and inventory['armor3'] > 0:
					inventory['armor3'] -= 1
					equipped = 310
					cursor.execute(f"UPDATE neko SET equipped = {equipped} WHERE id = {message.from_user.id}") 
					text = nam + ' с удовольствием будет носить эти обноски с ближайшей помойки'
					bot.send_message(message.chat.id, text)
					bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEGHbFjTQM_ocljKc2-O9GAUVL7Nb60TgACSQ8AAt46WUgVZwAB2AjTbT8qBA')
				elif item_name == 'коробка с украшениями' and inventory['loot_box'] > 0:
					inventory['loot_box'] -= 1
					item = random.randint(1,22)
					while item == item_one or item == item_two:
						item = random.randint(1,22)
					keyboard = types.InlineKeyboardMarkup(row_width=3)
					callback_button1 = types.InlineKeyboardButton(text = 'Замена 1️⃣',callback_data = 'item ' + str(message.from_user.id) + ' 1 ' + str(item))
					callback_button2 = types.InlineKeyboardButton(text = 'Замена 2️⃣',callback_data = 'item ' + str(message.from_user.id) + ' 2 ' + str(item))
					callback_button3 = types.InlineKeyboardButton(text = 'Не менять 🆗',callback_data = 'dont ' + str(message.from_user.id))
					keyboard.add(callback_button1,callback_button2)
					keyboard.add(callback_button3)
					item_phot = item_list[item][1]
					txt = 'Внутри коробки вы нашли странную вещь. ' + nam + ', однако, сочла её красивой и захотела надеть. Выбери какой предмет гардероба заменить:\n\n' + item_list[item_one][0] + '\n\n' + item_list[item_two][0]
					if gender == 1:
						txt = 'Внутри коробки вы нашли странную вещь. ' + nam + ', однако, сочёл её красивой и захотел надеть. Выбери какой предмет гардероба заменить:\n\n' + item_list[item_one][0] + '\n\n' + item_list[item_two][0]
					m = bot.send_photo(message.chat.id,photo = item_phot, caption = txt,reply_markup=keyboard)
					schedule.every(DELETE_MINUTES).minutes.do(job_delete,bot,m.chat.id,m.id)
				else:
					bot.send_message(message.chat.id, 'У тебя нет этого предмета либо его нельзя использовать, заебал короче')
					return
	 
				cursor.execute(f"UPDATE neko SET inventory = '{pack(inventory)}' WHERE id = {message.from_user.id}")    
		elif first_word == 'создать':
				if baza < 2:
					bot.send_message(message.chat.id,'На твоей базе нет верстака ебанат')
					return
				args = words
				if len(args) < 2:
					bot.send_message(message.chat.id,'Еблана ты кусок, после создать нужно писать название предмета')
					return
				args.pop(0)
				item_name = ' '.join(args)
				if item_name == 'штаны за 40 гривень' and coins >= 40:
					coins -= 40
					inventory['armor1'] += 1
					bot.send_message(message.chat.id, nam + ' определённо полюбит эту странную хуйню')
					bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEJndtkp3igBN0XtV3Fe_PqX-gRl4qS2wACSQ8AAt46WUgVZwAB2AjTbT8vBA')
				elif item_name == 'костюм горничной' and inventory['carton'] >= 5:
					inventory['carton'] -= 5
					inventory['armor2'] += 1
					bot.send_message(message.chat.id, nam + ' определённо полюбит эту странную хуйню')
					bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEJndtkp3igBN0XtV3Fe_PqX-gRl4qS2wACSQ8AAt46WUgVZwAB2AjTbT8vBA')
				elif item_name == 'куртка санса' and inventory['carton'] >= 10 and inventory['bone'] >= 5:
					inventory['carton'] -= 10
					inventory['bone'] -= 5
					inventory['armor3'] += 1
					bot.send_message(message.chat.id, nam + ' определённо полюбит эту странную хуйню')
					bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEJndtkp3igBN0XtV3Fe_PqX-gRl4qS2wACSQ8AAt46WUgVZwAB2AjTbT8vBA')
				else:
					bot.send_message(message.chat.id, 'Еблан, такой предмет нельзя скрафтить или у тебя недостаточно ресурсов для этого')
					return
				cursor.execute(f"UPDATE neko SET inventory = '{pack(inventory)}',coins = {coins} WHERE id = {message.from_user.id}")  
		elif cmd == 'починить':
				if baza < 2:
					bot.send_message(message.chat.id,'На твоей базе нет верстака хуила')
					return
				if equipped == 0:
					bot.send_message(message.chat.id,'А чинить то и нечего блять')
					return
				if (equipped % 100) == 10:
					bot.send_message(message.chat.id,'Шмот не бит не крашен, нахуя его чинить')
					return
				if inventory['carton'] < 1:
					bot.send_message(message.chat.id,'А чинить то и нечем ебать')
					return
				inventory['carton'] -= 1
				equipped = equipped - (equipped % 100) + 10
				cursor.execute(f"UPDATE neko SET equipped = {equipped}, inventory = '{pack(inventory)}' WHERE id = {message.from_user.id}")
				bot.send_message(message.chat.id,'Вау, тебе правда удалось починить эту хуйню')
				bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFOCFix4kIdkWwblTRCUvuw5oM3e3UQwACQRoAAvMOqEi2-xyG-vtxfCkE')
		elif first_word == 'донат':
			try:
				args = words
				if len(args) < 3:
					raise Exception("Эта команда не так работает, иди нахуй короче")
				args.pop(0)
				count = 0
				try:
					count = int(args[-1])
				except:
					raise Exception("Хуйню написал")
				if count <= 0:
					raise Exception("А ловко ты это придумал")
				args.pop(-1)
				item_name = ' '.join(args)
				if message.from_user.id == 1087968824:
					raise Exception("С анонимного акка нельзя")
				if message.reply_to_message is None:
					raise Exception("Ответом на сообщение")
				idk = message.reply_to_message.from_user.id
				if idk == message.from_user.id:
					raise Exception("Ты как себе собрался перевести блять")
				data = cursor.execute(f'SELECT coins,inventory FROM neko WHERE id = {idk}')
				data = data.fetchone()
				if data is None:
					raise Exception("У этого лоха нет некодевочки")
				c2 = data[0]
				inv2 = unpack(data[1])
				if item_name == 'некогривны' and coins >= count:
					c2 += count
					coins -= count
					bot.send_message(message.chat.id,'Деньги отправлены, комиссия за услуги банка составила 100%')
					bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFOCFix4kIdkWwblTRCUvuw5oM3e3UQwACQRoAAvMOqEi2-xyG-vtxfCkE')
				elif item_name == 'вискас' and inventory['whiskas'] >= count:
					inv2['whiskas'] += count
					inventory['whiskas'] -= count
					bot.send_message(message.chat.id,'Вискас отправлен новой почтой')
					bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFOCFix4kIdkWwblTRCUvuw5oM3e3UQwACQRoAAvMOqEi2-xyG-vtxfCkE')
				elif item_name == 'монстр' and inventory['monster'] >= count:
					inv2['monster'] += count
					inventory['monster'] -= count
					bot.send_message(message.chat.id,'Монстр отправлен новой почтой, будем надеяться грузчики его не выпьют')
					bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFOCFix4kIdkWwblTRCUvuw5oM3e3UQwACQRoAAvMOqEi2-xyG-vtxfCkE')
				elif item_name == 'антипохмелин' and inventory['antipohmelin'] >= count:
					inv2['antipohmelin'] += count
					inventory['antipohmelin'] -= count
					bot.send_message(message.chat.id,'Бутыль антипохмела отправлен новой почтой')
					bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFOCFix4kIdkWwblTRCUvuw5oM3e3UQwACQRoAAvMOqEi2-xyG-vtxfCkE')
				elif item_name == 'кость санса' and inventory['bone'] >= count:
					inv2['bone'] += count
					inventory['bone'] -= count
					bot.send_message(message.chat.id,'Останки какого-то еблана отправлены новой почтой')
					bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFOCFix4kIdkWwblTRCUvuw5oM3e3UQwACQRoAAvMOqEi2-xyG-vtxfCkE')
				elif item_name == 'коробка с неко' and inventory['neko_box'] >= count:
					inv2['neko_box'] += count
					inventory['neko_box'] -= count
					bot.send_message(message.chat.id,'К счастью, новая почта не интересовалась содержимым коробки')
					bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFOCFix4kIdkWwblTRCUvuw5oM3e3UQwACQRoAAvMOqEi2-xyG-vtxfCkE')
				elif item_name == 'коробка с хорни неко' and inventory['horny_neko_box'] >= count:
					inv2['horny_neko_box'] += count
					inventory['horny_neko_box'] -= count
					bot.send_message(message.chat.id,'К счастью, новая почта не интересовалась содержимым коробки')
					bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFOCFix4kIdkWwblTRCUvuw5oM3e3UQwACQRoAAvMOqEi2-xyG-vtxfCkE')
				elif item_name == 'коробка с украшениями' and inventory['loot_box'] >= count:
					inv2['loot_box'] += count
					inventory['loot_box'] -= count
					bot.send_message(message.chat.id,'Коробка с неведомой хуйней отправлена новой почтой')
					bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFOCFix4kIdkWwblTRCUvuw5oM3e3UQwACQRoAAvMOqEi2-xyG-vtxfCkE')
				elif item_name == 'gender changer' and inventory['gender_changer'] >= count:
					inv2['gender_changer'] += count
					inventory['gender_changer'] -= count
					bot.send_message(message.chat.id,'Ужасающее устройство отправлено новой почтой')
					bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFOCFix4kIdkWwblTRCUvuw5oM3e3UQwACQRoAAvMOqEi2-xyG-vtxfCkE')
				elif item_name == 'адреналин' and inventory['adrenalin'] >= count:
					inv2['adrenalin'] += count
					inventory['adrenalin'] -= count
					bot.send_message(message.chat.id,'Адреналин отправлен новой почтой, будем надеяться грузчики его не выпьют')
					bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFOCFix4kIdkWwblTRCUvuw5oM3e3UQwACQRoAAvMOqEi2-xyG-vtxfCkE')
				elif item_name == 'картон' and inventory['carton'] >= count:
					inv2['carton'] += count
					inventory['carton'] -= count
					bot.send_message(message.chat.id,'Картон не отправлен, его по дороге съел джензила, приношу свои пошел нахуй')
					bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFOCFix4kIdkWwblTRCUvuw5oM3e3UQwACQRoAAvMOqEi2-xyG-vtxfCkE')
				elif item_name == 'штаны за 40 гривень' and inventory['armor1'] >= count:
					inv2['armor1'] += count
					inventory['armor1'] -= count
					bot.send_message(message.chat.id,'Брендовый шмот отправлен новой почтой')
					bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFOCFix4kIdkWwblTRCUvuw5oM3e3UQwACQRoAAvMOqEi2-xyG-vtxfCkE')
				elif item_name == 'костюм горничной' and inventory['armor2'] >= count:
					inv2['armor2'] += count
					inventory['armor2'] -= count
					bot.send_message(message.chat.id,'Брендовый шмот отправлен новой почтой')
					bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFOCFix4kIdkWwblTRCUvuw5oM3e3UQwACQRoAAvMOqEi2-xyG-vtxfCkE')
				elif item_name == 'куртка санса' and inventory['armor3'] >= count:
					inv2['armor3'] += count
					inventory['armor3'] -= count
					bot.send_message(message.chat.id,'Брендовый шмот отправлен новой почтой')
					bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFOCFix4kIdkWwblTRCUvuw5oM3e3UQwACQRoAAvMOqEi2-xyG-vtxfCkE')
				else:
					raise Exception("У тебя недостаточно таких предметов, иди нахуй")
				cursor.execute(f"UPDATE neko SET coins = {coins}, inventory = '{pack(inventory)}' WHERE id = {message.from_user.id}")
				cursor.execute(f"UPDATE neko SET coins = {c2}, inventory = '{pack(inv2)}' WHERE id = {idk}")
			except Exception as e:
				bot.send_message(message.chat.id,str(e))
		elif first_word == 'разобрать':
			try:
				if baza < 2:
					raise Exception("На твоей базе нет верстака")
				args = words
				if len(args) < 3:
					raise Exception("Эта команда не так работает, иди нахуй короче")
				args.pop(0)
				count = 0
				try:
					count = int(args[-1])
				except:
					raise Exception("Хуйню написал")
				if count <= 0:
					raise Exception("А ловко ты это придумал")
				args.pop(-1)
				item_name = ' '.join(args)
				if item_name == 'коробка с неко' and inventory['neko_box'] >= count:
					inventory['neko_box'] -= count
					inventory['carton'] += count*2
					bot.send_message(message.chat.id,'Говно успешно превращено в палки')
					bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFOCFix4kIdkWwblTRCUvuw5oM3e3UQwACQRoAAvMOqEi2-xyG-vtxfCkE')
				elif item_name == 'коробка с хорни неко' and inventory['horny_neko_box'] >= count:
					inventory['horny_neko_box'] -= count
					inventory['carton'] += count*3
					bot.send_message(message.chat.id,'Говно успешно превращено в палки')
					bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFOCFix4kIdkWwblTRCUvuw5oM3e3UQwACQRoAAvMOqEi2-xyG-vtxfCkE')
				elif item_name == 'коробка с украшениями' and inventory['loot_box'] >= count:
					inventory['loot_box'] -= count
					inventory['carton'] += count*3
					bot.send_message(message.chat.id,'Говно успешно превращено в палки')
					bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFOCFix4kIdkWwblTRCUvuw5oM3e3UQwACQRoAAvMOqEi2-xyG-vtxfCkE')
				else:
					raise Exception("Ебанат, такие предметы нельзя разбирать или у тебя их недостаточно")
				cursor.execute(f"UPDATE neko SET inventory = '{pack(inventory)}' WHERE id = {message.from_user.id}")
			except Exception as e:
				bot.send_message(message.chat.id,str(e))
		elif first_word == 'бой':
			args = words		
			if len(args) == 2:
				if rep < REP_ARENA:
					text = 'К сожалению, у тебя не получилось убедить некодевочку пойти с тобой на арену'
					if gender == 1:
						text = 'К сожалению, у тебя не получилось убедить некомальчика пойти с тобой на арену'
					bot.send_message(message.chat.id, text)
					bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFP2VizLFlogiFH1n3Rpg9Hki7DC1y_wACjxEAAqg6WEjqQFCw4uPiwikE')
					return
				if arena_kd > 0:
					text = 'Некодевочке нужен час чтобы подготовиться к следующему бою'
					if gender == 1:
						text = 'Некомальчику нужен час чтобы подготовиться к следующему бою'
					bot.send_message(message.chat.id, text)
					bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFP2VizLFlogiFH1n3Rpg9Hki7DC1y_wACjxEAAqg6WEjqQFCw4uPiwikE')
					return
				try:
					c = args[1]
					cost = int(c)
				except:
					bot.send_message(message.chat.id,'Чет ты хуйню написал')
					return
				if coins < cost:
					bot.send_message(message.chat.id, 'А деньги где')
					return
				if cost < 10:
					bot.send_message(message.chat.id, 'Ставка на арене от 10 некогривен')
					return
				if message.reply_to_message is None:
					bot.send_message(message.chat.id, 'Ответом на сообщение еблан')
					return
				idk = message.reply_to_message.from_user.id
				if idk == message.from_user.id:
					bot.send_message(message.chat.id, 'Ты как с собой воевать собрался')
					return
				data = cursor.execute(f'SELECT gender, chel FROM neko WHERE id = '+str(idk))
				data = data.fetchone()
				if data is None:
					bot.send_message(message.chat.id,'У этого лоха нет некодевочки')
					return
				gender = data[0]
				chel = data[1]
				keyboard = types.InlineKeyboardMarkup(row_width=2)
				callback_button1 = types.InlineKeyboardButton(text = 'Принять ✅',callback_data = 'accept ' + str(message.from_user.id) + ' ' + str(idk) + ' ' + str(cost))
				callback_button2 = types.InlineKeyboardButton(text = 'Отклонить ❌',callback_data = 'decline ' + str(message.from_user.id) + ' ' + str(idk))
				callback_button3 = types.InlineKeyboardButton(text = 'Отозвать 🚫',callback_data = 'aremove ' + str(message.from_user.id) + ' ' + str(idk))
				keyboard.add(callback_button1,callback_button2)
				keyboard.add(callback_button3)
				text = '<a href="tg://user?id='+str(idk)+'">'+str(chel)+'</a>, твоей некодевочке бросили вызов! Приймешь или зассал?\nСтавка: ' + str(cost) + ' 💰'
				if gender == 1:
					text = '<a href="tg://user?id='+str(idk)+'">'+str(chel)+'</a>, твоему некомальчику бросили вызов! Приймешь или зассал?\nСтавка: ' + str(cost) + ' 💰'
				m = bot.send_message(message.chat.id, text,reply_markup=keyboard)
				struct = struct_battle.copy()
				struct['players'] = [message.from_user.id]
				struct['one'] = message.from_user.id
				struct['two'] = idk
				struct['wait'] = int(time.time() + 360)
				struct['cost'] = cost
				struct['chat'] = message.chat.id
				struct['message'] = m.id
				db[message.from_user.id] = pack(struct)
		elif cmd == 'арена':
			text = 'Очевидно, бои некодевочек нелегальны, поэтому опустим лишние подробности. Обязательным условием проведения боя является ставка, часть которой организаторы забирают себе. На входе тебя уверили, что ещё ни одна некодевочка не умерла\nЛучшие некодевочки арены:\n\n'
			data = cursor.execute(f'SELECT name,wins FROM neko ORDER BY wins DESC LIMIT 10')
			data = data.fetchall()
			i = 0
			if data is not None:
				for d in data:
					n = d[0]
					if n == 'Некодевочка' or n == 'Некомальчик':
						n = 'Безымянная шмара'			
					if i == 0:
						text += f'🏆 <b>{n}</b>  {d[1]} ⚔️\n'
					else:
						text += f'{i+1}.  {n}  {d[1]} ⚔️\n'
					i = i + 1
			text = text + '\nТвоих побед:  ' + str(wins) + ' ⚔️'
			text = text + '\n\n<code>Бой [Ставка]</code> - бросить вызов, ответом на сообщение'
			markup = types.InlineKeyboardMarkup()
			switch_button1 = types.InlineKeyboardButton(text='Бой 🗡', switch_inline_query_current_chat = "Бой 10")
			markup.add(switch_button1)
			bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQACqQpizlI_XJiCwrzrSCYH47ZtXq9cCwACfLwxG0_FeEqC6_m0bVQSoQEAAwIAA3MAAykE',caption = text,reply_markup=markup)
		elif cmd == 'лицензия':
				markup = types.InlineKeyboardMarkup()
				switch_button1 = types.InlineKeyboardButton(text='Продлить 📆', switch_inline_query_current_chat = "Продлить")
				switch_button2 = types.InlineKeyboardButton(text='Дизайн 🌈', switch_inline_query_current_chat = "Дизайн")
				markup.add(switch_button1)
				markup.add(switch_button2)
				if licension < 0:
					status = 'Недействительна ❌'
				else:
					status = 'Действует ✅'
				text = 'Здесь ты можешь взглянуть на свою лицензию на владение некодевочкой\n<b>Статус:  ' + status + '</b>\n\n<b>Продлить</b>  —  20 💰\nВам будет выдана новая лицензия со сроком действия 5 дней\n<b>Дизайн</b>  —  100 💰\nВозможно заказать лицензию с уникальным дизайном'
				if gender == 1:
					text = 'Здесь ты можешь взглянуть на свою лицензию на владение некомальчиком\n<b>Статус:  ' + status + '</b>\n\n<b>Продлить</b>  —  20 💰\nВам будет выдана новая лицензия со сроком действия 5 дней\n<b>Дизайн</b>  —  100 💰\nВозможно заказать лицензию с уникальным дизайном'
				bot.send_photo(message.chat.id,photo = photo_licension,caption = text,reply_markup=markup)
		elif cmd == 'продлить':
				cost = 20
				if coins < cost:
					bot.send_message(message.chat.id, 'А деньги где')
					return
				coins = coins - cost 
				f = create_licension(bot,phot,photo_design,message.from_user.first_name,gender)
				m = bot.send_photo(message.chat.id, photo=f,caption = 'Вот твоя новая лицензия 🎫, не теряй её и не забывай вовремя продлевать')
				fil = m.photo[-1].file_id
				cursor.execute(f"UPDATE neko SET photo_licension = '{fil}', licension = {int(time.time() + LICENSION_TIMEOUT)}, coins = {coins} WHERE id = {message.from_user.id}")		
		elif cmd == 'войти':
			if not car:
				bot.send_message(message.chat.id, 'Тебе нужен некомобиль еблана кусок')
				return
			if inventory['monster'] <= 0:
				bot.send_message(message.chat.id, 'Тебе нужны монстры дебил')
				return
			if dungeon_kd > 0:
				d = math.ceil(dungeon_kd/3600)
				if gender == 0:
					bot.send_message(message.chat.id, f'Харош, дай отдохнуть своей некодевочке хотя бы день\n\n<i>Осталось отдыхать {d} часов </i>')
				else:
					bot.send_message(message.chat.id, f'Харош, дай отдохнуть своему некомальчику хотя бы день\n\n<i>Осталось отдыхать {d} часов </i>')
				bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFP2VizLFlogiFH1n3Rpg9Hki7DC1y_wACjxEAAqg6WEjqQFCw4uPiwikE')
				return
			if rep < REP_DUNGEON:
				text = nam + ' отказалась входить, не стоит её заставлять'
				if gender == 1:
					text = nam + ' отказался входить, не стоит его заставлять'
				bot.send_message(message.chat.id,text)
				bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLY5iwIflAaGLlpw7vXvQvEvJcWilzgACjxEAAqg6WEjqQFCw4uPiwikE')
				return
			inventory['monster'] -= 1
			equipped = minus_durability(equipped)
			cursor.execute(f"UPDATE neko SET dungeon_kd = {int(time.time() + DUNGEON_TIMEOUT + + HAPPY_TIMEOUT[get_happiness_level(happy,baza)])},inventory = '{pack(inventory)}',equipped = {equipped} WHERE id = {message.from_user.id}")
			#Дальше идёт хитровыебанный алгоритм генерации
			mas = [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]
			generation = [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]
			generator = [2,2,2,3,3,3,3,4,4,5,5,6,7,8,8,8,8,8,8]
			stack = []
			mas[0][0] = 2
			generation[0][0] = 1
			cur_x = 0
			cur_y = 0
			while True:
				found = 0
				dirs = [1,2,3,4]
				if generation[cur_y][cur_x] == 0 and len(generator) > 0:
					d = random.choice(generator)
					generator.remove(d)
					generation[cur_y][cur_x] = d
				while len(dirs) != 0:
					d = random.choice(dirs)
					dirs.remove(d)
					if d == 1:
						if (cur_y-3) >= 0:
							if mas[cur_y-3][cur_x] == 0:
								mas[cur_y-1][cur_x] = 1
								mas[cur_y-2][cur_x] = 1
								stack.append(str(cur_x) + ' ' + str(cur_y))
								cur_y = cur_y - 3
								mas[cur_y][cur_x] = 2
								found = 1
								break
					if d == 2:
						if (cur_x+3) < len(mas[cur_y]):
							if mas[cur_y][cur_x+3] == 0:
								mas[cur_y][cur_x+1] = 1
								mas[cur_y][cur_x+2] = 1
								stack.append(str(cur_x) + ' ' + str(cur_y))
								cur_x = cur_x + 3
								mas[cur_y][cur_x] = 2
								found = 1
								break
					if d == 3:
						if (cur_y+3) < len(mas):
							if mas[cur_y+3][cur_x] == 0:
								mas[cur_y+1][cur_x] = 1
								mas[cur_y+2][cur_x] = 1
								stack.append(str(cur_x) + ' ' + str(cur_y))
								cur_y = cur_y + 3
								mas[cur_y][cur_x] = 2
								found = 1
								break
					if d == 4:
						if (cur_x-3) >= 0:
							if mas[cur_y][cur_x-3] == 0:
								mas[cur_y][cur_x-1] = 1
								mas[cur_y][cur_x-2] = 1
								stack.append(str(cur_x) + ' ' + str(cur_y))
								cur_x = cur_x - 3
								mas[cur_y][cur_x] = 2
								found = 1
								break
				if found == 1:
					continue
				else:
					if len(stack) == 0:
						break
					st = stack[len(stack)-1]
					stack.remove(st)
					args = st.split()
					cur_x = int(args[0])
					cur_y = int(args[1])
			mas[0][1] = 1
			mas[0][2] = 1
			mas[1][0] = 1
			mas[2][0] = 1
			mas[0][0] = 3
			maptxt = map_text(mas)
			print(mas)
			keyboard = types.InlineKeyboardMarkup(row_width=5)
			dungeon_keyboard(keyboard,message.from_user.id)
			text = nam + ' сразу же почуствовала прохладу и сырость, а её нога вступила во что-то мокрое. Да это же огромная пещера! Исходящее отовсюду разноцветное свечение прогоняет темноту даже с самых отдалённых уголков\n\n' + '0 💰   0 🍫   0 ⚡️   0 🍼\n'+maptxt
			if gender == 1:
				text = nam + ' сразу же почуствовал прохладу и сырость, а его нога вступила во что-то мокрое. Да это же огромная пещера! Исходящее отовсюду разноцветное свечение прогоняет темноту даже с самых отдалённых уголков\n\n' + '0 💰   0 🍫   0 ⚡️   0 🍼\n'+maptxt
			m = bot.send_photo(message.chat.id,photo = 'AgACAgIAAx0CZQN7rQACwxZi8uNUoMtUGP6J96D7X-pveAGj3wAC374xGxy_mEsWdB1RBPi4nQEAAwIAA3MAAykE',caption = text,reply_markup=keyboard)
			struct = struct_dungeon.copy()
			struct['players'] = [message.from_user.id]
			struct['map'] = mas
			struct['message'] = m.id
			struct['chat'] = message.chat.id
			struct['wait'] = int(time.time() + 1800)
			struct['generation'] = generation
			struct['hp'] = get_hp(equipped)
			struct['maxhp'] = get_hp(equipped)
			struct['name'] = nam
			struct['gender'] = gender
			struct['skills'] = [skill1,skill2]
			db[message.from_user.id] = pack(struct)
		elif cmd == 'сразиться':
			if not car:
				bot.send_message(message.chat.id, 'Тебе нужен некомобиль еблана кусок')
				return
			if inventory['monster'] < 1:
				bot.send_message(message.chat.id, 'Тебе нужны монстры дебил')
				return
			if boss_kd > 0:
				d = math.ceil(boss_kd/3600)
				if gender == 0:
					bot.send_message(message.chat.id, f'Харош, дай отдохнуть своей некодевочке хотя бы день\n\n<i>Осталось отдыхать {d} часов </i>')
				else:
					bot.send_message(message.chat.id, f'Харош, дай отдохнуть своему некомальчику хотя бы день\n\n<i>Осталось отдыхать {d} часов </i>')
				bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFP2VizLFlogiFH1n3Rpg9Hki7DC1y_wACjxEAAqg6WEjqQFCw4uPiwikE')
				return
			if rep < REP_BOSS:
				text = nam + ' зассала браться за это дело'
				if gender == 1:
					text = nam + ' зассал браться за это дело'
				bot.send_message(message.chat.id,text)
				bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFLY5iwIflAaGLlpw7vXvQvEvJcWilzgACjxEAAqg6WEjqQFCw4uPiwikE')
				return
			keyboard = types.InlineKeyboardMarkup(row_width=2)
			callback_button1 = types.InlineKeyboardButton(text = 'Присоединиться ➕',callback_data = 'bjoin ' + str(message.from_user.id))
			callback_button2 = types.InlineKeyboardButton(text = 'Старт ✅',callback_data = 'bstart ' + str(message.from_user.id))
			callback_button3 = types.InlineKeyboardButton(text = 'Отмена ❌',callback_data = 'bend ' + str(message.from_user.id))
			keyboard.add(callback_button1)
			keyboard.add(callback_button2,callback_button3)
			m = bot.send_message(message.chat.id, text = 'Идёт набор в тиму для легендарной пизделки с боссом\n\nВход 1 ⚡️, 120 💞\n<b>Игроков: 1</b>',reply_markup=keyboard)
			struct = struct_boss.copy()
			struct['players'] = [message.from_user.id]
			struct['wait'] = int(time.time() + 600)
			struct['chat'] = m.chat.id
			struct['message'] = m.id
			db[message.from_user.id] = pack(struct)
		elif cmd == 'портал' or cmd == 'данж':
			text = f'Это военный объект, но благодаря связям тебе удалось попасть сюда. Место, куда ведёт портал, принятно называть LGBT миром, и про него практически ничего неизвестно. Попасть туда могут только некодевочки с некомальчиками, обычные же люди даже не могут прикоснуться к порталу. К тому же, последняя исследовательская экспедиция считается пропавшей без вести\n\nУспешных забегов:  {dungeon_raids} 🏳️‍🌈'
			markup = types.InlineKeyboardMarkup()
			switch_button1 = types.InlineKeyboardButton(text='Войти 🏳️‍🌈', switch_inline_query_current_chat = "Войти")
			switch_button2 = types.InlineKeyboardButton(text='Гайд 📖', switch_inline_query_current_chat = "Гайд данж")
			markup.add(switch_button1,switch_button2)
			bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQACsRxi5CVwxElzGR26h0_tTvU6R5cFmAACHb8xG38aIEs12xAgGvf_ugEAAwIAA3MAAykE',caption = text,reply_markup=markup)
		elif cmd == 'босс':
			text = f'Некославия полна секретных лабораторий. В одной из таких проводился эксперимент по облучению некочанов ЛГБТ лучами, и образец №228 нарушил условия содержания. Правительство пообещало награду тому или тем, кто сможет дать ему пизды\n\nУспешных забегов:  {boss_raids} ☠️'
			markup = types.InlineKeyboardMarkup()
			switch_button1 = types.InlineKeyboardButton(text='Сразиться ☠️', switch_inline_query_current_chat = "Сразиться")
			switch_button2 = types.InlineKeyboardButton(text='Гайд 📖', switch_inline_query_current_chat = "Гайд босс")
			markup.add(switch_button1,switch_button2)
			bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQABAbGMZO0Qo8-OWNaBEGfKvxdDLtFhrsEAArzLMRvylGlLz6rcLB4h3QsBAAMCAANzAAMwBA',caption = text,reply_markup=markup)
		elif cmd == 'казино':
			text = 'Чтобы не платить деньги, казино Некославии часто предлагают в качестве выигрыша некодевочек и прочий мусор. Это, базирующееся в глубинах подвала твоего дома, не оказалось исключением. Способов проебать зарплату здесь не так уж и много\n\n<b>Слоты 🎰</b>\nПуск за 10 некогривен. Запусти слоты и попытай удачу если не зассал\n<b>Покер 🃏</b>\nИгра от 20 некогривен. Сыграй с такими же полупокерами как ты'
			markup = types.InlineKeyboardMarkup()
			switch_button1 = types.InlineKeyboardButton(text='Слоты 🎰', switch_inline_query_current_chat = "Пуск")
			switch_button2 = types.InlineKeyboardButton(text='Покер 🃏', switch_inline_query_current_chat = "Покер")
			switch_button3 = types.InlineKeyboardButton(text = 'Комбинации ❓',callback_data = 'comb ' + str(message.from_user.id))
			markup.add(switch_button1,switch_button3)
			markup.add(switch_button2)
			bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQACsadi5sd8T9_OueoaHagCng-OXhWKYQACmrsxG5NIMEuXRTxWMN6TQwEAAwIAA3MAAykE',caption = text,reply_markup=markup)
		elif cmd == 'верстак': 
			if baza < 2:
				bot.send_message(message.chat.id,'На твоей базе нет верстака, охуеть да?')
				return
			keyboard = types.InlineKeyboardMarkup(row_width=2)
			callback_button1 = types.InlineKeyboardButton(text = '⬅️ Разборка',callback_data = f'wikicraft {message.from_user.id} 1 {gender}')
			callback_button2 = types.InlineKeyboardButton(text = 'Починка ➡️',callback_data = f'wikicraft {message.from_user.id} 2 {gender}')
			keyboard.add(callback_button1,callback_button2)
			text = 'Используя это инновационное устройство на своей базе, ты можешь создавать стильную одежду для своей некодевочки, которая повысит её живучесть в бою'
			if gender == 1:
				text = 'Используя это инновационное устройство на своей базе, ты можешь создавать стильную одежду для своего некомальчика, которая повысит его живучесть в бою'
			text += '\n\n👖 Штаны за 40 гривень\nРецепт:  💰 Некогривны × 40\nХарактеристики:  +1 макс хп 💗\n\n👗 Костюм горничной\nРецепт:  📦 Картон × 5\nХарактеристики:  +2 макс хп 💗\n\n🦺 Куртка санса\nРецепт:  📦 Картон × 10 | 🦴 Кость санса × 5\nХарактеристики:  +4 макс хп 💗\n\n<code>Создать [назв]</code><i> - скрафтить указанный предмет</i>'
			m = bot.send_photo(message.chat.id, photo = 'AgACAgIAAx0CZQN7rQABAR65ZKYfNZQGIfOkltcTbpV6pEUaPwUAArvMMRsoDDFJwbOoTQHZinsBAAMCAANzAAMvBA',caption = text,reply_markup=keyboard)
			schedule.every(DELETE_MINUTES).minutes.do(job_delete,bot,m.chat.id,m.id)
		elif cmd == 'пуск' or cmd == 'слоты':
			cost = 10
			if coins < cost:
				bot.send_message(message.chat.id, 'А деньги где')
				return
			coins = coins - cost
			mas = ['🍉','🍓','🍒','🍋']
			first = random.choice(mas)
			second = random.choice(mas)
			third = random.choice(mas)
			text = 'Ты ничего не выиграл, лох'
			if first == '🍒' and second == '🍒' and third == '🍒':
				text = 'Ты выиграл целых 70 некогривен 💰, мои поздравления!'
				coins = coins + 80
			elif first == '🍓' and second == '🍓' and third == '🍓':
				text = 'Ты выиграл целых 50 некогривен 💰, мои поздравления!'
				coins = coins + 60
			elif first == '🍉' and second == '🍉' and third == '🍉':
				text = 'Ты выиграл целых 120 некогривен 💰, мои поздравления!'
				coins = coins + 130
			elif first == '🍋' and second == '🍋' and third == '🍋':
				text = 'Ты выиграл коробку с уникальной некодевочкой 🎁! Конечно, тебе решать, что делать с её содержимым'
				coins = coins + 10
				inventory['horny_neko_box'] += 1
			elif first == second == '🍓' or second == third == '🍓': #or first == third == '🍓'
				text = 'Ты выиграл 10 некогривен 💰, это мало, но лучше чем ничего'
				coins = coins + 20
			elif first == second == '🍒' or second == third == '🍒': #  or first == third == '🍒'
				text = 'Ты выиграл 10 некогривен 💰, это мало, но лучше чем ничего'
				coins = coins + 20
			elif first == second == '🍉' or second == third == '🍉': # or first == third == '🍉'
				text = 'Ты вышел в ноль, попробуй ещё раз если не ссыкло'
				coins = coins + 10
			elif first == second == '🍋' or second == third == '🍋': # or first == third == '🍉'
				text = 'Ты вышел в ноль, попробуй ещё раз если не ссыкло'
				coins = coins + 10
			cursor.execute(f"UPDATE neko SET inventory = '{pack(inventory)}', coins = {coins} WHERE id = {message.from_user.id}")
			markup = types.InlineKeyboardMarkup()
			switch_button2 = types.InlineKeyboardButton(text='Пуск 🎰', switch_inline_query_current_chat = "Пуск")
			markup.add(switch_button2)
			key = first + ' ' + second + ' ' + third
			f = casino_pics[key]
			bot.send_photo(message.chat.id, photo = f,caption = text,reply_markup=markup)
		elif cmd == 'гайд бои':
			text = guide_text[0]
			bot.send_message(message.chat.id, text)
		elif cmd == 'гайд данж':
			text = guide_text[1]
			bot.send_message(message.chat.id, text)
		elif cmd == 'гайд босс':
			text = guide_text[2]
			bot.send_message(message.chat.id, text)
		elif cmd == 'покер':
				minbet = 1
				if coins < minbet*5:
					bot.send_message(message.chat.id, 'А деньги где бомжара')
					return
				keyboard = poker_init_keyboard(message.from_user.id)
				m = bot.send_message(message.chat.id, text = f'Вход от {5*minbet} 💰',reply_markup=keyboard)
				struct = struct_poker.copy()
				struct['players'] = [message.from_user.id]
				struct['names'] = [nam]
				struct['bank'] = [minbet]
				struct['money'] = [coins]
				struct['wait'] = int(time.time() + 420)
				struct['chat'] = message.chat.id
				struct['message'] = m.id
				struct['minbet'] = minbet
				db[message.from_user.id] = pack(struct)
		elif first_word == 'фото':
				args = words
				a = int(args[1])
				i = int(args[2])
				if a == 0:
					bot.send_photo(message.chat.id, photo = photos[i])
				elif a == 1:
					bot.send_photo(message.chat.id, photo = elite_photos[i])
				elif a == 2:
					bot.send_photo(message.chat.id, photo = ero_photos[i])
				elif a == 3:
					bot.send_photo(message.chat.id, photo = trap_photos[i])
		elif cmd == 'покрасить базу' or cmd == 'покрасить машину' or cmd == 'дизайн':
			bot.send_message(message.chat.id, 'Нужно скинуть фото, написав в описании к нему эту команду')
			return
		elif first_word == '!set':
			if message.reply_to_message is None:
				bot.send_message(message.chat.id, 'Ответом на сообщение')
				return
			if message.from_user.id != ME_CHATID:
				bot.send_message(message.chat.id, 'Лол нет')
				return
			try:
				args = message.text.split()
				column = args[1]
				value = args[2]
				cursor.execute(f"UPDATE neko SET " + column + " = " + value + " WHERE id = " + str(message.reply_to_message.from_user.id))
				bot.send_message(message.chat.id, 'Допустим')
			except Exception as e:
				bot.send_message(message.chat.id, e)

def msg_photo(message,bot):
		cursor = bot.cursor

		if message.chat.id == SERVICE_CHATID:
			bot.send_message(message.chat.id,str(message.photo[-1].file_id) + ' ' + str(message.photo[-1].file_size) + ' ' + bot.get_file_url(message.photo[-1].file_id), reply_to_message_id=message.message_id)
		if message.caption is not None:
			message.caption = message.caption.replace('@NekoslaviaBot','')
			message.caption = message.caption.strip()
			cmd = message.caption.lower()
			
			if cmd not in cmd_photo:
				return
			if flood_counter_plus(bot,message):
				return
				
			data = cursor.execute(f'SELECT * FROM neko WHERE id = {message.from_user.id}')
			data = data.fetchone()
			if data is None:
				return      
			phot = data[5]
			bolnitsa = int(data[6] - time.time())
			base = data[8]
			car = data[9]
			event = data[10]
			coins = data[11]
			licension = data[23]
			gender = data[30]
			new_phot = data[33]
			base_buy = data[40]
			mobile_buy = data[41]
			licension_buy = data[42]
			if new_phot is not None:
				phot = new_phot

			if cmd == 'покрасить базу':
				if base < 7:
					bot.send_message(message.chat.id, 'Нужна база максимального уровня хуила')
					return
				if not base_buy:
					cost = 100
					if coins < cost:
						bot.send_message(message.chat.id, 'А деньги где')
						return
					coins = coins - cost
					txt = 'Ты успешно нанял таджиков, которые покрасили тебе стены. Можешь любоваться результатом\n\n<i>Плата в 100 некогривен снимается только первый раз, дальше бесплатно</i>'
				else:
					txt = 'Ты успешно нанял таджиков, которые покрасили тебе стены. Можешь любоваться результатом'
				bot.send_message(message.chat.id,txt)
				bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFOCFix4kIdkWwblTRCUvuw5oM3e3UQwACQRoAAvMOqEi2-xyG-vtxfCkE')

				im1 = get_pil(bot,message.photo[-1].file_id)
				im1 = img_resize(im1,1000,667)
				im0 = Image.new(mode = 'RGB',size = (1000,667))
				im0.paste(im1.convert('RGB'), (0,0))
				imcopy = im0.copy()
				with Image.open('bot/base/rm228.png') as im2:
					im0.paste(im2.convert('RGB'), (0,0), im2)
				m = bot.send_photo(ME_CHATID, photo=send_pil(im0))
				photo_base = m.photo[-1].file_id
				
				with Image.open('bot/base/rm229.png') as im2:
					imcopy.paste(im2.convert('RGB'), (0,0), im2)
				m = bot.send_photo(ME_CHATID, photo=send_pil(imcopy))
				photo_debil = m.photo[-1].file_id
			
				cursor.execute(f"UPDATE neko SET coins = {coins}, base_buy = TRUE, photo_base = '{photo_base}', photo_debil = '{photo_debil}' WHERE id = {message.from_user.id}")
				
			elif cmd == 'покрасить машину':
				if not car:
					bot.send_message(message.chat.id, 'Тебе нужен некомобиль ебанько')
					return
				if not mobile_buy:
					cost = 100
					if coins < cost:
						bot.send_message(message.chat.id, 'А деньги где')
						return
					coins = coins - cost
					txt = 'Ты успешно нанял таджиков, которые покрасили тебе машину. Можешь любоваться результатом\n\n<i>Плата в 100 некогривен снимается только первый раз, дальше бесплатно</i>'
				else:
					txt = 'Ты успешно нанял таджиков, которые покрасили тебе машину. Можешь любоваться результатом'
				bot.send_message(message.chat.id,txt)
				bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFOCFix4kIdkWwblTRCUvuw5oM3e3UQwACQRoAAvMOqEi2-xyG-vtxfCkE')
				im1 = get_pil(bot,message.photo[-1].file_id)
				im1 = img_resize(im1,480,240)
				im3 = Image.new(mode = 'RGB',size = (800,534))
				im3.paste(im1.convert('RGB'), (147,211))
				im1 = im3
				with Image.open('bot/base/garag228.png') as im2:
					im1.paste(im2.convert('RGB'), (0,0), im2)
				m = bot.send_photo(ME_CHATID, photo=send_pil(im1))
				photo_mobile = m.photo[-1].file_id
				cursor.execute(f"UPDATE neko SET coins = {coins}, mobile_buy = TRUE, photo_mobile = '{photo_mobile}' WHERE id = {message.from_user.id}") 
			elif cmd == 'дизайн':    
				if not licension_buy:
					cost = 100
					if coins < cost:
						bot.send_message(message.chat.id, 'А деньги где')
						return
					coins = coins - cost
					txt = 'Ты успешно заказал лицензию со своим дизайном. Можешь любоваться результатом\n\n<i>Плата в 100 некогривен снимается только первый раз, дальше бесплатно</i>'
				else:
					txt = 'Ты успешно заказал лицензию со своим дизайном. Можешь любоваться результатом'
				bot.send_message(message.chat.id,txt)
				bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFOCFix4kIdkWwblTRCUvuw5oM3e3UQwACQRoAAvMOqEi2-xyG-vtxfCkE')
				
				fil2 = message.photo[-1].file_id
				f = create_licension(bot,phot,fil2,message.from_user.first_name,gender,licension)
				m = bot.send_photo(ME_CHATID, photo=f)
				fil = m.photo[-1].file_id
				cursor.execute(f"UPDATE neko SET coins = {coins}, licension_buy = TRUE, photo_licension = '{fil}', photo_design = '{fil2}' WHERE id = {message.from_user.id}")
			
			