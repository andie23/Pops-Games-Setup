# Pops-Games-Setup
Automatically setup your entire PlayStation One(PSX) games to be played on your Modded Ps2 via USB or SMB. 

Through a VCD conversion tool CUE2POPS, an entire folder containing bin and cue files of your 
PlayStation One games are converted to VCD along with a copies of POPSTARTER.ELF with the name of the VCD.

Inorder to get up and running, you must first download the conversion tool CUE2POPS and Place the exe in the
same folder as the script. Next, download POPSTARTER and place POPSTARTER.ELF in the same directory as the script.

Usage:

run the following command inside a terminal:

  pops_games_setup.py "Drive:\[INSERT SOURCE DIRECTORY PATH HERE]" 
                          "DRIVE:\[INSERT DESTINATION DIRECTORY PATH HERE] 
                          "[INSERT PREFIX "XX" or "SB"]" (optional)
Note:
     1. Make sure to download and place CUE2POPS conversion tool in the same directory as the script
     2. POPSTARTER.ELF must also be in the same directory as the script. If the POPSTARTER file is a USB edition, 
        the optional prefix argument should be XX or if its SMB edition, the prefix should be SB.
     3. Only bin file images are supported
