# -*- coding: utf-8 -*-
'''
Module for text encoding
'''

class BaseEncoder:
    """
    Text encoder base class

    :param text: The string to be encoded (encapsulated)
    """
    unencoded = ''
    encoded = ''
    integerEncoded = '91'

    def __init__(self, text):
        """
        Constructor
        """
        self.unencoded = text
        self.encoded = self._encode(text)
        self.integerEncoded = self._integerEncode(self.encoded)
        
    def _encode(self, text):
        """
        Private, must be implemented by sub class.
        This method handles the actual encoding
        """
        raise NotImplementedError("Is abstract")
    
    def _integerEncode(self, text):
        """
        Private, must be implemented by sub class.
        This method creates an integer representation of an encoded text
        """
        raise NotImplementedError("Is abstract")
        
    def getUnencoded(self):
        """
        Returns the raw input string
        """
        return self.unencoded
        
    def getEncoded(self):
        """
        Returns the encoded value
        """
        return self.encoded

    def getAlphabet(self):
        """
        Gets the alphabet of the encoders language
        raise NotImplementedError("Is abstract")
        """
        
    def getIntegerEncoded(self):
        """
        raise NotImplementedError("Is abstract")
        """
        return self.integerEncoded
            
class EncoderEN(BaseEncoder):
    """
    Encodes english text.
    
    >>> EncoderEN("This is a (1) english text!").getEncoded()
    'THISISAENGLISHTEXT'

    >>> EncoderEN("This is a (1) english text!").getUnencoded()
    'This is a (1) english text!'
    """
    
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    def __init__(self, text):
        """
        Constructor
        """
        # calls super constructor
        super().__init__(text)
        
    def _encode(self, text):
        """
        Implemented!
        """
        tmp = ""
        for char in text:
            if char.isalpha():
                tmp += char
        return tmp.upper()
    
    def _integerEncode(self, text):
        """
        """
        if text == "":
            return -1
        tmp = ""
        for char in text:
            i = self.alphabet.find(char) + 1
            if i > 0 or i < len(self.alphabet):
                if i < 10:
                    tmp += "0" + str(i)
                else:
                    tmp += str(i)
            else:
                raise Exception
        return int(tmp)

    def getAlphabet(self):
        """
        Gets the alphabet of the encoders language

        >>> EncoderEN('').getAlphabet()
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        """
        return "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    
        
class EncoderSV(BaseEncoder):
    """
    Encodes swedish text
    
    >>> EncoderSV(u"Detta är en (1) svensk text1").getEncoded()
    'DETTAÄRENSVENSKTEXT'

    >>> EncoderSV(u"Detta är en (1) svensk text1").getUnencoded()
    'Detta är en (1) svensk text1'

    """

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"

    def __init__(self, text):
        """
        Constructor
        """
        # calls super constructor
        super().__init__(text)
        
    def _encode(self, text):
        """
        """
        tmp = ""
        for char in text:
            if char.isalpha():
                tmp += char
        return tmp.upper()
    
    def _integerEncode(self, text):
        """
        """
        
        if text == "":
            return -1
        
        tmp = ""
        for char in text:
            i = self.alphabet.find(char) + 1
            if i > 0 or i < len(self.alphabet):
                if i < 10:
                    tmp += "0" + str(i)
                else:
                    tmp += str(i)
            else:
                raise Exception
        return int(tmp)
    
    def getAlphabet(self):
        """
        >>> EncoderSV('').getAlphabet()
        'ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ'
        """
        return "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"
            

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
