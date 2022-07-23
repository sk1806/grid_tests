#!/usr/bin/env python

# gives an ls of dfc without recurisve behaviour 
# (i.e. doesnt recursively show the conetntes of folders in the given location)

# Usage:  $ ./dirac_list.py /t2k.org/user/

import sys

from DIRAC.Core.Base import Script
Script.initialize()
from DIRAC.Resources.Catalog.FileCatalog import FileCatalog




def is_file(filename):

    fc = FileCatalog()
    res = fc.isFile(filename)
    print(res)
    #{'OK': True, 'Value': {'Successful': {'/hyperk.org/aghhhhhh': False}, 'Failed': {}}}
    #print("res['OK'] =      " ,  res['OK'])
    #print("res['Value'] =      ", res['Value'])
    #print("res['Value']['Successful'] =      ", res['Value']['Successful'])    
    print("res['Value']['Successful']['",filename,"'] =      ", res['Value']['Successful'][filename])
    is_it = res['Value']['Successful'][filename]
    return is_it

def list_dir(path, out_file):

    fc = FileCatalog()
    res = fc.listDirectory(path)
    if not res['OK']:
        print >>sys.stderr, "Failed to list path '%s': %s", path, res['Message']
        return
    listing = res['Value']['Successful'][path]

    f_out = open(out_file, "w")
    for item in sorted(listing['Files'].keys() + listing['SubDirs'].keys()):
        f_out.write(item + '\n')


def list_dir_beta(path, out_file = ''):

    fc = FileCatalog()
    res = fc.listDirectory(path)
    if not res['OK']:
        print >>sys.stderr, "Failed to list path '%s': %s", path, res['Message']
        return
    listing = res['Value']['Successful'][path]

    if out_file != '':    
        f_out = open(out_file, "w")
    files = []
    for item in sorted(listing['Files'].keys() + listing['SubDirs'].keys()):
        if out_file != '':    
            f_out.write(item + '\n')
        files.append(item)
    return files



#sn_0000_000001360_wcsr.roo


#########################################
def extract_num_list(inList, outList, spacer = '-'):
#########################################
    
    # read in each line, extract numbers
    # from ABCD_EFGH in filename
    # to   ABCD EFGH in output list
    # write to a new file
    
    f_in  = open(inList, "r")
    f_num = open(outList, "w+")
    
   # if not (  os.path.isfile(inList)   ):
   #    print >>sys.stderr, "extract_number_list :: In file list does not exist"  
   #    return
    
    for line in f_in:
        #print(line)
        mod_0 = line.rstrip('\n')                    # strip end of line
        print(mod_0)
        mod_1 = mod_0.rsplit('/', 1)                 # remove directory structure. maxsplit 1 gives 2 elements.
        print('mod_1 = ' , mod_1)
        mod_2 = mod_1[1].rsplit('_', 1)                 # extract number code
        print('mod_2 = ' , mod_2)
        mod_3 = mod_2[0].rsplit('_',1)        
        print('mod_3 = ' , mod_3)
        mod_4 = mod_3[0].rsplit('_', 1)
        print('mod_4 = ' , mod_4)
        mod_5 = mod_4[1] + spacer + mod_3[1]   + '\n'    # write numbers with space and end of line
        print('mod_5 = ' , mod_5)
        f_num.write(mod_5)
    
    f_in.close()
    f_num.close()
#########################################


def extract_miss_rep( numList, misList, repList , startRun, endRun, startSub=0, endSub = 56, spacer = '-'):


    f_num = open(numList, "r")
    f_mis = open(misList,"w+")
    f_rep = open(repList,"w+")
    
