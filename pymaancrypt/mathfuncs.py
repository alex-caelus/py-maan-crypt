# -*- coding: utf-8 -*-
"""
Created on 27 sep 2013

@author: Alexander
"""
import random
import math
import decimal
import fractions

def millerRabinPrimalityTest(n, certainty=decimal.Decimal('0.995')):
    """
    tests if 'number' is a prime

    >>> [x for x in range(901, 1000) if millerRabinPrimalityTest(x)]
    [907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]

    >>> millerRabinPrimalityTest(6438080068035544392301298549614926991513861075340134\
3291807343952413826484237063006136971539473913409092293733259038472039\
7133335969549256322620979036686633213903952966175107096769180017646161\
851573147596390153)
    True
    
    >>> millerRabinPrimalityTest(7438080068035544392301298549614926991513861075340134\
3291807343952413826484237063006136971539473913409092293733259038472039\
7133335969549256322620979036686633213903952966175107096769180017646161\
851573147596390153)
    False
    """
    assert n >= 2
    assert certainty < 1 and certainty > 0

    if n == 2:
        return True

    if n % 2 == 0:
        return False

    nrOfTests = min(math.ceil(math.log(1/(1-certainty), 4)), n-3)

    k = 0
    m = n-1
    while m % 2 == 0:
        k += 1
        m = m // 2

    assert 2**k * m == n-1

    #define inner loop
    def tryComposite(b):
        if pow(b, m, n) in (1, n-1):
            return False

        for i in range(k): #1, 2, ..., k-1
            bi = pow(b, m * 2**i, n)
            if bi == n-1:
                return False
            elif bi == 1:
                return True
        return True
    
    tested = []
    for t in range(0, nrOfTests):
        b = random.randrange(2, n-1)
        while b in tested:
            b = random.randrange(2, n-1)
        tested.append(b)

        if tryComposite(b):
            return False

    return True


        
def getRandomPrime(bits):
    """
    Returns a prime number that is represented with a specified number of bits

    >>> p = getRandomPrime(5)
    >>> p >= 16 and p < 32
    True
    """
    while True:
        randomnumber = random.randrange(2 ** (bits-1), 2**(bits))

        if millerRabinPrimalityTest(randomnumber):
            return randomnumber

def gcd(a, b):
    """
    Caclulates the gcd of two numbers.
    """
    return egcd(a, b)[0]

def egcd(a, b):
    """
    Extended euclidiean algorithm
    take positive integers a, b as input, and return a triple (g, x, y), such that ax + by = g = gcd(a, b).

    source code taken from:
    http://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
    """
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q,r = b//a,b%a; m,n = x-u*q,y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    return b, x, y

def floorPowerOf(a, p):
    """
    This function floors a to the closest number that is a power of p

    Examples:

    >>> floorPowerOf(6, 2)
    4
    >>> floorPowerOf(8, 2)
    8
    >>> floorPowerOf(9, 2)
    8
    >>> floorPowerOf(31.99, 2)
    16
    """
    return p ** math.floor(math.log(a, p))


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
