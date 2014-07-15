# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 14:57:28 2013

@author: tdoughty1
"""

import CAPy.Globals


class Data(object):

    def __init__(self, name, isgeneral, iscut=False):

        self.__name__ = name
        self._isgeneral = isgeneral
        self._iscut = iscut

        # For general cut only need one check
        if(self._isgeneral):
            self._isloaded = False

        # For detector specific data need to check for each detector
        else:
            self._isloaded = []
            for i in range(15):
                self._isloaded.append(False)

    def __call__(self, *args):

        # First parse optional arguments (ie. detnum,cut)
        self._SetArgs(args)

        # Next check if data is currently stored
        # First check the Cut or DataBuffer
        if(self._iscut):
            pass
        else:
            if(self._isgeneral):
                return CAPy.Globals._DataManager.ReadData(self.__name__)
            else:
                detnum = CAPy.Globals.GetDetnum()
                return CAPy.Globals._DataManager.ReadData(self.__name__,
                                                          detnum)

            # If you make it here, it's the first time loading, so load data

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
                CAPy.Globals.SetCut(args[0])
            elif(len(args) == 1):
                CAPy.Globals.SetCut(args[0])

            # Now check to confirm that cut is defined
            if(CAPy.Globals.SetCut is None):
                print "Error in " + self.__name__ + ":"
                print "Cut must be either assigned in call, or globals!"

        # For detector specific data take at most two arguments: detnum and cut
        # Store detnum and cut in globals module
        else:
            if(len(args) > 2):
                print self.__name__ + ' takes at most two arguments' + \
                                      ' (detnum,cut).'
                print 'Ignoring additional arguments.'
                CAPy.Globals.SetDetnum(args[0])
                CAPy.Globals.SetCut(args[1])
            elif(len(args) == 2):
                CAPy.Globals.SetDetnum(args[0])
                CAPy.Globals.SetCut(args[1])
            elif(len(args) == 1):

                # There is some ambiguity here, is it a detnum or a cut
                # Treat it as a detector number if it's in the global list
                if(args[0] in CAPy.Globals._Detnums):
                    CAPy.Globals.SetDetnum(args[0])

                # Otherwise it must be a cut, so store as such
                else:
                    CAPy.Globals.SetCut(args[0])

            # Now check to confirm that both cut and detnum are defined
            if(CAPy.Globals.SetDetnum is None or
               CAPy.Globals.SetCut is None):
                print "Error in " + self.__name__ + ":"
                print "Detnum and cut must be either assigned in call, " + \
                      "or globals!"


class Cut(Data):

    # Overwrites Data class method
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
                CAPy.Globals.SetDetnum(args[0])
            elif(len(args) == 1):
                CAPy.Globals.SetDetnum(args[0])

            # Now check to confirm that detnum is defined
            if(CAPy.Globals.SetDetnum is None):
                print "Error in " + self.__name__ + ":"
                print "Detnum must be either assigned in call, or in globals!"
