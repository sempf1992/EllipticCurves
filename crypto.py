from stef import AES


def texttobytes(text):
    bytes = []
    i = 0
    while (i < len(text)):
        bytes.append(ord(text[i]))
        i += 1
    return bytes


def bytestotext(bytes):
    text = ""
    i = 0
    while (i < len(bytes)):
        text = text + chr(bytes[i])
        i += 1
    return text


class Crypto:
    def Crypto(self):
        # do the initialisation
        return

    def KeyAgreement(self):
        # do a Diffey-Helman key exchange
        key = texttobytes('h?2Trq]k8$s;H,D+')
        iv = texttobytes('h?2Trq]k8$s;H,D+')
        self.AES = AES(key, iv)
        return

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

        # set key and iv
        key = texttobytes('h?2Trq]k8$s;H,D+')
        iv = texttobytes('h?2Trq]k8$s;H,D+')

        # do a selftest
        self.AES = AES(key, iv)
        # self.AES.selftest()

        # encrypt
        self.AES = AES(key, iv)
        outstring = self.Encrypt(teststring)

        # decrypt
        # self.AES = AES(key, iv)
        # plaintext = self.Decrypt(outstring)

        # print(plaintext)

crypt = Crypto()
crypt.selftest()
