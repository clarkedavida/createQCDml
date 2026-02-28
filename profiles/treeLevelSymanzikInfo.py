# 
# treeLevelSymanzikInfo.py
# 
# D. Clarke 
# 
# Ensemble metadata that are specific to the HISQ action. 
#

actionType = 'treelevelSymanzikGluonAction'

gaugeGroup          = "SU(3)"
gaugeRepresentation = "fundamental"
gaugeBCs            = { "x" : "periodic", 
                        "y" : "periodic", 
                        "z" : "periodic", 
                        "t" : "periodic" }

normalization = 'c0_is_one'
symanzikCoeffs = { 'c0' : 5/4,
                   'c1' : -1/6,
                   'c2' : 0.0,
                   'c3' : 0.0 }
