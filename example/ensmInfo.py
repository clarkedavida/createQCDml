# 
# ensmInfo.py
# 
# D. Clarke 
# 
# This is an example profile when you want to make a QCDml file for an ensemble.
# By the way, you can also structure this as a class inside exampleQCDmlUtilScript
# if you prefer. 
#
from QCDmlUtils import makeConfURI, shell 

# This will be the output XML name. 
QCDmlEnsembleFileName = "example_ensemble.xml"

size = { "x" : 40,
         "y" : 40,
         "z" : 40,
         "t" : 8  }

license = "https://creativecommons.org/licenses/by/4.0/"

quarks = {"l", "s"}

Nf = {"l" : 2,
      "s" : 1}

couplings = { "beta" : 6.260,
              "ml"   : 0.002025,
              "ms"   : 0.0810 }

name                = "Lisa Simpson"
institution         = "Springfield University"
collaboration       = "HotQCD"
date                = shell('./hubert-mtime.pl')
projectName         = "f21_chiral"
ensembleName        = "l408f21b6260m002025m0810"
markovChainURI      = makeConfURI(collaboration,projectName,ensembleName)
