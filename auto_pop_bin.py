############################################################################################################################
# Author: Andrew Mfune
# Date: 18/06/2018
# Descriptions: Batch converts PlayStation One(PS1) bin Files 
#               to VCD using CUE2POP. Program also auto renames and duplicates
#               POPSTARTER.ELF with the name of the VCD in the destination folder.
#               The name contains prefix "XX" at the beginning of the filename.
# Usage:
#      run the following command inside a terminal: 
#           auto_pop_bin.py "Drive:\[INSERT SOURCE DIRECTORY PATH HERE]" "DRIVE:\[INSERT DESTINATION DIRECTORY PATH HERE]"
# Note:
#     1. Make sure to download and place CUE2POP conversion tool in the same directory as the script
#     2. POPSTARTER.ELF must also be in the same directory as the script.
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
            source = validatePath(sys.argv[1])
            dest = validatePath(sys.argv[2])
            processBinDumps(source, dest)
        except Exception as error:
            print(error)
    else:
        print('Source and destination directory arguments not provided...')

def validatePath(dirPath):
    if not os.path.exists(dirPath):
        raise Exception('Directory "%s" is not valid or does not exist' % dirPath)
    
    return dirPath

def processBinDumps(source, dest):
    print('Scanning for cuesheets in %s.....' % source)
    cues = getCueSheets(source)

    if not cues:
        raise Exception('Cue files not found')

    print('Found %s cues..' % len(cues))

    for cue in cues:
        print('Processing cue: %s' % cue)
        cbin = getBinName(cue, source)
        
        if not cBin:
            print('Invalid Bin was found! ignoring...')
            continue

        cueFile = os.path.join(source, cue)

        if convertBinToVcd(cueFile, dest, cBin) == 1:
            createPopsElf(cBin, dest)
            continue
        
        print('ElF file not created...')

def getCueSheets(directory):
    if not directory:
        print('Received empty directory')
        return []

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
       
        print('Found bin %s in cuesheet' % binName)

        if binName.find('.bin') < 0:
            print('Cue has invalid Bin File')
            return ''

        if binName.strip() in os.listdir(directory):
            return binName.replace('.bin', '')
        else:
            print ('Bin %s not found in %s' % (binName, directory))

def convertBinToVcd(cueFile, destPath, binName):
    cue2PopsEXE = os.path.join(os.curdir, 'CUE2POPS_2_3.exe')
    vcdName = '%s.VCD' % binName.strip()

    if vcdName in os.listdir(destPath):
        print('VCD already exist! ignoring....')
        return 0

    print('Executing CUE2POPS:')
    cue2PopProcess = subprocess.call([cue2PopsEXE, cueFile, vcdName])

    if cue2PopProcess == 1:
        print('Checking generated VCD...')
        vcdFile = os.path.join(os.curdir, vcdName)

        if os.path.exists(vcdFile): 
            print('Moving VCD from temp directory to %s' % destPath)
            shutil.move(vcdFile, destPath)    
            return 1

        print('VCD not found!')
        return -1

    return 0

def createPopsElf(name, destDir):
    popStarter = os.path.join(os.curdir, 'POPSTARTER.ELF')
    fileName = 'XX.%s.ELF' % name.strip()
   
    destFilePath = os.path.join(destDir, fileName) 
   
    print('Saving POPSTARTER.ELF as %s ....' % fileName)
    shutil.copy(popStarter, destFilePath)

    print('ELF file saved')

main()