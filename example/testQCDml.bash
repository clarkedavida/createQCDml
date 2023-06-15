#!/bin/bash
# 
# testQCDml.bash                                                               
# 
# D. Clarke 
# 
# Create example XML files using createQCDml utilities, then confirm that they validate
# againste the QCDml schema. 
# 

confFile=example_config.xml
ensFile=example_ensemble.xml

if [ -f $confFile ]; then rm $confFile; fi
if [ -f $ensFile ]; then rm $ensFile; fi

python3 exampleQCDmlUtilScript.py 
bash ../xml/doValidate.bash ../xml/QCDmlConfig1.3.1.xsd $confFile 
bash ../xml/doValidate.bash ../xml/QCDmlEnsemble1.4.8.xsd $ensFile
