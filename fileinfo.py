# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 13:26:04 2014

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
    
    def __call__(self, RQName, detnum):

        # Check if request is for data
        if RQName in self._dataInfo:
            setDetInfo = self._dataInfo[RQName]

        # Otherwise it should be a cut
        elif RQName in self._cutList:
            setDetInfo = self._cutList[RQName]
        
        # This means its neither a cut or data
        else:
            raise ValueError('ERROR in FileInfo:\n' +\
                             RQName + ' is not in data or cut files!')

        # Check if detector number in dict
        if detnum not in setDetInfo:
            raise ValueError('ERROR in FileInfo:\n' +\
                             'Detnum: ' + str(detnum) + ' has no data for + ' + RQName + '!')
            return None
        else:
            filePath = setDetInfo[detnum]['File']
            dirName = setDetInfo[detnum]['Dir']
            treeName = setDetInfo[detnum]['Tree']
            return (filePath, dirName, treeName)

    ######### 'Public' Methods ###########
    def AddDataFiles(self, fNames):
        '''
        
        '''
        self._AddFiles(fNames, 'Data')

    def AddCutFiles(self, fNames):
        '''
        
        '''
        self._AddFiles(fNames, 'Cut')

    ######### 'Hidden' Methods ###########
    def _AddFiles(self, fNames, fType):
        '''
        
        '''

        # if fNames is single name, put into into a list
        if isinstance(fNames, str):
            fNames = [fNames]
        elif isinstance(fNames, list):
            pass
        else:
            raise TypeError('ERROR in FileInfo.Add' + fType + 'Files:\n' + \
                            'Input files should be a list of files or a single file name!')
        
        # Select which list to add files
        if fType == 'Data':
            setList = self._dataList
        elif fType == 'Cut':
            setList = self._cutList
        else:
            raise ValueError('ERROR in FileInfo.Add' + fType + 'Files:\n' + \
                             'Unknown file type ' + fType + ' added to list!\n' + \
                             "Should be 'cut' or 'data'!")
        
        # Loop through all files in input list
        for fName in fNames:
            
            # Check if file exists in current list
            if fName in self._dataList:
                continue
            
            # Check if file exists
            if not isfile(fName):
                raise IOError('ERROR in FileInfo.Add' + fType + 'Files:\n' + \
                              'File ' + fName + " doesn't exist!")
                continue
            
            # Add good file to list
            setList.append(fName)

            # Map good file
            self._MapFile(fName, fType)

    def _MapFile(self, fName, fType):
        '''
        
        '''
        
        # Temporary for debugging
        # TODO: switch to a verbose flag
        print fName

        # Get list of directories in files that we don't use
        if fType == 'Data':
            skipDirs = ['calibInfoDir', 'infoDir', 'detectorConfigDir' ]
            fileInfo = self._dataInfo
        elif fType == 'Cut':
            skipDirs = ['cutInfoDir']
            fileInfo = self._cutInfo
    
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
                
                        # Check if RQ is in the dict, if not, create an empty dict
                        if branchName not in fileInfo:
                            fileInfo[branchName] = {}        
    
                        # Check if Detnum in RQ dict, if not create an empty list
                        if detnum not in fileInfo[branchName]:
                            fileInfo[branchName][detnum] = {'File': [], 'Dir': [], 'Tree': []}
                
                        # Store Filename, directory, and tree for each detector and RQ combo
                        fileInfo[branchName][detnum]['File'].append(fName)
                        fileInfo[branchName][detnum]['Dir'].append(dirName)
                        fileInfo[branchName][detnum]['Tree'].append(treeName)
            
                    # Clear Tree #FIXME - still have memory leak
                    tree.Delete()
            
                # Clear Directory #FIXME - still have memory leak
                rootDir.Delete()
