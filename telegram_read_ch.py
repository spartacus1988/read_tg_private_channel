from pytg.sender import Sender
from pytg.receiver import Receiver
from pytg.utils import coroutine

import json
import sys

@coroutine
def listen_function(receiver):
	try:
		while True:
		

			msg = (yield)

			#print('Full dump: {array}'.format(array=str(msg)))
			
			if msg.event == "message":
				print(msg)
				continue 

	except KeyboardInterrupt:
		receiver.stop()
		print("Exiting")


def history_function(sender, chat_id, deep_history):
	result = sender.history(chat_id, limit=1, offset=1)
	result = json.dumps(result, sort_keys=True, indent=4, separators=(',', ': '))
	result = json.loads(result)
	reverse_list = []
	for item in result[:deep_history]:
		reverse_list.insert(0, item['text'])
		
	for item in reverse_list:
		print(item)



if __name__ == '__main__':
	receiver = Receiver(port=8089)  				
	sender = Sender(host="127.0.0.1", port=8089) 

	history_function(sender, '$050000007011c644f7af479d18e7ddac', int(sys.argv[1]))
	
	receiver.start()  								
	receiver.message(listen_function(receiver))  	
	receiver.stop()									





