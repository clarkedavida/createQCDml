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

# beta 10/g2 for us, not 6/g2. 5/3 factored out into the beta?
normalization = 'c0_is_one'
symanzikCoeffs = { 'c0' : 1,
                   'c1' : -1/20,
                   'c2' : 0.0,
                   'c3' : 0.0 }
