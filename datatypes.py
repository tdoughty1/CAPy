# -*- coding: utf-8 -*-
"""
datatypes.py

Module contains the classes for accessing data/cuts.  Matches the functionality
of CAP data access routines.

Classes:
    Data_Access - Class for a data access object
    Cut_Access - Class for a cut access object. Subclass of Data_Access

Created on Sun Nov  3 14:57:28 2013

@author: tdoughty1
"""

import globals


class Data_Access(object):
    ''' Class to call data arrays from interactive shell.
    
        Modeled after the RQs from CAP, calling one of these 
    
        Called:
        
        Constructed:
        
        Hidden Methods:
            _SetArgs
    
    '''

    def __init__(self, name, isgeneral, iscut=False):
        ''' Constructs the Data Access object used to access data.
        
            Parameters:
                name: (str) - Name of data to read, corresponds to branch name.
                isgeneral: (bool) - True if it's general data, false if it's
                    detector specific.
                iscut: (bool) - True if it's created for a cut value, false if
                    it's standard data.

            Raises:
                #TODO - Implement Type checking
        '''

        self.__name__ = name
        self._isgeneral = isgeneral
        self._iscut = iscut


    def __call__(self, *args):
        ''' Return array of values.
        
            #TODO fill in possibilities
        
        '''

        # First parse optional arguments (ie. detnum,cut)
        self._SetArgs(args)

        # Next check if data is currently stored
        # First check the Cut or DataBuffer

    # Standard Get Data function should be good for RQs and RRQs
    # Need to overwrite in Cut class
    def _SetArgs(self, args):

        # Argument Parsing

        # First check if data is general or detector specific
        # For general data, take at most one argument: a cut
        # Store cut in globals module
        if(self._isgeneral):
            if(len(args) > 1):
                print self.__name__ + ' takes at most one argument (cut).'
                print 'Ignoring additional arguments.'
                globals.Set_LastCut(args[0])
            elif(len(args) == 1):
                globals.Set_LastCut(args[0])

            # Now check to confirm that cut is defined
            if(globals.Get_LastCut is None):
                print "Error in " + self.__name__ + ":"
                print "Cut must be either assigned in call, or globals!"

        # For detector specific data take at most two arguments: detnum and cut
        # Store detnum and cut in globals module
        else:
            if(len(args) > 2):
                print self.__name__ + ' takes at most two arguments' + \
                                      ' (detnum,cut).'
                print 'Ignoring additional arguments.'
                globals.Set_LastDetnum(args[0])
                globals.Set_LastCut(args[1])
            elif(len(args) == 2):
                globals.Set_LastDetnum(args[0])
                globals.Set_LastCut(args[1])
            elif(len(args) == 1):

                # There is some ambiguity here, is it a detnum or a cut
                # Treat it as a detector number if it's in the global list
                if(args[0] in globals._Detnums):
                    globals.Set_LastDetnum(args[0])

                # Otherwise it must be a cut, so store as such
                else:
                    globals.Set_LastCut(args[0])

            # Now check to confirm that both cut and detnum are defined
            if(globals.Set_LastDetnum is None or
               globals.Set_LastCut is None):
                print "Error in " + self.__name__ + ":"
                print "Detnum and cut must be either assigned in call, " + \
                      "or globals!"


class Cut_Access(Data_Access):
    ''' 
    
        Called:
        
        Constructed:
        
        Hidden Methods:
            _SetArgs
    
    '''

    # Overwrite Inherited method
    def _SetArgs(self, args):

        # First check if detector is general of detector specific
        # For general cuts, take no arguments
        if(self._isgeneral):
            if(len(args) > 0):
                print self.__name__ + ' takes no arguments.'
                print 'Ignoring any arguments.'

        # For detector specific cuts take at most one argument: detnum
        else:
            if(len(args) > 1):
                print self.__name__ + ' takes at most one argument (detnum).'
                print 'Ignoring additional arguments.'
                globals.Set_LastDetnum(args[0])
            elif(len(args) == 1):
                globals.Set_LastDetnum(args[0])

            # Now check to confirm that detnum is defined
            if(globals.Set_LastDetnum is None):
                print "Error in " + self.__name__ + ":"
                print "Detnum must be either assigned in call, or in globals!"
