# -*- coding: utf-8 -*-
"""
fileinfo.py

CAPy module for the FileInfo class.

An object of the FileInfo should be created with every CAPy session.  One of the
challenges in loading ROOT data is that many files have a different set of RQs
(primarily due to CDMSlite).  The solution is to map each file and get a list
of branch names as well as the detector numbers and files that have those files.
This object can then be asked to simplify the data loading process.

Classes: 
    FileInfo - Structure to hold root file mapping information.

Created on Mon Jul 14 13:26:04 2014 
Based on root_GetDir from cdmstools

@author: tdoughty1
"""

# Import Standard libraries
from os.path import isfile

# Import ROOT libraries
import rootpy.io as rpi

class FileInfo(object):
    ''' Class for a root file mapping information.
    
        This class is created during the startup of a CAPy session.  It holds
        a list of file names, root directory names and tree name for all the of
        the cuts and RQs.  Specifically which detector numbers occur for each RQ
        in each file.
        
        Called:
            fileNameList, dirNameList, treeNameList = FileInfo(dataname, detnum)
        
            Inputs:
                dataname: (str) - Name of rq or cut to be loaded.
                detnum: (int) - Detector number to be loaded (1 for event data 
                    or cut, ie. EventNumber).
        
            Outputs:
                fileNameList: (list) - Names of files to be loaded for input 
                    detnum and dataname.
                dirNameList: (list) - Names of root file directories to be 
                    loaded.
                treeNameList: (list) - Names of root trees to load data from.

        Constructed:
            FileInfo(dataFileList, cutFileList)
            
            Parameters:
                dataFileList: (list) - All data files to be studied in this 
                    session.
                cutFileList: (list) - All cut files to be studied in this 
                    session.

        Methods:
            AddDataFiles: Add one or more data files to current session.
            AddCutFiles: Add one or more cut files to current session.
            GetDataNames: Return list of data names in current session.
            GetCutNames: Return list of cut names in current session.
            IsGeneral: Checks if the branch is general (true) or detector
                specific (false).


        Hidden Methods:
            _AddFiles: Called by AddDataFiles and AddCutFiles, checks files
                existence, then add file to appropriate file list and calls
                _MapFile.
            _MapFile: Called by _AddFiles, loads root file and gets map of
                directory and tree names for use in loading data.

        Attributes:
            _dataList: (list) - All the datafiles included in the current 
                session.
            _dataInfo (dict) - dict of the lists corresponding to every data 
                branch found in any datafile and the detector numbers which 
                correspond to that RQ. Multilevel dict keyed first by data
                name, then by detector number. 
            _cutList: (list) - All the cutfiles in the current session.
            _cutInfo: (dict) - Contains lists corresponding to every 
                available cut and corresponding detectors.  Multilevel dict
                keyed first by cut name, then by detector number. 
    '''

    def __init__(self, dataList=None, cutList=None):
        ''' Constructs a file information object from a datalist and/or cutlist.
            
            Parameters:
                dataList: (list or str) - Filenames  of data files to be added
                    to CAPy session.
                cutList: (list or str) - Filenames of cut files to be added to 
                    Capy session. (optional)
        '''
            
        # RQ structure is a list of files and 
        # dict of file lists mapped to RQ/detnum combinations
        self._dataList = []
        self._dataInfo = {}
        
        # Cut structure is a list of files and 
        # dict of file lists mapped to cut/detnum combinations
        self._cutList = []
        self._cutInfo = {}
        
        # If datalist is given, map files and add into structures
        if dataList:
            self.AddDataFiles(dataList)
        
        # If cutlist is given, map files and add into structures
        if cutList:
            self.AddCutFiles(cutList)
    
    def __call__(self, dataName, detnum):
        ''' Accesses the list of files for a data value and detector number.
        
            Parameters:
                dataName: (str) - Name of cut or data value to get information
                detnum: (int) - Detector number (1 = general)
            
            Returns: (filePath, dirName, treeName)
                filePath: (list) - All files where detnum has data value
                dirName: (list) - Directories for detnum and branch.
                treeName: (list) - Trees for detnum and branch.
                
            Raises:
                ValueError
                
            #TODO - Switch to single dirName/treeName value?
        '''

        # Check if request is for data
        if dataName in self._dataInfo:
            setDetInfo = self._dataInfo[dataName]

        # Otherwise it should be a cut
        elif dataName in self._cutList:
            setDetInfo = self._cutList[dataName]
        
        # This means its neither a cut or data
        else:
            raise ValueError('ERROR in FileInfo:\n' +
                             dataName + ' is not in data or cut files!')

        # Check if detector number in dict
        if detnum not in setDetInfo:
            raise ValueError('ERROR in FileInfo:\n' +
                             'Detnum: ' + str(detnum) + 
                             ' has no data for + ' + dataName + '!')
            return None
        else:
            filePath = setDetInfo[detnum]['File']
            dirName = setDetInfo[detnum]['Dir']
            treeName = setDetInfo[detnum]['Tree']
            return (filePath, dirName, treeName)

    ######### 'Public' Methods ###########
    def AddDataFiles(self, dataNames):
        ''' Add a data file or list of files to the current session.
        
            Parameter:
                dataNames: (list or str) - Root data file(s) to be added to the 
                    current CAPy session.
        '''
        
        self._AddFiles(dataNames, 'Data')

    def AddCutFiles(self, cutNames):
        ''' Add a cut file or list of files to the current session.
        
            Parameter:
                cutNames: (list or str) - Root cut file(s) to be added to the 
                    current CAPy session.
        '''

        self._AddFiles(cutNames, 'Cut')
    
    def GetDataNames(self):
        ''' Return list of data names in current session.'''
        return self._DataInfo.keys()
    
    def GetCutNames(self):
        ''' Return list of cut names in current session.'''
        return self._CutInfo.keys()

    def IsGeneral(self, name):
        ''' Return true if it's a general value, otherwise false.
        
            Parameters:
                name: (str) - Name of data or cut branch to check.
            Raises:
                TypeError: If name is not a string
        '''
        
        # Check it's correct type
        if not isinstance(name, str):
            raise TypeError('ERROR in FileInfo.IsGeneral:\n' +
                            'Input branch name must be a string!')
        
        # Check its a valid name
        if name in self.GetDataNames():  # Data Branch name
            tempDict = self._dataInfo[name]
        elif name in self.GetCutNames():  # Cut Branch name
            tempDict = self._cutInfo[name]
        else:  # Not in any file
            print "WARNING in FileInfo.IsGeneral:"
            print "Input branch isn't in current session!"
            print "No value returned!"
            return None

        # A general data or cut should have 1 as it's only key        
        if len(tempDict.keys()) == 1 and 1 in tempDict:
            return True
        else: 
            return False

    ######### 'Hidden' Methods ###########
    def _AddFiles(self, fNames, fType):
        ''' Add root files to the current session.
        
            Checks that every file is a valid root file, stores filename in the
            appropriate file list, then passes the file name and file info dict
            to _MapFile.
        
            Called by both AddDataFiles and AddCutFiles with appropriate flag.
            
            Parameters:
                fNames: (list, str) - Root file(s) to be added to the current
                    CAPy session.
                fType: (str) - Either 'Data' or 'Cut' to select list to which to
                    add file(s).

            Raises:
                TypeError: If fNames is not a list or str.
                ValueError: If fType is neither 'Data' nor 'Cut'.
                IOError: If a file in fNames doesn't exist.
        '''

        # if fNames is single name, put into into a list
        if isinstance(fNames, str):
            fNames = [fNames]
        elif isinstance(fNames, list):
            pass
        else:
            raise TypeError('ERROR in FileInfo.Add' + fType + 'Files:\n' +
                            'Input files should be a list of files or a ' +
                            ' single file name!')
        
        # Select which list to add files
        if fType == 'Data':
            setList = self._dataList
        elif fType == 'Cut':
            setList = self._cutList
        else:
            raise ValueError('ERROR in FileInfo.Add' + fType + 'Files:\n' + 
                             'Unknown file type ' + fType + ' added!\n' + 
                             "Should be 'cut' or 'data'!")
        
        # Loop through all files in input list
        for fName in fNames:
            
            # Check if file exists in current list
            if fName in self._dataList:
                continue
            
            # Check if file exists
            if not isfile(fName):
                raise IOError('ERROR in FileInfo.Add' + fType + 'Files:\n' +
                              'File ' + fName + " doesn't exist!")
                continue
            
            # Add good file to list
            setList.append(fName)

            # Map good file
            self._MapFile(fName, fType)

    def _MapFile(self, fName, fType):
        ''' Get branch names for each file and store corresponding file, 
            directory, and tree names, as well as the appropriate detector 
            number(s).
        
            Parameters:
                fName: (str) - Name of file to map.
                fType: (str) - File type of fName: 'Cut' or 'Data'
        '''
        
        # Temporary for debugging
        # TODO: switch to a verbose flag
        print fName

        # List of directories in files that we don't use
        if fType == 'Data':
            skipDirs = ['calibInfoDir', 'infoDir', 'detectorConfigDir' ]
            fileInfo = self._dataInfo
        elif fType == 'Cut':
            skipDirs = ['cutInfoDir']
            fileInfo = self._cutInfo
    
        # Dict of branches copied between files and the directory to ignore
        doubleBranches = {'SeriesNumber', 'EventNumber', 'DetType', 'Empty'}
    
        # Open root file
        with rpi.root_open(fName, 'r') as rootFile:
    
            # Loop through Directories
            for keyDir in rootFile.GetListOfKeys():
                rootDir = keyDir.ReadObj()
                dirName = rootDir.GetName()
        
                # Ignore directory if it's not an RQ directory
                if dirName in skipDirs:
                    continue
        
                # Loop through the trees in directory
                for keyTree in rootDir.GetListOfKeys():
                    tree = keyTree.ReadObj()
                    treeName = tree.GetName()
            
                    # Get detector number if it's a ziptree
                    if 'zip' in treeName.lower():
                        detnum = 1100 + int(treeName.split('zip')[1])
                    # Otherwise it's a general quantity (detnum = 1)
                    else:
                        detnum = 1

                    # Loop through branches on tree
                    for branch in tree.GetListOfBranches():
                
                        branchName = branch.GetName()
                        branch.Clear()
                
                        # If branch is one of the ones in two different files,
                        # choose data from calib file.
                        if branchName in doubleBranches:
                            if 'calib' not in treeName:
                                continue
                
                        # Check if branch is in dict, if not create empty dict
                        if branchName not in fileInfo:
                            fileInfo[branchName] = {}        
    
                        # Check if Detnum in dict, if not create empty lists
                        if detnum not in fileInfo[branchName]:
                            fileInfo[branchName][detnum] = {'File': [],
                                                            'Dir': dirName,
                                                            'Tree': treeName}
                
                        # Store Filename for each combo
                        fileInfo[branchName][detnum]['File'].append(fName)
                        
                        # Check if treeName and dirName are the same
                        if fileInfo[branchName][detnum]['Dir'] != dirName:
                            raise ValueError('ERROR in _MapFile:\n' +
                                             'Directory ' + dirName + ' does ' +
                                             'not match the expected name: ' +
                                             fileInfo[branchName][detnum]['Dir'])
                        if fileInfo[branchName][detnum]['Tree'] != treeName:
                            raise ValueError('ERROR in _MapFile:\n' +
                                             'Directory ' + treeName + ' does ' +
                                             'not match the expected name: ' +
                                             fileInfo[branchName][detnum]['Tree'])
            
                    # Clear Tree #FIXME - still have memory leak
                    tree.Delete()
            
                # Clear Directory #FIXME - still have memory leak
                rootDir.Delete()
