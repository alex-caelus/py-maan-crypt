# -*- coding: utf-8 -*-
"""
Module for column transposition cipher encryption and decryption

Example

>>> e = ColumnTranspositionCipher(encoder.EncoderSV)
>>> c = e.encrypt("HEMLIGT", "Vi rymmer i gryningen. Glöm inte stegen.")
>>> m = e.decrypt("HEMLIGT", "IIGIGMNLSVRNMEMYGEYRNTNRGENEEIÖT")
"""

from . import encoder
from . import snippets

class ColumnTranspositionCipher(object):
    """
    Provides encryption and decryption mechanics using the 
    "Transposition Cipher" algorihtm

    :param encoderClass: Specifies which encoder to use when encoding before encryption. It also specifies the alphabet that is to be used when encrypting and decrypting.

    >>> e = ColumnTranspositionCipher(encoder.EncoderSV)
    """

    def __init__(self, encoderClass):
        """
        Constructor
        """
        self.encoderClass = encoderClass
        
    def encrypt(self, key, plaintext):
        """
        Encrypt data.
        
        :param key: string
        :param plaintext: string

        Example
        
        >>> e = ColumnTranspositionCipher(encoder.EncoderSV)
        >>> e.encrypt("HEMLIGT", "Vi rymmer i gryningen. Glöm inte stegen.")
        'IIGIGMNLSVRNMEMYGEYRNTNRGENEEIÖT'

        Each character in key is only used once, thus the following is True
        
        >>> e = ColumnTranspositionCipher(encoder.EncoderEN)
        >>> e.encrypt("SECRETS", "ENCRYPT ME NOW") == e.encrypt("SECRT", "ENCRYPT ME NOW")
        True

        """

        message = self.encoderClass(plaintext)

        key = snippets.uniquify(key)
        
        if len(key) > len(message.getEncoded()):
            raise AssertionError("Message longer than key!")
        
        sortedkey = sorted(key)

        table = {k:[] for k in key}

        for idx, val in enumerate(message.getEncoded()):
            k = key[idx % len(key)]
            table[k].append(val)
        
        encrypted = ""
        
        for k in sortedkey:
            encrypted += ''.join(table[k])

        return encrypted


    def decrypt(self, key, encrypteddata):
        """
        Decrypt data.
        key: string
        ciphermessage: string
        
        >>> e = ColumnTranspositionCipher(encoder.EncoderSV)
        >>> e.decrypt("HEMLIGT", "IIGIGMNLSVRNMEMYGEYRNTNRGENEEIÖT")
        'VIRYMMERIGRYNINGENGLÖMINTESTEGEN'

        Each character in key is only used once, thus the following is equivalent
        
        >>> e = ColumnTranspositionCipher(encoder.EncoderEN)
        >>> e.decrypt("SECRETS", "ATBADFGRDAGFDSG") == e.decrypt("SECRT", "ATBADFGRDAGFDSG")
        True
        """
        ciphermessage = encrypteddata

        key = snippets.uniquify(key)
        
        if len(key) > len(ciphermessage):
            raise AssertionError("Message longer than key!")
        
        sortedkey = sorted(key)
        table = {k:[] for k in key}

        decrypted = []

        itemspercolumn = len(ciphermessage)//len(key)
        start = 0
        for k in sortedkey:
            overflow = 1 if key.index(k) <  (len(ciphermessage) % len(key)) else 0
            stop = start + itemspercolumn + overflow
            for i in range(start, stop):
                table[k].append(ciphermessage[i])
            start = stop

        for i in range(0, len(ciphermessage)):
            decrypted.append(table[key[i%len(key)]][i//len(key)])

        return ''.join(decrypted)



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
