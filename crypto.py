from AES_good import AES
from EC import *
import random
import hmac
import hashlib

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
		return
        
	def KeyGen(self, KeyData):
		#do a Diffie-Helman key exchange	
		key =  texttobytes('h?2Trq]k8$s;H,D+')
		key2 = bytes('h?2Trq]k8$s;H,D+', 'utf-8')
		iv = texttobytes('h?2Trq]k8$s;H,D+')
		self.AES_enc = AES(key, iv)
		self.AES_dec = AES(key, iv)
		self.enc_hmac = hmac.new(key2)#, "", hashlib.sha256)
		self.dec_hmac = hmac.new(key2)#, "", hashlib.sha256)
		return
    
	def DHSendHost(self):
		self.a = random.randint(1, LSEC.n)
		return str(LSEC.G.Clone()*self.a) #send this to target

	def DHRecHost(self, UGmessage):
		if UGmessage == "id":
			RecPoint = Eenheid(LSEC.curve)
		else:
			prime = LSEC.p
			x_ = int(UGmessage.split()[1])
			x = FiniteFieldElem(prime, x_)
			y_ = int(UGmessage.split()[3])
			y = FiniteFieldElem(prime, y_)
			RecPoint = Punt(LSEC.curve, x,y)
		self.KeyGen(RecPoint * self.a)
		return
		
	def DHSendUser(self):
		self.b = random.randint(1,LSEC.n)
		return str(LSEC.G.Clone()*self.b) #send this to host
		
	def DHRecUser(self, HGmessage):
		if HGmessage == "id":
			RecPoint = Eenheid(LSEC.curve)
		else:
			prime = LSEC.p
			x_ = int(HGmessage.split()[1])
			x = FiniteFieldElem(prime, x_)
			y_ = int(HGmessage.split()[3])
			y = FiniteFieldElem(prime, y_)
			RecPoint = Punt(LSEC.curve, x,y)
		self.KeyGen(RecPoint * self.b)
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
