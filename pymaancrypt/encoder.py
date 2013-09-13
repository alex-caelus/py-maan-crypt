'''
Created on 12 sep 2013

@author: Marcus
'''

class BaseEncoder:
    """
    Text encoder base class
    """
    unencoded = ''
    encoded = ''

    def __init__(self, text):
        """
        Constructor
        """
        self.unencoded = text
        self.encoded = self._encode(text)
        
    def _encode(self, text):
        raise NotImplementedError("Is abstract")
        
    def getUnencoded(self):
        return self.unencoded
        
    def getEncoded(self):
        return self.encoded

    def getModulo(self):
        raise NotImplementedError("Is abstract")

            
class EncoderEN(BaseEncoder):
    """
    Encodes english text
    """
    
    def __init__(self, text):
        """
        Constructor
        """
        #calls super constructor
        super().__init__(text)
        
    def _encode(self, text):
        """
        """
        tmp = ""
        for char in text:
            if char.isalpha():
                tmp += char
        return tmp.upper()

    def getModulo(self):
        return 26
        
        
class EncoderSV(BaseEncoder):
    """
    Encodes swedish text
    """

    def __init__(self, text):
        """
        Constructor
        """
        #calls super constructor
        super().__init__(text)
        
    def _encode(self, text):
        """
        """
        tmp = ""
        for char in text:
            if char.isalpha():
                tmp += char
        return tmp.upper()
        
    def getModulo(self):
        return 29



def testmodule():
    import doctest
    return doctest.testmod()