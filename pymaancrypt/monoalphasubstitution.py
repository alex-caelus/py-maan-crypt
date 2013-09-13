# -*- coding: utf-8 -*-
"""
Created on 12 sep 2013

@author: Alexander
"""
import encoder

class MonoAlphaSubstitution(object):
    """
    Provides encryption and decryption mechanics using the 
    "Mono-Alphabetic Substitution Cipher" algorihtm
    """

    def __init__(self):
        """
        Constructor
        """
        pass
        
    def encrypt(self, key, plaindata):
        """
        Encrypt data.
        Arguments:
        key: scrambled list of the alphabeth to be used as key
        plaindata: Instance of pymaancrypt.encoder.BaseEncoder

        >>> e.encrypt(list("ENKROYCVDQBFMZSAILHPGTXUJ"), encoder.EncoderEN("Encrypt me!"))
        'OZKLJAPMOO'

        """
        
        m = plaindata.getEncoded()

        kIndex = 0
        encrypted = []

        for c in m:
            encrypted.append(key[ord(c)-ord('A')])

        return ''.join(encrypted)
        
    def decrypt(self, key, ciperdata):
        """
        Decrypt data.
        """
        pass
    
    def generateRandomKeyEN(self, seed):
        """
        Generates a 
        """
        pass

    def generateRandomKeySV(self, seed):
        pass


def testmodule():
    import doctest
    return doctest.testmod(extraglobs={'e': MonoAlphaSubstitution()})

if __name__ == "__main__":
    if test()[0] == 0:
        print("Success!")
