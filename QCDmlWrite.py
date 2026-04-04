#
# QCDmlWrite.py
#
# D. Clarke
#
# Methods for writing QCDml metadata files.
#


from QCDmlUtils import xmlWrite, getConfigOptional, getEnsOptional
import QCDmlGaugeAction as gluonTools
import QCDmlQuarkAction as quarkTools


def writeQCDmlConfigFile(p, dataLFN, markovChainURI):
    """
    Use the profile p, which can be a class or .py file, to create the QCDml file for
    a config or collection of configs. It is a good idea to run checkConfigProfile on
    p before calling this method

    Args:
        p (.py or class): profile 
        dataLFN (str)
        markovChainURI (str)
    """

    fout=open(p.QCDmlConfigFileName,'w')
    
    opt            = getConfigOptional(p)
    revisions      = opt['revisions']
    parameterName  = opt['parameterName']
    parameterValue = opt['parameterValue']
    revisionNumber = opt['revisionNumber']
    reference      = opt['reference']

    xmlWrite( fout,'?xml version="1.0" encoding="UTF-8" standalone="yes"?')
    xmlWrite( fout,'gaugeConfiguration xmlns="http://www.lqcd.org/ildg/QCDml/config2.0"')

    if dataLFN is None:
        xmlWrite( fout, 'dataLFN', p.dataLFN, indent=2 )
    else:
        xmlWrite( fout, 'dataLFN', dataLFN, indent=2 )

    xmlWrite( fout, 'management', indent=2 )
    if revisions is not None:
        xmlWrite( fout, 'revisions', revisions, indent=4 )
    if reference is not None:
        xmlWrite( fout, 'reference', reference, indent=4 )
    xmlWrite( fout, 'archiveHistory', indent=4 )
    for i in range(len(p.revisionAction)):
        xmlWrite( fout, 'archiveEvent', indent=6 )  # renamed from elem in 2.0
        if revisionNumber is not None:
            xmlWrite( fout, 'revision', revisionNumber[i], indent=8 )
        xmlWrite( fout, 'revisionAction', p.revisionAction[i], indent=8 )
        xmlWrite( fout, 'participant', indent=8)
        xmlWrite( fout, 'name', p.reviser[i], indent=10 )
        xmlWrite( fout, 'institution', p.reviserInstitute[i], indent=10 )
        xmlWrite( fout, '/participant', indent=8 )
        xmlWrite( fout, 'date', p.revisionDate[i], indent=8 )
        xmlWrite( fout, '/archiveEvent', indent=6 )
    xmlWrite( fout, '/archiveHistory', indent=4 )
    xmlWrite( fout, '/management', indent=2 )

    xmlWrite( fout, 'implementation', indent=2 )
    xmlWrite( fout, 'machine', indent=4 )
    xmlWrite( fout, 'name', p.machineName, indent=6 )
    xmlWrite( fout, 'institution', p.machineInstitute, indent=6 )
    xmlWrite( fout, 'machineType', p.machineType, indent=6 )
    xmlWrite( fout, '/machine', indent=4 )
    xmlWrite( fout, 'code', indent=4 )
    try:
        xmlWrite( fout, 'annotation', p.codeComment, indent=6 )
    except AttributeError:
        pass
    xmlWrite( fout, 'name', p.code, indent=6 )
    xmlWrite( fout, 'version', p.codeVersion, indent=6 )
    xmlWrite( fout, 'date', p.codeCompileDate, indent=6 )
    xmlWrite( fout, '/code', indent=4 )
    xmlWrite( fout, '/implementation', indent=2 )

    xmlWrite( fout, 'algorithm', indent=2 )
    xmlWrite( fout, 'parameters', indent=4 )
    if parameterName is not None:
        for i in range(len(parameterName)):
            xmlWrite( fout, 'parameter', indent=6 )
            xmlWrite( fout, 'name', parameterName[i], indent=8)
            xmlWrite( fout, 'value', parameterValue[i], indent=8)
            xmlWrite( fout, '/parameter', indent=6 )
    xmlWrite( fout, '/parameters', indent=4 )
    xmlWrite( fout, '/algorithm', indent=2 )
    xmlWrite( fout, 'precision', p.precision, indent=2 )

    # markovSequence replaces the old top-level markovStep in QCDml 2.0
    xmlWrite( fout, 'markovSequence', indent=2 )
    if markovChainURI is None:
        xmlWrite( fout, 'markovChainURI', p.markovChainURI, indent=4 )
    else:
        xmlWrite( fout, 'markovChainURI', markovChainURI, indent=4 )
    xmlWrite( fout, 'series', p.series, indent=4 )
    if isinstance(p.update,str):
        xmlWrite( fout, 'markovStep', indent=4 )
        try:
            xmlWrite( fout, 'annotation', p.confComment, indent=6 )
        except AttributeError:
            pass
        xmlWrite( fout, 'update', p.update, indent=6 )
        xmlWrite( fout, 'record', indent=6 )
        xmlWrite( fout, 'field', p.field, indent=8 )
        xmlWrite( fout, 'crcCheckSum', p.checksum, indent=8 )
        xmlWrite( fout, 'avePlaquette', p.plaquette, indent=8 )
        xmlWrite( fout, '/record', indent=6 )
        xmlWrite( fout, '/markovStep', indent=4 )
    elif isinstance(p.update,list): 
        for i in range(len(p.update)):
            xmlWrite( fout, 'markovStep', indent=4 )
            try:
                xmlWrite( fout, 'annotation', p.confComment[i], indent=6 )
            except AttributeError:
                pass
            xmlWrite( fout, 'update', p.update[i], indent=6 )
            xmlWrite( fout, 'record', indent=6 )
            xmlWrite( fout, 'field', p.field, indent=8 )
            xmlWrite( fout, 'crcCheckSum', p.checksum[i], indent=8 )
            xmlWrite( fout, 'avePlaquette', p.plaquette[i], indent=8 )
            xmlWrite( fout, '/record', indent=6 )
            xmlWrite( fout, '/markovStep', indent=4 )
    xmlWrite( fout, '/markovSequence', indent=2 )

    xmlWrite( fout, '/gaugeConfiguration' )
    fout.close()


