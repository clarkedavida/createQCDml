#
# QCDmlWrite.py
#
# D. Clarke
#
# Methods for writing QCDml metadata files. Requires Python 3.9+.
#
import xml.etree.ElementTree as ET
from QCDmlUtils import getConfigOptional, getEnsOptional
import QCDmlGaugeAction as gluonTools
import QCDmlQuarkAction as quarkTools


def _sub(parent, tag, text=None):
    """ Create a SubElement, optionally setting its text content. """
    el = ET.SubElement(parent, tag)
    if text is not None:
        el.text = str(text)
    return el


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

    opt            = getConfigOptional(p)
    revisions      = opt['revisions']
    parameterName  = opt['parameterName']
    parameterValue = opt['parameterValue']
    revisionNumber = opt['revisionNumber']
    reference      = opt['reference']

    root = ET.Element('gaugeConfiguration')
    root.set('xmlns', 'http://www.lqcd.org/ildg/QCDml/config2.0')

    _sub(root, 'dataLFN', p.dataLFN if dataLFN is None else dataLFN)

    mgmt = _sub(root, 'management')
    if revisions is not None:
        _sub(mgmt, 'revisions', revisions)
    if reference is not None:
        _sub(mgmt, 'reference', reference)
    history = _sub(mgmt, 'archiveHistory')
    for i in range(len(p.revisionAction)):
        event = _sub(history, 'archiveEvent')
        if revisionNumber is not None:
            _sub(event, 'revision', revisionNumber[i])
        _sub(event, 'revisionAction', p.revisionAction[i])
        participant = _sub(event, 'participant')
        _sub(participant, 'name', p.reviser[i])
        _sub(participant, 'institution', p.reviserInstitute[i])
        _sub(event, 'date', p.revisionDate[i])

    impl = _sub(root, 'implementation')
    machine = _sub(impl, 'machine')
    _sub(machine, 'name', p.machineName)
    _sub(machine, 'institution', p.machineInstitute)
    _sub(machine, 'machineType', p.machineType)
    code = _sub(impl, 'code')
    try:
        _sub(code, 'annotation', p.codeComment)
    except AttributeError:
        pass
    _sub(code, 'name', p.code)
    _sub(code, 'version', p.codeVersion)
    _sub(code, 'date', p.codeCompileDate)

    algo = _sub(root, 'algorithm')
    params = _sub(algo, 'parameters')
    if parameterName is not None:
        for i in range(len(parameterName)):
            param = _sub(params, 'parameter')
            _sub(param, 'name', parameterName[i])
            _sub(param, 'value', parameterValue[i])

    _sub(root, 'precision', p.precision)

    markov_seq = _sub(root, 'markovSequence')
    _sub(markov_seq, 'markovChainURI', p.markovChainURI if markovChainURI is None else markovChainURI)
    _sub(markov_seq, 'series', p.series)

    if isinstance(p.update, str):
        step = _sub(markov_seq, 'markovStep')
        try:
            _sub(step, 'annotation', p.confComment)
        except AttributeError:
            pass
        _sub(step, 'update', p.update)
        record = _sub(step, 'record')
        _sub(record, 'field', p.field)
        _sub(record, 'crcCheckSum', p.checksum)
        _sub(record, 'avePlaquette', p.plaquette)
    elif isinstance(p.update, list):
        for i in range(len(p.update)):
            step = _sub(markov_seq, 'markovStep')
            try:
                _sub(step, 'annotation', p.confComment[i])
            except AttributeError:
                pass
            _sub(step, 'update', p.update[i])
            record = _sub(step, 'record')
            _sub(record, 'field', p.field)
            _sub(record, 'crcCheckSum', p.checksum[i])
            _sub(record, 'avePlaquette', p.plaquette[i])

    tree = ET.ElementTree(root)
    ET.indent(tree)
    tree.write(p.QCDmlConfigFileName, encoding='UTF-8', xml_declaration=True)


