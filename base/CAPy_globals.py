# -*- coding: utf-8 -*-
"""
globals. py

Module to keep track CAPy session settings.

Attributes:
    _FileInfo (FileInfo) - Structure containing list of root files and branches
        with detector numbers mapped to the corresponding file, directory, and
        tree names.
    _Detnums (list) - All the valid detector numbers.
    _LastDetnum (int) - Detector number used last time a data function was 
        called.  Allows simplification of data function call. Similar to
        CAP_last_detnum.
    _LastCut (cut) - Detector number used last time a cut function was 
        called. Allows simplification of data function call. Similar to 
        CAP_last_cut.

Functions:
    Set_LastDetnum: Store the last detector number called.
    Get_LastDetnum: Return the last detector number called.
    Set_LastCut: Store the last cut called.
    Get_LastCut: Return the last cut called.

Created on Tue Nov  5 14:19:11 2013

@author: tdoughty1
"""

_FileInfo = None
_Detnums = None
_LastDetnum = None
_LastCut = None


def Set_LastDetnum(detnum):
    ''' Store the last detector number called.
        
        Parameters:
            detnum: (int) - Detector number
        
        Raises:
            TypeError: If detnum is not an integer
            ValueError: If detnum is not in valid list
    '''
    global _LastDetnum
    
    if not isinstance(detnum, int):
        raise TypeError('ERROR in Set_LastDetnum:\n' +
                        'Detnum must be an integer!')
    
    # Detnum must be in expected range
    if(detnum not in _Detnums):
        raise ValueError('ERROR in Set_LastDetnum:\n' +
                         'Detnum must be in the current detector list!')
    
    _LastDetnum = detnum


def Get_LastDetnum():
    ''' Return last detector number called. '''
    return _LastDetnum


def Set_LastCut(cut):
    ''' Store the last detector number called.
        
        Parameters:
            cut: (np.ndarray?) - Selection cut applied in most recent function
                call.
        
        Raises:
            TypeError: If cut is not a valid object
        
        #TODO: Implement cut class?
    '''    
    global _LastCut

    #TODO implement type checking
    _LastCut = cut


def Get_LastCut():
    ''' Return last cut called. '''
    return _LastCut
