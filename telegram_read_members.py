from telethon import TelegramClient
from telethon import utils
from telethon import events
from telethon.tl.functions.messages import SearchRequest
from telethon.tl.types import InputMessagesFilterEmpty
from telethon.tl.functions.contacts import ResolveUsernameRequest

import time
import logging

def init_log():
	logging.basicConfig(
		format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
		level=logging.DEBUG,
		filename='bot.log',
		filemode='w',
	)
	logger = logging.getLogger(__name__)
	return logger


def extract_credentials(pathfile):
	with open(pathfile, 'r') as f:
			for line in f:
				api_id, api_hash = line.strip().split(':')
				return api_id, api_hash

api_id, api_hash = extract_credentials('aman_sethi.txt')
client = TelegramClient('aman_sethi_session_name', api_id, api_hash, update_workers=1, spawn_read_thread=False)
client.start()


def history_function(chat_name, list_of_queries, min_date, limit):	
	filter = InputMessagesFilterEmpty()
	for query in list_of_queries:	
		result = client(SearchRequest(
			peer=chat_name,				# On which chat/conversation
			q=query,					# What to search for
			filter=filter,				# Filter to use (maybe filter for media)
			min_date=min_date,			# Unix time
			max_date=None,				# Maximum date
			offset_id=0,				# ID of the message to use as offset
			add_offset=0,				# Additional offset
			limit=limit,				# How many results
			max_id=0,					# Maximum message ID
			min_id=0,					# Minimum message ID
			from_id=None				# Who must have sent the message (peer)
		))
		#print(result.messages[0].message)
		print(result.messages)




# @client.on(events.NewMessage)
# def keywords_handler(event):
# 	logger.info(event.raw_text)

# @client.on(events.NewMessage(chats=('')))
# def keywords_handler(event):
# 	print('msg')
# 	logger.info(event.raw_text)
# 	for keyword in keywords:
# 		if keyword in event.raw_text:
# 			print(event.raw_text)
# 			logger.info(event.raw_text)
			




if __name__ == '__main__':

	#logger = init_log()

	#Set param for searching
	chat_name = 'IT Jobs in Australia'
	keywords = ['it', 'job', 'Australia']
	now = int(time.time())
	#print(now)
	yesterday = now - 86400
	limit = 100

	#history_function(chat_name, keywords, yesterday, limit)

	print('main')

	#channel = client(ResolveUsernameRequest('IT_Jobs_in_Australia')) # Your channel username
	#entity = client.get_dialogs(limit=10,offset_id=0)

	
	entity = client.get_dialogs(offset_id=0)
	print(entity[0])

	print('channel')

	#client.idle()