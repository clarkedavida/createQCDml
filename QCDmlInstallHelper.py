# 
# QCDmlInstallHelper.py
# 
# D. Clarke 
# 
# Just to help edit the bashrc. 
# 

import sys

bashrcFile=sys.argv[1]
pathToQCDml=sys.argv[2]

infile=open(bashrcFile,'r')
outfile=open(bashrcFile+'.temp','w')

# Copy everything except the PYTHONPATH line, which we append to.
PYTHONPATHexists=False
for line in infile:
    if line.startswith('export PYTHONPATH'):
        outfile.write(line.strip()[:-1]+':'+pathToQCDml+'"\n')
        PYTHONPATHexists=True
    else:
        outfile.write(line)

# If the PYTHONPATH line wasn't there, simply put it at the end.
if not PYTHONPATHexists:
    outfile.write('export PYTHONPATH="${PYTHONPATH}:'+pathToQCDml+'"\n')

infile.close()
outfile.close()
