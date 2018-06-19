############################################################################################################################
# Author: Andrew Mfune
# Date: 18/06/2018
# Descriptions: This program converts entire batches of PlayStation One(PSX) 
#               bin files to VCDs through CUE2POPS conversion tool. It also
#               creates a copy of POPSTARTER.ELF with the name of the VCD along with 
#               optional prefixes XX or SB provided by the user.
# Usage:
#      run the following command inside a terminal: 
#           auto_pop_bin.py "Drive:\[INSERT SOURCE DIRECTORY PATH HERE]" 
#                           "DRIVE:\[INSERT DESTINATION DIRECTORY PATH HERE] 
#                           "[INSERT PREFIX "XX" or "SB"]" (optional)
# Note:
#     1. Make sure to download and place CUE2POPS conversion tool in the same directory as the script
#     2. POPSTARTER.ELF must also be in the same directory as the script. If the POPSTARTER file is a USB edition, 
#        the optional prefix argument should be XX or if its SMB edition, the prefix should be SB.
#     3. Only bin file images are supported
#############################################################################################################################
import os
import subprocess
import sys
import shutil

def main():
    sys.argv

    if len(sys.argv) >= 2:
        try:
            sourceDir = validatePath(sys.argv[1])
            destDir = validatePath(sys.argv[2])
            elfPrefix = 'XX'
            
            if len(sys.argv) > 3:
                elfPrefix = validateElfPrefix(sys.argv[3])

            processBinDumps(sourceDir, destDir, elfPrefix)
        except Exception as error:
            print(error)
    else:
        print('Provide Source and Destination paths....')

def validateElfPrefix(prefix):
    validPrefixes = ['XX', 'SB']
    prefix = prefix.upper().strip()
    
    if prefix not in validPrefixes:
        raise Exception('Invalid Elf prefix %s' % prefix)

    return prefix 

def validatePath(dirPath):
    if not os.path.exists(dirPath):
        raise Exception('Directory "%s" is not valid or does not exist' % dirPath)
    
    return dirPath

def processBinDumps(sourceDir, destDir, elfPrefix):
    print('Scanning for cuesheets in %s.....' % sourceDir)
    cues = getCueSheets(sourceDir)

    if not cues:
        raise Exception('Cue files not found')

    print('Found %s cues..' % len(cues))

    for cue in cues:
        print('Processing cue: %s' % cue)
        cbin = getBinName(cue, sourceDir)
        
        if not cbin:
            continue

        cueFile = os.path.join(sourceDir, cue)

        if convertBinToVcd(cueFile, destDir, cbin) == 1:
            createPopStarterCopy(cbin, destDir, elfPrefix)
            continue

        print('POPSTARTER.ElF copy was not created...')

def getCueSheets(directory):
    files = os.listdir(directory)
    cueList = []
    
    for file in files:
        if file.find('.cue') >= 0:
            cueList.append(file)  
    
    return cueList

def getBinName(cue, directory):
    cuePath = os.path.join(directory, cue)

    with open(cuePath) as cueFile:
        binDefinitionLine = cueFile.readline()
        binName = binDefinitionLine.replace('FILE', '').replace('BINARY', '').replace('"', '')
       
        print('Found %s' % binName)

        if binName.find('.bin') < 0:
            print('Unsupported image file found! ignoring...')
            return ''

        if binName.strip() in os.listdir(directory):
            return binName.replace('.bin', '')
        else:
            print ('Bin does not exist! ignoring....')

def convertBinToVcd(cueFile, destPath, binName):
    cue2PopsEXE = os.path.join(os.curdir, 'CUE2POPS.exe')
    vcdName = '%s.VCD' % binName.strip()

    if vcdName in os.listdir(destPath):
        print('VCD already exist! ignoring....')
        return 0

    print('Executing CUE2POPS:')
    cue2PopProcess = subprocess.call([cue2PopsEXE, cueFile, vcdName])

    if cue2PopProcess == 1:
        vcdFile = os.path.join(os.curdir, vcdName)

        if os.path.exists(vcdFile): 
            print('Moving VCD from temp directory to %s' % destPath)
            # For some reason, CUE2POPS doesn't support converting 
            # a VCD directly to a specified drive or folder... 
            # A workaround is to move the VCD from the root folder to a specified 
            # destination 
            shutil.move(vcdFile, destPath)    
            return 1

        print('VCD not found!')
        return -1

    return 0

def createPopStarterCopy(name, destDir, elfPrefix):
    popStarter = os.path.join(os.curdir, 'POPSTARTER.ELF')
    fileName = '%s.%s.ELF' % (elfPrefix, name.strip())
   
    destFilePath = os.path.join(destDir, fileName) 
   
    print('Saving POPSTARTER.ELF as %s ....' % fileName)
    shutil.copy(popStarter, destFilePath)

    print('ELF file saved')

main()