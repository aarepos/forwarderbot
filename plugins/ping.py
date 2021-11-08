from pyrogram import Client, filters
from . import var

@Client.on_message(filters.regex('[Pp]ing') & filters.user(var.admin))
def pong(client, message):
	message.reply_text('pong!')