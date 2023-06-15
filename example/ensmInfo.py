# 
# ensmInfo.py
# 
# D. Clarke 
# 
# Generic ensemble metadata. 
#
from QCDmlUtils import makeConfURI 

# This will be the output XML name. 
QCDmlEnsembleFileName = "example_ensemble.xml"

size = { "X" : 40,
         "Y" : 40,
         "Z" : 40,
         "T" : 8  }

gaugeGroup          = "SU(3)"
gaugeRepresentation = "fundamental"
gaugeBCs            = [ "periodic", "periodic", "periodic", "periodic" ]

quarks = {"l", "s"}

Nf = {"l" : 2,
      "s" : 1}

couplings = { "beta" : 6.260,
              "ml"   : 0.002025,
              "ms"   : 0.0810 }

collaboration       = "HotQCD"
projectName         = "f21_chiral"
ensembleName        = "l408f21b6260m002025m0810"
markovChainURI      = makeConfURI(collaboration,projectName,ensembleName)
