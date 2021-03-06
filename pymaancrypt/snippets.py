# -*- coding: utf-8 -*-
"""
Module containing arbitrary help functions
"""

def uniquify(seq):
    """
    Takes a list and outputs a copy with duplicates removed

    >>> uniquify("HELLO")
    ['H', 'E', 'L', 'O']

    >>> uniquify((1, 3, 5, 2, 6, 3, 4, 2, 1, 4, 5, 3, 6))
    [1, 3, 5, 2, 6, 4]
    """
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]
    

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
