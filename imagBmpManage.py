import binascii, os.path, urllib, random
 
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from PIL import Image
import os

class BmpManager():
    def __init__(self,image,motdepass):
        self.imageClear = image
        self.getHeader()
        # Initialization Vector
        self.IV = 'mastersidi202203'.encode('utf8')
        #AES KEY
        self.KEY = motdepass.encode("utf8")
        #AES Mode
        self.mode = AES.MODE_CBC


    def getHeader(self):
        imgBin = open(self.imageClear, 'rb')
        # BMP is 14 bytes
        bmpheader = imgBin.read(14)
        # DIB is 40 bytes
        dibheader = imgBin.read(40)
        self.__get_sizes__(dibheader)
        self._bmpheader = bmpheader
        self._dibheader = dibheader
        imgBin.close()

    def __get_sizes__(self, dibheader):
        # Get image's dimensions (at offsets 4 and 8 of the DIB header)
        DIBheader = []
        for i in range(0,80,2):
            DIBheader.append(int(binascii.hexlify(dibheader)[i:i+2],16))
        self.width = sum([DIBheader[i+4]*256**i for i in range(0,4)])
        self.height = sum([DIBheader[i+8]*256**i for i in range(0,4)])
        #print(f"size :",self.width,self.height)

    def encrypt(self):
        BLOCK_SIZE = 16  # Bytes
        self.img_enc = "img_enc.bmp"
        f_in = open(self.imageClear, 'rb')
        f_out = open(self.img_enc, 'wb')
        f_out.write(self._bmpheader)
        f_out.write(self._dibheader)

        image_data = f_in.read()[54:]
        print("ima data enc :", len(image_data))

        cleartext = binascii.unhexlify(binascii.hexlify(image_data))

        cleartext = pad(cleartext, BLOCK_SIZE)

        encryptor = AES.new(self.KEY, self.mode)#,self.IV)
        # Perform the encryption and write output to file

        enc = encryptor.encrypt(cleartext)
        print ("len after enc :" ,len(enc))

        f_out.write(enc)
        f_in.close()
        f_out.close()

    def decrypt(self):
        BLOCK_SIZE = 16  # Bytes
        self.img_enc = "img_enc.bmp"
        f_in = open(self.img_enc, 'rb')

        # BMP is 14 bytes
        bmpheader = f_in.read(14)
        # DIB is 40 bytes
        dibheader = f_in.read(40)
        self.__get_sizes__(dibheader)
        self._bmpheader = bmpheader
        self._dibheader = dibheader
        f_out = open("dec.bmp", 'wb')
        f_out.write(self._bmpheader)
        f_out.write(self._dibheader)

        image_data = f_in.read()

        print("len to dec :", len(image_data))

        #cleartext = binascii.unhexlify(binascii.hexlify(image_data))

        decryptor = AES.new(self.KEY, self.mode)#, self.IV)
        # Perform the encryption and write output to file

        dec = decryptor.decrypt(image_data)

        cleartext = unpad(dec, BLOCK_SIZE)

        print("len unpad :", len(cleartext))

        f_out.write(cleartext)

        f_in.close()
        f_out.close()


'''
        # 256-bit symmetric key
        key = os.urandom(16)

        # AES ECB cipher
        aes_ecb_cipher = Cipher(AES(key), ECB())

        aes_block_size_in_bits = 128
        pkcs7_padder = padding.PKCS7(aes_block_size_in_bits).padder()
        padded_plaintext = pkcs7_padder.update(cleartext) + pkcs7_padder.finalize()

        encryptedImage = aes_ecb_cipher.encryptor().update(padded_plaintext)

        f_out.write(encryptedImage)
        f_in.close()
        f_out.close()
'''
       # im = Image.open(self.img_enc)
        # im.show()
