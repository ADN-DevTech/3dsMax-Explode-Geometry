'''
Based from Sublime3dsmax : http://cbuelter.de/?p=535
Removed unecessary Sublime portions of the script
'''
import os

import tomax

MAX_NOT_FOUND = r"Could not find a 3ds Max instance."
RECORDER_NOT_FOUND = r"Could not find MAXScript Macro Recorder"

def run(cmd):
    if not tomax.connectToMax(): # Always connect first
        print (MAX_NOT_FOUND)
        return
    if tomax.gMiniMacroRecorder:
        tomax.fireCommand(cmd)
        tomax.gMiniMacroRecorder = None # Reset for next reconnect
    else:
        print(RECORDER_NOT_FOUND)