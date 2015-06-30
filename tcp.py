# Tcp Chat server

import socket, select
from crypto import Crypto
#define a user class, this keeps track of the data stream to and from this user
class User:
	def __init__(self, sock_, client):
		self.sock = sock_
		self.client = client

	def __eq__(self, other):
		try:
			return self.client == other.client
		except:
			return False
	def setup(self):
		#do the key exchange
		self.crypto= Crypto()
		msg = self.crypto.DHSendHost()
		self.sock.send(('k' + msg).encode('utf-8'))
		return

	def encrypt(self, msg):
		return self.crypto.Encrypt(msg)

	def decrypt(self, msg):
		return self.crypto.Decrypt(msg)
        
	def fileno(self):
		return self.sock.fileno()
	
	def KeyExchange(self, msg):
		self.crypto.DHRecHost(msg)
		return
	def __str__(self):
		return str(self.client)
#Function to broadcast chat messages to all connected clients
def broadcast_data (USER_rec, message):
	#Do not send the message to master socket and the client who has send us the message
	for user in USER_LIST:
		if user != server_user and user != USER_rec and user in USER_LIST:
			#try:
			msg = user.encrypt(message)
			msg = ('m' + msg).encode('utf-8')
			user.sock.send(msg)
			#except :
				#broken socket connection may be, chat client pressed ctrl+c for example
			#	print("user left")
			#	user.sock.close()
			#	USER_LIST.remove(user)
				

if __name__ == "__main__":
	
	# List to keep track of socket descriptors
	USER_LIST = []
	RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
	PORT = 5000
	
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# this has no effect, why ?
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind(("0.0.0.0", PORT))
	server_socket.listen(10)

	# Add server socket to the list of readable connections
	client = 0
	server_user = User(server_socket, client)
	USER_LIST.append(server_user)

	print("Chat server started on port " + str(PORT))

	while 1:
		# Get the list sockets which are ready to be read through select
		read_users, _, _ = select.select(USER_LIST,[],[])

		for user in read_users:
			#New connection
			if user == server_user:
				# Handle the case in which there is a new connection recieved through server_socket
				sockfd, addr = server_user.sock.accept()
				client += 1
				new_user = User(sockfd, client)
				new_user.setup()
				USER_LIST.append(new_user)
				
				broadcast_data(new_user, "[%s:%s] entered room\n" % addr)
			
			#Some incoming message from a client
			elif user in USER_LIST:
				# Data recieved from client, process it
				#In Windows, sometimes when a TCP program closes abruptly,
				# a "Connection reset by peer" exception will be thrown
				try:

                                        #read data
					data = user.sock.recv(RECV_BUFFER)
                                        #decode the data to string
					if data:
						data = data.decode('utf-8')
						if data[0]=='m':
	                                                #decrypt the data
							data = data[1:]
							data = user.decrypt(data)
							broadcast_data(user, "\r" + '<' + str(user.sock.getpeername()) + '> ' + data)
						elif data[0]=='k':
							data = data[1:]
							data = user.KeyExchange(data)
						else:
							print('received data of unspecified format')
				except:
					broadcast_data(user, "Client (%s, %s) is offline" % addr)
					print("Client (%s, %s) is offline" % addr)
					user.sock.close()
					USER_LIST.remove(user)
					continue
	
	server_socket.close()
