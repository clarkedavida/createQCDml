# 
# QCDmlUtils.py 
# 
# D. Clarke 
# 
# Some useful utilities for creating QCDml files. 
# 
import sys, re
from subprocess import run, PIPE
from types import ModuleType


def shell(*args):
    """ 
    Carry out the passed arguments args in the shell. Can be passed as a single 
    string or as a list. Captures and returns output of shell command. E.g.
        shell('ls -lah') 
    """
    args = [str(s) for s in args]
    process = run(' '.join(args),shell=True,check=True,stdout=PIPE,universal_newlines=True)
    return process.stdout


def verboseShell(*args):
    """ 
    Same as shell, but display results instead to screen. 
    """
    args = [str(s) for s in args]
    process = run(' '.join(args),shell=True,check=True,stdout=PIPE,universal_newlines=True)
    print(process.stdout)



def QCDmlFail(*args):
    """ 
    Exit with error code -1. 
    """
    args = [str(s) for s in args]
    print('  FAIL: '+(' '.join(args)))
    sys.exit(-1)


def QCDmlError(*args) -> bool:
    """ 
    Print error message and give flag to program that you failed. 
    """ 
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
    """ 
    Convert a date into an integer such that later dates are larger
    than earlier dates. WARNING: Doesn't yet know about time zones. 
    """

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


def getConfigOptional(p) -> dict:
    """
    Set any missing, optional metadata for config to None. 

    Args:
        p (.py or class): profile 

    Returns:
        dict: optional metadata 
    """
    res = {}
    try:
        res['revisions']=p.revisions
    except AttributeError:
        res['revisions']=None
    try:
        res['parameterName']=p.parameterName
    except AttributeError:
        res['parameterName']=None
    try:
        res['parameterValue']=p.parameterValue
    except AttributeError:
        res['parameterValue']=None
    try:
        res['revisionNumber']=p.revisionNumber
    except AttributeError:
        res['revisionNumber']=None
    try:
        res['reference']=p.reference
    except AttributeError:
        res['reference']=None
    return res


def getEnsOptional(p) -> dict:
    """
    Set any missing, optional metadata for ensemble to None. 

    Args:
        p (.py or class): profile 

    Returns:
        dict: optional metadata 
    """
    res = {}
    try:
        res['orcid']=p.orcid
    except AttributeError:
        res['orcid']=None
    try:
        res['funders']=p.fundingInstitutes
    except AttributeError:
        res['funders']=None
    try:
        res['awards']=p.fundingAwards
    except AttributeError:
        res['awards']=None
    try:
        res['awardNos']=p.fundingAwardNos
    except AttributeError:
        res['awardNos']=None
    return res


