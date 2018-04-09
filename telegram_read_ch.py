
from telethon import TelegramClient
from telethon import utils
from telethon import events
from telethon.tl.functions.messages import SearchRequest
from telethon.tl.types import InputMessagesFilterEmpty

import time


def extract_credentials(pathfile):
	 with open(pathfile, 'r') as f:
			for line in f:
				api_id, api_hash = line.strip().split(':')
				return api_id, api_hash

api_id, api_hash = extract_credentials('credentials.txt')
client = TelegramClient('session_name', api_id, api_hash, update_workers=1, spawn_read_thread=False)
client.start()


def history_function(chat_name, list_of_queries, min_date, limit):	
	filter = InputMessagesFilterEmpty()
	for query in list_of_queries:	
		result = client(SearchRequest(
			peer=chat_name,      		# On which chat/conversation
			q=query,      				# What to search for
			filter=filter,  			# Filter to use (maybe filter for media)
			min_date=min_date,  		# Unix time
			max_date=None,  			# Maximum date
			offset_id=0,    			# ID of the message to use as offset
			add_offset=0,   			# Additional offset
			limit=limit,       			# How many results
			max_id=0,       			# Maximum message ID
			min_id=0,       			# Minimum message ID
			from_id=None    			# Who must have sent the message (peer)
		))
		#print(result.messages[0].message)
		print(result.messages)




# @client.on(events.NewMessage)
# def keywords_handler(event):
# 	if '12' in event.raw_text:
# 		print("ss")

# 	for keyword in keywords:
# 		if keyword in event.raw_text:
# 			print(event.raw_text)

@client.on(events.NewMessage(chats=('Signal Profits')))
def keywords_handler(event):
	for keyword in keywords:
	    if keyword in event.raw_text:
	    	print(event.raw_text)




if __name__ == '__main__':

	#Set param for searching
	chat_name = 'Signal Profits'
	keywords = ['buy', 'target', 'stoploss']
	now = int(time.time())
	#print(now)
	yesterday = now - 86400
	limit = 100

	history_function(chat_name, keywords, yesterday, limit)

	print('main')

	client.idle()