# -*- coding: utf-8 -*-
"""
Module for mono-alphabetic substitution encryption and decryption

Example

>>> e = MonoAlphaSubstitution(encoder.EncoderSV)
>>> c = e.encrypt(e.makeKey("ENKROYCVDQBFMZSÖAIÅLWHPGÄTXUJ"), "Kryptera mig, åäö!")
>>> m = e.decrypt(e.makeKey("ENKROYCVDQBFMZSÖAIÅLWHPGÄTXUJ"), "BIÄÖLOIEMDCXUJ")
"""

import random

from . import encoder

class MonoAlphaSubstitution(object):
    """
    Provides encryption and decryption mechanics using the 
    "Mono-Alphabetic Substitution Cipher" algorihtm

    :param encoderClass: Specifies which encoder to use when encoding before encryption. It also specifies the alphabet that is to be used when encrypting and decrypting.

    >>> e = MonoAlphaSubstitution(encoder.EncoderSV)

    """

    def __init__(self, encoderClass):
        """
        Constructor
        """
        self.encoderClass = encoderClass
        
    def encrypt(self, keyobj, plaindata):
        """
        Encrypts a string.

        :param keyobj: Special object as returned by :meth:`makeKey` method
        :param plaindata: string to encrypt
        :returns: string
         
        Examples: 

        >>> e = MonoAlphaSubstitution(encoder.EncoderSV)
        >>> e.encrypt(e.makeKey("ENKROYCVDQBFMZSÖAIÅLWHPGÄTXUJ"), "Kryptera mig, åäö!")
        'BIÄÖLOIEMDCXUJ'

        """
        
        m = self.encoderClass(plaindata).getEncoded()

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
        
        :param keyobj: Special object as returned by :meth:`makeKey` method
        :param cipherdata: string to decrypt
        :returns: string

        Examples:
        
        >>> e = MonoAlphaSubstitution(encoder.EncoderSV)
        >>> key = e.makeKey("ENKROYCVDQBFMZSÖAIÅLWHPGÄTXUJ")
        >>> e.decrypt(key, 'BIÄÖLOIEMDCXUJ')
        'KRYPTERAMIGÅÄÖ'
        """
        
        return self.encrypt(keyobj['inverted'], cipherdata)

    def makeKey(self, key):
        """
        Takes a alphabet as a string and converts it to a dictionary with the standard alphabet as index.

        :param key: String containing the entire alphabet in a random order.
        :returns: Internal representation of a key, as used by the :meth:`encrypt` and :meth:`decrypt` methods.

        Example:
        
        >>> e = MonoAlphaSubstitution(encoder.EncoderSV)
        >>> key = e.makeKey("ENKROYCVDQBFMZSÖAIÅLWHPGÄTXUJ")
        >>> key['key'] == {'A': 'E', 'B': 'N', 'C': 'K', 'D': 'R', 'E': 'O', 'F': 'Y', 'G': 'C', 'H': 'V', 'I': 'D', 'J': 'Q', 'K': 'B', 'L': 'F', 'M': 'M', 'N': 'Z', 'O': 'S', 'P': 'Ö', 'Q': 'A', 'R': 'I', 'S': 'Å', 'T': 'L', 'U': 'W', 'V': 'H', 'W': 'P', 'X': 'G', 'Y': 'Ä', 'Z': 'T', 'Ä': 'U', 'Å': 'X', 'Ö': 'J'}
        True
        """
        key = self.encoderClass(key)
        inputString = key.getEncoded()
        alphabet = list(key.getAlphabet())
        alphabetLen = len(alphabet)
        i = 0
        keyobj = {'key': {}}
        
        for k in inputString:
            keyobj['key'][alphabet[i]] = k
            i += 1
        
        keyobj["inverted"] = {v:k for k, v in keyobj['key'].items()}

        kLen = len(keyobj['key'])
        iLen = len(keyobj["inverted"] )

        if kLen != alphabetLen or iLen != alphabetLen:
            raise AssertionError("Input is not a valid key")

        return keyobj
            
    def generateRandomKey(self):
        """
        Generates a random key from the alphabet of the specified encoder (in constructor)

        :returns: Internal representation of a key, as used by the :meth:`encrypt` and :meth:`decrypt` methods.

        Example:
        
        >>> e = MonoAlphaSubstitution(encoder.EncoderSV)
        >>> len(e.generateRandomKey()['key'])
        29
        """
        s = self.encoderClass.getAlphabet(None)
        return self.makeKey(''.join(random.sample(s, len(s))))


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
