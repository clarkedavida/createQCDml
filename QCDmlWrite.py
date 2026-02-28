#
# QCDmlWrite.py
#
# D. Clarke
#
# Methods for writing QCDml metadata files.
#


from QCDmlUtils import xmlWrite
import QCDmlGaugeAction as gluonTools
import QCDmlQuarkAction as quarkTools


def writeQCDmlConfigFile(p, dataLFN=None, markovChainURI=None):

    """ Use the profile p to generate the QCDml config file.  """

    fout=open(p.QCDmlConfigFileName,'w')

    # Set any missing, optional metadata to None.
    try:
        revisions=p.revisions
    except AttributeError:
        revisions=None
    try:
        reference=p.reference
    except AttributeError:
        reference=None
    try:
        revisionNumber=p.revisionNumber
    except AttributeError:
        revisionNumber=None
    try:
        parameterName=p.parameterName
    except AttributeError:
        parameterName=None
    try:
        parameterValue=p.parameterValue
    except AttributeError:
        parameterValue=None

    xmlWrite( fout,'?xml version="1.0" encoding="UTF-8" standalone="yes"?')
    xmlWrite( fout,'gaugeConfiguration xmlns="http://www.lqcd.org/ildg/QCDml/config2.0"')

    # dataLFN is now the first element in QCDml 2.0
    if dataLFN is None:
        xmlWrite( fout, 'dataLFN', p.dataLFN, indent=2 )
    else:
        xmlWrite( fout, 'dataLFN', dataLFN, indent=2 )

    xmlWrite( fout, 'management', indent=2 )
    if revisions is not None:
        xmlWrite( fout, 'revisions', revisions, indent=4 )
    if reference is not None:
        xmlWrite( fout, 'reference', reference, indent=4 )
    # NOTE: crcCheckSum moved to record element in QCDml 2.0
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
        # NOTE: comment element removed from managementActionType in QCDml 2.0
        xmlWrite( fout, '/archiveEvent', indent=6 )
    xmlWrite( fout, '/archiveHistory', indent=4 )
    xmlWrite( fout, '/management', indent=2 )

    xmlWrite( fout, 'implementation', indent=2 )
    xmlWrite( fout, 'machine', indent=4 )
    xmlWrite( fout, 'name', p.machineName, indent=6 )
    xmlWrite( fout, 'institution', p.machineInstitute, indent=6 )
    xmlWrite( fout, 'machineType', p.machineType, indent=6 )
    # NOTE: comment element removed from machine in QCDml 2.0
    xmlWrite( fout, '/machine', indent=4 )
    xmlWrite( fout, 'code', indent=4 )
    xmlWrite( fout, 'name', p.code, indent=6 )
    xmlWrite( fout, 'version', p.codeVersion, indent=6 )
    xmlWrite( fout, 'date', p.codeCompileDate, indent=6 )
    # NOTE: comment element removed from code in QCDml 2.0
    xmlWrite( fout, '/code', indent=4 )
    xmlWrite( fout, '/implementation', indent=2 )

    xmlWrite( fout, 'algorithm', indent=2 )
    xmlWrite( fout, 'parameters', indent=4 )
    if parameterName is not None:
        for i in range(len(parameterName)):
            xmlWrite( fout, 'parameter', indent=6 )
            fout.write('        <name>'+parameterName[i]+'</name>\n')
            fout.write('        <value>'+parameterValue[i]+'</value>\n')
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
    xmlWrite( fout, 'markovStep', indent=4 )
    xmlWrite( fout, 'update', p.update, indent=6 )
    xmlWrite( fout, 'record', indent=6 )
    xmlWrite( fout, 'field', p.field, indent=8 )
    xmlWrite( fout, 'crcCheckSum', p.checksum, indent=8 )
    xmlWrite( fout, 'avePlaquette', p.plaquette, indent=8 )
    xmlWrite( fout, '/record', indent=6 )
    xmlWrite( fout, '/markovStep', indent=4 )
    xmlWrite( fout, '/markovSequence', indent=2 )

    xmlWrite( fout, '/gaugeConfiguration' )
    fout.close()


# How to treat Nf=2+1? ( similar to wilsonTMquark: have one that is 2-flavor
#   and another one that is 1-flavor)

def writeQCDmlEnsembleFile(p, gluonProf, quarkProf):

    """ Use the profiles p, gluonProf, and quarkProf to generate the QCDml ensemble file.  """

    fout=open(p.QCDmlEnsembleFileName,'w')

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

    xmlWrite( fout, 'physics', indent=2 )
    xmlWrite( fout, 'size', indent=4 )
    for direction in p.size:
        xmlWrite( fout, direction, p.size[direction], indent=6 )
    xmlWrite( fout, '/size', indent=4 )

    xmlWrite( fout, 'action', indent=4 )

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

    # At the moment, this assumes all quarks have everything in common except m_f and Nf
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
