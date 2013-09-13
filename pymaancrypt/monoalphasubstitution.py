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
        key: must implement pymaancrypt.encoder.BaseEncoder interface
        """
        k = key.getEncoded()
        m = plaindata.getEncoded()
        return "TEST"
        
    def decrypt(self, key, ciperdata):
        """
        Decrypt data.
        """
        pass

if __name__ == "__main__":
    m = MonoAlphaSubstitution()
    encrypted = m.encrypt(encoder.EncoderEN("This is a key"), encoder.EncoderEN(u"Encrypt me!"))
    print(encrypted)