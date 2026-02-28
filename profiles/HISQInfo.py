# 
# HISQInfo.py
# 
# D. Clarke 
# 
# Ensemble metadata that are specific to the HISQ action. Assumes 
# there is no heavy-quark (e.g. charm) correction epsilon. 
#

actionType = 'hisqQuarkAction'

# Taken from 
quarkNormalization        = "sqrt(2)" 
projectGroupLinkTreatment = "U(3)"

quarkBCs = { "x" : "periodic",
             "y" : "periodic",
             "z" : "periodic",
             "t" : "antiperiodic" }
fat7QuarkLinks = { 'c1Link'      : 1/8,
                   'c3Link'      : 1/16,
                   'c5LinkChair' : 1/64,
                   'c7LinkTwist' : 1/384,
                   'u0'          : 1.0  }
asqTadQuarkLinks = { 'cNaik'       : -1/24,
                     'c1Link'      : 1,
                     'c3Link'      : 1/16,
                     'c5LinkChair' : 1/64,
                     'c7LinkTwist' : 1/384,
                     'cLepage'     : -1/8,
                     'u0'          : 1.0  }

algorithm = "RHMC"

glossary = 'https://latticeqcd.github.io/SIMULATeQCD/05_modules/HISQforce.html'
