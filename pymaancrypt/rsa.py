"""
Created on 26 sep 2013

@author: Marcus
"""

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
        
    def decrypt(self, n, d, c):
        """
        """
        # m = c^d (mod n)
        
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