def checkConfigProfile(p):
    """ 
    Run some checks on the profile p that the metadata makes sense. 
    """

    opt            = getConfigOptional(p)
    revisions      = opt['revisions']
    parameterName  = opt['parameterName']
    parameterValue = opt['parameterValue']
    revisionNumber = opt['revisionNumber']

    lcheck=True

    if (not isinstance(p.update,list)) and (not isinstance(p.update,str)):
        lcheck *= QCDmlError("update must be list or str.")
    if isinstance(p.update,list):
        if not isinstance(p.plaquette,list):
            lcheck *= QCDmlError("update being list enforces plaquette should be list.")
        if not isinstance(p.checksum,list):
            lcheck *= QCDmlError("update being list enforces checksum should be list.")
        if not checkEqualLengths( p.update, p.plaquette, p.checksum ):
            lcheck *= QCDmlError("update, plaquette, and checksum lists must have same length.")

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
        lcheck *= QCDmlError("Precision ",p.precision,"not allowed! Must be single, double, or mixed.")

    if isinstance(p.plaquette,list):    
        for i in range(len(p.plaquette)):
            if not -1.0 <= float(p.plaquette[i]) <= 1.0:
                lcheck *= QCDmlError("Detected |plaquette| > 1.0 for conf",i)
    else:
        if not -1.0 <= float(p.plaquette) <= 1.0:
            lcheck *= QCDmlError("Detected |plaquette| > 1.0.")

    if revisionNumber is not None:
        numRevisions = max( len(p.revisionAction), len(p.reviser), len(p.reviserInstitute), len(revisionNumber) )
    else:
        numRevisions = max( len(p.revisionAction), len(p.reviser), len(p.reviserInstitute) )

    if not checkEqualLengths(p.revisionAction,p.reviser,p.reviserInstitute,p.revisionNumber):
        lcheck *= QCDmlError("revisionAction, reviser, reviserInstitute, and revisionNumber must have same length.")

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
    """ 
    Run some checks on the profile p that the metadata makes sense. 
    """

    lcheck=True

    opt      = getEnsOptional(p)
    orcid    = opt['orcid']
    funders  = opt['funders']
    awards   = opt['awards']
    awardNos = opt['awardNos']

    # First check some of the required info is there. 
    try:
        p.license
    except AttributeError: 
        lcheck *= QCDmlError("QCDml ensemble requires license.")
    try:
        p.markovChainURI
    except AttributeError: 
        lcheck *= QCDmlError("QCDml ensemble requires markovChainURI.")
    try:
        p.collaboration
    except AttributeError: 
        lcheck *= QCDmlError("QCDml ensemble requires collboration.")
    try:
        p.projectName
    except AttributeError: 
        lcheck *= QCDmlError("QCDml ensemble requires project name.")
    try:
        p.size
    except AttributeError: 
        lcheck *= QCDmlError("QCDml ensemble requires size.")
    try:
        p.QCDmlEnsembleFileName
    except AttributeError: 
        lcheck *= QCDmlError("QCDml ensemble requires QCDmlEnsembleFileName.")

    if not p.QCDmlEnsembleFileName.endswith('.xml'):
        lcheck *= QCDmlError("QCDml ensemble name must end with xml.")

    if len(p.size)!=4:
        lcheck *= QCDmlError("ILDG only supports 4D configurations currently.") 

    for direction in p.size:
        if not isinstance(p.size[direction],int):
            lcheck *= QCDmlError("Direction",direction,"must be an integer.")
        if p.size[direction]<1:
            lcheck *= QCDmlError("Direction",direction,"must be positive.")

    if orcid is not None:
        if not isinstance(orcid,str):
            lcheck *= QCDmlError('ORCID must be string.')
        orcid_pattern = r'^\d{4}-\d{4}-\d{4}-\d{3}[0-9X]$'
        if not re.match(orcid_pattern, orcid):
            lcheck *= QCDmlError('ORCID must have form XXXX-XXXX-XXXX-XXXX.')

    if not (((funders is None) and (awards is None) and (awardNos is None)) 
            or
            ((funders is not None) and (awards is not None) and (awardNos is not None))
            ):
        lcheck *= QCDmlError('fundingInstitutes, fundingAwards, and fundingAwardNos must be set together.')
    if funders is not None:
        if not isinstance(funders,list): 
            lcheck *= QCDmlError('fundingInstitutes must be list.')
        if not isinstance(awards,list): 
            lcheck *= QCDmlError('fundingAwards must be list.')
        if not isinstance(awardNos,list): 
            lcheck *= QCDmlError('fundingAwardNos must be list.')
        if not checkEqualLengths(funders,awards,awardNos):
            lcheck *= QCDmlError('fundingInstitutes, fundingAwards, and fundingAwardNos must have same length.')

    if not lcheck:
        QCDmlFail("One or more errors in ensemble profile detected.")


def makeURI(*args) -> str:
    """ 
    Generate a URI from ensemble information. Example usage:
            makeURI( ensembleInfoFile )
            makeURI( collaboration, projectName, ensembleName )
    All URIs have to have the same structure; this script enforces that structure.
    """
    if len(args)==1:
        p = args[0]
        if not isinstance(p,ModuleType): 
            QCDmlFail("Pass either ensemble info or collaboration, project name, and ensemble name.")
        return f"mc://ldg/{p.collaboration}/{p.projectName}/{p.ensembleName}"
    else:
        try:
            collaboration = args[0]
            projectName   = args[1]
            ensembleName  = args[2]
            return f"mc://ldg/{collaboration}/{projectName}/{ensembleName}"
        except:
            QCDmlFail("Pass either ensemble info or collaboration, project name, and ensemble name.")


def makeLFN(collaboration,projectName,ensembleName,confName) -> str:
    """ 
    Generate an LFN from ensemble and config information. All LFNs have to have the same structure,
    and it is convenient if the structure matches the URI. This script enforces that structure.
    """
    return f"lfn://ldg/{collaboration}/{projectName}/{ensembleName}/{confName}"
