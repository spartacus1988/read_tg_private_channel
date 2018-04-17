from telethon import TelegramClient
from telethon import utils
from telethon import events
from telethon.tl.functions.messages import SearchRequest
from telethon.tl.types import InputMessagesFilterEmpty
from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.tl.types import ChannelParticipantsSearch, InputChannel
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsRecent
from telethon.utils import get_input_peer

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




def dump_users(client, chat_id, access_hash):
	counter = 0
	offset = 0
	limit = 100
	# нам нужно сделать объект чата, как сказано в документации 
	chat_object = InputChannel(chat_id, access_hash)
	all_participants = []
	while True:
		# тут мы получаем пользователей
		# всех сразу мы получить не можем для этого нам и нужен offset 
		participants = client.invoke(GetParticipantsRequest(
					chat_object, ChannelParticipantsSearch(''), offset, limit, hash=access_hash
				))
		# если пользователей не осталось, т.е мы собрали всех, выходим
		if not participants.users:
			break
		all_participants.extend(['{} {}'.format(x.id, x.username)
						   for x in participants.users])
		users_count = len(participants.users)
		# увеличиваем offset на то кол-во юзеров которое мы собрали
		offset += users_count
		counter += users_count
		print('{} users collected'.format(counter))
		# не забываем делать задержку во избежания блокировки
		sleep(2)
	# сохраняем в файл
	with open('users.txt', 'w') as file:
		file.write('\n'.join(map(str, all_participants)))
			


def dump_userss(client, chat):
	counter = 0
	offset = 0
	limit = 100
	# нам нужно сделать объект чата, как сказано в документации 
	#chat_object = InputChannel(chat_id, access_hash)
	all_participants = []
	while True:
		# тут мы получаем пользователей
		# всех сразу мы получить не можем для этого нам и нужен offset 
		participants = client.invoke(GetParticipantsRequest(
					chat, ChannelParticipantsSearch(''), offset, limit, hash=0
				))
		# если пользователей не осталось, т.е мы собрали всех, выходим
		if not participants.users:
			break
		all_participants.extend(['{} {}'.format(x.id, x.username)
						   for x in participants.users])
		users_count = len(participants.users)
		# увеличиваем offset на то кол-во юзеров которое мы собрали
		offset += users_count
		counter += users_count
		print('{} users collected'.format(counter))
		# не забываем делать задержку во избежания блокировки
		sleep(2)
	# сохраняем в файл
	with open('users.txt', 'w') as file:
		file.write('\n'.join(map(str, all_participants)))




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
	#print(entity[20])
	print(entity[0].name)
	print(entity[0].id)
	print(entity[0].entity.access_hash)
	#print(entity[20].draft)

	#channel = client(ResolveUsernameRequest(entity[0].name)) # Your channel username
	#print(channel)

	#dump_users(client, entity[0].id, entity[0].entity.access_hash)
	#dump_userss(client, entity[0])

	chat_object = InputChannel(entity[20].id, entity[20].entity.access_hash)

	#participants = client.get_participants(chat_object, search='', limit=10)
	#print(participants)


	result = client.invoke(
	GetParticipantsRequest(entity[0].name,  # Getting 7th chat participants
						   filter=ChannelParticipantsRecent(),
						   # List of filters https://lonamiwebs.github.io/Telethon/types/channel_participants_filter.html
						   offset=0,  # getting info from 0th user
						   limit=5,
						   hash=0)  # limiting number of users in a request
	)

	print(result)
	print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa")
	print(result.users[4])
	#info = result
	#print(info.users[3]) # prints info about 4th %filtered% Chat participant

	print('channel')

	#client.idle()