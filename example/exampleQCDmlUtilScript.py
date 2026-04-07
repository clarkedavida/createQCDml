#!/bin/python3

# 
# createQCDml.py
# 
# D. Clarke 
# 
# An example script how to use the QCDmlUtils to take metadata from the
# ensemble and config profiles and structure them into xml files that follow
# the QCDml schema. 
#

# Some ingredients from createQCDml
from createQCDml.QCDmlUtils import makeURI, makeLFN, checkConfigProfile, checkEnsembleProfile 
from createQCDml.QCDmlWrite import writeQCDmlConfigFile, writeQCDmlEnsembleFile

# Your input metadata that aren't related to the action. 
import ensmInfo as ensmInfo
import confInfoMulti as confInfo 

# Skeletons for action metadata
import createQCDml.profiles.treeLevelSymanzikInfo as gActInfo
import createQCDml.profiles.HISQInfo as qActInfo

# Some basic checks that the supplied data are reasonable.
checkConfigProfile( confInfo )
checkEnsembleProfile( ensmInfo )

# Also possible to call like: makeURI( collaboration, projectName, ensembleName )
URI = makeURI( ensmInfo )
LFN = makeLFN( ensmInfo.collaboration, ensmInfo.projectName, ensmInfo.ensembleName, confInfo.configurationName )

# Make the ensemble and configuration XML files.
writeQCDmlEnsembleFile( ensmInfo, gActInfo, qActInfo )
writeQCDmlConfigFile( confInfo, dataLFN=LFN, markovChainURI=URI )

