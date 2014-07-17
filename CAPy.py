# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 15:09:47 2014 

@author: tdoughty1
"""

# Import CAPy modules
from base.fileinfo import FileInfo
from base.datatypes import Data_Function

# Import Global session variables
import CAPy_globals

def Start_Session(fileList):
    
    f = open('fileList.txt','r')
    files = f.readlines()
    f.close()

    CAPy_globals._FileInfo = FileInfo()    

    try:
        CAPy_globals._FileInfo.AddDataFiles(files)
    except ValueError:
        print "ERROR in CAPy.Start_Session:"
        print "Unknown file in filelist."
        return None

    print "Successfully Loaded Data"