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

    def __init__(self):
        """
        Constructor
        """
        raise NotImplementedError

            
class EncoderEN(BaseEncoder):
    """
    Encodes english text
    """
    
    def __init__(self, text):
        """
        Constructor
        """
        
        self.unencoded = text
        self.encoded = self.encode(text)
        
    def encode(self, text):
        """
        """
        tmp = ""
        for char in text:
            if char.isalpha():
                tmp += char
        return tmp.upper()
        
    def getUnencoded(self):
        return self.unencoded
        
    def getEncoded(self):
        return self.encoded
        
        
class EncoderSV(BaseEncoder):
    """
    Encodes swedish text
    """

    def __init__(self, text):
        """
        Constructor
        """
        
        self.unencoded = text
        self.encoded = self.encode(text)
        
    def encode(self, text):
        """
        """
        tmp = ""
        for char in text:
            if char.isalpha():
                tmp += char
        return tmp.upper()
        
    def getUnencoded(self):
        return self.unencoded
        
    def getEncoded(self):
        return self.encoded
        