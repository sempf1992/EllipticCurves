from AES_good import AES
from EC import *
import random

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
		p = 1
		a = 0
		b = 0
		xG = 0 #xG,yG finite field elements
		yG = 0
		G = Punt(xG,yG)
class Crypto:
    def Crypto(self):
        #do the initialisation
        return
        
    def KeyAgreement(self):
        #do a Diffie-Helman key exchange	
        key =  texttobytes('h?2Trq]k8$s;H,D+')
        iv = texttobytes('h?2Trq]k8$s;H,D+')
        self.AES = AES(key, iv)
        return
    
	def DHSendHost(self, target):
	    a = random.randint(5014,7234)
		return LSEC.G*a #send this to target

	def DHRecHost(self, UGmessage):
		return UGmessage*a #shared secret for host
		
	def DHSendUser(self, host):
		b = random.random(2012,4234)
		return LSEC.G*b #send this to host
		
	def DHRecUser(self, HGmessage):
		return HGmessage*b #shared secret for user with host
	
    def Encrypt(self, plaintext):
        plaintextbytes = texttobytes(plaintext)
        ciphertextbytes = self.AES.encrypt(plaintextbytes)
        return ciphertextbytes
        
    def Decrypt(self, ciphertextbytes):
        plaintextbytes = self.AES.decrypt(ciphertextbytes)
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

crypt = Crypto()
crypt.selftest()
