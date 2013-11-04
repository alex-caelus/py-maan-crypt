# -*- coding: utf-8 -*-

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
    Base class for all block modes
    """

    def __init__(self, encryptor, maxBlockLength):
        """
        Constructor
        """
        self.encryptor = encryptor
        self.blockLengthBits = mathfuncs.floorPowerOf( maxBlockLength, 2 )
        self.blockLengthBytes = int(self.blockLengthBits / 8)

        if self.blockLengthBits < 8:
            raise AssertionError("Max Block Length must be larger than 8 bits (one byte)")

    def encryptFromString(self, data, keyobj):
        """
        Convenience method for encrypting a string of data, return type is bytearray
        """
        return self.encryptByteArray(bytearray(data, 'utf-8'), keyobj)

    def decryptToString(self, data, keyobj):
        """
        Convenience method for decrypting a bytearray, return type is utf-8 encoded string
        """
        return self.decryptByteArray(data, keyobj).decode().split('\x00')[0]

    def encryptByteArray(self, data, keyobj):
        """
        Encryption method
        """
        raise NotImplementedError("Is abstract")

    def decryptByteArray(self, data, keyobj):
        """
        Decryption method
        """
        raise NotImplementedError("Is abstract")



class ECB(BaseBlockMode):
    """
    Electronic code book block encryption scheme, this is the least secure of all 
    block modes and should only be used for educational purposes
    """

    def __init__(self, encryptor, maxBlockLength):
        """
        Constructor
        """
        super().__init__(encryptor, maxBlockLength)

    def encryptByteArray(self, data, keyobj):
        """
        Encrypts a variable length bytearray with the provided encryptor with the ECB
        block scheme.

        padding will be all zeroes due to the fact that encryption expects 
        a c-style string as payload

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
            for mb in c:
                M.append(mb)

        return M


    
def testmodule():
    """
    Should return (#failed, #tried)
    """
    import doctest
    import sys
    thismodule = sys.modules[__name__]
    return doctest.testmod(m=thismodule)

if __name__ == "__main__":
    if testmodule()[0] == 0:
        print("Success!")
