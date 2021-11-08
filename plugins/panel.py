from pyrogram import Client, filters
from tinydb import TinyDB, Query
from . import var
import re
import os

q = Query()







def insert(client, message, from_ch, to_ch):
	try:
		from_ch = int(from_ch)
		to_ch = int(to_ch)
	except:
		message.reply_text(var.invalid_ids)
		return

	search_for_from_ch = TinyDB('database/map.json').search(q.origin == from_ch)
	if len(search_for_from_ch) == 0:
		
		try:
			TinyDB('database/map.json').insert({
				'origin': from_ch,
				'aim': [to_ch]
			})
		except:
			message.reply_text(var.error)
			return

		message.reply_text(var.inserted)
		return
	else:

		get_aim = search_for_from_ch[0]['aim']
		if to_ch in get_aim:
			message.reply_text(var.to_ch_is_exsists)
			return

		get_aim.append(to_ch)

		try:
			TinyDB('database/map.json').update({'aim': get_aim}, q.origin == from_ch)
		except:
			message.reply_text(var.error)
			return

		message.reply_text(var.updated)
		return

def remove(client, message, remove_ch, from_ch):
	
	try:
		from_ch = int(from_ch)
		remove_ch = int(remove_ch)
	except:
		message.reply_text(var.invalid_ids)
		return


	search_for_from_ch = TinyDB('database/map.json').search(q.origin == from_ch)
	if len(search_for_from_ch) == 0:
		message.reply_text(var.from_ch_not_found)
		return

	get_aim = search_for_from_ch[0]['aim']
	if remove_ch in get_aim:
		get_aim.remove(remove_ch)

		try:
			TinyDB('database/map.json').update({'aim': get_aim}, q.origin == from_ch)
		except:
			message.reply_text(var.error)
			return
			
		message.reply_text(var.removed)
	else:
		message.reply_text(var.remove_ch_not_found)
		return

def delete_func(client, message, remove_ch):

	try:
		remove_ch = int(remove_ch)
	except:
		message.reply_text(var.invalid_ids)
		return

	search_for_from_ch = TinyDB('database/map.json').search(q.origin == remove_ch)
	if len(search_for_from_ch) == 0:
		message.reply_text(var.from_ch_not_found)
		return

	TinyDB('database/map.json').remove(q.origin == remove_ch)


	try:
		ccid = str(remove_ch).split('-')[1]
	except:
		ccid = remove_ch

	try:
		os.remove('database')
	except:
		pass


	message.reply_text(var.removed)




@Client.on_message(filters.regex(r'^[Ff]rom (-?\d*) to (-?\d*)$') & filters.chat(var.admin))
def set(client, message):

	text = message.text

	m = re.match(r'^[Ff]rom (-?\d*) to (-?\d*)$', text)
	from_ch = m[1]
	to_ch = m[2]
	insert(client, message, from_ch, to_ch)


@Client.on_message(filters.regex(r'^[Rr]emove (-?\d*) from (-?\d*)$') & filters.chat(var.admin))
def rem(client, message):

	text = message.text

	m = re.match(r'^[Rr]emove (-?\d*) from (-?\d*)$', text)
	remove_ch = m[1]
	from_ch = m[2]
	remove(client, message, remove_ch, from_ch)


@Client.on_message(filters.regex(r'^[Rr]emove (-?\d*)$') & filters.chat(var.admin))
def delete_ch(client, message):
	text = message.text

	m = re.match(r'^[Rr]emove (-?\d*)$', text)
	remove_ch = m[1]
	delete_func(client, message, remove_ch)


@Client.on_message(filters.regex(r'^[Ll]ist$') & filters.chat(var.admin))
def list(client, message):
	
	
	all_channels = TinyDB('database/map.json').all()

	if len(all_channels) == 0:
		message.reply_text(var.all_channels_is_empty)
		return

	message.reply_text('Sending...')
	
	for ch in all_channels:

		origin = ch['origin']
		aim = ch['aim']

		aim_list = []
		for a in aim:
			aim_list.append(str(a))

		aim_list = ' ,'.join(aim_list)

		fmsg = f"""**Origin**: {origin}\n\n**Goals**: {aim_list}"""
		message.reply_text(fmsg, parse_mode = 'markdown')


@Client.on_message(filters.regex(r'^[Ss]ign for (-?\d*)$') & filters.reply & filters.chat(var.admin))
def set_sign_handler(client, message):
	
	text = message.text

	m = re.match(r'^[Ss]ign for (-?\d*)$', text)
	channel = m[1]
	
	try:
		text = message.reply_to_message.text
		channel = int(channel)

	except:
		message.reply_text(var.invalid_syntax)
		return

	search_for_channel = TinyDB('database/sign.json').search(q.id == channel)
	if len(search_for_channel) == 0:

		TinyDB('database/sign.json').insert({'id': channel, 'sign': text})
		message.reply_text(var.inserted)
	else:

		try:
			TinyDB('database/sign.json').update({
				'sign': text
			}, q.id == channel)
		except:
			message.reply_text(var.error)
			return

		message.reply_text(var.updated)





	