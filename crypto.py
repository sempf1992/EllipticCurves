from AES_good import AES
from EC import *
import os
import random
import hmac
import hashlib
import math
def compare_digest(x, y):
    if not (isinstance(x, bytes) and isinstance(y, bytes)):
        raise TypeError("both inputs should be instances of bytes")
    if len(x) != len(y):
        return False
    result = 0
    for a, b in zip(x, y):
        result |= a ^ b
    return result == 0

def texttobytes(text):
    bytes = []
    i = 0
    while ( i < len(text)):
        bytes.append(ord(text[i]))
        i += 1
    return bytes

def bytestotext(bytes):
    text = ""
    i = 0
    while ( i < len(bytes)):
        text = text + chr(bytes[i])
        i += 1
    return text
        
class LSEC: #Locally Stored Elliptic Curve
		#using curve P-521, source: http://cs.ucsb.edu/~koc/ccs130h/notes/ecdsa-cert.pdf page 42 
		p = 23
		a = 2
		b = 1
		n = 15
		curve = Curve(p,a,b)
		xG = FiniteFieldElem(p,10) #xG,yG finite field elements
		yG = FiniteFieldElem(p,3) #xG,yG finite field elements
		G = Punt(curve,xG,yG)
		##Method for finding points
		##for x in range(1, 22):
		##	xG = FiniteFieldElem(p,x) #xG,yG finite field elements
		##	for y in range(1, 22):
		##		try:
		##			yG = FiniteFieldElem(p,3)
		##			G = Punt(curve,xG,yG)
		##			print(G)
		##			break
		##		except:
		##			continue

