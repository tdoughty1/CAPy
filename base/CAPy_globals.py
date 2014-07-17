# -*- coding: utf-8 -*-
"""
globals. py

Module to keep track CAPy session settings.

Functions:
    SetLastDetnum: Store the last detector number called.
    GetLastDetnum: Return the last detector number called.
    SetLastCut: Store the last cut called.
    GetLastCut: Return the last cut called.
    GetDataNames: Return list of data branches in current session.
    GetCutNames: Return list of cut branches in current session.
    IsGeneral: Checks if branch name is a general value.
    GetDetnums: Return list of valid detector numbers.

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

Created on Tue Nov  5 14:19:11 2013

@author: tdoughty1
"""

######################## Global Data Attributes ###############################

_FileInfo = None
_LastDetnum = None
_LastCut = None

######################## Data Access Methods ##################################
def SetLastDetnum(detnum):
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
    if(detnum not in _FileInfo.GetDetnums()):
        raise ValueError('ERROR in Set_LastDetnum:\n' +
                         'Detnum must be in the current detector list!')
    
    _LastDetnum = detnum


def GetLastDetnum():
    ''' Return last detector number called. '''
    return _LastDetnum


def SetLastCut(cut):
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


def GetLastCut():
    ''' Return last cut called. '''
    return _LastCut

def GetDataNames():
    ''' Return list of data branch names in current session.'''
    return _FileInfo.GetDataNames()

def GetCutNames():
    ''' Return list of cut branch names in current session.'''
    return _FileInfo.GetCutNames()

def IsGeneral(name):
    ''' Checks if branch name is a general data or cut value.'''
    return _FileInfo.IsGeneral(name)

def GetDetnums():
    ''' Return list of detector numbers in current session files.'''
    return _FileInfo.GetDetnums()
