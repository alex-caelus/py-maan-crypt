# -*- coding: utf-8 -*-
'''
Module for One time pad encryption and decryption

Example

>>> e = OneTimePad(encoder.EncoderSV)
>>> c = e.encrypt("SECRET", "Vi rymmer i gryningen. Glöm inte stegen.")
>>> m = e.decrypt("SECRET", "KMTMQCWVKXVOCMPXIDYPBAMDIIUHIZWR")
'''
from random import randint

from . import encoder

class OneTimePad(object):
    '''
    Class for the One-Time-Pad encryption scheme.

    :param encoderClass: Specifies which encoder to use when encoding before encryption. It also specifies the alphabet that is to be used when encrypting and decrypting.

    >>> e = OneTimePad(encoder.EncoderSV)
    '''

    def __init__(self, encoderClass):
        '''
        Constructor
        '''
        self.encoder = encoderClass
        self.alphabet = self.encoder.getAlphabet(None)
        
    def encrypt(self, key, plaintext):
        """
        Encrypt data

        :param key: string
        :param plaintext: string
        :returns: string
        
        Examples:

        >>> e = OneTimePad(encoder.EncoderSV)
        >>> e.encrypt("SECRET", "Vi rymmer i gryningen. Glöm inte stegen.")
        'KMTMQCWVKXVOCMPXIDYPBAMDIIUHIZWR'
        """
        
        plaintext = self.encoder(plaintext)
        
        if key is None:
                key = self.generateRandomKey(len(plaintext.getEncoded()))
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

        :param key: string
        :param ciphertext: string
        :returns: ciphertext
        
        >>> e = OneTimePad(encoder.EncoderSV)
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
        Generates a random key form the alphabet of the specified encoder (argument to constructor)
        
        :param length: The length of the generated key
        :returns: A stiring of random letters

        >>> e = OneTimePad(encoder.EncoderSV)
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
    This launches the doctests in this module. 

    Anyone who wants to run tests on this module separately should call this function.

    It takes no arguments.

    :returns: Tuple containing the number of failed testcases followed by the total number of testcases tried.

    ::
    
        return (#failed, #tried)
    """
    import doctest
    import sys
    thismodule = sys.modules[__name__]
    return doctest.testmod(m=thismodule)

if __name__ == "__main__":
    if testmodule()[0] == 0:
        print("Success!")
