# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 14:19:11 2013

@author: tdoughty1
"""

###############################################################################
# Data Type Global Variables
###############################################################################

_CurrentDetnum = None
_CurrentCut = None

#TEMP implement automatic generation of _Detnums
_Detnums = range(1101, 1116)

_DataDict = None
_CutDict = None

# Global Methods defined
def SetDetnum(detnum):

    global _CurrentDetnum
    
    # Detnum must be in expected range
    if(detnum in _Detnums):
        _CurrentDetnum = detnum


def GetDetnum():
    return _CurrentDetnum


def SetCut(cut):
    
    global _CurrentCut

    # Implement Cut Type Checking here
    _CurrentCut = cut


def GetCut():
    return _CurrentCut
