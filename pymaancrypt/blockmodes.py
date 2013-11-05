# -*- coding: utf-8 -*-
"""
A module containing classes for cipher block chaining modes.

The `BaseBlockMode` is a supposed to define a common interface for all blockmodes.

Currently only the Electronic Code Book mode is implemented.

Construction of a block mode takes an encryptor object and a blocklength (in bits) as parameters.

Encryption and decryption is then done as in the following example:

>>> keyobj = None #Should be a real key based on whatever encryption scheme you use.
>>> message = "Hello, I'm a long text that must be divided into several blocks"
>>> blockmode = ECB(__DummyEncryptor__(), 32)
>>> encrypted = blockmode.encryptFromString(message, keyobj)
>>> decrypted = blockmode.decryptToString(encrypted, keyobj)
>>> decrypted == message
True

You may also use the `blockmode.encryptByteArray` and `blockmode.decryptByteArray` instead of the FromString and ToString variants used above.

"""

import math
from . import mathfuncs


class __DummyEncryptor__:
    """
    This dummy encryptor is only used for testing purposes and does not actually perform any encryption.
    """

    def encrypt(self, data, keyobj):
        return data

    def decrypt(self, data, keyobj):
        return data

class BaseBlockMode(object):
    """
    :param encryptor: The encryptor object (see below) that handles the actual encryption of a block.
    :param maxBlockLength: The block length (integer) in bits.

    Base class for all block modes, this should not be used except as a base class for those who wish to
    define their own blockmode.
    
    Any class who inherits from this class should only need to override the `encryptByteArray` and `decryptByteArray`.

    The constructor takes an encryptor object (with encrypt and decrypt methods) and block length (integer) in bits.

    The encryptor must implement the following interface:
    ::

        class ExampleEncryptor(object):
            def encrypt(self, dataAsBytearray, keyobj):
                #returns a bytearray
                pass

            def decrypt(self, dataAsByteArray, keyobj):
                #returns a bytearray
                pass

    """

    def __init__(self, encryptor, maxBlockLength):
        """
        Constructor, documentation above.
        """
        self.encryptor = encryptor
        self.blockLengthBits = mathfuncs.floorPowerOf( maxBlockLength, 2 )
        self.blockLengthBytes = int(self.blockLengthBits / 8)

        if self.blockLengthBits < 8:
            raise AssertionError("Max Block Length must be larger than 8 bits (one byte)")

    def encryptFromString(self, data, keyobj):
        """
        Convenience method for encrypting a string (utf-8 encoded) of data.

        :param data: string to encrypt.
        :param keyobj: The key that is passed on to the encryption scheme.
        :returns: A bytearray
        """
        return self.encryptByteArray(bytearray(data, 'utf-8'), keyobj)

    def decryptToString(self, data, keyobj):
        """
        Convenience method for decrypting data to a string (utf-8 encoded).

        :param data: bytearray of data to decrypt.
        :param keyobj: The key that is passed on to the decryption scheme.
        :returns: A utf-8 encoded string.
        """
        return self.decryptByteArray(data, keyobj).decode().split('\x00')[0]

    def encryptByteArray(self, data, keyobj):
        """
        Encrypts a variable length array of bytes

        :param data: Bytearray of data to encrypt
        :param keyobj: Object to pass on to the encrypt method of the `encryptor`
        :returns: A bytearray
        """
        raise NotImplementedError("Is abstract")

    def decryptByteArray(self, data, keyobj):
        """
        Decrypts an array of bytes

        :param data: Bytearray of data to decrypt
        :param keyobj: Object to pass on to the decrypt method of the `encryptor`
        :returns: A bytearray
        """
        raise NotImplementedError("Is abstract")



class ECB(BaseBlockMode):
    """
    Electronic code book block encryption scheme, this is the least secure of all 
    block modes and should only be used for educational purposes

    See :class:`BaseBlockMode` for further documentaton on constructor arguments and usage.

    :param encryptor: The encryptor object that handles the actual encryption of a block.
    :param maxBlockLength: The block length (integer) in bits.
    """

    def __init__(self, encryptor, maxBlockLength):
        """
        Constructor, documentation above.
        """
        super().__init__(encryptor, maxBlockLength)

    def encryptByteArray(self, data, keyobj):
        """
        Encrypts a variable length bytearray with the provided encryptor with the ECB
        block scheme.

        :param data: Bytearray of data to encrypt
        :param keyobj: Object to pass on to the encrypt method of the `encryptor`
        :returns: A bytearray

        This implementation uses zeroes for padding.

        >>> if True:
        ...     e = __DummyEncryptor__()
        ...     ecb = ECB(e, 32)
        ...     c = ecb.encryptFromString('This is a test', None)
        ...     c.decode()
        'This is a test\\x00\\x00'
        """

        nrOfBlocks = int(math.ceil(len(data)/self.blockLengthBytes))
        C = bytearray()

        for i in range(nrOfBlocks):
            m = bytearray(self.blockLengthBytes)
            for j in range(self.blockLengthBytes):
                index = i*self.blockLengthBytes+j
                if index < len(data):
                    m[j] = data[index]
            c = self.encryptor.encrypt(m, keyobj)
            if len(c) != self.blockLengthBytes:
                raise AssertionError("Encryptor is not symmetric! "+
                        "Block Cipher modes require encryptors "+
                        "with equal length of input & output blocks.")
            for cb in c:
                C.append(cb)

        return C
            
    
    def decryptByteArray(self, data, keyobj):
        """
        Decrypts a variable length bytearray with the provided encryptor with the ECB
        block scheme.
        
        :param data: Bytearray of data to decrypt
        :param keyobj: Object to pass on to the decrypt method of the `encryptor`
        :returns: A bytearray

        Padding will not be removed since there is no way to detrimine if trailing zeroes are part of plaintext or not.

        >>> if True:
        ...     e = __DummyEncryptor__()
        ...     ecb = ECB(e, 32)
        ...     ecb.decryptToString(bytearray('This is a test\\x00\\x00', 'utf-8'), None)
        'This is a test'
        """

        nrOfBlocks = int(math.ceil(len(data)/self.blockLengthBytes))
        M = bytearray()

        for i in range(nrOfBlocks):
            c = bytearray(self.blockLengthBytes)
            for j in range(self.blockLengthBytes):
                index = i*self.blockLengthBytes+j
                if index < len(data):
                    c[j] = data[index]
            m = self.encryptor.decrypt(c, keyobj)
            for mb in m:
                M.append(mb)

        return M


    
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
