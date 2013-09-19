# -*- coding: utf-8 -*-
"""
Created on 12 sep 2013

@author: Alexander
"""

import random

try:
    import encoder
except ImportError:
    import pymaancrypt.encoder

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
        
    def encrypt(self, keyobj, plaindata):
        """
        Encrypt data.
        Arguments:
        key: scrambled list of the alphabeth to be used as key
        plaindata: Instance of pymaancrypt.encoder.BaseEncoder

        >>> e.encrypt(e.makeKey(encoder.EncoderEN("ENKROYCVDQWBFMZSAILHPGTXUJ")), encoder.EncoderEN("Encrypt me!"))
        'OMKIUSHFO'
        
        >>> e.encrypt(e.makeKey(encoder.EncoderSV("ENKROYCVDQBFMZSÖAIÅLWHPGÄTXUJ")), encoder.EncoderSV(u"Kryptera mig, åäö!"))
        'BIÄÖLOIEMDCXUJ'

        """
        
        m = plaindata.getEncoded()

        encrypted = []

        key = keyobj['key'] if 'key' in keyobj else keyobj

        for p in m:
            if p not in key.keys():
                raise LookupError("char %c does not exist in key" % (p,))
            encrypted.append(key[p])

        return ''.join(encrypted)
        
    def decrypt(self, keyobj, cipherdata):
        """
        Decrypt data.
        
        Here follows some usage examples:

        >>> key = e.makeKey(encoder.EncoderEN("ENKROYCVDQWBFMZSAILHPGTXUJ"))
        >>> e.decrypt(key, 'OMKIUSHFO')
        'ENCRYPTME'

        >>> key = e.makeKey(encoder.EncoderSV("ENKROYCVDQBFMZSÖAIÅLWHPGÄTXUJ"))
        >>> e.decrypt(key, 'BIÄÖLOIEMDCXUJ')
        'KRYPTERAMIGÅÄÖ'
        """
        
        return self.encrypt(keyobj['inverted'], keyobj['encoder'](cipherdata))

    def makeKey(self, input):
        """
        takes a encoder.BaseEncoder derived object and converts it to a dictionary with original alphabet as index

        Example:
        >>> key = e.makeKey(encoder.EncoderSV("ENKROYCVDQBFMZSÖAIÅLWHPGÄTXUJ"))
        >>> key['key'] == {'A': 'E', 'B': 'N', 'C': 'K', 'D': 'R', 'E': 'O', 'F': 'Y', 'G': 'C', 'H': 'V', 'I': 'D', 'J': 'Q', 'K': 'B', 'L': 'F', 'M': 'M', 'N': 'Z', 'O': 'S', 'P': 'Ö', 'Q': 'A', 'R': 'I', 'S': 'Å', 'T': 'L', 'U': 'W', 'V': 'H', 'W': 'P', 'X': 'G', 'Y': 'Ä', 'Z': 'T', 'Ä': 'U', 'Å': 'X', 'Ö': 'J'}
        True
        """
        alphabet = list(input.getAlphabet())
        alphabetLen = len(alphabet)
        i = 0
        keyobj = {'key': {}}
        
        for k in input.getEncoded():
            keyobj['key'][alphabet[i]] = k
            i += 1
        
        keyobj["inverted"] = {v:k for k, v in keyobj['key'].items()}
        keyobj["encoder"] = input.__class__

        kLen = len(keyobj['key'])
        iLen = len(keyobj["inverted"] )

        if kLen != alphabetLen or iLen != alphabetLen:
            raise AssertionError("Input is not a valid key")

        return keyobj
            
    def generateRandomKey(self, encClass):
        """
        Generates a random key form the alphabet of the specified encoder

        >>> len(e.generateRandomKey(encoder.EncoderSV)['key'])
        29
        """
        s = encClass.getAlphabet(None)
        return self.makeKey(encClass(''.join(random.sample(s, len(s)))))


def testmodule():
    """
    Should return (#failed, #tried)
    """
    import doctest
    import sys
    thismodule = sys.modules[__name__]
    return doctest.testmod(m=thismodule, extraglobs={'e': MonoAlphaSubstitution()})

if __name__ == "__main__":
    if testmodule()[0] == 0:
        print("Success!")
