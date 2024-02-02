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

def callback_get(call,bot):
	blocked_messages = bot.antiflood['blocked_messages']
	blocked_users = bot.antiflood['blocked_users']

	strkey = f'{call.message.chat.id} {call.message.message_id}'
	if strkey in blocked_messages or call.from_user.id in blocked_users:
		answer_callback_query(bot,call,'Подожди заебал')
		return
	blocked_messages.append(strkey)
	blocked_users.append(call.from_user.id)
	try:
		callback_process(call,bot)
	finally:
		blocked_messages.remove(strkey)
		blocked_users.remove(call.from_user.id)
		
def callback_process(call,bot):
	cursor = bot.cursor
	db = bot.db
	today_text = bot.zavod['today_text']
	patch_version = bot.gazeta['patch_version']
	patch_image = bot.gazeta['patch_image']

	cmd_for_many = ['decline','accept','pvp','pjoin','bjoin','buy','poker','hand','boss']
	cmd_for_db = [
	'pplus','pminus','pcontinue','poker','pjoin','pstart','hand',
	'paper',
	'move','pve','interact','back',
	'bend','bjoin','bstart','bcontinue','buy','boss',
	'decline','accept','aremove','pvp'
	]
	args = call.data.split()
	cmd = args[0]
	if cmd == "no" or cmd == "nothing":
		answer_callback_query(bot,call,'Хуйню нажал')
		return
	idk = int(args[1])
	key = idk
	if call.from_user.id != idk and cmd not in cmd_for_many:
		answer_callback_query(bot,call,'Пашол нахуй')
		return
	if key not in db.keys() and cmd in cmd_for_db:
		answer_callback_query(bot,call,'Чет хуйня какая-то')
		txt = 'В связи хуй знает с чем данные были утеряны и эта штука больше не работает'
		if call.message.text is not None:
			bot.edit_message_text(text=txt, chat_id=call.message.chat.id, message_id=call.message.message_id)
		elif call.message.caption is not None:
			bot.edit_message_caption(caption=txt, chat_id=call.message.chat.id, message_id=call.message.message_id)
		print(db.keys())
		return
	data = cursor.execute(f'SELECT event,bolnitsa FROM neko WHERE id = {call.from_user.id}')
	data = data.fetchone()
	if data is None:
		answer_callback_query(bot,call,'У тебя нет некодевочки')
		return
	event = data[0]
	bolnitsa = int(data[1] - time.time())
	if event > 0:
		answer_callback_query(bot,call,'Ты гуляешь')
		return
	if bolnitsa > 0:
		answer_callback_query(bot,call,'Ты в больнице')
		return
	
	if cmd == "decline":
		one = int(args[1])
		two = int(args[2])
		if call.from_user.id != two:
			answer_callback_query(bot,call,'Пашол нахуй')
			return
		del db[key]
		answer_callback_query(bot,call,'Успешно')
		chel = html.escape(call.from_user.first_name, quote = True)
		txt = '<a href="tg://user?id='+str(two)+'">'+str(chel)+'</a> оказался ссыклом...'
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=txt)
	elif cmd == "aremove":
		one = int(args[1])
		two = int(args[2])
		answer_callback_query(bot,call,'Успешно')
		del db[key]
		bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
	elif cmd == "accept":
		one = int(args[1])
		two = int(args[2])
		cost = int(args[3])
		if call.from_user.id != two:
			answer_callback_query(bot,call,'Пашол нахуй')
			return
		if check_all(bot, call.from_user.id) is not None :
			answer_callback_query(bot,call,check_all(bot, call.from_user.id))
			return
		struct = unpack(db[key])
		data = cursor.execute(f'SELECT * FROM neko WHERE id = {one}')
		data = data.fetchone()
		nam1 = data[1]
		phot1 = data[5]
		new_phot = data[33]
		if new_phot is not None:
			phot1 = new_phot
		skill1 = data[27]
		skill2 = data[28]
		gender1 = data[30]
		inv1 = unpack(data[36])
		bone_automate1 = data[37]
		equipped1 = data[38]
		skills1 = [skill1,skill2]

		data = cursor.execute(f'SELECT * FROM neko WHERE id = ' + str(call.from_user.id))
		data = data.fetchone()
		rep2 = data[2]
		nam2 = data[1]
		arena_kd2 = int(data[16] - time.time())
		c2 = data[11]
		phot2 = data[5]
		new_phot = data[33]
		if new_phot is not None:
			phot2 = new_phot
		skill1 = data[27]
		skill2 = data[28]
		gender2 = data[30]
		inv2 = unpack(data[36])
		bone_automate2 = data[37]
		equipped2 = data[38]
		skills2 = [skill1,skill2]
		if rep2 < 20:
			txt = 'Некодевочка недостаточно доверяет тебе'
			if gender2 == 1:
				txt = 'Некомальчик недостаточно доверяет тебе'
			answer_callback_query(bot,call,txt)
			return
		if arena_kd2 > 0:
			txt = 'Некодевочка не готова'
			if gender2 == 1:
				txt = 'Некомальчик не готов'
			answer_callback_query(bot,call,txt)
			return
		if c2 < cost:
			answer_callback_query(bot,call,'А деньги где')
			return
		answer_callback_query(bot,call,'Успешно')
		
		use_bones1 = 0
		if bone_automate1 and inv1['bone'] > 0:
			use_bones1 = 1
			inv1['bone'] -= 1
		use_bones2 = 0
		if bone_automate2 and inv2['bone'] > 0:
			use_bones2 = 1
			inv2['bone'] -= 1
		maxhp1 = get_hp(equipped1)
		hp1 = maxhp1
		maxhp2 = get_hp(equipped2)
		hp2 = maxhp2
		equipped1 = minus_durability(equipped1)
		equipped2 = minus_durability(equipped2)
		cursor.execute(f"UPDATE neko SET arena_kd = {int(time.time() + BATTLE_TIMEOUT)},equipped  = {equipped1}, inventory = '{pack(inv1)}' WHERE id = {one}")
		cursor.execute(f"UPDATE neko SET arena_kd = {int(time.time() + BATTLE_TIMEOUT)},equipped  = {equipped2}, inventory = '{pack(inv2)}' WHERE id = {call.from_user.id}")

		field1 = generate_field(skills1)
		field2 = generate_field(skills2)
		im1 = get_pil(bot,phot1)
		im1 = img_resize(im1,781,800)
		im3 = Image.new(mode = 'RGB',size = (781,800))
		im3.paste(im1.convert('RGB'), (0,0))
		im1 = im3
		if use_bones2 > 0:
			filenam = 'bot/battle/bone_hands.png'
		else:
			filenam = 'bot/battle/hands.png'
		with Image.open(filenam) as im2:
			im1.paste(im2.convert('RGBA'), (0,0),im2)
		m = bot.send_photo(ME_CHATID, photo=send_pil(im1))
		image1 = m.photo[-1].file_id
		
		im1 = get_pil(bot,phot2)
		im1 = img_resize(im1,781,800)
		im3 = Image.new(mode = 'RGB',size = (781,800))
		im3.paste(im1.convert('RGB'), (0,0))
		im1 = im3
		if use_bones1 > 0:
			filenam = 'bot/battle/bone_hands.png'
		else:
			filenam = 'bot/battle/hands.png'
		with Image.open(filenam) as im2:
			im1.paste(im2.convert('RGBA'), (0,0),im2)
		m = bot.send_photo(ME_CHATID, photo=send_pil(im1))
		image2 = m.photo[-1].file_id
		struct['players'].append(two)
		struct['event'] = 1
		struct['wait'] = int(time.time()+1200)
		struct['bone_one'] = use_bones1
		struct['bone_two'] = use_bones2
		struct['imageone'] = image1
		struct['imagetwo'] = image2
		struct['nameone'] = nam1
		struct['nametwo'] = nam2
		struct['fieldone'] = field1
		struct['fieldtwo'] = field2
		db[key] = pack(struct)
		two = call.from_user.id
		txt = 'Некодевочки выйдут на арену через 15 секунд, собирайте символы по 4 в ряд чтобы поддерживать своих некодевочек с трибун\n\n🟥 🟧 - блок\n\n🟡 🟢 - атака\n\n💙 - плюс один ход'
		if gender1 == 1 or gender2 == 1:
			txt = 'Некодевочки и некомальчики выйдут на арену через 15 секунд, собирайте символы по 4 в ряд чтобы поддерживать своих неко с трибун\n\n🟥 🟧 - блок\n\n🟡 🟢 - атака\n\n💙 - плюс один ход'
		if gender1 == 1 and gender2 == 1:
			txt = 'Некомальчики выйдут на арену через 15 секунд, собирайте символы по 4 в ряд чтобы поддерживать своих некомальчиков с трибун\n\n🟥 🟧 - блок\n\n🟡 🟢 - атака\n\n💙 - плюс один ход'
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=txt)
		b = [one,two]
		turn = random.choice(b)
		if turn == one:
			field = field1
			skills = skills1
			hpbal = hp1 <= hp2
		else:
			field = field2
			skills = skills2
			hpbal = hp2 <= hp1
		blocks1 = 0
		blocks2 = 0
		turns = get_player_turns(skills,hpbal,1)
		
		keyboard = types.InlineKeyboardMarkup(row_width=6)
		dat = 'pvp ' + str(one) + ' ' + str(two) + ' ' + str(turn) + ' ' + str(hp1) + ' ' + str(hp2) + ' ' + str(maxhp1) + ' ' + str(maxhp2) + ' ' + str(turns) + ' ' + str(blocks1) + ' ' + str(blocks2)
		field_keyboard(keyboard,dat,field,1,1,skills)
		txt = pvp_text(nam1,nam2,maxhp1,maxhp2,hp1,hp2,0,0,skills1,skills2)
		if turn == one:
			nam = nam1
		else:
			nam = nam2
		txt = txt + 'Ходит <a href="tg://user?id='+str(turn)+'">'+str(nam)+'</a>\n'
		txt = txt + 'Осталось ходов до атаки врага:  ' + str(turns)
		time.sleep(15)
		if turn == one:
			image = image2
		else:
			image = image1
		m = bot.send_photo(call.message.chat.id, photo=image,caption = txt,reply_markup=keyboard)
		bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
		struct['event'] = 2
		struct['message'] = m.id
		struct['skillone'] = skills1
		struct['skilltwo'] = skills2
		db[key] = pack(struct)
	elif cmd == "pvp":
		one = int(args[1])
		turn = int(args[3])
		hp1 = int(args[4])
		hp2 = int(args[5])
		maxhp1 = int(args[6])
		maxhp2 = int(args[7])
		turns = int(args[8])
		blocks1 = int(args[9])
		blocks2 = int(args[10])
		pos = int(args[11])
		rer1 = int(args[12])
		rer2 = int(args[13])
		if call.from_user.id != turn:
			answer_callback_query(bot,call,'Не твой ход')
			return
		struct = unpack(db[key])
		cost = struct['cost']
		field1 = struct['fieldone']
		field2 = struct['fieldtwo']
		selected = struct['selected']
		nam1 = struct['nameone']
		nam2 = struct['nametwo']
		image1 = struct['imageone']
		image2 = struct['imagetwo']
		skills1 = struct['skillone']
		skills2 = struct['skilltwo']
		bone1 = struct['bone_one']
		bone2 = struct['bone_two']
		starter = struct['starter']
		atack = 0
		ability = 0
		if turn == one:
			field = field1
			skills = skills1
			hp = hp1
			maxhp = maxhp1
		else:
			field = field2
			skills = skills2
			hp = hp2
			maxhp = maxhp2
		if pos < 0:
			ability = abs(pos)
			result = use_skill(bot,ability,selected,call,field) 
			if result[0] == -1:
				return
			selected = -1
			atack += result[1]
			if turn == one:
				blocks1 += result[2]
			else:
				blocks2 += result[2]
			turns += result[3]
		else:
			result = change_figures(bot,selected,pos,call,field)
			if result[0] == -1:
				selected = result[1]
			else:
				turns -= 1
				selected = -1

		result = field_calculate(field,skills,True)
		atack += result[0]
		turns += result[2]
		if turn == one:
			blocks1 += result[1]
			hp1 += result[3]
			if hp1 > maxhp1:
				hp1 = maxhp1
			if blocks1 > 3:
				blocks1 = 3
			atack = get_player_damage(skills,hp,maxhp,atack,turns,blocks1)
		else:
			blocks2 += result[1]
			hp2 += result[3]
			if hp2 > maxhp2:
				hp2 = maxhp2
			if blocks2 > 3:
				blocks2 = 3
			atack = get_player_damage(skills,hp,maxhp,atack,turns,blocks2)
		if turn == one and atack != 0:
			prev = hp2
			hp2, blocks2 = use_player_defence(skills2,atack,blocks2,hp2,False) 
			if bone1 != 0 and prev != hp2:
				bone_atack(field2,3)
			if hp2 <= 0:
					txt = pvp_text(nam1,nam2,maxhp1,maxhp2,hp1,hp2,blocks1,blocks2,skills1,skills2)
					bot.edit_message_caption(caption = txt, chat_id=call.message.chat.id, message_id=call.message.message_id)
					time.sleep(1)
					newcost = cost
					del db[key]
					data = cursor.execute(f'SELECT coins,wins,gender FROM neko WHERE id = {one}')
					data = data.fetchone()
					c1 = data[0]
					w1 = data[1]
					gender1 = data[2]
					c1 = c1 + newcost
					w1 = w1 + 1
					txt = 'Победила дружба, наебал, победила <a href="tg://user?id='+str(one)+'">'+str(nam1)+'</a>. Выигрыш составил ' + str(newcost) + ' 💰, владельцам арены понравился бой и они не взяли процентов. Не забудьте дать некодевочкам отдохнуть хотя бы час'
					if gender1 == 1:
						txt = 'Победила дружба, наебал, победил <a href="tg://user?id='+str(one)+'">'+str(nam1)+'</a>. Выигрыш составил ' + str(newcost) + ' 💰, владельцам арены понравился бой и они не взяли процентов. Не забудьте дать некодевочкам отдохнуть хотя бы час'
					bot.send_message(call.message.chat.id, txt )
					data = cursor.execute(f'SELECT coins FROM neko WHERE id = {two}')
					data = data.fetchone()
					c2 = data[0]
					c2 = c2 - cost
					cursor.execute(f"UPDATE neko SET wins = {w1}, coins = {c1} WHERE id = {one}")
					cursor.execute(f"UPDATE neko SET coins = {c2} WHERE id = {two}")
					return
		if turn == two and atack != 0:
			prev = hp1
			hp1, blocks1 = use_player_defence(skills1,atack,blocks1,hp1,False) 
			if bone2 != 0 and prev != hp1:
				bone_atack(field1,3)
			if hp1 <= 0:
					txt = pvp_text(nam1,nam2,maxhp1,maxhp2,hp1,hp2,blocks1,blocks2,skills1,skills2)
					bot.edit_message_caption(caption = txt, chat_id=call.message.chat.id, message_id=call.message.message_id)
					time.sleep(1)
					newcost = cost
					del db[key]
					data = cursor.execute(f'SELECT coins,wins,gender FROM neko WHERE id = {two}')
					data = data.fetchone()
					c1 = data[0]
					w1 = data[1]
					gender2 = data[2]
					c1 = c1 + newcost
					w1 = w1 + 1
					txt = 'Победила дружба, наебал, победила <a href="tg://user?id='+str(two)+'">'+str(nam2)+'</a>. Выигрыш составил ' + str(newcost) + ' 💰, владельцам арены понравился бой и они не взяли процентов. Не забудьте дать некодевочкам отдохнуть хотя бы час'
					if gender2 == 1:
						txt = 'Победила дружба, наебал, победил <a href="tg://user?id='+str(two)+'">'+str(nam2)+'</a>. Выигрыш составил ' + str(newcost) + ' 💰, владельцам арены понравился бой и они не взяли процентов. Не забудьте дать некодевочкам отдохнуть хотя бы час'
					bot.send_message(call.message.chat.id, txt)
					data = cursor.execute(f'SELECT coins FROM neko WHERE id = {one}')
					data = data.fetchone()
					c2 = data[0]
					c2 = c2 - cost
					cursor.execute(f"UPDATE neko SET wins = {w1}, coins = {c1} WHERE id = {two}")
					cursor.execute(f"UPDATE neko SET coins = {c2} WHERE id = {one}")
					return
		if turns == 0:
			rer1 = 1
			rer2 = 1
			if starter == 1:
				struct['starter'] = 0
				turns = 1
			else:
				turns = 2
			
			if turn == one:
				turn = two
				field = field2
				skills = skills2
				hpbal = hp2 <= hp1
			else:
				turn = one
				field = field1
				skills = skills1
				hpbal = hp1 <= hp2
			turns = get_player_turns(skills,hpbal,turns)

		if turn == one:
			image = image2
		else:
			image = image1

		keyboard = types.InlineKeyboardMarkup(row_width=6)
		dat = 'pvp ' + str(one) + ' ' + str(two) + ' ' + str(turn) + ' ' + str(hp1) + ' ' + str(hp2) + ' ' + str(maxhp1) + ' ' + str(maxhp2) + ' ' + str(turns) + ' ' + str(blocks1) + ' ' + str(blocks2)
		field_keyboard(keyboard,dat,field,rer1,rer2,skills,selected)
		txt = pvp_text(nam1,nam2,maxhp1,maxhp2,hp1,hp2,blocks1,blocks2,skills1,skills2)
		if turn == one:
			nam = nam1
		else:
			nam = nam2
		txt = txt + 'Ходит <a href="tg://user?id='+str(turn)+'">'+str(nam)+'</a>\n'
		txt = txt + 'Осталось ходов до атаки врага:  ' + str(turns)
		struct['selected'] = selected
		db[key] = pack(struct)
		time.sleep(1)
		bot.edit_message_media(media=telebot.types.InputMedia(media=image,caption = txt,type="photo", parse_mode='HTML'),chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)

	elif cmd == "pve":
		turns = int(args[2])
		blocks = int(args[3])
		targ = int(args[4])
		pos = int(args[5])
		rer1 = int(args[6])
		rer2 = int(args[7])
		atack = 0
		ability = 0

		struct = unpack(db[key])
		mas = struct['map']
		generation = struct['generation']
		co = struct['co']
		wh = struct['wh']
		mo = struct['mo']
		he = struct['he']
		field = struct['field']
		selected = struct['selected']
		next_x = struct['cur_x']
		next_y = struct['cur_y']
		hp = struct['hp']
		maxhp = struct['maxhp']
		nam = struct['name']
		gender = struct['gender']
		skills = struct['temp_skills']
		enemies = struct['enemies']
		
		if pos < 0:
			ability = abs(pos)
			if ability >= 200:
				result = change_target(bot,ability,targ,call,enemies)
				if result == -1:
					return
				targ = result
			else:
				result = use_skill(bot,ability,selected,call,field) 
				if result[0] == -1:
					return
				selected = -1
				atack += result[1]
				blocks += result[2]
				turns += result[3]
		else:
			result = change_figures(bot,selected,pos,call,field)
			if result[0] == -1:
				selected = result[1]
			else:
				turns -= 1
				selected = -1
		result = field_calculate(field,skills,True)
		atack += result[0]
		blocks += result[1]
		turns += result[2]
		hp += result[3]
		if hp > maxhp:
			hp = maxhp
		if blocks > 3:
			blocks = 3
		
		atack = get_player_damage(skills,hp,maxhp,atack,turns,blocks)
		turns = player_atack(enemies,targ,turns,atack,False)
	  
		if turns <= 0:
			rer1 = 1
			rer2 = 1
			turns = get_player_turns(skills, hp <= sum_enemies_hp(enemies), 2)
			enemy_atack = 0
			#АТАКА ВРАГОВ КРОМЕ СЛИЗНЯ
			for i in range(3):
				enemy_atack += enemies_turn(enemies,i)
			#АТАКА СЛИЗНЯ
			for i in range(3):
				if enemies[i]['id'] == 6:
					for j in range(3):
						if enemies[j]['id'] == 0:
							enemies[j] = enemy_list[7].copy()
							break
					break
					
			hp, blocks = use_player_defence(skills,enemy_atack,blocks,hp,False) 
			if hp <= 0:
					txt = hp_bar(nam,maxhp,hp)
					phot = enemy_photos[f"{enemies[0]['id']} {enemies[1]['id']} {enemies[2]['id']}"]
					if gender == 0:
						txt += '\n\n' + nam + ' вышла из портала вся покрытая синяками и странной белой жидкостью. Боюсь даже представить, что с ней произошло. Будь осторожнее в следующий раз'
					else:
						txt += '\n\n' + nam + ' вышел из портала весь покрытый синяками и странной белой жидкостью. Боюсь даже представить, что с ним произошло. Будь осторожнее в следующий раз'
					del db[key]
					bot.edit_message_media(media=telebot.types.InputMedia(media=phot,caption=txt,type="photo", parse_mode='HTML'),chat_id=call.message.chat.id, message_id=call.message.message_id)
					time.sleep(1)
					return
		
		if sum_enemies_hp(enemies) <= 0:
			txt = hp_bar(nam,maxhp,hp)
			if gender == 0:
				txt += '\n\nТвоя некодевочка победила!'
			else:
				txt += '\n\nТвой некомальчик победил!'
			generation[next_y][next_x] = 0
			struct['hp'] = hp
			db[key] = pack(struct)
			txt += f'\n\nДобыча:   {co} 💰   {wh} 🍫   {mo} ⚡️   {he} 🍼\n\n'
			txt += map_text(mas)
			keyboard = types.InlineKeyboardMarkup(row_width=4)
			dungeon_keyboard(keyboard,idk)
			bot.edit_message_media(media=telebot.types.InputMedia(media='AgACAgIAAx0CZQN7rQACwsFi8ct1qI3M_i1Bt1Tk_WvAbq7BWAACqcQxG-SBkUvkDVBnBMaohgEAAwIAA3MAAykE',caption=txt,type="photo", parse_mode='HTML'),chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
			time.sleep(1)
			return
		targ = change_zero_target(targ,enemies)
		keyboard = types.InlineKeyboardMarkup(row_width=6)
		dat = f'pve {idk} {turns} {blocks} {targ}'
		target_keyboard(keyboard,targ,dat,rer1,rer2)
		field_keyboard(keyboard,dat,field,rer1,rer2,skills,selected)
		struct['selected'] = selected
		struct['hp'] = hp
		db[key] = pack(struct)
		txt = pve_text(enemies,nam,hp,maxhp,blocks,skills)
		txt +=  f"Осталось ходов до атаки врага:  {turns}"
		phot = enemy_photos[f"{enemies[0]['id']} {enemies[1]['id']} {enemies[2]['id']}"]
	   
		time.sleep(1)
		bot.edit_message_media(media=telebot.types.InputMedia(media=phot,caption=txt,type="photo", parse_mode='HTML'),chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=keyboard)
	elif cmd == "interact":
		action = int(args[2])
		answer_callback_query(bot,call,'Успешно')
		time.sleep(1)
		struct = unpack(db[key])
		mas = struct['map']
		generation = struct['generation']
		co = struct['co']
		wh = struct['wh']
		mo = struct['mo']
		he = struct['he']
		next_x = struct['cur_x']
		next_y = struct['cur_y']
		hp = struct['hp']
		maxhp = struct['maxhp']
		nam = struct['name']
		gender = struct['gender']
		if action == 1:
			d = random.randint(1,10)
			co = co - 2
			if d != 10:
				phot = 'AgACAgIAAx0CZQN7rQACwwRi8t920_InxPRHCFJRBhJHi609NAAC274xGxy_mEtJHCxhP9SvfQEAAwIAA3MAAykE'
				new_txt = 'Удивительно, но ничего не произошло. А на что ты вообще надеялся?'
			else:
				mo = mo + 1
				phot = 'AgACAgIAAx0CZQN7rQACwwJi8t1lkPUz0QvhDBUeUT7KBUQJgQAC2b4xGxy_mEtae5LvKUzKfgEAAwIAA3MAAykE'
				new_txt = 'Что ж, это можно назвать чудом. Вместо воды в фонтане начал течь розовый монстр ⚡️! Лучше будет взять с собой немного'
		elif action == 3:
			hp = maxhp
			phot = 'AgACAgIAAx0CZQN7rQACwgZi7aTwuv6M-OsOvCsRGijo6gohwwACZb8xG3RJaUufsVKea9BUKAEAAwIAA3MAAykE'
			new_txt = nam + ' поела немного пиццы и теперь чувствует себя заметно лучше!'
			if gender == 1:
				new_txt = nam + ' поел немного пиццы и теперь чувствует себя заметно лучше!'
			new_txt += hp_bar(nam,maxhp,hp)
		elif action == 2:
			d = random.randint(1,2)
			if d == 1:
				he = he + 1
				phot = 'AgACAgIAAx0CZQN7rQACwd1i7HKMaDbODOjA7IV5RYxI01bcTAACwMAxG3RJYUvRcTOFHbiG3QEAAwIAA3MAAykE'
				new_txt = nam + ' как можно быстрее набрала бутыль антипохмелина 🍼 и отошла от берега. К счастью, ничего опасного не произошло, но будет ли так и впредь?'
				if gender == 1:
					new_txt = nam + ' как можно быстрее набрал бутыль антипохмелина 🍼 и отошел от берега. К счастью, ничего опасного не произошло, но будет ли так и впредь?'
			else:
				phot = 'AgACAgIAAx0CZQN7rQACwfxi7Zem-ltmGFEQZvc-sg97JYwNewACTb8xG3RJaUs9wsxj9zofxwEAAwIAA3MAAykE'
				new_txt = 'Оказалось, что в озере живёт огромный тентаклевый монстр! К сожалению, все мы знаем, что делают тентаклевые монстры с маленькими некодевочками... 💔'
				if gender == 1:
					new_txt = 'Оказалось, что в озере живёт огромный тентаклевый монстр! К сожалению, все мы знаем, что делают тентаклевые монстры с маленькими некомальчиками... 💔'
				hp = hp - 2
				new_txt += hp_bar(nam,maxhp,hp)
				if hp <= 0:
					if gender == 0:
						new_txt += '\n\n' + nam + ' вышла из портала вся покрытая синяками и странной белой жидкостью. Боюсь даже представить, что с ней произошло. Будь осторожнее в следующий раз'
					else:
						new_txt += '\n\n' + nam + ' вышел из портала весь покрытый синяками и странной белой жидкостью. Боюсь даже представить, что с ним произошло. Будь осторожнее в следующий раз'
					del db[key]
					bot.edit_message_media(media=telebot.types.InputMedia(media=phot,caption=new_txt,type="photo",parse_mode='HTML'),chat_id=call.message.chat.id, message_id=call.message.message_id)
					return              
		generation[next_y][next_x] = 0
		struct['co'] = co
		struct['wh'] = wh
		struct['mo'] = mo
		struct['he'] = he
		struct['hp'] = hp
		db[key] = pack(struct)
		txt = new_txt + f'\n\nДобыча:   {co} 💰   {wh} 🍫   {mo} ⚡️   {he} 🍼\n\n'
		txt += map_text(mas)
		keyboard = types.InlineKeyboardMarkup(row_width=4)
		dungeon_keyboard(keyboard,idk)
		bot.edit_message_media(media=telebot.types.InputMedia(media=phot,caption=txt,type="photo", parse_mode='HTML'),chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
   
	elif cmd == "move":
		d = int(args[2])
		struct = unpack(db[key])
		mas = struct['map']
		generation = struct['generation']
		co = struct['co']
		wh = struct['wh']
		mo = struct['mo']
		he = struct['he']
		cur_x = struct['cur_x']
		cur_y = struct['cur_y']
		hp = struct['hp']
		maxhp = struct['maxhp']
		nam = struct['name']
		gender = struct['gender']
		skills = struct['skills']
		if d == 1 and ((cur_y-3) < 0 or mas[cur_y-1][cur_x] == 0):
			answer_callback_query(bot,call,'Тупик')
			return
		elif d == 2 and ((cur_x+3) > 9 or mas[cur_y][cur_x+1] == 0):
			answer_callback_query(bot,call,'Тупик')
			return
		elif d == 3 and ((cur_y+3) > 12 or mas[cur_y+1][cur_x] == 0):
			answer_callback_query(bot,call,'Тупик')
			return
		elif d == 4 and ((cur_x-3) < 0 or mas[cur_y][cur_x-1] == 0):
			answer_callback_query(bot,call,'Тупик')
			return
		mas[cur_y][cur_x] = 4
		if d == 1:
			next_x = cur_x
			next_y = cur_y-3
		elif d == 2:
			next_x = cur_x+3
			next_y = cur_y
		elif d == 3:
			next_x = cur_x
			next_y = cur_y+3
		elif d == 4:
			next_x = cur_x-3
			next_y = cur_y
		mas[next_y][next_x] = 3
		if generation[cur_y][cur_x] != 0 and generation[cur_y][cur_x] != 1:
			mas[cur_y][cur_x] = 5
		next_gen = generation[next_y][next_x]
		keyboard = types.InlineKeyboardMarkup(row_width=4)
		answer_callback_query(bot,call,'Успешно')
		time.sleep(1)
		if next_gen == 1:
			phot = 'AgACAgIAAx0CZQN7rQACwxZi8uNUoMtUGP6J96D7X-pveAGj3wAC374xGxy_mEsWdB1RBPi4nQEAAwIAA3MAAykE'
			new_txt = 'К счастью, портал никуда не делся. Может быть, самое время вернуться?'
			if gender == 1:
				new_txt = 'К счастью, портал никуда не делся. Может быть, самое время вернуться?'
		elif next_gen == 2:
			wh = wh + 1
			generation[next_y][next_x] = 0
			phot = 'AgACAgIAAx0CZQN7rQACwvRi8tr6ixHXhD5-CLOdFikGnPqDcgACzb4xGxy_mEvGxDZ1JQABuSIBAAMCAANzAAMpBA'
			new_txt = 'Похоже, эта коробка - часть припасов пропавшей экспедиции. Внутри лежало несколько пустых бутылок водки и совсем немного вискаса 🍫'
			if gender == 1:
				new_txt = 'Похоже, эта коробка - часть припасов пропавшей экспедиции. Внутри лежало несколько пустых бутылок водки и совсем немного вискаса 🍫'
		elif next_gen == 3:
			co = co + 10
			generation[next_y][next_x] = 0
			phot = 'AgACAgIAAx0CZQN7rQACwvhi8tv5UTGRY0Ly30leGF-iVeph4AAC074xGxy_mEtCwi5QjU5PowEAAwIAA3MAAykE'
			new_txt = 'Странный кристалл, переливающийся всеми цветами радуги, преградил вам путь. К счастью, весит он не очень много. Его можно хорошо продать 💰, если удастся вынести'
		elif next_gen == 4:
			callback_button0 = types.InlineKeyboardButton(text = 'Бросить монетку 💸',callback_data = f'interact {idk} 1')
			keyboard.add(callback_button0)
			phot = 'AgACAgIAAx0CZQN7rQACwwRi8t920_InxPRHCFJRBhJHi609NAAC274xGxy_mEtJHCxhP9SvfQEAAwIAA3MAAykE'
			new_txt = 'Весьма изысканный фонтан стоял посреди небольшого озера. Кто и зачем его сюда поставил? Как бы то ни было, ' + nam + ' предложила кинуть туда монетку'
			if gender == 1:
				new_txt = 'Весьма изысканный фонтан стоял посреди небольшого озера. Кто и зачем его сюда поставил? Как бы то ни было, ' + nam + ' предложил кинуть туда монетку'
		elif next_gen == 5:
			callback_button0 = types.InlineKeyboardButton(text = 'Набрать 🍼',callback_data = f'interact {idk} 2')
			keyboard.add(callback_button0)
			phot = 'AgACAgIAAx0CZQN7rQACwd1i7HKMaDbODOjA7IV5RYxI01bcTAACwMAxG3RJYUvRcTOFHbiG3QEAAwIAA3MAAykE'
			new_txt =  'Да это же целое озеро антипохмелина! На протяжении веков эта жидкость использовалась от похмелья, и лишь недавние исследования показали, что он лечит остальные болезни тоже. Но рецепт был безвозвратно утерян, нельзя упускать такую возможность'
			new_txt += hp_bar(nam,maxhp,hp)
		elif next_gen == 6:
			callback_button0 = types.InlineKeyboardButton(text = 'Съесть пиццу 🍕',callback_data = f'interact {idk} 3')
			keyboard.add(callback_button0)
			phot = 'AgACAgIAAx0CZQN7rQACwwABYvLc79baJMP4YDV4iM_6n0U1Y0kAAte-MRscv5hL2-WMSvjaptEBAAMCAANzAAMpBA'
			new_txt = 'Вам повезло, вы нашли несколько кустов пиццы. Найти дикорастущую пиццу - большая удача. ' + nam + ' может съесть плоды и восстановить свои силы'
			if gender == 1:
				new_txt = 'Вам повезло, вы нашли несколько кустов пиццы. Найти дикорастущую пиццу - большая удача. ' + nam + ' может съесть плоды и восстановить свои силы'
			new_txt += hp_bar(nam,maxhp,hp)
		elif next_gen == 7:
			phot = 'AgACAgIAAx0CZQN7rQACwvZi8tuNp4bk85D-ypnCu5OUalrZwwAC0L4xGxy_mEvzEzdkcbipPgEAAwIAA3MAAykE'
			generation[next_y][next_x] = 0
			d = random.randint(1,2)
			if d == 1:
				letters = ['<b>"День 1. LGBT мир находится под землёй на глубине примерно 50 км, и официальной целью нашей экспедиции является поиск залежей антипохмелина, обнаруженных при последнем геосканировании. Однако, настоящая, мало кому известная цель - доказать существование LGBTQ+ мира"</b>',
				'<b>"День 2. Размеры этой сети пещер и запутанность её тоннелей действительно удивляют. Мы в пути уже целый день, однако, снова и снова каким-то образом возвращаемся обратно к порталу! К счастью, я додумался начать рисовать карту"</b>',
				'<b>"День 3. Наши припасы стремительно заканчиваются. Возможно, не стоило брать водки больше, чем еды. К тому же, заканчивается и топливо для огнемётов, которыми мы отбиваемся от полчищ фурри. Поскорее бы это всё закончилось"</b>',
				'<b>"День 4. Сегодня нам улыбнулась удача, нашли целое озеро антипохмелина! Никто не верил в то, что где-то ещё осталась хотя бы капля, но вот же он! Что ж, вот появился и повод выпить оставшиеся запасы водки"</b>',
				'<b>"День 5. Остались только я и парень по имени Рикардо. Остальные бухие пошли купаться в озере, и на моих глазах их всех мгновенно что-то утащило под воду. Мы сразу же поплыли на помощь, но никого не нашли... Нужно срочно возвращаться и запросить помощь"</b>',
				'<b>"День 6. Несмотря на напряжение, нам удалось немного поговорить в дороге. Рикардо оказался известным бразильским танцором, а отправился сюда в поисках достойного противника для флекс баттла. И вот, когда портал уже виднелся на горизонте, надо мной пролетела человеческая фигура и унесла Рикардо с собой"</b>'
				'<b>"День 7. Нельзя это так оставлять, я должен спасти своего нового друга. Именно с такими мыслями я отправился в путь. Гнездо, куда то существо унесло Рикардо, располагалось на вершине скалы. Целый день взбирался на неё, стерев руки в кровь. Однако то, что я там увидел, уже не было моим товарищем...</b>'
				]
				let = random.choice(letters)
				new_txt = 'Похоже, здесь экспедиция остановилась для привала, но было это очень давно. Среди пустых бутылок водки ' + nam + ' нашла клочок бумаги. Видимо, это отрывок из журнала экспедиции:\n' + let
				if gender == 1:
					new_txt = 'Похоже, здесь экспедиция остановилась для привала, но было это очень давно. Среди пустых бутылок водки ' + nam + ' нашел клочок бумаги. Видимо, это отрывок из журнала экспедиции:\n' + let
			elif d == 2:
				new_txt = 'Похоже, здесь экспедиция остановилась для привала, но было это очень давно. Среди пустых бутылок водки ' + nam + ' нашла несколько обрывков бумаги. Соединив их вместе, получилось карта 🗺! Крестиком, судя по всему, отмечены опасные места'
				if gender == 1:
					new_txt = 'Похоже, здесь экспедиция остановилась для привала, но было это очень давно. Среди пустых бутылок водки ' + nam + ' нашел несколько обрывков бумаги. Соединив их вместе, получилась карта 🗺! Крестиком, судя по всему, отмечены опасные места'
				for i in range(0,13):
					for j in range(0,10):
						if generation[i][j] == 8:
							mas[i][j] = 6
		
		elif next_gen == 8:
			keyboard = types.InlineKeyboardMarkup(row_width=6)
			gen = random.randint(1,4)
			if gen == 1:
				enemies = [enemy_list[0].copy(),enemy_list[1].copy(),enemy_list[3].copy()]
			elif gen == 2:
				enemies = [enemy_list[0].copy(),enemy_list[4].copy(),enemy_list[0].copy()]
			elif gen == 3:
				enemies = [enemy_list[0].copy(),enemy_list[6].copy(),enemy_list[0].copy()]
			elif gen == 4:
				enemies = [enemy_list[0].copy(),enemy_list[8].copy(),enemy_list[0].copy()]

			new_txt = 'Тишину оборвал звук быстро приближающихся шагов. Кто бы это ни был, идёт он явно не с добрыми намерениями\n\nБой начнётся через 15 секунд, собирай символы по 4 в ряд чтобы поддерживать некодевочку\n\n🟥 🟧 - блок\n\n🟡 🟢 - атака\n\n💙 - плюс один ход'
			if gender == 1:
				new_txt = 'Тишину оборвал звук быстро приближающихся шагов. Кто бы это ни был, идёт он явно не с добрыми намерениями\n\nБой начнётся через 15 секунд, собирай символы по 4 в ряд чтобы поддерживать некомальчика\n\n🟥 🟧 - блок\n\n🟡 🟢 - атака\n\n💙 - плюс один ход'
			bot.edit_message_media(media=telebot.types.InputMedia(media='AgACAgIAAx0CZQN7rQACwsFi8ct1qI3M_i1Bt1Tk_WvAbq7BWAACqcQxG-SBkUvkDVBnBMaohgEAAwIAA3MAAykE',caption=new_txt,type="photo", parse_mode='HTML'),chat_id=call.message.chat.id, message_id=call.message.message_id)
			
			field = generate_field(skills)
			blocks = 0
			turns = get_player_turns(skills, hp <= sum_enemies_hp(enemies), 2)
			targ = 1
			dat = f'pve {idk} {turns} {blocks} {targ}'
			target_keyboard(keyboard,targ,dat,1,1)
			field_keyboard(keyboard,dat,field,1,1,skills)
			txt = pve_text(enemies,nam,hp,maxhp,blocks,skills)
			txt +=  f"Осталось ходов до атаки врага:  {turns}"
			phot = enemy_photos[f"{enemies[0]['id']} {enemies[1]['id']} {enemies[2]['id']}"]
			struct['cur_x'] = next_x
			struct['cur_y'] = next_y
			struct['field'] = field
			struct['selected'] = -1
			struct['enemies'] = enemies
			struct['temp_skills'] = skills
			db[key] = pack(struct)
			time.sleep(15)
			bot.edit_message_media(media=telebot.types.InputMedia(media=phot,caption=txt,type="photo", parse_mode='HTML'),chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=keyboard)
			return
		else:
			phot = 'AgACAgIAAx0CZQN7rQACsTdi5aOWZGH8r_RsZ4ZDXbGXHwZZxwACz8AxG2fEKUv9PoikvhKaVgEAAwIAA3MAAykE'
			new_txt = 'Масштабы этих пещер действительно удивляют, а их красота завораживает. Пока что тишину лишь изредка нарушает падение капель воды'
		struct['co'] = co
		struct['wh'] = wh
		struct['mo'] = mo
		struct['he'] = he
		struct['cur_x'] = next_x
		struct['cur_y'] = next_y
		db[key] = pack(struct)
		txt = new_txt + f'\n\nДобыча:   {co} 💰   {wh} 🍫   {mo} ⚡️   {he} 🍼\n\n'
		txt += map_text(mas)
		dungeon_keyboard(keyboard,idk)
		bot.edit_message_media(media=telebot.types.InputMedia(media=phot,caption=txt,type="photo", parse_mode='HTML'),chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)

	elif cmd == "back":
		answer_callback_query(bot,call,'Успешно')
		time.sleep(1)
		data = cursor.execute(f'SELECT coins,inventory,base,gender FROM neko WHERE id = {idk}')
		data = data.fetchone()
		coins = data[0]
		inventory = unpack(data[1])
		baza = data[2]
		gender = data[3]
		struct = unpack(db[key])
		co = struct['co']
		wh = struct['wh']
		mo = struct['mo']
		he = struct['he']
		coins = coins + co
		inventory['whiskas'] += wh
		if wh != 0 and baza >= 7:
			inventory['whiskas'] += 1
		inventory['monster'] += mo
		inventory['antipohmelin'] += he
		if co != 0 or wh != 0 or mo != 0 or he != 0:
			cursor.execute(f"UPDATE neko SET dungeon_raids = dungeon_raids + 1 WHERE id = {idk}")
		cursor.execute(f"UPDATE neko SET coins = {coins},inventory = '{pack(inventory)}' WHERE id = {idk}")
		del db[key]
		txt = 'Твоя некодевочка вернулась обратно и принесла всё, что нашла в этом загадочном мире. Может стоит наградить её вискасом?'
		if gender == 1:
			txt = 'Твой некомальчик вернулся обратно и принёс всё, что нашёл в этом загадочном мире. Может стоит наградить его вискасом?'
		bot.edit_message_media(media=telebot.types.InputMedia(media='AgACAgIAAx0CZQN7rQACwxZi8uNUoMtUGP6J96D7X-pveAGj3wAC374xGxy_mEsWdB1RBPi4nQEAAwIAA3MAAykE',caption=txt,type="photo", parse_mode='HTML'),chat_id=call.message.chat.id, message_id=call.message.message_id)

	elif cmd == "get":
		answer_callback_query(bot,call,'Успешно')
		keyboard = types.InlineKeyboardMarkup(row_width=3)
		callback_button1 = types.InlineKeyboardButton(text = 'ТОЧНО БЛЯТЬ ВЗЯТЬ? ✅',callback_data = 'fuck ' + str(idk))
		keyboard.add(callback_button1)
		callback_button2 = types.InlineKeyboardButton(text = 'Не брать ❌',callback_data = 'dont ' + str(idk))
		keyboard.add(callback_button2)
		bot.edit_message_media(media=telebot.types.InputMedia(media=call.message.photo[-1].file_id,type="photo", parse_mode='HTML'),chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=keyboard)
		time.sleep(1)
	elif cmd == "delacc":
		answer_callback_query(bot,call,'Успешно')
		keyboard = types.InlineKeyboardMarkup(row_width=1)
		callback_button1 = types.InlineKeyboardButton(text = '✅ ПОДУМАЙ ЕЩЁ РАЗ',callback_data = 'fuckdel ' + str(idk))
		callback_button2 = types.InlineKeyboardButton(text = '❌ Да ну нахуй',callback_data = 'dont ' + str(idk))
		keyboard.add(callback_button1)
		keyboard.add(callback_button2)
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text='Подумай ещё раз',reply_markup=keyboard)
		time.sleep(1)
	elif cmd == "fuckdel":
		answer_callback_query(bot,call,'Ну и пошел нахуй')
		data = cursor.execute(f'SELECT name FROM neko WHERE id = {idk}')
		data = data.fetchone()
		nam = data[0]
		cursor.execute(f"DELETE FROM neko WHERE id = {idk}")
		add_to_dead(cursor,nam,'Выкинул хозяин (пидор)')
		bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
		time.sleep(1)

	elif cmd == "wear":
		answer_callback_query(bot,call,'Успешно')
		photka = call.message.photo[-1].file_id
		cursor.execute(f"UPDATE neko SET gifka = NULL,new_phot = '"+photka+"' WHERE id = "+ str(idk))
		bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
		time.sleep(1)

	elif cmd == "fuck":
		data = cursor.execute(f'SELECT name,base,gender FROM neko WHERE id = '+str(idk))
		data = data.fetchone()
		answer_callback_query(bot,call,'Успешно')
		nam = data[0]
		baza = data[1]
		gender = data[2]
		if gender == 0:
			text = 'Поздравляю, это твоя новая некодевочка! Старую мы сами выкинем в ближайшую канаву, тебе не нужно об этом беспокоиться ☠️'
		else:
			text = 'Поздравляю, это твой новый некомальчик! Старого мы сами выкинем в ближайшую канаву, тебе не нужно об этом беспокоиться ☠️'
		bot.send_message(call.message.chat.id,text)
		photka = call.message.photo[-1].file_id
		kill_neko(cursor,idk,gender,photka,nam,baza,call.message.chat.id,'Хозяин нашел замену')
		bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
		time.sleep(1)

	elif cmd == "dont":
		answer_callback_query(bot,call,'Успешно')
		bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
		time.sleep(1)

	elif cmd == "skill":
		turn = int(args[2])
		sk = int(args[3])
		data = cursor.execute(f'SELECT skill_one,skill_two FROM neko WHERE id = '+str(idk))
		data = data.fetchone()
		skill1 = data[0]
		skill2 = data[1]
		if turn == 1:
			cursor.execute(f"UPDATE neko SET skill_one = " + str(sk) + " WHERE id = "+ str(idk))
			skill1 = sk
		else:
			cursor.execute(f"UPDATE neko SET skill_two = " + str(sk) + " WHERE id = "+ str(idk))
			skill2 = sk
		if skill1 > 100:
			sktxt1 = active_skill_list[skill1-100]
		else:
			sktxt1 = passive_skill_list[skill1]
		if skill2 > 100:
			sktxt2 = active_skill_list[skill2-100]
		else:
			sktxt2 = passive_skill_list[skill2]

		answer_callback_query(bot,call,'Успешно')
		time.sleep(1)
		txt = 'Навыки изменены:\n\n' + sktxt1 + '\n' + sktxt2
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text = txt)

	elif cmd == "item":
		turn = int(args[2])
		itm = int(args[3])
		answer_callback_query(bot,call,'Успешно')
		if turn == 1:
			cursor.execute(f"UPDATE neko SET new_phot = NULL, item_one = " + str(itm) + " WHERE id = "+ str(idk))
		else:
			cursor.execute(f"UPDATE neko SET new_phot = NULL, item_two = " + str(itm) + " WHERE id = "+ str(idk))
		bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
		time.sleep(1)
	elif cmd == "pplus":
		struct = unpack(db[key])
		minbet = struct['minbet']
		minbet += 1
		data = cursor.execute(f'SELECT coins FROM neko WHERE id = '+str(idk))
		data = data.fetchone()
		coins = data[0]
		if coins < minbet*5:
			answer_callback_query(bot,call,'Ты бомж')
			return
		answer_callback_query(bot,call,'Успешно')
		struct['minbet'] = minbet
		struct['bank'] = [minbet]
		struct['money'] = [coins]
		keyboard = poker_init_keyboard(key)
		time.sleep(1)
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text = f'Вход от {5*minbet} 💰',reply_markup=keyboard)
		db[key] = pack(struct)
	elif cmd == "pminus":
		struct = unpack(db[key])
		minbet = struct['minbet']
		minbet -= 1
		if minbet < 1:
			answer_callback_query(bot,call,'Хуйня')
			return
		answer_callback_query(bot,call,'Успешно')
		struct['minbet'] = minbet
		struct['bank'] = [minbet]
		keyboard = poker_init_keyboard(key)
		time.sleep(1)
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text = f'Вход от {5*minbet} 💰',reply_markup=keyboard)
		db[key] = pack(struct)
	elif cmd == "pcontinue":
		struct = unpack(db[key])
		minbet = struct['minbet']
		players = struct['players']
		answer_callback_query(bot,call,'Успешно')
		keyboard = poker_join_keyboard(key)
		time.sleep(1)
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text = f'Идёт набор в покер, кто не отзовётся тот быдло\n\nВход от {5*minbet} 💰\n<b>Игроков: {len(players)}</b>',reply_markup=keyboard)
	elif cmd == "pend":
		answer_callback_query(bot,call,'Успешно')
		time.sleep(1)
		bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
		del db[key]
	elif cmd == "pjoin":
		struct = unpack(db[key])
		minbet = struct['minbet']
		players = struct['players']
		bank = struct['bank']
		names = struct['names']
		money = struct['money']
		data = cursor.execute(f'SELECT coins, name FROM neko WHERE id = '+str(call.from_user.id))
		data = data.fetchone()
		coins = data[0]
		name = data[1]
		if coins < minbet*5:
			answer_callback_query(bot,call,'Ты бомж')
			return
		if check_all(bot, call.from_user.id) is not None :
			answer_callback_query(bot,call,check_all(bot, call.from_user.id))
			return
		if len(players) == 6:
			answer_callback_query(bot,call,'Максимум игроков')
			return
		answer_callback_query(bot,call,'Успешно')
		players.append(call.from_user.id)
		bank.append(minbet)
		names.append(name)
		money.append(coins)
		keyboard = poker_join_keyboard(key)
		time.sleep(1)
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text = f'Идёт набор в покер, кто не отзовётся тот быдло\n\nВход от {5*minbet} 💰\n<b>Игроков: {len(players)}</b>',reply_markup=keyboard)
		db[key] = pack(struct)
	elif cmd == "pstart":
		struct = unpack(db[key])
		minbet = struct['minbet']
		players = struct['players']
		bank = struct['bank']
		names = struct['names']
		money = struct['money']
		cards = struct['cards']
		hand = struct['hand']
		if len(players) < 2:
			answer_callback_query(bot,call,'Недостаточно игроков')
			return
		answer_callback_query(bot,call,'Успешно')
		deck = [
		(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(9,1),(10,1),(11,1),(12,1),(13,1),(14,1),
		(2,2),(3,2),(4,2),(5,2),(6,2),(7,2),(8,2),(9,2),(10,2),(11,2),(12,2),(13,2),(14,2),
		(2,3),(3,3),(4,3),(5,3),(6,3),(7,3),(8,3),(9,3),(10,3),(11,3),(12,3),(13,3),(14,3),
		(2,4),(3,4),(4,4),(5,4),(6,4),(7,4),(8,4),(9,4),(10,4),(11,4),(12,4),(13,4),(14,4)
		]
		for i in range(5):
			d = random.choice(deck)
			deck.remove(d)
			cards.append(d)
		for j in range(len(players)):
			for i in range(2):
				d = random.choice(deck)
				deck.remove(d)
				hand.append(d)
		turn = players[0]
		pos = 0
		r = 1
		txt = poker_text(players,names,bank,turn,pos,money)
		keyboard = poker_keyboard(True,1,key,turn,pos,money,bank,False,players,base_bet = minbet)
		time.sleep(1)
		f = 'AgACAgIAAx0CZQN7rQABAjYqZSgLBGe5IXK5GmfOVwbxuvUxsTwAAgvNMRsUZEBJHzsUg8_DUQABAQADAgADeQADMAQ'
		m = bot.send_photo(call.message.chat.id, photo=f,caption = txt,reply_markup=keyboard)
		bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
		struct['wait'] = int(time.time() + 420)
		struct['event'] = 2
		struct['message'] = m.id
		db[key] = pack(struct)
	elif cmd == "poker":
		struct = unpack(db[key])
		cards = struct['cards']
		event = struct['event']
		hand = struct['hand']
		players = struct['players']
		bank = struct['bank']
		names = struct['names']
		money = struct['money']
		dead = struct['dead']
		vabank = struct['vabank']
		minbet = struct['minbet']
		turn = int(args[2])
		pos = int(args[3])
		action = int(args[4])
		r = int(args[5])
		if call.from_user.id != turn:
			answer_callback_query(bot,call,'Не твой ход')
			return
		answer_callback_query(bot,call,'Успешно')
		if action == 1:
			act_txt = names[pos] + ' ccыт и пропускает ход\n\n'
		elif action == 2:
			act_txt = names[pos] + ' ливает из игры обоссавшись и обосравшись\n\n'
			names[pos] = '☠️☠️☠️'
			dead.append(turn)
		else:
			if action == 3:
				act_txt = names[pos] + ' поддерживает ставку\n\n'
			elif action == 4:
				act_txt = names[pos] + ' повышает ставку\n\n'
			bet = int(args[6])
			bank[pos] += bet
			if bank[pos] >= money[pos]:
				vabank.append(turn)
				act_txt = names[pos] + ' ставит душу своей матери\n\n'
				names[pos] = f'<i>{names[pos]}</i>'
		#уравнивание банка для расчетов
		bal_bank = bank.copy()
		for i in range(len(players)):
			if players[i] in dead or players[i] in vabank:
				bal_bank[i] = max(bank)
		balance = max(bal_bank) == min(bal_bank)
		islastbet = (len(dead)+len(vabank)) >= len(players) - 1
		#смена ходящего игрока
		if r == 1:
			pos += 1
			while pos != len(players) and (players[pos] in dead or players[pos] in vabank):
				pos = pos + 1
		#новая стадия или конец
		if (r == 1 and pos == len(players) and balance) or (r == 2 and balance) or (islastbet and balance):
			if islastbet:
				event = 5
			r = 1
			pos = 0
			while pos != len(players) and (players[pos] in dead or players[pos] in vabank):
				pos += 1
			f = poker_image(cards,event)
			event += 1
			if event == 6:
				#ПРОСЧЕТ КОМБИНАЦИЙ
				combinations = ['Старшая карта','Пара','Две пары','Сет','Стрит','Флеш','Фулл хаус','Каре','Стрит флеш','Флеш рояль']
				player_combs = []
				for j in range(len(players)):
					crd = cards.copy()
					crd.append(hand[j*2])
					crd.append(hand[j*2+1])
					player_combs.append(combinator(crd))
				#ГЕНЕРАЦИЯ ТЕКСТА
				txt = act_txt
				for i in range(len(players)):
					hd = [hand[i*2],hand[i*2+1]]
					txt = txt + names[i] + '  ' + str(bank[i]) + ' 💰\n'
					txt += card_text(hd)
					txt += str(combinations[round(player_combs[i])]) + '\n\n'
				#ВЫБОР ПОБЕДИТЕЛЯ
				for i in range(len(players)):
					if players[i] in dead:
						player_combs[i] = -1
				max_comb = max(player_combs)
				if player_combs.count(max_comb) == 1:
					winners = [player_combs.index(max_comb)]
				else:
					for i in range(len(players)):
							if math.isclose(player_combs[i],max_comb):
								player_combs[i] = max(hand[i*2][0],hand[i*2+1][0])
							else:
								player_combs[i] = -1
					max_comb = max(player_combs)
					winners = []
					for i in range(len(players)):
						if math.isclose(player_combs[i],max_comb):
							winners.append(i)
				#ГЕНЕРАЦИЯ ТЕКСТА
				if len(winners) == 1:
					txt += 'Победитель <a href="tg://user?id='+str(players[winners[0]])+'">'+str(names[winners[0]])+'</a>, остальные сосут бибу'
				else:
					txt += 'Победители '
					for j in winners:
						txt += '<a href="tg://user?id='+str(players[j])+'">'+str(names[j])+'</a>, '
					txt += 'остальные сосут бибу'
				#РАСПРЕДЕЛЕНИЕ ДЕНЕГ
				max_cash = []
				for j in winners:
					max_cash.append(bank[j])
				max_cash = max(max_cash)
				cash = 0
				for i in range(len(players)):
					if i in winners:
						continue
					if bank[i] > max_cash:
						cash += max_cash
						cursor.execute(f"UPDATE neko SET coins = coins - " + str(max_cash) + " WHERE id = " + str(players[i]))
					else:
						cash += bank[i]
						cursor.execute(f"UPDATE neko SET coins = coins - " + str(bank[i]) + " WHERE id = " + str(players[i]))
				cash = round(cash/len(winners))
				for j in winners:
					cursor.execute(f"UPDATE neko SET coins = coins + " + str(cash) + " WHERE id = " + str(players[j]))
				time.sleep(1)
				bot.edit_message_media(media=telebot.types.InputMedia(media=f,caption = txt,type="photo", parse_mode='HTML'),chat_id=call.message.chat.id, message_id=call.message.message_id)
				del db[key]
				return
			struct['event'] = event
			turn = players[pos]
			txt = act_txt + poker_text(players,names,bank,turn,pos,money)
			keyboard = poker_keyboard(True,1,key,turn,pos,money,bank,False,players,base_bet = minbet)
			time.sleep(1)
			bot.edit_message_media(media=telebot.types.InputMedia(media=f,caption = txt,type="photo", parse_mode='HTML'),chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=keyboard)
			db[key] = pack(struct)
		else:
			if (r == 1 and pos == len(players)) or r == 2:
				r = 2
				pos = bal_bank.index(min(bal_bank))
			turn = players[pos]
			txt = act_txt + poker_text(players,names,bank,turn,pos,money)
			keyboard = poker_keyboard(balance,r,key,turn,pos,money,bank,islastbet,players,base_bet = minbet)
			time.sleep(1)
			bot.edit_message_media(media=telebot.types.InputMedia(media=call.message.photo[-1].file_id,caption = txt,type="photo", parse_mode='HTML'),chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=keyboard)
			db[key] = pack(struct)
	elif cmd == "hand":
		turn = int(args[2])
		pos = int(args[3])
		if call.from_user.id != turn:
			answer_callback_query(bot,call,'Не твой ход')
			return
		struct = unpack(db[key])
		cards = struct['cards']
		hand = struct['hand']
		event = struct['event']
		hand = [hand[pos*2],hand[pos*2+1]]
		cards = cards.copy()
		if event == 2:
			event = 0
		for i in range(5-event):
			cards.pop()
		combinations = ['Старшая карта','Пара','Две пары','Сет','Стрит','Флеш','Фулл хаус','Каре','Стрит флеш','Флеш рояль']
		txt = all_cards_text(cards)
		txt += 'Карты у тебя в руке:\n'
		txt += card_text(hand)
		txt += '\nТекущая комбинация:\n'
		cards.append(hand[0])
		cards.append(hand[1])
		comb = combinator(cards)
		txt += combinations[round(comb)]
		answer_callback_query(bot,call,txt,True)
	elif cmd == "bend":
		answer_callback_query(bot,call,'Успешно')
		bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
		del db[key]
	elif cmd == "bjoin":
		data = cursor.execute(f'SELECT rep,car,inventory,boss_kd FROM neko WHERE id = '+str(call.from_user.id))
		data = data.fetchone()
		rep = data[0]
		car = data[1]
		inventory = unpack(data[2])
		boss_kd = int(data[3] - time.time())
		if not car:
			answer_callback_query(bot,call,'Нужен некомобиль')
			return
		if inventory['monster'] < 1:
			answer_callback_query(bot,call,'Нету монстров')
			return
		if boss_kd > 0:
			answer_callback_query(bot,call,'Дай неко отдохнуть')
			return
		if rep < 120:
			answer_callback_query(bot,call,'Недостаточно доверия')
			return
		if check_all(bot, call.from_user.id) is not None :
			answer_callback_query(bot,call,check_all(bot, call.from_user.id))
			return
		struct = unpack(db[key])
		players = struct['players']
		if len(players) == 3:
			answer_callback_query(bot,call,'Максимум игроков')
			return
		answer_callback_query(bot,call,'Успешно')
		players.append(call.from_user.id)
		db[key] = pack(struct)
		keyboard = types.InlineKeyboardMarkup(row_width=2)
		callback_button1 = types.InlineKeyboardButton(text = 'Присоединиться ➕',callback_data = 'bjoin ' + str(idk))
		callback_button2 = types.InlineKeyboardButton(text = 'Старт ✅',callback_data = 'bstart ' + str(idk))
		callback_button3 = types.InlineKeyboardButton(text = 'Отмена ❌',callback_data = 'bend ' + str(idk))
		keyboard.add(callback_button1)
		keyboard.add(callback_button2,callback_button3)
		time.sleep(1)
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text = f'Идёт набор в тиму для легендарной пизделки с боссом\n\nВход 1 ⚡️, 120 💞\n<b>Игроков: {len(players)}</b>',reply_markup=keyboard)
	elif cmd == "bstart":
		struct = unpack(db[key])
		players = struct['players']
		answer_callback_query(bot,call,'Успешно')
		all_hp = []
		all_field = []
		all_name = []
		all_skills = []
		for player in players:
			data = cursor.execute(f'SELECT inventory, equipped, skill_one, skill_two, name, base, happy FROM neko WHERE id = '+str(player))
			data = data.fetchone()
			if data is not None:
				inventory = unpack(data[0])
				equipped = data[1]
				skill1 = data[2]
				skill2 = data[3]
				name = data[4]
				baza = data[5]
				happy = int(time.time() - data[6])
				all_hp.append(get_hp(equipped))
				all_field.append(generate_field([skill1,skill2]))
				all_name.append(name)
				all_skills.append([skill1,skill2])
				equipped = minus_durability(equipped)
				inventory['monster'] -= 1
				boss_kd = int(time.time() + BOSS_TIMEOUT + HAPPY_TIMEOUT[get_happiness_level(happy,baza)])
				cursor.execute(f"UPDATE neko SET equipped = {equipped}, inventory = '{pack(inventory)}', boss_kd = {boss_kd} WHERE id = {player}")
		hps = [4,7,8]
		second = [0,0,13]
		n = len(players)-1
		boss_enemy = enemy_list[10].copy()
		boss_enemy['maxhp'] = hps[n]
		boss_enemy['hp'] = boss_enemy['maxhp']
		enemies = [enemy_list[13].copy(),boss_enemy,enemy_list[second[n]].copy()]
		keyboard = types.InlineKeyboardMarkup(row_width=2)
		zakup_buy_keyboard(keyboard,idk)
		txt = 'Несмотря на то, что вход в лабораторию находится в ебенях вдали от цивилизации, рядом со входом вы увидели небольшой ларёк\n\nМожно купить (всё по 10 💰):\n\n<b>Просроченная растишка 🧃</b>\nПревращает кости в фигуры выбранного цвета\n\n<b>Лечебная питса 🍕</b>\nИзлечивает от яда и восстанавливает 1 хп\n\nПока ничего не куплено'
		ph = 'AgACAgQAAx0CZQN7rQABAtnbZXYk4pKnBrEkF7e3EjSTSxHp9foAAviuMRvh4lVQbYm8gqzvDf0BAAMCAAN4AAMzBA'
		time.sleep(1)
		m = bot.send_photo(chat_id=call.message.chat.id, photo=ph,caption = txt,reply_markup=keyboard)
		bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
		struct['all_hp'] = all_hp
		struct['all_maxhp'] = all_hp
		struct['enemies'] = enemies
		struct['all_field'] = all_field
		struct['all_name'] = all_name
		struct['all_skills'] = all_skills
		struct['event'] = 1
		struct['wait'] = int(time.time() + 600)
		struct['message'] = m.id
		db[key] = pack(struct)
	elif cmd == "bcontinue":
		struct = unpack(db[key])
		players = struct['players']
		zakup = struct['zakup']
		all_hp = struct['all_hp']
		all_maxhp = struct['all_maxhp']
		enemies = struct['enemies']
		all_poisoned = struct['all_poisoned']
		all_blocks = struct['all_blocks']
		all_field = struct['all_field']
		all_name = struct['all_name']
		all_skills = struct['all_skills']
		answer_callback_query(bot,call,'Успешно')
		time.sleep(1)
		txt = 'Внутри не было ни души. Некоторое время побродив по пустым коридорам, вы увидели силуэт, медленно приближающийся к вам\n\nБой начнётся через 15 секунд, собирай символы по 4 в ряд чтобы поддерживать некочана\n\n🟥 🟧 - блок\n\n🟡 🟢 - атака\n\n💙 - плюс один ход'
		ph = 'AgACAgIAAx0CZQN7rQABAdk2ZQABZ1Oxc7bJUQwI0_AR_Fwa1Ak_AAKWyzEb5toBSEn9Jkb9RNRMAQADAgADcwADMAQ'
		bot.edit_message_media(media=telebot.types.InputMedia(media=ph,caption=txt,type="photo", parse_mode='HTML'),chat_id=call.message.chat.id, message_id=call.message.message_id.id)
		pindex = 0
		player = players[pindex]
		keyboard = types.InlineKeyboardMarkup(row_width=6)
		turns = get_player_turns(all_skills[pindex], all_hp[pindex] <= sum_enemies_hp(enemies), 2)
		targ = 1
		item_use = 1
		dat = f'boss {idk} {player} {pindex} {turns} {targ} {item_use}'
		target_keyboard(keyboard,targ,dat,1,1)
		field_keyboard(keyboard,dat,all_field[pindex],1,1,all_skills[pindex])
		zakup_use_keyboard(keyboard,zakup,dat,1,1,item_use)
		txt = boss_text(enemies,all_name[pindex],all_poisoned[pindex],all_hp[pindex],all_maxhp[pindex],all_blocks[pindex],all_skills[pindex],player)
		txt += f'Осталось ходов до атаки врага:  {turns}'
		phot = boss_photos[f"{enemies[0]['id']} {enemies[1]['id']} {enemies[2]['id']}"]
		struct['wait'] = int(time.time() + 1800)
		struct['event'] = 2  
		db[key] = pack(struct)
		time.sleep(15)
		bot.edit_message_media(media=telebot.types.InputMedia(media=phot,caption=txt,type="photo", parse_mode='HTML'),chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=keyboard)
	elif cmd == "boss":
		player = int(args[2])
		pindex = int(args[3])
		turns = int(args[4])
		targ = int(args[5])
		item_use = int(args[6])
		pos = int(args[7])
		rer1 = int(args[8])
		rer2 = int(args[9])
		if call.from_user.id != player:
			answer_callback_query(bot,call,'Пашол нахуй')
			return
		atack = 0
		ability = 0
		splash = False
		struct = unpack(db[key])
		players = struct['players']
		zakup = struct['zakup']
		all_hp = struct['all_hp']
		all_maxhp = struct['all_maxhp']
		enemies = struct['enemies']
		all_poisoned = struct['all_poisoned']
		all_blocks = struct['all_blocks']
		all_field = struct['all_field']
		selected = struct['selected']
		all_name = struct['all_name']
		all_skills = struct['all_skills']
		if pos < 0:
			ability = abs(pos)
			if ability >= 300:
				item = ability - 300
				if item == 0:
					#растишка
					if selected == -1:
						answer_callback_query(bot,call,'Сначала выбери фигуру')
						return
					figa = all_field[pindex][selected]
					if figa == 5 or figa == 6:
						answer_callback_query(bot,call,'Выбрана неподходящая фигура')
						return
					if all_field[pindex].count(6) == 0:
						answer_callback_query(bot,call,'Нет костей')
						return
					for i in range(36):
						if all_field[pindex][i] == 6:
							all_field[pindex][i] = figa
				elif item == 1:
					#питса  
					all_poisoned[pindex] = False
					all_hp[pindex] += 1
				elif item == 2:
					#корсар
					atack += 1
					splash = True
				answer_callback_query(bot,call,'Предмет использован')
				zakup.remove(item)
				item_use = 0
			elif ability >= 200:
				result = change_target(bot,ability,targ,call,enemies)
				if result == -1:
					return
				targ = result
			else:
				result = use_skill(bot,ability,selected,call,all_field[pindex]) 
				if result[0] == -1:
					return
				selected = -1
				atack += result[1]
				all_blocks[pindex] += result[2]
				turns += result[3]
		else:
			result = change_figures(bot,selected,pos,call,all_field[pindex])
			if result[0] == -1:
				selected = result[1]
			else:
				turns -= 1
				selected = -1
		result = field_calculate(all_field[pindex],all_skills[pindex],True)
		atack += result[0]
		all_blocks[pindex] += result[1]
		turns += result[2]
		all_hp[pindex] += result[3]
		if all_hp[pindex] > all_maxhp[pindex]:
			all_hp[pindex] = all_maxhp[pindex]
		if all_blocks[pindex] > 3:
			all_blocks[pindex] = 3
			
		atack = get_player_damage(all_skills[pindex],all_hp[pindex],all_maxhp[pindex],atack,turns,all_blocks[pindex])
		turns = player_atack(enemies,targ,turns,atack,splash)

		if turns <= 0:
			rer1 = 1
			rer2 = 1
			item_use = 1
			pindex = boss_choose_player(pindex, all_hp)
			if pindex == -1:
				#АТАКА ЯДА
				for i in range(len(players)):
					if all_poisoned[i]:
						all_hp[i], all_blocks[i] = use_player_defence(all_skills[i],1,all_blocks[i],all_hp[i],True) 
				#ОБЩАЯ АТАКА ВРАГОВ
				for i in range(3):
						atk = enemies_turn(enemies,i)
						for j in range(len(players)):
							all_hp[j], all_blocks[j] = use_player_defence(all_skills[j],atk,all_blocks[j],all_hp[j],False) 
				#АТАКА СОСАНСА
				for i in range(3):
					if enemies[i]['id'] == 10 or enemies[i]['id'] == 11:
							for j in range(len(players)):
								prevhp = all_hp[j]
								all_hp[j], all_blocks[j] = use_player_defence(all_skills[j],2,all_blocks[j],all_hp[j],False) 
								if prevhp != all_hp[j]:
									do = random.randint(1,2)
									if do == 1 or all_poisoned[j]:
										bone_atack(all_field[j],5)
									elif do == 2:
										all_poisoned[j] = True

						
				if not check_alive(all_hp):
					txt = boss_hp_bar(all_name,all_hp,all_maxhp)
					phot = boss_photos[f"{enemies[0]['id']} {enemies[1]['id']} {enemies[2]['id']}"]
					txt += '\n\nК сожалению, все участвовавшие в зарубе некочаны были отпизжены и ещё долго отмывались от пилка'
					time.sleep(1)
					bot.edit_message_media(media=telebot.types.InputMedia(media=phot,caption=txt,type="photo", parse_mode='HTML'),chat_id=call.message.chat.id, message_id=call.message.message_id)
					del db[key]
					return    
				pindex = boss_choose_player(pindex, all_hp)
				
			turns = get_player_turns(all_skills[pindex], all_hp[pindex] <= sum_enemies_hp(enemies), 2)
		
		if sum_enemies_hp(enemies) <= 0:
			n = len(players) - 1
			coins_reward = [150,75,50]
			bones_reward = [8,4,3]
			boxes_reward = [2,1,1]
			txt = boss_hp_bar(all_name,all_hp,all_maxhp)
			phot = boss_photos[f"{enemies[0]['id']} {enemies[1]['id']} {enemies[2]['id']}"]
			txt += '\n\nНекочаны одержали грандиозную победу, и условия содержания образца №228 были успешно восстановлены. Теперь вы можете получить обещанную награду от Некославии'
			time.sleep(1)
			bot.edit_message_media(media=telebot.types.InputMedia(media=phot,caption=txt,type="photo", parse_mode='HTML'),chat_id=call.message.chat.id, message_id=call.message.message_id)
			txt = f"Вы решили справедливо разделить добычу, поэтому каждый участник эпической зарубы получает:\n\n💰 Некогривны × {coins_reward}\n🦴 Кость санса × {bones_reward}\n🎁 Коробка с украшениями × {boxes_reward}"
			time.sleep(1)
			bot.send_message(call.message.chat.id, txt)
			for player in players:
				data = cursor.execute(f'SELECT inventory, coins, boss_raids FROM neko WHERE id = '+str(player))
				data = data.fetchone()
				if data is not None:
					inventory = unpack(data[0])
					coins = data[1]
					boss_raids = data[2]
					inventory['bone'] += bones_reward[n]
					inventory['loot_box'] += boxes_reward[n]
					coins += coins_reward[n]
					boss_raids += 1
					cursor.execute(f"UPDATE neko SET inventory = '{pack(inventory)}', coins = {coins}, boss_raids = {boss_raids} WHERE id = {player}")
			del db[key]
			return
			
		targ = change_zero_target(targ,enemies)
		keyboard = types.InlineKeyboardMarkup(row_width=6)
		player = players[pindex]
		dat = f'boss {idk} {player} {pindex} {turns} {targ} {item_use}'
		target_keyboard(keyboard,targ,dat,rer1,rer2)
		field_keyboard(keyboard,dat,all_field[pindex],rer1,rer2,all_skills[pindex],selected)
		zakup_use_keyboard(keyboard,zakup,dat,rer1,rer2,item_use)
		txt = boss_text(enemies,all_name[pindex],all_poisoned[pindex],all_hp[pindex],all_maxhp[pindex],all_blocks[pindex],all_skills[pindex],player)
		txt += f'Осталось ходов до атаки врага:  {turns}'
		phot = boss_photos[f"{enemies[0]['id']} {enemies[1]['id']} {enemies[2]['id']}"] 
		struct['selected'] = selected
		db[key] = pack(struct)
		time.sleep(1)
		bot.edit_message_media(media=telebot.types.InputMedia(media=phot,caption=txt,type="photo", parse_mode='HTML'),chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=keyboard)   
	elif cmd == "buy":
		item = int(args[2])
		struct = unpack(db[key])
		zakup = struct['zakup']
		players = struct['players']
		if call.from_user.id not in players:
			answer_callback_query(bot,call,'Пашол нахуй')
			return
		if len(zakup) >= 3:
			answer_callback_query(bot,call,'Максимум предметов')
			return
		data = cursor.execute(f'SELECT coins FROM neko WHERE id = {call.from_user.id}')
		data = data.fetchone()
		coins = data[0]
		if coins < 10:
			answer_callback_query(bot,call,'Недостаточно денег')
			return
		answer_callback_query(bot,call,'Успешно')
		zakup.append(item)
		emojes = ['🧃 ','🍕 ','🧨 ']
		emoji_text = ''
		for itm in zakup:
			emoji_text += emojes[itm]
		keyboard = types.InlineKeyboardMarkup(row_width=2)
		zakup_buy_keyboard(keyboard,idk)
		txt = 'Несмотря на то, что вход в лабораторию находится в ебенях вдали от цивилизации, рядом со входом вы увидели небольшой ларёк\n\nМожно купить (всё по 10 💰):\n\n<b>Просроченная растишка 🧃</b>\nПревращает кости в фигуры выбранного цвета\n\n<b>Лечебная питса 🍕</b>\nИзлечивает от яда и восстанавливает 1 хп\n\nКуплено:  ' + emoji_text
		cursor.execute(f"UPDATE neko SET coins = coins - 10 WHERE id = {call.from_user.id}")
		db[key] = pack(struct)
		time.sleep(1)
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = txt, reply_markup=keyboard)
		
	elif cmd == "read":
		answer_callback_query(bot,call,'Успешно')
		bot.edit_message_media(media=telebot.types.InputMedia(media=patch_image,type="photo", parse_mode='HTML'),chat_id=call.message.chat.id, message_id=call.message.message_id)

	elif cmd == "paper":
		b1 = eval(args[2])
		b2 = eval(args[3])
		reason = int(args[4])
		starter = int(args[5])
		struct = unpack(db[key])
		images = struct['images']
		stage = struct['stage']
		mistakes = struct['mistakes']
		if starter == 1:
			answer_callback_query(bot,call,'Успешно')
		else:
			if b1 == b2:
				answer_callback_query(bot,call,'Правильно 👍')
			else:
				reasons = ['Нужно было пропустить','Неверная фотография','Не выполнены особые условия','Неверная дата выдачи','Лицензия просрочена','Проблемы с печатью']
				answer_callback_query(bot,call,f'Неправильно 👎\n{reasons[reason]}',True)
				mistakes += 1
			stage += 1
		if stage == 3:
			data = cursor.execute(f'SELECT coins,version FROM neko WHERE id = '+str(idk))
			data = data.fetchone()
			coins = data[0]
			version = data[1]
			phot = 'AgACAgIAAx0CZQN7rQAC3fFj7PN2eIWEEvqIJy3vH2FBpAUl1AACKsUxG7OiaUu7MhScqwbHIAEAAwIAA3MAAy4E'
			c = 20 - 5*mistakes
			coins += c
			cursor.execute(f"UPDATE neko SET coins = "+ str(coins) +" WHERE id = "+str(idk))
			del db[key]
			time.sleep(1)
			if mistakes == 0:
				txt = 'За эту смену тебе удалось заработать ' + str(c) + ' некогривен 💰. Ты не совершил ни единой ошибки, руководство завода гордится тобой!'
			else:
				txt = 'За эту смену тебе удалось заработать ' + str(c) + ' некогривен 💰. К сожалению, сегодня твоя работа не была идеальной, и руководство завода запомнит это'
			#elif mistakes == 3:
			#    txt = 'За эту смену тебе ничего не удалось заработать. Партия всё чаще подумывает о том, что ты недостоин своей некодевочки'
			#r = random.randint(1,10)
			r = 1
			if r == 10:
				biba = random.randint(10800,21600)
				b = int(time.time() + biba)
				biba = math.ceil(biba/3600)
				cursor.execute(f'UPDATE neko SET bolnitsa  = '+str(b)+' WHERE id = ' + str(idk))
				txt += '\n\nК сожалению, непрошедшие проверку некочаны сговорились и отпиздили тебя после работы, благодаря чему ' + str(biba) + ' часов ты проведёшь в больнице 💊'
			bot.edit_message_media(media=telebot.types.InputMedia(media=phot,caption=txt,type="photo", parse_mode='HTML'),chat_id=call.message.chat.id, message_id=call.message.message_id)
			if version != patch_version:
				cursor.execute(f"UPDATE neko SET version = "+ str(patch_version) +" WHERE id = "+str(idk))
				keyboard = types.InlineKeyboardMarkup()
				callback_button1 = types.InlineKeyboardButton(text = 'Читать 👀',callback_data = 'read ' + str(idk))
				keyboard.add(callback_button1)
				callback_button2 = types.InlineKeyboardButton(text = 'Не читать ❌',callback_data = 'dont ' + str(idk))
				keyboard.add(callback_button2)
				bot.send_photo(call.message.chat.id, photo = 'AgACAgIAAx0CZQN7rQACznBjQgABiPsE5FE7am8mfAOKiXsSOEsAAju9MRuS1hFKlyErHhjWQfcBAAMCAANzAAMqBA',caption = 'Возвращаясь с работы, ты заметил свежую газету, торчащую из твоего почтового ящика. Прочитать её?',reply_markup=keyboard)
		else:
			args = images[stage]
			args = args.split()
			phot = str(args[0])
			propusk = eval(args[1])
			reason = int(args[2])
			keyboard = types.InlineKeyboardMarkup(row_width=2)
			callback_button1 = types.InlineKeyboardButton(text = 'Пропустить ✅',callback_data = f'paper {idk} True {propusk} {reason} 0')
			callback_button2 = types.InlineKeyboardButton(text = 'Дать пизды ❌',callback_data = f'paper {idk} False {propusk} {reason} 0')
			callback_button3 = types.InlineKeyboardButton(text = 'Условия ❔',callback_data = 'spravka ' + str(idk))
			keyboard.add(callback_button1,callback_button2)
			keyboard.add(callback_button3)
			struct['stage'] = stage
			struct['mistakes'] = mistakes
			time.sleep(1)
			bot.edit_message_media(media=telebot.types.InputMedia(media=phot,type="photo", parse_mode='HTML'),chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=keyboard)
			db[key] = pack(struct)
	elif cmd == "spravka":
		txt = today_text
		answer_callback_query(bot,call,txt,True)
	elif cmd == "wikicmd":
		state = int(args[2])
		answer_callback_query(bot,call,'Успешно')
		keyboard = types.InlineKeyboardMarkup(row_width=2)
		if state == 0:
			callback_button1 = types.InlineKeyboardButton(text = '⬅️',callback_data = f'wikicmd {call.from_user.id} 2')
			callback_button2 = types.InlineKeyboardButton(text = '➡️',callback_data = f'wikicmd {call.from_user.id} 1')
			text = help_text[0]
		elif state == 1:
			callback_button1 = types.InlineKeyboardButton(text = '⬅️',callback_data = f'wikicmd {call.from_user.id} 0')
			callback_button2 = types.InlineKeyboardButton(text = '➡️',callback_data = f'wikicmd {call.from_user.id} 2')
			text = help_text[1]
		elif state == 2:
			callback_button1 = types.InlineKeyboardButton(text = '⬅️',callback_data = f'wikicmd {call.from_user.id} 1')
			callback_button2 = types.InlineKeyboardButton(text = '➡️',callback_data = f'wikicmd {call.from_user.id} 0')
			text = help_text[2]
		keyboard.add(callback_button1,callback_button2)
		time.sleep(1)
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=keyboard)
	elif cmd == "wikicraft":
		state = int(args[2])
		gender = int(args[3])
		answer_callback_query(bot,call,'Успешно')
		keyboard = types.InlineKeyboardMarkup(row_width=2)
		if state == 1:
			callback_button1 = types.InlineKeyboardButton(text = '⬅️ Починка',callback_data = f'wikicraft {idk} 2 {gender}')
			callback_button2 = types.InlineKeyboardButton(text = 'Создание ➡️',callback_data = f'wikicraft {idk} 3 {gender}')
			text = 'Для создания хайпового брендового шмота необходимы современные материалы, получаемые при разборе предметов. Давайте не будем думать о том, куда деваются некодевочки из коробок при этом'
			text += '\n\n🎁 Коробка с неко\nРезультат:  📦 Картон × 2\n\n🎁 Коробка с хорни неко\nРезультат:  📦 Картон × 3\n\n🎁 Коробка с украшениями\nРезультат:  📦 Картон × 3\n\n<code>Разобрать [назв] [колво]</code><i> - разобрать указанный предмет</i>'
		elif state == 2:
			callback_button1 = types.InlineKeyboardButton(text = '⬅️ Создание',callback_data = f'wikicraft {idk} 3 {gender}')
			callback_button2 = types.InlineKeyboardButton(text = 'Разборка ➡️',callback_data = f'wikicraft {idk} 1 {gender}')
			text = 'Созданную из говна и палок вещь можно надеть с помощью команды использовать. Даже самый охуенный и пиздатый шмот со временем ломается, поэтому его нужно чинить, стоимость полной починки всегда одинаковая и составляет 1 картон 📦'
			text += '\n\n<code>Починить</code><i> - починить надетую вещь</i>'
		else:
			callback_button1 = types.InlineKeyboardButton(text = '⬅️ Разборка',callback_data = f'wikicraft {idk} 1 {gender}')
			callback_button2 = types.InlineKeyboardButton(text = 'Починка ➡️',callback_data = f'wikicraft {idk} 2 {gender}')
			text = 'Используя это инновационное устройство на своей базе, ты можешь создавать стильную одежду для своей некодевочки, которая повысит её живучесть в бою'
			if gender == 1:
				text = 'Используя это инновационное устройство на своей базе, ты можешь создавать стильную одежду для своего некомальчика, которая повысит его живучесть в бою'
			text += '\n\n👖 Штаны за 40 гривень\nРецепт:  💰 Некогривны × 40\nХарактеристики:  +1 макс хп 💗\n\n👗 Костюм горничной\nРецепт:  📦 Картон × 5\nХарактеристики:  +2 макс хп 💗\n\n🦺 Куртка санса\nРецепт:  📦 Картон × 10 | 🦴 Кость санса × 5\nХарактеристики:  +4 макс хп 💗\n\n<code>Создать [назв]</code><i> - скрафтить указанный предмет</i>'
		keyboard.add(callback_button1,callback_button2)
		time.sleep(1)
		phot = call.message.photo[-1].file_id
		bot.edit_message_caption(caption = text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
	elif cmd == "comb":
		txt = 'В случае выигрыша 10 некогривен за пуск возвращаются. Возможные комбинации:\n🍋🍋 - 0 💰\n🍉🍉 - 0 💰\n🍓🍓 - 10 💰\n🍒🍒 - 10 💰\n🍓🍓🍓 - 50 💰\n🍒🍒🍒 - 70 💰\n🍉🍉🍉 - 120 💰\n🍋🍋🍋 - хорни некодевочка 🐱'
		answer_callback_query(bot,call,txt,True)
