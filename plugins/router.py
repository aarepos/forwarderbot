from pyrogram import Client, filters
from tinydb import TinyDB, Query
from . import var
import re

q = Query()


async def save_in_db(cid, mid, message_ids, to_mid = None):
	TinyDB(f'database/{cid}.json').insert({"mid": mid,"to_mid": to_mid, "message_ids": message_ids})


def check_point(update):
	
	cid = update.chat.id

	search_for_channel = TinyDB('database/map.json').search(q.origin == cid)
	if len(search_for_channel) == 0:
		return False
	get_aim = search_for_channel[0]['aim']
	if len(get_aim) == 0:
		return False
	
	return True


@Client.on_message(filters.channel & filters.create(
    func = lambda f, c, u: check_point(u)
) & ~filters.reply & ~filters.edited)
async def send_new_post(client, message):

	cid = message.chat.id
	mid = message.message_id
	get_aim = TinyDB('database/map.json').search(q.origin == cid)[0]['aim']

	# print(message)

	try:
		text = message.text
		if text == None: raise
		is_text = True
	except:
		try:
			text = message.caption
			if text == None: raise
			is_text = False
		except:
			text = ''
			is_text = False

	
	try:
		text = re.sub(r'(@[A-Za-z1-9_]*)', '', text)
	except:
		pass

	message_ids = {}

	for ch in get_aim:

		search_for_sign = TinyDB('database/sign.json').search(q.id == ch)
		if len(search_for_sign) == 0:
			sign = var.default_sign
		else:
			sign = search_for_sign[0]['sign']

		if is_text == True:
			try:
				# print('is text is True')
				post = await client.send_message(
					chat_id = ch,
					text = text + '\n' + sign,
					parse_mode = 'markdown'
				)
				message_ids[ch] = post.message_id

			except:
				print(f"I CAN'T SEND MESSAGE TO {ch}")
				return

		else:
			# print('hi')
			try:
				post = await client.copy_message(
					chat_id = ch,
					from_chat_id = cid,
					message_id = mid,
					caption = text + '\n' + sign,
					parse_mode = 'markdown'
				)
				
				message_ids[ch] = post.message_id

			except:
				print(f"I CAN'T SEND MESSAGE TO {ch}")
				return

	cid = str(cid).split('-')[1]
	await save_in_db(cid, mid, message_ids)


@Client.on_message(filters.channel & filters.create(
    func = lambda f, c, u: check_point(u)
) & filters.reply)
async def send_new_post_with_reply(client, message):

	cid = message.chat.id
	mid = message.message_id
	to_mid = message.reply_to_message.message_id
	get_aim = TinyDB('database/map.json').search(q.origin == cid)[0]['aim']

	# print(message)

	ccid = str(cid).split('-')[1]
	search_for_to_mid = TinyDB(f'database/{ccid}.json').search(q.mid == to_mid)
	if len(search_for_to_mid) == 0:
		return

	msg_ids = search_for_to_mid[0]['message_ids']

	try:
		text = message.text
		if text == None: raise
		is_text = True
	except:
		try:
			text = message.caption
			if text == None: raise
			is_text = False
		except:
			text = ''
			is_text = False

	
	try:
		text = re.sub(r'(@[A-Za-z1-9_]*)', '', text)
	except:
		pass

	message_ids = {}

	for ch in get_aim:

		reply_to = msg_ids[str(ch)]
		search_for_sign = TinyDB('database/sign.json').search(q.id == ch)
		if len(search_for_sign) == 0:
			sign = var.default_sign
		else:
			sign = search_for_sign[0]['sign']

		if is_text == True:
			try:
				# print('is text is True')
				post = await client.send_message(
					chat_id = ch,
					text = text + '\n' + sign,
					parse_mode = 'markdown',
					reply_to_message_id = reply_to
				)
				message_ids[ch] = post.message_id

			except:
				print(f"I CAN'T SEND MESSAGE TO {ch}")
				return

		else:
			# print('hi')
			try:
				post = await client.copy_message(
					chat_id = ch,
					from_chat_id = cid,
					message_id = mid,
					caption = text + '\n' + sign,
					parse_mode = 'markdown',
					reply_to_message_id = reply_to
				)
				
				message_ids[ch] = post.message_id

			except:
				print(f"I CAN'T SEND MESSAGE TO {ch}")
				return

	cid = str(cid).split('-')[1]
	await save_in_db(cid, mid, message_ids, to_mid)


