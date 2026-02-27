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

size = { "x" : 40,
         "y" : 40,
         "z" : 40,
         "t" : 8  }

gaugeGroup          = "SU(3)"
gaugeRepresentation = "fundamental"
gaugeBCs            = { "x" : "periodic", "y" : "periodic", "z" : "periodic", "t" : "periodic" }

license             = "https://creativecommons.org/licenses/by/4.0/"

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
