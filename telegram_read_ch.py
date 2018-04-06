from pytg.sender import Sender
from pytg.receiver import Receiver
from pytg.utils import coroutine

import json

@coroutine
def example_function(receiver):
	try:
		while True:
		

			msg = (yield)

			print('Full dump: {array}'.format(array=str(msg)))
			
			if msg.event == "message":
				print(msg)
				continue 

	except KeyboardInterrupt:
		receiver.stop()
		print("Exiting")


if __name__ == '__main__':
	receiver = Receiver(port=8089)  				
	sender = Sender(host="127.0.0.1", port=8089) 

	#result = sender.dialog_list()
	#print(str(result)) 

	result = sender.history('$050000007011c644f7af479d18e7ddac', limit=1, offset=1)

	result = json.dumps(result, sort_keys=True, indent=4, separators=(',', ': '))
	#print(str(result))

	result = json.loads(result)
	#print(str(result))

	#print(result[0]['text'])


	print(result[0])

	# for item in result:
	# 	print(item['text'])
		


	#print(str(result['to'])) 




	#receiver.start()  								
	#receiver.message(example_function(receiver))  	
	#receiver.stop()									





