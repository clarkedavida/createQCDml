#!/bin/bash

# 
# installQCDmlUtils.bash                                                               
# 
# D. Clarke 
# 
# Script to set up QCDml tools for you. 
# 

currentDirectory=$(pwd)
bashrcFile=${HOME}/.bashrc

read -p "This will add a line to the end of your ~/.bashrc or edit the PYTHONPATH there. Is that okay? (Y/y to proceed.) "
if ! [[ $REPLY =~ [Yy]$ ]]; then
    exit
fi

python3 QCDmlInstallHelper.py ${bashrcFile} ${currentDirectory}
mv ${bashrcFile}.temp ${bashrcFile}

source ${bashrcFile}

echo "QCDmlTools installed."

