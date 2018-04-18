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
	all_participants = []
	current_user = []
	while True:
		participants = client.invoke(
		GetParticipantsRequest(chat_name,  
						   filter=ChannelParticipantsRecent(),
						   offset=offset,  
						   limit=200,
						   hash=0)  
		)
		if not participants.users:
			break
		#if counter>5000:
		#	break

		for user in participants.users:
			current_user = []
			current_user.append(user.first_name)
			current_user.append(user.last_name)
			current_user.append(user.phone)
			current_user.append(user.username)
			all_participants.append(current_user)

		users_count = len(participants.users)
		offset += users_count
		counter += users_count
		print('{} users collected'.format(counter))
		time.sleep(0.5)
		
	file_name = "%s.csv" %  str(chat_name)
	columns = ["first_name", "last_name", "phone", "username"]
	pd.DataFrame(all_participants, columns = columns).to_csv(file_name, index = False)
			






if __name__ == '__main__':

	#logger = init_log()
	list_of_chats = []
	print('main')
	entitys = client.get_dialogs(limit=100, offset_id=0)
	#print(entity[0])
	#print(entitys[0].name)
	#print(entitys[0].id)
	#print(entitys[0].entity.access_hash)

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
			#print("condition success")
			list_of_chats.append(entity.name)

	#print(list_of_chats)
	#dump_users(client, list_of_chats[1])
	#dump_users(client, 'Aus NZ Jobs')
	#dump_users(client, 'IT Jobs in Australia 🇦🇺')
	#dump_users(client, 'Jobs IT Australia - thegongzuo.com. send CVs to aucv@nextgentechinc.com')
	#dump_users(client, 'IT jobs in Australia')
	#dump_users(client, 'Jobs - non IT Australia')
	#dump_users(client, 'Alpha People AZ-NZ Job board- Madhu.mutyam@alpha-people.com.au')

	for chat_name in list_of_chats:
		dump_users(client, chat_name)







