# -*- coding: utf-8 -*-
'''
Created on 12 sep 2013

@author: Marcus
'''

from . import encoder

class Caesar(object):
    '''
    classdocs
    '''
    encoder = None
    alphabet = ""

    def __init__(self, encoderClass):
        """
        Constructor
        """
        self.encoder = encoderClass
        self.alphabet = self.encoder.getAlphabet(None)
        
    def encrypt(self, key, plaintext):
        """
        Encrypt data
        key: integer
        plaintext: string
        
        >>> e.encrypt(3, "Vi rymmer i gryningen. Glöm inte stegen.")
        'YLUÄPPHULJUÄQLQJHQJOCPLQWHVWHJHQ'
        """
        
        plaintext = self.encoder(plaintext)
        
        encrypted = ""
        for p in plaintext.getEncoded():
            encrypted += self.shift(p, key)
        return encrypted
        
    def decrypt(self, key, ciphertext):
        """
        Decrypt data
        key: integer
        ciphertext: string
        
        >>> e.decrypt(3, "YLUÄPPHULJUÄQLQJHQJOCPLQWHVWHJHQ")
        'VIRYMMERIGRYNINGENGLÖMINTESTEGEN'
        """
        
        ciphertext = self.encoder(ciphertext)
        
        decrypted = ""
        for p in ciphertext.getEncoded():
            decrypted += self.shift(p, -int(key))
        return decrypted
    
    
    def shift(self, character, key):
        """
        Shifts the supplied character, the amount of steps specified by key, to the right
        
        >>> e.shift('A', 3)
        'D'
        """
        charIndex = self.alphabet.find(character.upper())
        newIndex = (charIndex + key) % len(self.alphabet)
        return self.alphabet[newIndex]

def testmodule():
    """
    Should return (#failed, #tried)
    """
    import doctest
    import sys
    thismodule = sys.modules[__name__]
    return doctest.testmod(m=thismodule, extraglobs={'e': Caesar(encoder.EncoderSV)})

if __name__ == "__main__":
    if testmodule()[0] == 0:
        print("Success!")
