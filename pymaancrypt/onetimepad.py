# -*- coding: utf-8 -*-
'''
Created on 24 sep 2013

@author: Marcus
'''
from random import randint

try:
    import encoder
except ImportError:
    import pymaancrypt.encoder

class OneTimePad(object):
    '''
    classdocs
    '''

    def __init__(self, alphabet):
        '''
        Constructor
        '''
        
    def encrypt(self, key, plaindata):
        """
        Encrypt data
        key: string
        plaindata: Instance of pymaancrypt.encoder.BaseEncoder
        
        >>> e.encrypt("SECRET", encoder.EncoderSV("Vi rymmer i gryningen. Glöm inte stegen."))
        'KMTMQCWVKXVOCMPXIDYPBAMDIIUHIZWR'
        """
        alphabet = plaindata.getAlphabet()
        if key is None:
                key = self.generateRandomKey(plaindata, len(plaindata.getEncoded()))
                print("Generated key: " + key)
        encrypted = ""
        i = 0
        for p in plaindata.getEncoded():
            currIndex = alphabet.find(p.upper())
            keyIndex = alphabet.find(key[i].upper())
            encrypted += alphabet[(currIndex + keyIndex)%len(alphabet)]
            i = (i + 1) % len(key)
        
        return encrypted
        
    def decrypt(self, key, cipherdata):
        """
        Decrypt data
        key: string
        ciphertext: Instance of pymaancrypt.encoder.BaseEncoder
        
        >>> e.decrypt("SECRET", "KMTMQCWVKXVOCMPXIDYPBAMDIIUHIZWR")
        'VIRYMMERIGRYNINGENGLÖMINTESTEGEN'
        """
        alphabet = cipherdata.getAlphabet()
        decrypted = ""
        i = 0
        for p in cipherdata.getEncoded():
            currIndex = alphabet.find(p.upper())
            keyIndex = alphabet.find(key[i].upper())
            decrypted += alphabet[(currIndex - keyIndex)%len(alphabet)]
            i = (i + 1) % len(key)
        return decrypted
    
    def generateRandomKey(self, encodeClass, length):
        """
        Generates a random key form the alphabet of the specified encoder

        >>> len(e.generateRandomKey(encoder.EncoderSV, 15))
        15
        """
        key=""
        try:
            s = encodeClass.getAlphabet()
        except:
            s = encodeClass.getAlphabet(None)
        for i in range(length):
            key += s[randint(0, len(s)-1)]
        return key
        
def testmodule():
    """
    Should return (#failed, #tried)
    """
    import doctest
    import sys
    thismodule = sys.modules[__name__]
    return doctest.testmod(m=thismodule, extraglobs={'e': OneTimePad("ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ")})

if __name__ == "__main__":
    if testmodule()[0] == 0:
        print("Success!")