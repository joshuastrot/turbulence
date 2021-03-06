#!/usr/bin/env python

import os
from sys import exit

from tools_ import logger
from tools_ import utils_detector

#Stops people from running this program directly. 
if __name__ == "__main__":
    print("This script should not be ran manually. It's apart of a package for the turbulence utility.")
    exit()
    

#Needed variables
homeDir = os.path.expanduser("~")
neededFiles = {
    "kwinrc": "/.kde4/share/config/kwinrc", 
    "auroraerc": "/.kde4/share/config/auroraerc",
    "kdeglobals": "/.kde4/share/config/kdeglobals"
}

#Attempts to set file paths
for themeFileName, themeFile in neededFiles.items():
    try:
       with open(homeDir + themeFile):
           if themeFileName == "kwinrc":
               kwinRC = homeDir + themeFile
           elif themeFileName == "auroraerc":
               auroraeRC = homeDir + themeFile
    except IOError:
       if not utils_detector.detectOpenBox():
           print("I couldn't find the themefile: " + themeFileName)
           if themeFileName == "auroraerc":
               if os.path.isdir(homeDir + '/.kde4/share/config'):
                  print("Creating " + themeFileName)
                  auroraeRC = homeDir + themeFile
                  open(auroraeRC, "w")
               else:
                  os.makedirs(homeDir + '/.kde4/share/config')
                  print("Creating " + themeFileName)
                  auroraeRC = homeDir + themeFile
                  open(auroraeRC, "w")

#Changes the kwin theme
def kwinThemer(theme):
    kwinThemes = {
        "air-black": ["PluginLib=kwin3_aurorae", True, "[Engine]\nThemeName=Air-black-remix-green"],
        "cupertino-ish": ["PluginLib=kwin3_aurorae", True, "[Engine]\nThemeName=cupertino-ish"],
        "oxygen": ["PluginLib=kwin3_oxygen", False, None],
        "plastik": ["PluginLib=kwin3_aurorae", True, "[Engine]\nEngineType=qml\nThemeName=kwin4_decoration_qml_plastik"],
    }
    
    for themeName, themeSettings in kwinThemes.items():
        if theme == themeName:
            query = "PluginLib"
            with open(kwinRC, mode='r', encoding='utf-8') as search:
                for line in search:
                    line = line.rstrip()
                    if line.startswith(query):
                        search.close()
                        break
            kwinFileRead = open(kwinRC).read()
            kwinFileRead = kwinFileRead.replace(line, themeSettings[0])
            kwinFileWrite = open(kwinRC, mode='w', encoding='utf-8')
            kwinFileWrite.write(kwinFileRead)
            kwinFileWrite.close()
        
            if themeSettings[1]:
                openAuroraerc = open(auroraeRC, mode='w', encoding='utf-8')
                openAuroraerc.write(themeSettings[2])
                openAuroraerc.close()
        
            logger.writeLog('changeTheme', themeName)
            return True
        

