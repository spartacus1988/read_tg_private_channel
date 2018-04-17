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
import pandas as pd
import os
import csv

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





def dump_users(client, chat_name):
	counter = 0
	offset = 0
	#limit = 100
	all_participants = []
	current_user = []
	while True:
		# тут мы получаем пользователей
		# всех сразу мы получить не можем для этого нам и нужен offset 
		participants = client.invoke(
		GetParticipantsRequest(chat_name,  # Getting 7th chat participants
						   filter=ChannelParticipantsRecent(),
						   # List of filters https://lonamiwebs.github.io/Telethon/types/channel_participants_filter.html
						   offset=offset,  # getting info from 0th user
						   limit=200,
						   hash=0)  # limiting number of users in a request
		)
		# если пользователей не осталось, т.е мы собрали всех, выходим
		if not participants.users:
			break
		if counter>5000:
			break
		# all_participants.extend(['{} {} {} {}'.format(x.first_name, x.last_name, x.phone, x.username)
		# 				   for x in participants.users])


		for user in participants.users:
			current_user = []
			current_user.append(user.first_name)
			current_user.append(user.last_name)
			current_user.append(user.phone)
			current_user.append(user.username)
			all_participants.append(current_user)

		users_count = len(participants.users)
		# увеличиваем offset на то кол-во юзеров которое мы собрали
		offset += users_count
		counter += users_count
		print('{} users collected'.format(counter))
		# не забываем делать задержку во избежания блокировки
		time.sleep(0.5)
		
	# сохраняем в файл
	#with open('users.txt', 'w') as file:
	#with open('users.csv', 'w') as csvfile:
		#file.write('\n'.join(map(str, all_participants)))

	file_name = "%s.csv" %  str(chat_name)
	columns = ["first_name", "last_name", "phone", "username"]
	pd.DataFrame(all_participants, columns = columns).to_csv(file_name, index = False)
			






if __name__ == '__main__':

	#logger = init_log()

	#Set param for searching
	chat_name = 'IT Jobs in Australia'
	keywords = ['it', 'job', 'Australia']
	now = int(time.time())
	#print(now)
	yesterday = now - 86400
	limit = 100
	list_of_chats = []

	#history_function(chat_name, keywords, yesterday, limit)

	print('main')

	#channel = client(ResolveUsernameRequest('IT_Jobs_in_Australia')) # Your channel username
	#entity = client.get_dialogs(limit=10,offset_id=0)


	entitys = client.get_dialogs(limit=100, offset_id=0)
	#print(entity[20])
	print(entitys[0].name)
	print(entitys[0].id)
	print(entitys[0].entity.access_hash)

	for entity in entitys:
		#print(entity.name)
		if entity.name == 'IT Jobs in Australia 🇦🇺'\
		or\
		entity.name == 'Jobs IT Australia - thegongzuo.com. send CVs to aucv@nextgentechinc.com'\
		or\
		entity.name == 'Aus NZ Jobs'\
		or\
		entity.name == 'IT jobs in Australia'\
		or\
		entity.name == 'Jobs - non IT Australia'\
		or\
		entity.name == 'Alpha People AZ-NZ Job board- Madhu.mutyam@alpha-people.com.au':
			print("condition success")
			list_of_chats.append(entity.name)

	print(list_of_chats)




	#dump_users(client, list_of_chats[1])

	dump_users(client, 'Aus NZ Jobs')







	#print(entity[20].draft)

	#channel = client(ResolveUsernameRequest(entity[0].name)) # Your channel username
	#print(channel)

	#dump_users(client, entity[0].id, entity[0].entity.access_hash)
	#dump_userss(client, entity[0])

	#chat_object = InputChannel(entity[20].id, entity[20].entity.access_hash)

	#participants = client.get_participants(chat_object, search='', limit=10)
	#print(participants)


	# result = client.invoke(
	# GetParticipantsRequest(entity[0].name,  # Getting 7th chat participants
	# 					   filter=ChannelParticipantsRecent(),
	# 					   # List of filters https://lonamiwebs.github.io/Telethon/types/channel_participants_filter.html
	# 					   offset=0,  # getting info from 0th user
	# 					   limit=5,
	# 					   hash=0)  # limiting number of users in a request
	# )

	# print(result)
	# print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa")
	# print(result.users[0])
	# print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa")
	# print(result.users[1])
	# print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa")
	# print(result.users[2])
	# #info = result
	# #print(info.users[3]) # prints info about 4th %filtered% Chat participant

	print('channel')

	#client.idle()