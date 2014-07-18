# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 15:09:47 2014 

@author: tdoughty1
"""

import __main__

# Import CAPy modules
from base.fileinfo import FileInfo
from base.datatypes import Data_Function

# Import Global session variables
import base.CAPy_globals as CAPy_globals

def Start_Session(fileList):
    
    f = open(fileList,'r')
    files = f.readlines()
    f.close()

    fNames = []
    for fName in files:
        fNames.append(fName.strip())

    CAPy_globals._FileInfo = FileInfo() 

    try:
        CAPy_globals._FileInfo.AddDataFiles(fNames)
    except ValueError:
        print "ERROR in CAPy.Start_Session:"
        print "Unknown file in filelist."
        return None

    print "Successfully Loaded Data"
    
    for name in CAPy_globals._FileInfo.GetDataNames():
        __main__.__dict__[name] = Data_Function(name)

    print "Populated Namespace"
