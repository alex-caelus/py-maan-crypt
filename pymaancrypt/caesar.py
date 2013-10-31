# -*- coding: utf-8 -*-
'''
Created on 12 sep 2013

@author: Marcus
'''

try:
    import encoder
except ImportError:
    import pymaancrypt.encoder

class Caesar(object):
    '''
    classdocs
    '''

    def __init__(self):
        """
        Constructor
        """
        
    def encrypt(self, key, plaindata):
        """
        Encrypt data
        key: integer
        plaindata: Instance of pymaancrypt.encoder.BaseEncoder
        
        >>> e.encrypt(3, encoder.EncoderSV("Vi rymmer i gryningen. Glöm inte stegen."))
        'YLUÄPPHULJUÄQLQJHQJOCPLQWHVWHJHQ'
        """
        encrypted = ""
        for p in plaindata.getEncoded():
            encrypted += self.shift(p, key, plaindata.getAlphabet())
        return encrypted
        
    def decrypt(self, key, cipherdata):
        """
        Decrypt data
        key: integer
        cipherdata: Instance of pymaancrypt.encoder.BaseEncoder
        
        >>> e.decrypt(3, "YLUÄPPHULJUÄQLQJHQJOCPLQWHVWHJHQ")
        'VIRYMMERIGRYNINGENGLÖMINTESTEGEN'
        """
        decrypted = ""
        for p in cipherdata.getEncoded():
            decrypted += self.shift(p, -int(key), cipherdata.getAlphabet())
        return decrypted
    
    
    def shift(self, character, key, alphabet):
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
    return doctest.testmod(m=thismodule, extraglobs={'e': Caesar("ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ")})

if __name__ == "__main__":
    if testmodule()[0] == 0:
        print("Success!")
