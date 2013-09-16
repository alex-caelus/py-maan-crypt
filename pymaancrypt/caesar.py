'''
Created on 12 sep 2013

@author: Marcus
'''

class Caesar(object):
    '''
    classdocs
    '''


    def __init__(self):
        """
        Constructor
        """
        
    def encrypt(self, key, plaindata):
        """
        Encrypt data using Caesar cipher
        """
        
        
    def decrypt(self, key, ciperdata):
        """
        Decrypt data encrypted using Caesar cipher
        """
        


def testmodule():
    """
    Should return (#failed, #tried)
    """
    import doctest
    import sys
    thismodule = sys.modules[__name__]
    return doctest.testmod(m=thismodule, extraglobs={'e': Caesar()})

if __name__ == "__main__":
    if testmodule()[0] == 0:
        print("Success!")
