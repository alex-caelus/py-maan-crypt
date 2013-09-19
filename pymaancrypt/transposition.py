# -*- coding: utf-8 -*-
"""
Created on 19 sep 2013

@author: Alexander
"""

try:
    import encoder
except ImportError:
    import pymaancrypt.encoder

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

        >>> e.encrypt("HEMLIGT", encoder.EncoderSV("Vi rymmer i gryningen. glöm inte stegen."))
        'IIGIGMNLSVRNMEMYGEYRNTNRGENEEIÖT'

        """
        key = list(key)
        table = {k:[] for k in key}

        for idx, val in enumerate(message.getEncoded()):
            k = key[idx % len(key)]
            table[k].append(val)
        
        encrypted = ""
        
        for k in sorted(key):
            encrypted += ''.join(table[k])

        return encrypted


    def decrypt(self, key, ciphermessage):
        """
        Decrypt data.
        key: string
        ciphermessage: string

        >>> e.decrypt("HEMLIGT", "IIGIGMNLSVRNMEMYGEYRNTNRGENEEIÖT")
        'VIRYMMERIGRYNINGENGLÖMINTESTEGEN'
        """
        key = list(key)
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
