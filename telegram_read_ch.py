# from pytg import Telegram

# tg = Telegram(telegram="~/read_tg_ch/telegram-cli/tg/bin/telegram-cli", pubkey_file="~/read_tg_ch/telegram-cli/tg/tg-server.pub")


#receiver = tg.receiver
# sender = tg.sender



# sender.send_msg("@spartacusxxxxxx", "Hello World!")



#tg.msg("@spartacusxxxxxx", "Hello World!")




#/usr/local/src/tg/bin/telegram-cli --json -k /usr/local/src/tg/tg-server.pub -W -d -P 8089 &


#~/read_tg_ch/telegram-cli/tg/bin/telegram-cli --json -k ~/read_tg_ch/telegram-cli/tg/tg-server.pub -W -d -P 8089 &







# from pytg.sender import Sender

# sender = Sender("127.0.0.1", 8089)
   

# res = sender.msg("@spartacusxxxxxx", "Hello!")



from pytg.receiver import Receiver
from pytg.utils import coroutine


@coroutine
def example_function(receiver):
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


if __name__ == '__main__':
	receiver = Receiver(port=8089)  				# get a Receiver Connector instance
	receiver.start()  								# start the Connector.
	receiver.message(example_function(receiver))  	# add "example_function" function as listeners. You can supply arguments here (like receiver).
	receiver.stop()									# continues here, after exiting while loop in example_function()