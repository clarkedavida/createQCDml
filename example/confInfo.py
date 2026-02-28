# 
# confInfo.py 
# 
# D. Clarke 
# 
# This is an example profile when you want to make a QCDml file for a configuration.
# By the way, you can also structure this as a class inside exampleQCDmlUtilScript
# if you prefer. 
#

from QCDmlUtils import shell


QCDmlConfigFileName = "example_config.xml"
reference           = "myreference"
revisionNumber      = [0,1]
revisionAction      = ["generate","add"]
reviser             = ["Dr. Strangelove","Merkin Muffley"]
reviserInstitute    = ["Bielefeld University","Brookhaven National Laboratory"]
revisionDate        = ["2022-08-21T00:00:00+00:00",shell("./hubert-mtime.pl")]
revisionComment     = "myrevision"
revisions           = len(revisionNumber)


#--- Code information.


code                = "SIMULATeQCD"
codeVersion         = "0.1"
codeComment         = "mycode"
codeCompileDate     = "2022-01-21T00:00:00+00:00"


#--- Machine on which configuration was generated. 


machineType         = "IBM"
machineName         = "Summit"
machineInstitute    = "Oakridge National Laboratory"
machineComment      = "mymachine"


#--- Configuration-specific information. 


parameterName       = ["A","B","C"]
parameterValue      = ["1","2","3"]

series              = "0"
update              = "400"
configurationName   = "l408f21b6260m002025m0810a_0.400"

plaquette           = "1.0"
precision           = "single"
checksum            = "12ec367d"
field               = "su3gauge"
