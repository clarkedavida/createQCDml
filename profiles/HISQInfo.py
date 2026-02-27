# 
# HISQInfo.py
# 
# D. Clarke 
# 
# Ensemble metadata that are specific to the HISQ action. 
#

actionType = 'hisqQuarkAction'

quarkNormalization = 'DoNotKnowYet'

# [periodic, antiperiodic, dirichlet, cstar, open, openSF]
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

glossary = 'http://www.lqcd.org/ildg/actionGlossaries/hisqQuarkAction.pdf'
