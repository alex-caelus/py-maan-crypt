"""
Created on 26 sep 2013

@author: Marcus
"""
import random

try:
    import mathfuncs
    import math
except ImportError:
    import pymaancrypt.mathfuncs as mathfuncs
    import math

class RSA(object):
    """
    classdocs
    """


    def __init__(self):
        """
        Constructor
        """
        
    def encrypt(self, message, keyobj):
        """
        Encrypts a message represented as bytearray using RSA
        c = m ^ e (mod n)
        
        >>> e.encrypt(bytearray('Hi', 'utf-8'), e.makeKeyObject(78563, public=57691))
        bytearray(b'\\x00\\x955')
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
        
        >>> e.decrypt(bytearray(b'\\x00\\x955'), e.makeKeyObject(78563, private=43411)).decode()
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
        Returns an object containing both public and private random keys.

        Number of bits generated N is returned is: bits+1 <= result <= bits+2

        The generated key is large enough so that the maximum block length 
        is guaranteed be at least 'bits' long (this means that N may actually
        be 1-2 bits larger than 'bits'

        1-2 is because there is a fifty percent probability of the most significant 
        bit beeing a 0, which is not counted when represented as a number.

        >>> key = RSA().generatePrivatePublicKey(512)
        >>> isinstance( key.getPublicKey(), int)
        True
        >>> isinstance( key.getPrivateKey(), int)
        True
        >>> key.getN().bit_length()
        513
        >>> key.getMaxBlockLength()
        512

        >>> RSA().generatePrivatePublicKey(16).getMaxBlockLength()
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
        Returns an object containing both public and private random keys.

        Please note that one of public and private keys may be None, but not both.

        >>> key = e.makeKeyObject(78563, public=57691, private=43411)
        >>> key.getMaxBlockLength()
        16

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
    Should return (#failed, #tried)
    """
    import doctest
    import sys
    thismodule = sys.modules[__name__]
    return doctest.testmod(m=thismodule, extraglobs={'e': RSA()})

if __name__ == "__main__":
    if testmodule()[0] == 0:
        print("Success!")