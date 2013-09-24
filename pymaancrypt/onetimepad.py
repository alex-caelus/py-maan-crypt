# -*- coding: utf-8 -*-
'''
Created on 24 sep 2013

@author: Marcus
'''

try:
    import encoder
except ImportError:
    import pymaancrypt.encoder

class OneTimePad(object):
    '''
    classdocs
    '''
    alphabet = ""

    def __init__(self, alphabet):
        '''
        Constructor
        '''
        self.alphabet = alphabet
        
    def encrypt(self, key, plaintext):
        """
        Encrypt data
        key: string
        plaintext: string
        
        >>> e.encrypt("SECRET", encoder.EncoderSV("Vi rymmer i gryningen. Glöm inte stegen."))
        'KMTMQCWVKXVOCMPXIDYPBAMDIIUHIZWR'
        """
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
        decrypted = ""
        i = 0
        for p in ciphertext:
            currIndex = self.alphabet.find(p.upper())
            keyIndex = self.alphabet.find(key[i].upper())
            decrypted += self.alphabet[(currIndex - keyIndex)%len(self.alphabet)]
            i = (i + 1) % len(key)
        return decrypted
        
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