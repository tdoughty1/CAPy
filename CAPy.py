# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 15:09:47 2014 

@author: tdoughty1
"""

from Tkinter import Tk
from tkFileDialog import askopenfilename


def Start_Session():
    
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    print(filename)