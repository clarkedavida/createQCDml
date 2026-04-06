#
# QCDmlQuarkAction.py
#
# D. Clarke
#
# The ensemble metadata vary depending on the gauge action and quark action. Here
# we implement some quark-action-specific classes and methods.
#
import xml.etree.ElementTree as ET


class quarkAction:

    """ There are certain metadata that all quark actions have in common. Some actions are
        in some sense special cases of other actions, which lends itself well to a class
        structure. More specific actions will inherit from this quarkAction class. """

    def __init__(self, quarkProf):
        self.quarkProf = quarkProf

    def writeLinkTreatment(self, parent):
        pass


class HISQAction(quarkAction):

    """ Structures special to HISQ. """

    def writeLinkTreatment(self, parent):
        link = ET.SubElement(parent, 'LinkTreatment')

        fat7 = ET.SubElement(link, 'fat7QuarkLinkTreatment')
        ET.SubElement(fat7, 'glossary').text = treatmentGlossary['fat7QuarkLinkTreatment']
        for construct in self.quarkProf.fat7QuarkLinks:
            ET.SubElement(fat7, construct).text = str(self.quarkProf.fat7QuarkLinks[construct])

        proj = ET.SubElement(link, 'projectGroupLinkTreatment')
        ET.SubElement(proj, 'glossary').text = treatmentGlossary['projectGroupLinkTreatment']

        asq = ET.SubElement(link, 'asqTadQuarkLinkTreatment')
        ET.SubElement(asq, 'glossary').text = treatmentGlossary['asqTadQuarkLinkTreatment']
        for construct in self.quarkProf.asqTadQuarkLinks:
            ET.SubElement(asq, construct).text = str(self.quarkProf.asqTadQuarkLinks[construct])


#
# Algorithm lookup tables.
#
algorithmGlossary          = { 'RHMC' : 'https://latticeqcd.github.io/SIMULATeQCD/03_applications/rhmc.html' }
algorithmReference         = { 'RHMC' : 'Phys. Rev. Lett. 98 (2007) 051601' }
algorithmExactness         = { 'RHMC' : 'true' }
algorithmReweightingNeeded = { 'RHMC' : 'false' }

#
# Link treatment glossary lookup table.
#
treatmentGlossary = { 'fat7QuarkLinkTreatment'    : 'http://www.lqcd.org/ildg/actionGlossaries/fat7QuarkLinkTreatment.pdf',
                      'projectGroupLinkTreatment' : 'http://www.lqcd.org/ildg/actionGlossaries/projectGroupLinkTreatment.pdf',
                      'asqTadQuarkLinkTreatment'  : 'http://www.lqcd.org/ildg/actionGlossaries/asqTadQuarkLinkTreatment.pdf' }