def writeQCDmlEnsembleFile(p, gluonProf, quarkProf):
    """
    Use profiles p, gluonProf, and quarkProf to create the QCDml file for the ensemble.

    Args:
        p (.py or class): profile 
        gluonProf (.py or class): profile for gluon action. Can use one from profiles directory 
        quarkProf (.py or class): profile for quark action. Can use one from profiles directory
    """

    fout = open(p.QCDmlEnsembleFileName,'w')

    opt      = getEnsOptional(p)
    orcid    = opt['orcid']
    funders  = opt['funders']
    awards   = opt['awards']
    awardNos = opt['awardNos']

    xmlWrite( fout, '?xml version="1.0" encoding="UTF-8" standalone="yes"?' )
    xmlWrite( fout, 'markovChain xmlns="http://www.lqcd.org/ildg/QCDml/ensemble2.0"' )
    xmlWrite( fout, 'markovChainURI', p.markovChainURI, indent=2 )

    xmlWrite( fout, 'management', indent=2 )
    xmlWrite( fout, 'collaboration', p.collaboration, indent=4 )
    xmlWrite( fout, 'projectName', p.projectName, indent=4 )
    xmlWrite( fout, 'archiveHistory', indent=4 )
    xmlWrite( fout, 'archiveEvent', indent=6 )  # renamed from elem in 2.0
    xmlWrite( fout, 'revisionAction', 'add', indent=8 )
    xmlWrite( fout, 'participant', indent=8 )
    if orcid is not None: 
        xmlWrite( fout, 'orcid', orcid, indent=10 )
    xmlWrite( fout, 'name', p.name, indent=10 )
    xmlWrite( fout, 'institution', p.institution, indent=10 )
    xmlWrite( fout, '/participant', indent=8 )
    xmlWrite( fout, 'date', p.date, indent=8 )
    xmlWrite( fout, '/archiveEvent', indent=6 )
    xmlWrite( fout, '/archiveHistory', indent=4 )
    xmlWrite( fout, '/management', indent=2 )

    xmlWrite( fout, 'license', indent=2 )
    xmlWrite( fout, 'licenseURI', p.license, indent=4 )
    xmlWrite( fout, '/license', indent=2 )

    if funders is not None: 
        xmlWrite( fout, 'fundingReferences', indent=2)
        for i in range(len(funders)):
            xmlWrite( fout, 'fundingReference', indent=4)
            xmlWrite( fout, 'funderName', funders[i], indent=6)
            if awards[i] is not None:
                xmlWrite( fout, 'awardTitle', awards[i], indent=6)
            if awardNos[i] is not None:
                xmlWrite( fout, 'awardNumber', awardNos[i], indent=6)
            xmlWrite( fout, '/fundingReference', indent=4)
        xmlWrite( fout, '/fundingReferences', indent=2)

    xmlWrite( fout, 'physics', indent=2 )
    xmlWrite( fout, 'size', indent=4 )
    for direction in p.size:
        xmlWrite( fout, direction, p.size[direction], indent=6 )
    xmlWrite( fout, '/size', indent=4 )

    xmlWrite( fout, 'action', indent=4 )

    #--- Gluon action
    if gluonProf.actionType=='treelevelSymanzikGluonAction':
        gluonMD = gluonTools.treeSymanzikAction(fout,gluonProf)
    else:
        gluonMD = gluonTools.gluonAction(fout,gluonProf)

    xmlWrite( fout, 'gluon', indent=6 )
    xmlWrite( fout, gluonProf.actionType, indent=8 )
    xmlWrite( fout, 'glossary', gluonTools.glossaryDict[gluonProf.actionType], indent=10 )
    xmlWrite( fout, 'gluonField', indent=10 )
    xmlWrite( fout, 'gaugeGroup', gluonProf.gaugeGroup, indent=12 )
    xmlWrite( fout, 'representation', gluonProf.gaugeRepresentation, indent=12 )
    xmlWrite( fout, 'boundaryCondition', indent=12 )
    for direction, bc in gluonProf.gaugeBCs.items():
        xmlWrite( fout, direction, bc, indent=14 )
    xmlWrite( fout, '/boundaryCondition', indent=12 )
    xmlWrite( fout, '/gluonField', indent=10 )
    xmlWrite( fout, 'beta', p.couplings["beta"] , indent=10 )

    gluonMD.writeImprovement()

    xmlWrite( fout, '/'+gluonProf.actionType, indent=8 )
    xmlWrite( fout, '/gluon', indent=6 )
    xmlWrite( fout, 'quark', indent=6 )

    if quarkProf.actionType=='hisqQuarkAction':
        quarkMD = quarkTools.HISQAction(fout,quarkProf)
    else:
        quarkMD = quarkTools.quarkAction(fout,quarkProf)

    #--- Quark action
    for f in p.quarks:
        m_f = "m"+f
        xmlWrite( fout, quarkProf.actionType, indent=8 )
        xmlWrite( fout, 'glossary', quarkProf.glossary, indent=10 )
        xmlWrite( fout, 'quarkField', indent=10 )
        xmlWrite( fout, 'normalisation', quarkProf.quarkNormalization, indent=12 )
        xmlWrite( fout, 'boundaryCondition', indent=12 )
        for direction, bc in quarkProf.quarkBCs.items():
            xmlWrite( fout, direction, bc, indent=14 )
        xmlWrite( fout, '/boundaryCondition', indent=12 )
        xmlWrite( fout, '/quarkField', indent=10 )
        xmlWrite( fout, 'numberOfFlavours', p.Nf[f], indent=10 )
        xmlWrite( fout, 'mass', p.couplings[m_f],indent=10 )
        quarkMD.writeLinkTreatment()
        xmlWrite( fout, '/'+quarkProf.actionType, indent=8 )

    xmlWrite( fout, '/quark', indent=6 )
    xmlWrite( fout, '/action', indent=4 )
    xmlWrite( fout, '/physics', indent=2 )

    xmlWrite( fout, 'algorithm', indent=2 )
    xmlWrite( fout, 'name', quarkProf.algorithm,indent=4 )
    xmlWrite( fout, 'glossary', quarkTools.algorithmGlossary[quarkProf.algorithm], indent=4 )
    xmlWrite( fout, 'reference', quarkTools.algorithmReference[quarkProf.algorithm], indent=4 )
    xmlWrite( fout, 'exact', quarkTools.algorithmExactness[quarkProf.algorithm], indent=4 )
    xmlWrite( fout, 'reweightingNeeded', quarkTools.algorithmReweightingNeeded[quarkProf.algorithm], indent=4 )
    xmlWrite( fout, '/algorithm', indent=2 )
    xmlWrite( fout, '/markovChain' )

    fout.close()