@Client.on_deleted_messages(filters.channel & filters.create(
    func = lambda f, c, u: check_point(u)
), group = -1)
async def delete_messagess(client, message):
	# print(message[0]['message_id'])
	# print('start deleting...')
	for msg in message:
		cid = msg['chat']['id']
		mid = msg['message_id']

		ccid = str(cid).split('-')[1]
		# search_for_to_mid = TinyDB(f'database/{ccid}.json').search(q.to_mid == mid)
		# if search_for_to_mid != 0:
		# 	for i in search_for_to_mid:
		# 		msg_ids = i['message_ids']
				
		# 		# sub_mid = i['mid']

		# 		# while True:

		# 		# 	search_for_sub_posts = TinyDB(f'database/{ccid}.json').search(q.to_mid == sub_mid)
		# 		# 	if search_for_sub_posts == 0:
		# 		# 		break

		# 		# 	sub_msg_ids = search_for_sub_posts[0]['message_ids']
		# 		# 	sub_mid = search_for_sub_posts[0]['mid']
		# 		# 	for ch in sub_msg_ids:
		# 		# 		try:
		# 		# 			await client.delete_messages(
		# 		# 				chat_id = ch,
		# 		# 				message_ids = sub_msg_ids[ch]
		# 		# 			)
		# 		# 			print('done')
		# 		# 		except:
		# 		# 			print(f"I CAN'T DELETE MESSAGE IN {ch}")



		# 		for ch in msg_ids:
		# 			try:
		# 				await client.delete_messages(
		# 					chat_id = ch,
		# 					message_ids = msg_ids[ch]
		# 				)
		# 				print('done')
		# 			except:
		# 				print(f"I CAN'T DELETE MESSAGE IN {ch}")
		# else:
		# 	print('no sub')

		search_for_mid = TinyDB(f'database/{ccid}.json').search(q.mid == mid)
		if len(search_for_mid) != 0:
			msg_ids = search_for_mid[0]['message_ids']
			for ch in msg_ids:
				try:
					await client.delete_messages(
						chat_id = ch,
						message_ids = msg_ids[ch]
					)
				except:
					print(f"I CAN'T DELETE MESSAGE IN {ch}")

			TinyDB(f'database/{ccid}.json').remove(q.mid == mid)
		else:
			print('not found')


@Client.on_message(filters.channel & filters.create(
    func = lambda f, c, u: check_point(u)
) & filters.edited)
async def edit_message(client, message):
	

	try:
		text = message.text
		if text == None: raise
		is_text = True
	except:
		try:
			text = message.caption
			if text == None: raise
			is_text = False
		except:
			text = ''
			is_text = False


	try:
		text = re.sub(r'(@[A-Za-z1-9_]*)', '', text)
	except:
		pass


	cid = message.chat.id
	mid = message.message_id
	ccid = str(cid).split('-')[1]
	search_for_mid = TinyDB(f'database/{ccid}.json').search(q.mid == mid)

	if len(search_for_mid) == 0: return

	channels = search_for_mid[0]['message_ids']


	for ch in channels:
		msg_id = channels[ch]

		search_for_sign = TinyDB('database/sign.json').search(q.id == int(ch))
		if len(search_for_sign) == 0:
			sign = var.default_sign
		else:
			sign = search_for_sign[0]['sign']

		if is_text == True:

			await client.edit_message_text(
				chat_id = ch,
				message_id = msg_id,
				text = text + '\n' + sign,
				parse_mode = 'markdown'
			)

		else:
			await client.edit_message_caption(
				chat_id = ch,
				message_id = msg_id,
				caption = text + '\n' + sign,
				parse_mode = 'markdown'
			)

	

@Client.on_message(~filters.channel & filters.create(
    func = lambda f, c, u: check_point(u)
))
async def send_post_from_bot(client, message):

	cid = message.chat.id
	mid = message.message_id
	get_aim = TinyDB('database/map.json').search(q.origin == cid)[0]['aim']

	# print(message)

	try:
		text = message.text
		if text == None: raise
		is_text = True
	except:
		try:
			text = message.caption
			if text == None: raise
			is_text = False
		except:
			text = ''
			is_text = False

	
	try:
		text = re.sub(r'(@[A-Za-z1-9_]*)', '', text)
	except:
		pass

	message_ids = {}

	for ch in get_aim:

		search_for_sign = TinyDB('database/sign.json').search(q.id == ch)
		if len(search_for_sign) == 0:
			sign = var.default_sign
		else:
			sign = search_for_sign[0]['sign']

		if is_text == True:
			try:
				# print('is text is True')
				post = await client.send_message(
					chat_id = ch,
					text = text + '\n' + sign,
					parse_mode = 'markdown'
				)
				message_ids[ch] = post.message_id

			except:
				print(f"I CAN'T SEND MESSAGE TO {ch}")
				return

		else:
			# print('hi')
			try:
				post = await client.copy_message(
					chat_id = ch,
					from_chat_id = cid,
					message_id = mid,
					caption = text + '\n' + sign,
					parse_mode = 'markdown'
				)
				
				message_ids[ch] = post.message_id

			except:
				print(f"I CAN'T SEND MESSAGE TO {ch}")
				return

	
	try:
		cid = str(cid).split('-')[1]
	except:
		pass

	await save_in_db(cid, mid, message_ids)












