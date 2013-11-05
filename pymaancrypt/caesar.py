# -*- coding: utf-8 -*-
'''
Module for Caesar encryption and decryption.

Example

>>> e = Caesar(encoder.EncoderSV)
>>> c = e.encrypt(3, "Vi rymmer i gryningen. Glöm inte stegen.")
>>> m = e.decrypt(3, "YLUÄPPHULJUÄQLQJHQJOCPLQWHVWHJHQ")
'''

from . import encoder

class Caesar(object):
    """
    Encryptor class for the Caesar encryption scheme

    :param encoderClass: Specifies which encoder to use when encoding before encryption. It also specifies the alphabet that is to be used when encrypting and decrypting.
    """

    def __init__(self, encoderClass):
        """
        Constructor
        """
        self.encoder = encoderClass
        self.alphabet = self.encoder.getAlphabet(None)
        
    def encrypt(self, key, plaintext):
        """
        Encrypt data

        :param key: integer
        :param plaintext: string
        
        >>> Caesar(encoder.EncoderSV).encrypt(3, "Vi rymmer i gryningen. Glöm inte stegen.")
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
        
        >>> Caesar(encoder.EncoderSV).decrypt(3, "YLUÄPPHULJUÄQLQJHQJOCPLQWHVWHJHQ")
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
        
        >>> Caesar(encoder.EncoderSV).shift('A', 3)
        'D'
        """
        charIndex = self.alphabet.find(character.upper())
        newIndex = (charIndex + key) % len(self.alphabet)
        return self.alphabet[newIndex]

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
