# 
# QCDmlUtils.py 
# 
# D. Clarke 
# 
# Some useful utilities for creating QCDml files. 
# 


# Some Python 3.5+ standard libraries
import sys
from subprocess import run, PIPE
from types import ModuleType


def shell(*args):
    """ Carry out the passed arguments args in the shell. Can be passed as a single 
        string or as a list. Captures and returns output of shell command. E.g.
            shell('ls -lah') 
    """
    args = [str(s) for s in args]
    process = run(' '.join(args),shell=True,check=True,stdout=PIPE,universal_newlines=True)
    return process.stdout


def verboseShell(*args):
    """ Same as shell, but display results instead to screen. """
    args = [str(s) for s in args]
    process = run(' '.join(args),shell=True,check=True,stdout=PIPE,universal_newlines=True)
    print(process.stdout)


def xmlWrite(fileUnit,tag,*args,indent=0):
    """ Wrapper for writing in xml format. """
    sindent = ' '*indent
    if len(args)==0:
        fileUnit.write(sindent+'<'+tag+'>\n')
    else:
        args    = [str(s) for s in args]
        output  = ' '.join(args)
        fileUnit.write(sindent+'<'+tag+'>'+output+'</'+tag+'>\n')


def QCDmlFail(*args):
    """ Exit with error code -1. """
    args = [str(s) for s in args]
    print('  FAIL: '+(' '.join(args)))
    sys.exit(-1)


def QCDmlError(*args) -> bool:
    """ Print error message and give flag to program that you failed. """ 
    args = [str(s) for s in args]
    print('  ERROR: '+(' '.join(args)))
    return False 


def checkEqualLengths(*args) -> bool:
    """ 
    Check that all array-like objects passed have the same length. From AnalysisToolbox 
    """
    length = len(args[0])
    for i in range(len(args)):
        if args[i] is not None:
            len_i = len(args[i])
            if len_i != length:
                print(length, len(args[i]))
                return QCDmlError(f'Array length mismatch detected for array {i}. len, len[i] = {length}, {len_i}')
    return True


def getDateInt(dateString):
    """ Convert a date into an integer such that later dates are larger
        than earlier dates. WARNING: Doesn't yet know about time zones. """

    date  = dateString.split("T")[0]
    time  = dateString.split("T")[1]
    year  = date.split("-")[0]
    month = date.split("-")[1]
    day   = date.split("-")[2]

    if "+" in time:
        localTime = time.split("+")[0]
    elif "-" in time:
        localTime = time.split("-")[0]
    else:
        QCDmlFail('Encountered unexpected character in time',time)
    localHour   = localTime.split(":")[0]
    localMinute = localTime.split(":")[1]
    second      = localTime.split(":")[2]

    try:
        dateInt  = 12*31*24*60*60*int(year) + 31*24*60*60*int(month) + 24*60*60*int(day) 
        dateInt += 60*60*int(localHour) + 60*int(localMinute) + int(second)
    except ValueError:
        QCDmlFail("Can't convert y, m, d, h, min, s = ",year,month,day,localHour,localMinute,second)

    return dateInt


