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
    encoder = None
    alphabet = ""

    def __init__(self, encoderClass):
        '''
        Constructor
        '''
        self.encoder = encoderClass
        self.alphabet = self.encoder.getAlphabet(None)
        
    def encrypt(self, key, plaintext):
        """
        Encrypt data
        key: string
        plaintext: string
        
        >>> e.encrypt("SECRET", "Vi rymmer i gryningen. Glöm inte stegen.")
        'KMTMQCWVKXVOCMPXIDYPBAMDIIUHIZWR'
        """
        
        plaintext = self.encoder(plaintext)
        
        if key is None:
                key = self.generateRandomKey(plaintext, len(plaintext.getEncoded()))
                print("Generated key: " + key)
        encrypted = ""
        i = 0
        for p in plaintext.getEncoded():
            currIndex = self.alphabet.find(p.upper())
            keyIndex = self.alphabet.find(key[i].upper())
            encrypted += self.alphabet[(currIndex + keyIndex)%len(self.alphabet)]
            i = (i + 1) % len(key)
        
        return encrypted
        
    def decrypt(self, key, ciphertext):
        """
        Decrypt data
        key: string
        ciphertext: string
        
        >>> e.decrypt("SECRET", "KMTMQCWVKXVOCMPXIDYPBAMDIIUHIZWR")
        'VIRYMMERIGRYNINGENGLÖMINTESTEGEN'
        """
        
        ciphertext = self.encoder(ciphertext)
        
        decrypted = ""
        i = 0
        for p in ciphertext.getEncoded():
            currIndex = self.alphabet.find(p.upper())
            keyIndex = self.alphabet.find(key[i].upper())
            decrypted += self.alphabet[(currIndex - keyIndex)%len(self.alphabet)]
            i = (i + 1) % len(key)
        return decrypted
    
    def generateRandomKey(self, length):
        """
        Generates a random key form the alphabet of the specified encoder

        >>> len(e.generateRandomKey(15))
        15
        """
        key=""
        s = self.encoder.getAlphabet(None)
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
    return doctest.testmod(m=thismodule, extraglobs={'e': OneTimePad(encoder.EncoderSV)})

if __name__ == "__main__":
    if testmodule()[0] == 0:
        print("Success!")