#!/bin/bash
# 
# doValidate.bash                                                               
# 
# D. Clarke
# 
# This script shows how to validate an xml file. This is mostly for people
# like me who have trouble remembering Bash commands. 
# 

function _checkExtension {
  case $1 in *.$2) return 1;; esac
  return 0
}

schema=$1
xmldoc=$2

usage() {
echo "USAGE: $0 [xsd file] [xml file]"
exit
}

_checkExtension $schema xsd
if [ ! $? -eq 1 ]; then usage; fi

_checkExtension $xmldoc xml
if [ ! $? -eq 1 ]; then usage; fi

# This is the only important line
xmllint --schema $schema $xmldoc --noout
