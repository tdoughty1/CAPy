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

# Import Standard Libraries
from warnings import warn

# Import CAPy global settings
import CAPy_globals

# Store functions into a dict for convenience in accessing
class Data_Function(object):
    
    def __init__(self, name):
        ''' Constructs the Data Access object used to access data.
        
            Parameters:
                name: (str) - Name of data to read, corresponds to branch name.

            Raises:
                TypeError: If expected types of arguments doesn't match given.
                ValueError: If name isn't key in the dict of data or cut branch
                    names.
        '''
        
        if not isinstance(name, str):
            raise TypeError('ERROR in Data_Array():\n' +
                            'Name must be a string!')

        # Store name and check if its a global (only detnum = 1) value
        self.__name__ = name
        self._isgeneral = CAPy_globals.IsGeneral(name)

        # Set Key Flag for general status
        if self._isgeneral:
            key1 = 'Gen'
        else:
            key1 = 'Det'

        # Check if it's a cut or data
        if name in CAPy_globals.GetDataNames():
            self._iscut = False
            key2 = 'Data'
        elif name in CAPy_globals.GetCutNames():
            self._iscut = True
            key2 = 'Cut'
        else:
            raise ValueError('ERROR in Data_Array():\n' + 
                             name + ' not loaded into the current session!')
        
        # Assign appropriate check function
        self._FunctionType = key1+key2
                     
    def __call__(self, *args):
    
        if self._FunctionType == 'GenCut':
    	    return self._GenCut(args)

        if self._FunctionType == 'DetCut':
            return self._DetCut(args)
		
        if self._FunctionType == 'GenData':
            return self._GenData(args)
        
        if self._FunctionType == 'DetData':
            return self._DetData(args)
		    		

    ############# Define different calling option functions ###################
    def _GenCut(self, args):
        ''' Loads the data for a general cut. '''

        # For a general cut, no arguments should be given
        if len(args) > 0:
            warn('WARNING in ' + self.__name__ + ':\n\t' + self.__name__ + 
                 ' takes no arguments. Ignoring all arguments.', UserWarning)

        # Now call data
        print '#TODO: Load Data for ' + self.__name__ + '() here!'

    def _DetCut(self, args):
        ''' Loads the data for a detector specific cut.'''

        if len(args) > 1:
            warn('WARNING in ' + self.__name__ + ':\n\t' + self.__name__ + 
                 ' takes a single argument: detector number. Ignoring' 
                 ' additional arguments.', UserWarning)

        # If it's not a valid detector number
        if not self._Check_Detnum(args[0]):
        
            # Get Last Detector number
            detnum = CAPy_globals.GetLastDetnum
    
        # If it is a valid detector number
        else:
            detnum = args[0]

        # Store Detector Number
        CAPy_globals.SetLastDetnum(detnum)

        # Now call data
        if detnum:
            warn('WARNING in ' + self.__name__ + ':\n\t' + 'No detector'
                 ' given and none stored in globals. Returning nothing',
                 UserWarning)
            return None
        else:
            print '#TODO: Load Data for ' + self.__name__ + '(' + \
            str(detnum) + ') here!'

    def _GenData(self, args):
        ''' Loads the data for a general data value. '''
    
        if len(args) > 1:
            warn('WARNING in ' + self.__name__ + ':\n\t' + self.__name__ + 
                 ' takes a single argument: cut. Ignoring additional' +
                 ' arguments.', UserWarning)

        # If it's not a valid cut
        if not self._Check_Cut(args[0]):
        
            # Get Last Cut
            cut = CAPy_globals.GetLastCut()

        # If it is a valid cut
        else:
            cut = args[0]
        
            # Store Cut
            CAPy_globals.SetLastCut(cut)

        # Now call data
        if cut:
            print '#TODO: Load Data for ' + self.__name__ + ' here!'
        else:
            print '#TODO: Load Data for ' + self.__name__ + '(cut)' + \
                  ' here!'                

    def _DetData(self, args):
        ''' Loads the data for a detector specific value. '''
    
        # If there are more than 2 arguments
        if len(args) > 2:
            warn('WARNING in ' + self.__name__ + ':\n\t' + self.__name__ + 
                 ' takes two arguments: detnum and cut. Ignoring additional' +
                 ' arguments.', UserWarning)
            detnum = args[0]
            cut = args[1]
    
        # If there are just 2 arguments
        elif len(args) == 2:
            detnum = args[0]
            cut = args[1]
      
        # If there is one argument
        elif len(args) == 1:
            if self._Check_Detnum(args[0]):
                detnum = args[0]
                CAPy_globals.SetLastDetnum(detnum)
                cut = CAPy_globals.GetLastCut()
            elif self._Check_Cut(args[1]):
                cut = args[0]
                CAPy_globals.SetLastCut(cut)
                detnum = CAPy_globals.GetLastDetnum()
            else:
                warn('WARNING in ' + self.__name__ + ':\n\tArgument is' +
                     ' neither a detnum nor a cut. Ignoring argument.',
                     UserWarning)
                detnum = CAPy_globals.GetLastDetnum()
                cut = CAPy_globals.GetLastCut()
    
        # If there are no arguments:
        else:
    
            print 'No Arguments'
            detnum = CAPy_globals.GetLastDetnum()
            cut = CAPy_globals.GetLastCut()
            print detnum, cut
    
        # Now call data
        if detnum:
            if cut:
                print '#TODO: Load Data for ' + self.__name__ + ' here!'
            else:
                print '#TODO: Load Data for ' + self.__name__ + '(cut) here!'
        else:
            warn('WARNING in ' + self.__name__ + ':\n\t' + 'No detector' +
                 ' given and none stored in globals. Returning nothing',
                 UserWarning)
            return None

    ############# Define useful functions for checking arguments ##############
    def _Check_Detnum(self, detnum):
        ''' Check if argument is a valid detector number. '''
    
        if not isinstance(detnum, int):
            warn('WARNING in ' + self.__name__ + ':\n\tDetnum should be an' + 
                 ' integer. Using last detector number.')
            return False

        if detnum not in CAPy_globals.GetDetnums():
            warn('WARNING in ' + self.__name__ + ':\n\t' + str(detnum) + ' is' 
                 ' not a valid detector number. Using last detector number.')
            return False
    
        return True

    def _Check_Cut(self, cut):
        ''' Check if argument is a valid cut. '''
    
        #TODO: Implement Cut testing/possibly a class
        return True
