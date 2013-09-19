# -*- coding: utf-8 -*-
"""
Created on 19 sep 2013

@author: Alexander
"""

def uniquify(seq):
    """
    Takes a list and outputs a copy with duplicates removed
    """
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]
    