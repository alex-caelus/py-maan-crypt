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
        
    def encrypt(self, n, e, m):
        """
        """
        # c = m^e (mod n)
        bytes = str.encode(m, encoding='utf_8', errors='strict')
        encoded = int.from_bytes(bytes, byteorder='little', signed=False)
        if encoded >= n:
            raise Exception
        else:
            return (encoded**e) % n
                
    def decrypt(self, n, d, c):
        """
        """
        # m = c^d (mod n)
        
    def splitList(self, byteArray, length):
        """
        
        """
        listOfLists = []
        while not byteArray:
            first = byteArray[length:]
            rest = byteArray[:len(byteArray)-length]
            
            if len(first) < length:
                for i in range((len(first)-length)):
                    first.insert(i, 0)
            
            listOfLists.append(first)
            byteArray = rest
        return listOfLists
                    

    def generatePrivatePublicKey(self, bits):
        """
        Returns an object containing both public and private random keys.

        Number of bits generated N is returned is: bits-1 <= result <= bits

        >>> key = RSA().generatePrivatePublicKey(1024)
        >>> isinstance( key.getPublicKey(), int)
        True
        >>> isinstance( key.getPrivateKey(), int)
        True
        >>> len(bin(key.getN())) in [1023, 1024]
        True
        """

        class Key:
            """
            Key class used as encapsulation for key information
            """

            def __init__(self, e, d, n):
                """
                Constructor
                """
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

        bits -= 1

        pbits = random.randrange(bits//4, 3*bits//4)
        qbits = bits - pbits - 1

        p = mathfuncs.getRandomPrime(pbits)
        q = mathfuncs.getRandomPrime(qbits)

        e, d = 0, 0
        
        fi_n = (p-1) * (q-1)
                
        while True:
            randomnumber = random.randrange(3, min(2**16 + 1, fi_n))
            g, x, y = mathfuncs.egcd(randomnumber, fi_n)
            if g == 1:
                e = randomnumber
                d = x % fi_n
                break

        return Key(e, d, p * q)



        
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