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
from QCDmlUtils import makeConfURI, makeDataLFN, checkConfigProfile, checkEnsembleProfile 
from QCDmlWrite import writeQCDmlConfigFile, writeQCDmlEnsembleFile

# Your input metadata that aren't related to the action. 
import example.ensmInfo as ensmInfo
import example.confInfo as confInfo # For fun, try also confInfoDamaged and confInfoSuppressOptional

# Skeletons for action metadata
import profiles.treeLevelSymanzikInfo as gActInfo
import profiles.HISQInfo as qActInfo

# Some basic checks that the supplied data are reasonable.
checkConfigProfile( confInfo )
checkEnsembleProfile( ensmInfo )

# Also possible to call like: makeConfURI( collaboration, projectName, ensembleName )
URI = makeConfURI( ensmInfo )
LFN = makeDataLFN( URI, confInfo.configurationName )

# Make the ensemble and configuration XML files.
writeQCDmlEnsembleFile( ensmInfo, gActInfo, qActInfo )
writeQCDmlConfigFile( confInfo, dataLFN=LFN, markovChainURI=URI )
