"""
Module for RSA encryption and decryption.

Example

>>> e = RSA()
>>> c = e.encrypt(bytearray('Hi', 'utf-8'), e.makeKeyObject(78563, public=57691))
>>> m = e.decrypt(bytearray(b'\\xab-\\x00'), e.makeKeyObject(78563, private=43411)).decode()
"""
import random
import math

from . import mathfuncs

class RSA(object):
    """
    A class for encryption of bytearray using the RSA encryption scheme, the constructor takes no parameters.

    >>> e = RSA()
    """

    def __init__(self):
        """
        Constructor
        """
        
    def encrypt(self, message, keyobj):
        """
        Encrypts a message represented as bytearray using RSA
        c = m ^ e (mod n)
        
        :param message: The message to encrypt in the form of a bytearray. Size of message must be less than `keyobj.getMaxBlockLength()` in bits.
        :param keyobj: The key in the form of the internal representation returned by :meth:`makeKeyObject`
        :returns: A bytearray of the same size as the binary represenation of N in the key.

        Example

        >>> e = RSA()
        >>> e.encrypt(bytearray('Hi', 'utf-8'), e.makeKeyObject(78563, public=57691))
        bytearray(b'\\xab-\\x00')
        """
        m = int.from_bytes(message, 'little')
        n = keyobj.getN()
        e = keyobj.getPublicKey()
        if m.bit_length() <= keyobj.getMaxBlockLength():
            c = pow(m, e, n)
            length = int(math.ceil(n.bit_length()/8))
            c = bytearray(c.to_bytes(length, 'little'))
            return c
        else:
            raise AssertionError("Encryption error: Message is to large, try again with larger key or smaller message!")
                
    def decrypt(self, message, keyobj):
        """
        Decrypts a RSA-message and returns it represented as an integer
        m = c ^ d (mod n)
        
        :param message: The message to decrypt in the form of a bytearray. Size of message must be same size as the binary represenation of N in the key.
        :param keyobj: The key in the form of the internal representation returned by :meth:`makeKeyObject`
        :returns: A bytearray of less than the size of `keyobj.getMaxBlockLength()` in bits.
        
        >>> e = RSA()
        >>> e.decrypt(bytearray(b'\\xab-\\x00'), e.makeKeyObject(78563, private=43411)).decode()
        'Hi'
        """
        c = int.from_bytes(message, 'little')
        n = keyobj.getN()
        d = keyobj.getPrivateKey()
        if c < n:
            m = pow(c, d, n)
            length = int(keyobj.getMaxBlockLength()/8)
            m = m.to_bytes(length, 'little')
            return m
        else:
            raise AssertionError("Decryption error: Message is to large, try again with larger key or smaller message!")
                    

    def generatePrivatePublicKey(self, bits):
        """
        Returns an object containing both public and private random keys. It uses the same internal format as the :meth:`makeKeyObject` method.

        :param bits: The maximum bitsize of any message to be enrypted with this string,
        :returns: An internal representation of the key.

        Number of bits (of N) that is generated is: bits+1 <= result <= bits+2

        The generated key is large enough so that the maximum block length 
        is guaranteed be at least 'bits' long (this means that N may actually
        be 1-2 bits larger than 'bits'

        1-2 is because there is a fifty percent probability of the most significant 
        bit beeing a 0, which is not counted when represented as a number.
        
        Examples

        >>> e = RSA()
        >>> key = e.generatePrivatePublicKey(512)
        >>> isinstance( key.getPublicKey(), int)
        True
        >>> isinstance( key.getPrivateKey(), int)
        True
        >>> key.getN().bit_length()
        513
        >>> key.getMaxBlockLength()
        512

        >>> e.generatePrivatePublicKey(16).getMaxBlockLength()
        16
        """

        bits += 1

        pbits = random.randrange(bits//2, 3*bits//4)
        qbits = bits - pbits

        p = mathfuncs.getRandomPrime(pbits)
        q = 0
        nbits = 0

        tries = 0
        while nbits != bits:
            if tries > 10:
                p = mathfuncs.getRandomPrime(pbits)
                tries = 0
            q = mathfuncs.getRandomPrime(qbits)
            tries += 1
            nbits = (p * q).bit_length()

        e, d = 0, 0
        
        fi_n = (p-1) * (q-1)
                
        while True:
            randomnumber = random.randrange(3, min(2**16 + 1, fi_n))
            g, x, y = mathfuncs.egcd(randomnumber, fi_n)
            if g == 1:
                e = randomnumber
                d = x % fi_n
                break

        return self.makeKeyObject(p * q, e, d)

    def makeKeyObject(self, n, public=None, private=None):
        """
        Returns an object containing both public and private keys.

        :param n: N in the RSA encryption scheme.
        :param public: The public part of the key (may be None).
        :param private: The private part of the key (may be None).
        :returns: A object containing the required information of an RSA key.

        Please note that one of public and private keys may be None, but not both.

        Examples:
        
        >>> e = RSA()
        >>> key = e.makeKeyObject(78563, public=57691, private=43411)
        >>> key.getMaxBlockLength()
        16
        >>> key.getPublicKey()
        57691
        >>> key.getPrivateKey()
        43411
        >>> key.getN()
        78563
        """

        class Key:
            """
            Key class used as encapsulation for key information
            """

            def __init__(self, n, e, d):
                """
                Constructor
                """
                if not isinstance(n, int) :
                    raise  TypeError("N must be integer")
                if not isinstance(e, int) and e is not None:
                    raise  TypeError("Public key must be integer or None")
                if not isinstance(d, int) and d is not None:
                    raise  TypeError("Private key must be integer or None")
                if None in (e, d) and e == d:
                    raise TypeError("Both public and private key may not be None")
                if e and e >= n:
                    raise ValueError("Public key may not be larger than N")
                if d and d >= n:
                    raise ValueError("Private key may not be larger than N")
                self.maxBlockLength = n.bit_length() - 1
                self.e = e
                self.d = d
                self.n = n

            def getPublicKey(self):
                """
                Returns the public part of the key a.k.a. 'e'
                """
                return self.e

            def getPrivateKey(self):
                """
                Returns the private part of the key as a dict
                with keys 'd' and 'n'
                """
                return self.d

            def getN(self):
                return self.n

            def getMaxBlockLength(self):
                return self.maxBlockLength

        return Key(n, public, private)



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
