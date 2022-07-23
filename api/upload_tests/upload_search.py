#!/usr/bin/env python

import sys
import os
from os import listdir
from os.path import isfile, join
import sys
import gridTools


# print dm.putAndRegister( LFN, LOCAL, SE )
# dirac-dms-add-file       LFN Path SE 


# TODO .. no need to have this as a script, can put it into class functions

def main():

    
    print('len(sys.argv) = ' + str(len(sys.argv)))
    if int(len(sys.argv)) < 2:  # First argument is name of script, first user input is arg1
        print('ERROR:  One argument minimum required  ')
        print('Usage: upload_search.py grifolder subsuffix')
        print('gridfolder is the LFN folder - mandatory')
        print('subsuffix is the suffix to add to subfolder e.g. "ecalmod" for  cali_ecalmod')
        exit(1)

    gridpath = sys.argv[1] # First argument is name of script, first user input is arg1

    if (len(sys.argv)) == 3:
        subsuffix = sys.argv[2]
    else:
        subsuffix = ''


    mypath = './'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    print onlyfiles
    #for files in only
    
    
    
    mypath = './'
    
   
    
    #SE = 'CA-SFU-T21-disk'
    SE = 'UKI-LT2-QMUL2-disk'
    
    f_upload = open('upload_search.list' , 'w+')
    
    b_allOK = True
    files = listdir(mypath)
    print('\n Files in dir: \n')
    print(files)
    print('')
    for f in files:
        print f
        if isfile(join(mypath, f)):  # check this is a file (not directory)
    
            b_upload = False
            if 'evtr' in f and '.root' in f:
                TYPE = 'evrt'
                b_upload = False
            elif 'numc' in f and '.root' in f and '.geo.root' not in f:   # TODO - make optional.  We dont 
                TYPE = 'numc'
                b_upload = False
            elif 'cata' in f and '.tar.gz' in f:
                TYPE = 'cata'
                b_upload = True
            elif 'logn' in f and '.log' in f:
                TYPE = 'logn'
                b_upload = True
            elif 'g4mc' in f and '.root' in f:
                TYPE = 'g4mc'
                b_upload = True
            elif 'elmc' in f and '.root' in f:
                TYPE = 'elmc'
                b_upload = True
            elif 'cali' in f and '.root' in f:
                TYPE = 'cali'
                b_upload = True
            elif 'reco' in f and '.root' in f:
                TYPE = 'reco'
                b_upload = True
            elif 'anal' in f and '.root' in f:
                TYPE = 'anal'
                b_upload = True
            elif 'logf' in f and '.log' in f:
                TYPE = 'logf'
                b_upload = True
            elif '.cfg' in f:
                TYPE = 'cnfg'
                b_upload = True  # Be careful!  
            elif ('.DAT' in f or '.dat' in f):
                TYPE = 'dat'
                b_upload = False  # Be careful!  
                if 'catalogue' in f:
                    b_upload = False
            elif ('stft' in f and 'root' in f):
                TYPE = 'stft'
                b_upload = True
            elif ('cmud' in f and 'root' in f):
                TYPE = 'cmud'
                b_upload = True
    
    
            if b_upload == True:
                if subsuffix != '':
                    TYPE = TYPE + '_' + subsuffix
                LFN = gridpath.rstrip('/') + '/' + TYPE +  '/' + f
                LFN_LOCAL_SE = LFN + ' \n' #'  ' + f + '  ' + SE + ' \n'
                print LFN_LOCAL_SE
                f_upload.write( LFN_LOCAL_SE )
                b_uploaded = gridTools.upload(LFN, f, SE)
                print('Upload:  ', b_uploaded)
                if b_uploaded == 2:
                    b_allOK = False
                    print('Upload failed: ' + LFN)
                    break
    
    f_upload.close()
    if b_allOK == False:
        print('Upload of a file failed... cleaning all files')
        com_del = 'dirac-dms-remove-files upload_search.list'
        clean = os.system(com_del)
        if clean == 0:
            print('Clean complete')
        else: 
            print('Clean failed')
    
     
    
    # Better to put the files into a text file or list
    # cos then when #you upload them, if one fails, you have the full set to make sure you delete 

main()