class Crypto:
	def Crypto(self):
		#do the initialisation
		self.KeySetup = False
		return
        
	def KeyGen(self, KeyData, isHost):

		#transform the key from the diffie-Helman key exchange into bytes
		KeyData = bytes(str(KeyData), 'utf-8')
		#hash that bytestring using a key derrivation sheme
		if isHost:
			dk  = hashlib.pbkdf2_hmac('sha256', KeyData, b'keyhost',   100000, 16)
			dk2 = hashlib.pbkdf2_hmac('sha256', KeyData, b'keyclient', 100000, 16)
			
			#generate IV
			di  = hashlib.pbkdf2_hmac('sha256', KeyData, b'ivhost',   100000, 16)
			di2 = hashlib.pbkdf2_hmac('sha256', KeyData, b'ivclient', 100000, 16)
			
			#hmac keys
			dh  = hashlib.pbkdf2_hmac('sha256', KeyData, b'machost',   100000, 16)
			dh2 = hashlib.pbkdf2_hmac('sha256', KeyData, b'macclient', 100000, 16)

		else:
			#generate keys
			dk  = hashlib.pbkdf2_hmac('sha256', KeyData, b'keyclient', 100000, 16)
			dk2 = hashlib.pbkdf2_hmac('sha256', KeyData, b'keyhost',   100000, 16)

			#generate IV
			di  = hashlib.pbkdf2_hmac('sha256', KeyData, b'ivclient', 100000, 16)
			di2 = hashlib.pbkdf2_hmac('sha256', KeyData, b'ivhost',   100000, 16)
			
			#hmac keys
			dh  = hashlib.pbkdf2_hmac('sha256', KeyData, b'macclient', 100000, 16)
			dh2 = hashlib.pbkdf2_hmac('sha256', KeyData, b'machost',   100000, 16)

		#do a Diffie-Helman key exchange	
		key =  texttobytes('h?2Trq]k8$s;H,D+')
		key2 = bytes('h?2Trq]k8$s;H,D+', 'utf-8')
		iv = texttobytes('h?2Trq]k8$s;H,D+')

		self.AES_enc = AES(dk,  di)
		self.AES_dec = AES(dk2, di2)

		self.enc_hmac = hmac.new(dh,  bytes('', 'utf-8'), hashlib.sha256)
		self.dec_hmac = hmac.new(dh2, bytes('', 'utf-8'), hashlib.sha256)

		return
    
	def DHSendHost(self):
		self.a = random.randint(1, LSEC.n)
			#work for later does not work as of yet but is better
			#randombytes = os.urandom(int(math.log(LSEC.n)//8)
			#randomint = int.from_bytes(b'\x00\x10', byteorder='big', signed=False)# % LSEC.n
			#self.a = randomint
		self.KeySetup = True
		return str(LSEC.G.Clone()*self.a) #send this to target

	def DHRecHost(self, UGmessage):
		if self.KeySetup:
			if UGmessage == "id":
				RecPoint = Eenheid(LSEC.curve)
			else:
				prime = LSEC.p
				x_ = int(UGmessage.split()[1])
				x = FiniteFieldElem(prime, x_)
				y_ = int(UGmessage.split()[3])
				y = FiniteFieldElem(prime, y_)
				RecPoint = Punt(LSEC.curve, x,y)
			self.KeyGen(RecPoint * self.a, True)
			self.a = 0
			self.KeySetup = False
		return
		
	def DHSendUser(self):
		self.b = random.randint(1,LSEC.n)
			#work for later does not work as of yet but is better
			#randombytes = os.urandom(int(math.log(LSEC.n)//8)
			#randomint = int.from_bytes(randombytes, byteorder='big', signed=False)# % LSEC.n
			#self.b = randomint
		self.KeySetup = True
		return str(LSEC.G.Clone()*self.b) #send this to host
		
	def DHRecUser(self, HGmessage):
		if self.KeySetup:
			if HGmessage == "id":
				RecPoint = Eenheid(LSEC.curve)
			else:
				prime = LSEC.p
				x_ = int(HGmessage.split()[1])
				x = FiniteFieldElem(prime, x_)
				y_ = int(HGmessage.split()[3])
				y = FiniteFieldElem(prime, y_)
				RecPoint = Punt(LSEC.curve, x,y)
			self.KeyGen(RecPoint * self.b, False)
			self.b = 0
			self.KeySetup = False
		return 
	
	def Encrypt(self, plaintext):
		plaintextbytes = texttobytes(plaintext)
		ciphertextbytes = self.AES_enc.encrypt(plaintextbytes)
		ciphertext = bytestotext(ciphertextbytes)
		#now put an hmac on the text
		self.enc_hmac.update(bytes(ciphertext, 'utf-8'))
		digest = self.enc_hmac.hexdigest()
		ciphertext = ciphertext + str(digest)
		return ciphertext
        
	def Decrypt(self, ciphertext):
		#split the digest from the rest of the ciphertext
		digest = ciphertext[len(ciphertext)-2*self.dec_hmac.digest_size:]
		digest = bytes(digest, 'utf-8')
		ciphertext = ciphertext[:len(ciphertext) - 2*self.dec_hmac.digest_size]	
		#compare to the rest of the ciphertext
		self.dec_hmac.update(bytes(ciphertext, 'utf-8'))
		byteshex = bytes(self.dec_hmac.hexdigest(), 'utf-8')
		if compare_digest(digest, byteshex):
			#continue if correct		
			ciphertextbytes = texttobytes(ciphertext)
			plaintextbytes = self.AES_dec.decrypt(ciphertextbytes)
			plaintext = bytestotext(plaintextbytes)
			return plaintext
        
	def selftest(self):
        
		teststring = "teststring"

		#set key and iv
		key =  texttobytes('h?2Trq]k8$s;H,D+')
		iv = texttobytes('h?2Trq]k8$s;H,D+')
        
		#do a selftest
		self.AES = AES(key, iv)
		self.AES.selftest()
		teststring2 = teststring
		run = 1
        
		while ( run < 100):
			teststring2 = teststring2 + teststring
			#encrypt
			self.AES = AES(key, iv)
			outstring = self.Encrypt(teststring2)
			
			#decrypt
			self.AES = AES(key, iv)
			plaintext = self.Decrypt(outstring)
            
			if (plaintext != teststring2):
				print("fout by run = " + str(run))
				print(teststring2)
				print(plaintext)
                
			run += 1
        
		print("klaar")

#crypt = Crypto()
#crypt.selftest()