#    startRun = 90910000
#    endRun   = 90910105 # excludes this numebr
#    startSub = 0
#    endSub   = 56  # excludes this number
    
    
    firstFind = [-99999999, -9999]
        
    
    # create a list, where each element is a line from the text file
    lines = f_num.readlines()
    n_lines = len(lines)
    print('# lines = ')
    print(n_lines)
    print(lines[0])
    print('')
    
    
    # to find repeated lines, you just need to check each line compared to the line above
    # should sort first  = 0
    
    
    # add missing file codes (ABCD_EFGH) to text file
    # f_miss
    
    # also add missing file codes  (ABCD_EFGH) to a list
    missing=[]
    missing_index = 0
    
    # check which file codes are in the list
    # once a code is matched, move to th next line
    lines_index = 0
    
    # loop though the list of desired codes
    # if it matches the current code from the file, move to the next
    # if it does not match, add to missing list
    
    num = (  lines[lines_index].rstrip('\n')  ).split(spacer, 1)  #  THIS WILL BREAK FOR T2K because .num have spare not -  ... but i should change this XXX
    print('num = ', num)
    print('num[0] = ', num[0])
    print('startRun = ', startRun)

    num[1] = str( int(num[1])/10 ) # TEMP FOR SN
    print(num[1])

    if( int(num[0]) < startRun ):
        print('First file run number is below loop range!! ')
        exit()
    if( int(num[1]) < startSub ):
        print('First file subrun number is below loop range!! ')
        exit()

    # i,j are the full set of numbers you are looking for
    # num and lines_index searches the numbers you have in the file    
    for i in range (startRun, endRun, 1):
        for k in range (startSub, endSub, 1):
            print('')
            print('Searching:  '+ str(i) + spacer +str(k) )
            print('Checking line:      ' + str(num[0]).zfill(4) + spacer + str(num[1]).zfill(8) )  # 8 not 9 temp 
            print('lines_index = ' + str(lines_index) )

            # check for repeated run codes     
            # check if line is the same as the one before
            # if it is then write this line to the rep file
            # then increase the line index (and hence 'num') 
            # so you can still do the other checks now you skipped to the next line
            # while keeping number i,k the same
            while( lines_index>0 and lines[lines_index] == lines[lines_index -1]  ):
                print('Repeated entry:  ' +  lines[lines_index] )
                # write the line to the file (node the i,k because these are now ahead)
                code = str(num[0]).zfill(4) + spacer + str(num[1]).zfill(8)   # 8 not 9 temp
                f_rep.write( code )
                f_rep.write('\n')
                #lines_index += 1
                # only need to update num when we increase the index
                # provided it isnt at the end
                if ( lines_index    != n_lines - 1  ):
                    lines_index += 1            
                    num = (  lines[lines_index].rstrip('\n')  ).split(spacer, 1)  
                    num[1] = str( int(num[1])/10 ) # TEMP FOR SN
                    print('num[1] = ', num[1])
                    print(' - new index = ' + str(lines_index) )
                    print(' - new line to check: ' + str(num[0]).zfill(4) + spacer + str(num[1]).zfill(8) )   # 8 not 9 temp
            # check if we exhausted list of files 
            # in which case just add to missing list
            if( lines_index  == n_lines  ):  
                print('Exhausted list')
                #print('End of file')
                code = str(i).zfill(4) + spacer + str(k).zfill(8)  # temp 8 not 9
                f_mis.write( code )
                f_mis.write('\n')
                missing.append( (i,k) )
                missing_index += 1
                continue

            if( (i,k) == ( int(num[0]), int(num[1]) ) ):
                print('Found ' + str(i) + spacer +str(k) )
                #lines_index += 1            
                # only need to update num when we increase the index
                # provided it isnt at the end
                if ( lines_index  != n_lines - 1  ):
                    lines_index += 1            
                    num = (  lines[lines_index].rstrip('\n')  ).split(spacer, 1) #
                    num[1] = str( int(num[1])/10 ) # TEMP FOR SN
                    #  XXX using a dash which will break t2k - but i should change t2k num file to have dash not space
                    print('num = ', num )
                    print(' - new index = ' + str(lines_index) )                 
                    print(' - new line to check: ' + str(num[0]).zfill(4) + spacer + str(num[1]).zfill(8) )   # 8 not 9 temp

            else:
                print('Not found: ' + str(i) + spacer +str(k) )
                code = str(i).zfill(4) + spacer + str(k).zfill(8)
                f_mis.write( code )
                f_mis.write('\n')
                missing.append( (i,k) )
                missing_index += 1
                reread = False
                #print('--- MISSING num = i')
    
    #print( missing )


    f_num.close()
    f_mis.close()
    f_rep.close() 




########################################################
def search_codes(numList, inpList, outList, spacer = '-'):
########################################################
    """Takes a file containing number codes ABCD EFGH,
       adds the dash, and searches another list of files for these codes
       numList   = file containing list of numbers to search in form 'ABCD EFGH' (no dash)
       inpList   = file containing a list of files to search for the codes
       outList  = file containing a list of files that match the codes
     """

    if not ( os.path.isfile(numList) ):
       print >>sys.stderr, numList + ' does not exist'
       return
    if not ( os.path.isfile(inpList) ):
       print >>sys.stderr, inpList + ' does not exist'
       return

    print('Reading numbers from:  ' + numList)
    print('Searching files in:  ' + inpList)
    print('Preparing list::  ' + numList)

    f_num = open(numList, "r")
    f_inp = open(inpList, "r")
    f_out = open(outList, "w")

    nseek = 0
    # loop over file containing run codes
    for num in f_num:
        mod_0 = num.rstrip('\n')          # strip end of line
        mod_1 = mod_0.rsplit(spacer, 1)       # remove space
        mod_2 = mod_1[0] + spacer + mod_1[1]    # add dash
        #print('----------------------------------------')
        #print('')
        #print('Searching for:  ' + mod_2)
        # loop over list of files to search for run code matches
        # start at beggning each time
        # could be more clever and go back to the position of last find? 
        f_inp.seek(nseek)
        for line in f_inp:
            found = line.find(mod_2)
            #print('')
            #print('line = ' + line)
            #print('Found = ' + str(found))
            if(found != -1):
                #print('*** Found:  ' + line)
                f_out.write(line)
                # Assuming files are in order
                # the next search carries on from same place
                # minus 10 safety net for duplicates
                if(nseek>9):
                    nseek = f_inp.readline() - 10
                break

    f_num.close()
    f_inp.close()
    f_out.close()
########################################################

#1/wcsim/v1.9.3_B/wcsr/sn_001_000020170_wcsr.root