def checkConfigProfile(p):
    """ Run some checks on the profile p that the metadata makes sense. """

    # Set any missing, optional metadata to None.
    try:
        revisions=p.revisions
    except AttributeError:
        revisions=None
    try:
        parameterName=p.parameterName
    except AttributeError:
        parameterName=None
    try:
        parameterValue=p.parameterValue
    except AttributeError:
        parameterValue=None
    try:
        revisionNumber=p.revisionNumber
    except AttributeError:
        revisionNumber=None

    lcheck=True

    if (not isinstance(p.update,list)) and (not isinstance(p.update,str)):
        lcheck *= QCDmlError("update must be list or str")
    if isinstance(p.update,list):
        if not isinstance(p.plaquette,list):
            lcheck *= QCDmlError("update being list enforces plaquette should be list")
        if not isinstance(p.checksum,list):
            lcheck *= QCDmlError("update being list enforces checksum should be list")
        lcheck *= checkEqualLengths( p.update, p.plaquette, p.checksum )

    if not p.QCDmlConfigFileName.endswith('.xml'):
        lcheck *= QCDmlError("QCDml config name must end with xml.")
    
    for action in p.revisionAction:
        if not action in ["generate","add","replace","remove"]:
            lcheck *= QCDmlError("Revision action",action,"not allowed!")

    if p.revisionAction[0] != "generate":
        lcheck *= QCDmlError("First revision action must be 'generate'.")
    if p.revisionAction[1] != "add":
        lcheck *= QCDmlError("Second revision action must be 'add'.")

    try:    
        for date in p.revisionDate:
            if getDateInt(p.codeCompileDate) > getDateInt(date):
                lcheck *= QCDmlError("Compile date suggests code was compiled after running.")
    except AttributeError:
        pass

    if not p.precision in ["single","double","mixed"]:
        lcheck *= QCDmlError("Precision ",p.precision,"not allowed!")

    if isinstance(p.plaquette,list):    
        for i in range(len(p.plaquette)):
            if not -1.0 <= float(p.plaquette[i]) <= 1.0:
                lcheck *= QCDmlError("Detected |plaquette| > 1.0 for conf",i)
    else:
        if not -1.0 <= float(p.plaquette) <= 1.0:
            lcheck *= QCDmlError("Detected |plaquette| > 1.0.")

    if revisionNumber is not None:
        numRevisions = max( len(p.revisionAction), len(p.reviser), len(p.reviserInstitute), 
                            len(revisionNumber) )
    else:
        numRevisions = max( len(p.revisionAction), len(p.reviser), len(p.reviserInstitute) )

    lcheck *= checkEqualLengths(p.revisionAction,p.reviser,p.reviserInstitute,p.revisionNumber)

    if len(p.revisionAction) != numRevisions:
        lcheck *= QCDmlError("Number revision actions != number revisions.")
    
    if len(p.reviser) != numRevisions:
        lcheck *= QCDmlError("Number revisers != number revisions.")
    
    if len(p.reviserInstitute) != numRevisions:
        lcheck *= QCDmlError("Number reviser institutes != number revisions.")

    try:    
        if len(p.revisionDate) != numRevisions:
            lcheck *= QCDmlError("Number revision dates != number revisions.")
    except AttributeError:
        pass

    if revisionNumber is not None:
        if len(revisionNumber) != numRevisions:
            lcheck *= QCDmlError("Number revision identifiers != number revisions.")
        if revisionNumber != sorted(revisionNumber):
            lcheck *= QCDmlError("Revision identifiers out of order.")
        if revisionNumber[0] != 0:      
            lcheck *= QCDmlError("First revision identifier must be 0.")
        if revisionNumber[1] != 1:      
            lcheck *= QCDmlError("Second revision identifier must be 1.")

    if revisions is not None:
        if int(revisions) != numRevisions:
            lcheck *= QCDmlError("Number revisions incorrectly set.") 

    if parameterName is not None:
        numParameters = max( len(parameterName), len(parameterValue) )
        if len(parameterName) != numParameters:
            lcheck *= QCDmlError("Number parameter names != number parameters.") 
        if len(parameterValue) != numParameters:
            lcheck *= QCDmlError("Number parameter values != number parameters.") 
    
    if not lcheck:
        QCDmlFail("One or more errors in config profile detected.")


def checkEnsembleProfile(p):
    """ Run some checks on the profile p that the metadata makes sense. """

    lcheck=True

    # First check some of the required info is there. 
    if p.license is None:
        lcheck *= QCDmlError("QCDml ensemble requires a license.")
    if p.markovChainURI is None:
        lcheck *= QCDmlError("QCDml ensemble requires markovChainURI.")
    if p.collaboration is None:
        lcheck *= QCDmlError("QCDml ensemble requires collboration.")
    if p.projectName is None:
        lcheck *= QCDmlError("QCDml ensemble requires project name.")

    if not p.QCDmlEnsembleFileName.endswith('.xml'):
        lcheck *= QCDmlError("QCDml ensemble name must end with xml.")

    if len(p.size)!=4:
        lcheck *= QCDmlError("ILDG only supports 4D configurations currently.") 

    for direction in p.size:
        if not isinstance(p.size[direction],int):
            lcheck *= QCDmlError("Direction",direction,"must be an integer.")
        if p.size[direction]<1:
            lcheck *= QCDmlError("Direction",direction,"must be positive.")

    if not lcheck:
        QCDmlFail("One or more errors in ensemble profile detected.")


def makeConfURI(*args):
    """ Generate a configuration URI from ensemble information. Example usage:
            makeConfURI( ensembleInfoFile )
            makeConfURI( collaboration, projectName, ensembleName )
    """ 
    if len(args)==1:
        p = args[0]
        if not isinstance(p,ModuleType): 
            QCDmlFail("Pass either ensemble info or collaboration, project name, and ensemble name.")
        return "mc://ldg/"+p.collaboration+"/"+p.projectName+"/"+p.ensembleName
    else:
        try:
            collaboration = args[0]
            projectName   = args[1]
            ensembleName  = args[2]
            return "mc://ldg/"+collaboration+"/"+projectName+"/"+ensembleName
        except:
            QCDmlFail("Pass either ensemble info or collaboration, project name, and ensemble name.")


def makeDataLFN(confURI,confName):
    return confURI+"/"+confName
