# -*- coding: utf-8 -*-
"""
Created on 19 sep 2013

@author: Alexander
"""

try:
    import encoder
    import snippets
except ImportError:
    import pymaancrypt.encoder as encoder
    import pymaancrypt.snippets as snippets

class ColumnTranspositionCipher(object):
    """
    Provides encryption and decryption mechanics using the 
    "Transposition Cipher" algorihtm
    """

    def __init__(self):
        """
        Constructor
        """
        pass
        
    def encrypt(self, key, message):
        """
        Encrypt data.
        key: string
        plaindata: Instance of pymaancrypt.encoder.BaseEncoder

        >>> e.encrypt("HEMLIGT", encoder.EncoderSV("Vi rymmer i gryningen. Glöm inte stegen."))
        'IIGIGMNLSVRNMEMYGEYRNTNRGENEEIÖT'

        Each character in key is only used once, thus the following is True

        >>> e.encrypt("SECRETS", encoder.EncoderEN("ENCRYPT ME NOW")) == e.encrypt("SECRT", encoder.EncoderEN("ENCRYPT ME NOW"))
        True

        """

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


    def decrypt(self, key, ciphermessage):
        """
        Decrypt data.
        key: string
        ciphermessage: string

        >>> e.decrypt("HEMLIGT", "IIGIGMNLSVRNMEMYGEYRNTNRGENEEIÖT")
        'VIRYMMERIGRYNINGENGLÖMINTESTEGEN'

        Each character in key is only used once, thus the following is equivalent

        >>> e.decrypt("SECRETS", "ATBADFGRDAGFDSG") == e.decrypt("SECRT", "ATBADFGRDAGFDSG")
        True
        """

        key = snippets.uniquify(key)
        
        if len(key) > len(ciphermessage):
            raise AssertionError("Message longer than key!")
        
        sortedkey = sorted(key)
        table = {k:[] for k in key}

        decrypted = []
        index = 0

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
    Should return (#failed, #tried)
    """
    import doctest
    import sys
    thismodule = sys.modules[__name__]
    return doctest.testmod(m=thismodule, extraglobs={'e': ColumnTranspositionCipher()})

if __name__ == "__main__":
    if testmodule()[0] == 0:
        print("Success!")