def writeQCDmlEnsembleFile(p, gluonProf, quarkProf):
    """
    Use profiles p, gluonProf, and quarkProf to create the QCDml file for the ensemble.

    Args:
        p (.py or class): profile
        gluonProf (.py or class): profile for gluon action. Can use one from profiles directory
        quarkProf (.py or class): profile for quark action. Can use one from profiles directory
    """

    opt      = getEnsOptional(p)
    orcid    = opt['orcid']
    funders  = opt['funders']
    awards   = opt['awards']
    awardNos = opt['awardNos']

    root = ET.Element('markovChain')
    root.set('xmlns', 'http://www.lqcd.org/ildg/QCDml/ensemble2.0')
    _sub(root, 'markovChainURI', p.markovChainURI)

    mgmt = _sub(root, 'management')
    _sub(mgmt, 'collaboration', p.collaboration)
    _sub(mgmt, 'projectName', p.projectName)
    history = _sub(mgmt, 'archiveHistory')
    event = _sub(history, 'archiveEvent')
    _sub(event, 'revisionAction', 'add')
    participant = _sub(event, 'participant')
    if orcid is not None:
        _sub(participant, 'orcid', orcid)
    _sub(participant, 'name', p.name)
    _sub(participant, 'institution', p.institution)
    _sub(event, 'date', p.date)

    license_el = _sub(root, 'license')
    _sub(license_el, 'licenseURI', p.license)

    if funders is not None:
        funding = _sub(root, 'fundingReferences')
        for i in range(len(funders)):
            ref = _sub(funding, 'fundingReference')
            _sub(ref, 'funderName', funders[i])
            if awards[i] is not None:
                _sub(ref, 'awardTitle', awards[i])
            if awardNos[i] is not None:
                _sub(ref, 'awardNumber', awardNos[i])

    physics = _sub(root, 'physics')
    size_el = _sub(physics, 'size')
    for direction in p.size:
        _sub(size_el, direction, p.size[direction])

    action_el = _sub(physics, 'action')

    #--- Gluon action
    gluon_el      = _sub(action_el, 'gluon')
    gluon_type_el = _sub(gluon_el, gluonProf.actionType)
    _sub(gluon_type_el, 'glossary', gluonTools.glossaryDict[gluonProf.actionType])
    gluon_field = _sub(gluon_type_el, 'gluonField')
    _sub(gluon_field, 'gaugeGroup', gluonProf.gaugeGroup)
    _sub(gluon_field, 'representation', gluonProf.gaugeRepresentation)
    bc_el = _sub(gluon_field, 'boundaryCondition')
    for direction, bc in gluonProf.gaugeBCs.items():
        _sub(bc_el, direction, bc)
    _sub(gluon_type_el, 'beta', p.couplings["beta"])

    if gluonProf.actionType == 'treelevelSymanzikGluonAction':
        gluonMD = gluonTools.treeSymanzikAction(gluonProf)
    else:
        gluonMD = gluonTools.gluonAction(gluonProf)
    gluonMD.writeImprovement(gluon_type_el)

    #--- Quark action
    quark_el = _sub(action_el, 'quark')
    if quarkProf.actionType == 'hisqQuarkAction':
        quarkMD = quarkTools.HISQAction(quarkProf)
    else:
        quarkMD = quarkTools.quarkAction(quarkProf)

    for f in p.quarks:
        m_f           = "m" + f
        quark_type_el = _sub(quark_el, quarkProf.actionType)
        _sub(quark_type_el, 'glossary', quarkProf.glossary)
        quark_field = _sub(quark_type_el, 'quarkField')
        _sub(quark_field, 'normalisation', quarkProf.quarkNormalization)
        bc_el = _sub(quark_field, 'boundaryCondition')
        for direction, bc in quarkProf.quarkBCs.items():
            _sub(bc_el, direction, bc)
        _sub(quark_type_el, 'numberOfFlavours', p.Nf[f])
        _sub(quark_type_el, 'mass', p.couplings[m_f])
        quarkMD.writeLinkTreatment(quark_type_el)

    algo = _sub(root, 'algorithm')
    _sub(algo, 'name', quarkProf.algorithm)
    _sub(algo, 'glossary', quarkTools.algorithmGlossary[quarkProf.algorithm])
    _sub(algo, 'reference', quarkTools.algorithmReference[quarkProf.algorithm])
    _sub(algo, 'exact', quarkTools.algorithmExactness[quarkProf.algorithm])
    _sub(algo, 'reweightingNeeded', quarkTools.algorithmReweightingNeeded[quarkProf.algorithm])

    tree = ET.ElementTree(root)
    ET.indent(tree)
    tree.write(p.QCDmlEnsembleFileName, encoding='UTF-8', xml_declaration=True)
