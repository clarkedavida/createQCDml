# 
# confInfoSuppressOptional.py 
# 
# D. Clarke 
# 
# Input data special to configurations. Optional stuff is missing. 
# 


QCDmlConfigFileName = "example_config.xml"

checksum            = "12ec367d"
#checksumb          = "90a40185"

# Multiple revisions possible, implemented as a list.
revisionNumber      = [0,1]
revisionAction      = ["generate","add"]
reviser             = ["Dr. Strangelove","Merkin Muffley"]
reviserInstitute    = ["Bielefeld University","Brookhaven National Laboratory"]
revisionDate        = ["2022-08-21T00:00:00+00:00","2022-08-22T00:00:00+00:00"]

# Code information.
code                = "SIMULATeQCD"
codeCompileDate     = "2022-01-01T01:02:03+04:00"
codeVersion         = "0.1"

# Machine on which configuration was generated.
machineType         = "IBM"
machineName         = "Summit"
machineInstitute    = "Oakridge National Laboratory"

# Configuration-specific information. 
configurationName   = "l408f21b6260m002025m0810a_0.400"
series              = "0"
update              = "400"
plaquette           = 1.0
precision           = "single"
