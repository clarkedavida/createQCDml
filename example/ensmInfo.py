# 
# ensmInfo.py
# 
# D. Clarke 
# 
# This is an example profile when you want to make a QCDml file for an ensemble.
# By the way, you can also structure this as a class inside exampleQCDmlUtilScript
# if you prefer. 
#
from QCDmlUtils import makeURI, shell 

QCDmlEnsembleFileName = "example_ensemble.xml"  # This will be the output XML name. 

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

name                = "Lisa Simpson"                     # Archiver
institution         = "Springfield University"
collaboration       = "HotQCD"
date                = shell('./hubert-mtime.pl')         # Archival date
projectName         = "f21_chiral"
ensembleName        = "l408f21b6260m002025m0810"
markovChainURI      = makeURI(collaboration,projectName,ensembleName)

# Optional funding info. These must be lists, but you can
# always set an individual element to None if you don't
# know it. Make sure that element i of the three lists all
# correspond to the same award.
fundingInstitutes   = ["Sneed's","ACME"]                 # Names of funding providers
fundingAwards       = ["Feed and Seed","ANVIL project"]  # Human-readable title of award/grant
fundingAwardNos     = ["Grant 12345",None]               # Code assigned by funder to sponsered award
