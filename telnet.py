# telnet program example
import socket, select, string, sys
from crypto import Crypto

def prompt() :
	sys.stdout.write('<You> ')
	sys.stdout.flush()

#main function
if __name__ == "__main__":
	
	if(len(sys.argv) < 3) :
		print('Usage : python telnet.py hostname port')
		sys.exit()
	
	host = sys.argv[1]
	port = int(sys.argv[2])
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(2)
	
	# connect to remote host
	try :
		s.connect((host, port))
	except :
		print('Unable to connect')
		sys.exit()

	crypto = Crypto()
	msg = ('k' + crypto.DHSendUser()).encode('utf-8')
	try:
		s.send(msg)
	except:
		print('connection error')
		sys.exit()
		
	print('Connected to remote host. Start sending messages')
	prompt()
	
	while 1:
		socket_list = [sys.stdin, s]
		# Get the list sockets which are readable
		read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
		for sock in read_sockets:
			#incoming message from remote server
			if sock == s:
				data = sock.recv(4096)
				if not data :
					print('\nDisconnected from chat server')
					sys.exit()
				else:
					#print data
					data = data.decode('utf-8')
					if data[0] == 'm':
						data = data[1:]
						sys.stdout.write(crypto.Decrypt(data))
					elif data[0] == 'k':
						data = data[1:]
						crypto.DHRecUser(data)
						sys.stdout.write('\rHandshake complete\n')
					else:
						sys.stdout.write('Input data of non specified format received')
					prompt()
			
			#user entered a message
			else :
				msg = sys.stdin.readline()
				s.send(('m' + crypto.Encrypt(msg)).encode('utf-8'))
				prompt()
