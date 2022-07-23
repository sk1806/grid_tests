#!/usr/bin/env python


#https://dirac.readthedocs.io/en/stable/CodeDocumentation/DataManagementSystem/Client/DataManager.html
#https://dirac.readthedocs.io/en/stable/DeveloperGuide/AddingNewComponents/DevelopingCommands/index.html#coding-commands


#  Relevant functions
#
# DataManager module
  # putAndRegister(lfn, fileName, diracSE, guid=None, path=None, checksum=None, overwrite=False)
  #  e.g.  print dm.putAndRegister('/t2k.org/user/king/test_api_DFCname.txt', './test_api.txt', 'UKI-LT2-QMUL2-disk')

import os
import sys
import optparse
import time

import dfc_tools
from dfc_tools import * 
import gridTools

from DIRAC.Core.Base import Script
Script.parseCommandLine()

from DIRAC.DataManagementSystem.Client.DataManager import DataManager
dm = DataManager()




def upload(LFN='', LOCAL='', SE='CA-SFU-T21-disk'):
    """usage: uploads LOCAL file to storage element SE, under the path/name LFN 
       returns:  0 - uploaded,   1 - file already existed,  2 - upload failed"""
    

    # TODO - Maybe add an option for overwriting if the file already exists
 
    print('') 
    print('Upload:  ' + LFN + '  ' + LOCAL + ' ' + SE)
    print('')

    returns = 9999

    if( is_file(LFN) ):
        print('File ' + LFN + 'already exists.  NOT attempting to upload.')
        returns = 1
    else:
        print('Checked file does not exist, now attempting upload')
        b_uploaded = False # while loop starts with false, when it attemps it will update this
        returns = 0 # assume it will upload, and set to 2 if it does not
        count = 0
        while (b_uploaded == False and count < 10):
            print('Upload attempt ' + str(count) ) 
            upload = dm.putAndRegister( LFN, LOCAL, SE )
            print('')
            print(upload)
            print('')
            b_uploaded = upload['OK']
            time.sleep(10)
            # If all 10 attemps fail, then run in command line with -ddd to get some debugging
            if count == 9:
                com_upload = 'dirac-dms-add-file -ddd  ' + LFN + '  ' + LOCAL + ' ' + SE 
                print(com_upload)
                final = os.system(com_upload)
                if final != 0:
                    b_uploaded = False
                    returns = 2
            count = count + 1

    print('upload(LFN, LOCAL, SE) returns:  ' + str(returns) )
    return returns

