# 
# QCDmlQuarkAction.py                                                               
# 
# D. Clarke 
# 
# The ensemble metadata vary depending on the gauge action and quark action. Here
# we implement some quark-action-specific classes and methods. 
#

from QCDmlUtils import xmlWrite


class quarkAction:

    """ There are certain metadata that all quark actions have in common. Some actions are
        in some sense special cases of other actions, which lends itself well to a class
        structure. More specific actions will inherit from this quarkAction class. """

    def __init__(self, fout, quarkProf):
        self.fout      = fout
        self.quarkProf = quarkProf

    def writeLinkTreatment(self):
        pass


class HISQAction(quarkAction):

    """ Structures special to HISQ. """

    def writeLinkTreatment(self):
        xmlWrite( self.fout, 'LinkTreatment', indent=10 )
        xmlWrite( self.fout, 'fat7QuarkLinkTreatment', indent=12 )
        xmlWrite( self.fout, 'glossary', treatmentGlossary['fat7QuarkLinkTreatment'], indent=14 )
        for construct in self.quarkProf.fat7QuarkLinks:
            xmlWrite( self.fout, construct, self.quarkProf.fat7QuarkLinks[construct], indent=14 )
        xmlWrite( self.fout, '/fat7QuarkLinkTreatment', indent=12 )
        xmlWrite( self.fout, 'projectGroupLinkTreatment', indent=12 )
        xmlWrite( self.fout, 'glossary', treatmentGlossary['projectGroupLinkTreatment'], indent=14 )
        xmlWrite( self.fout, '/projectGroupLinkTreatment', indent=12 )
        xmlWrite( self.fout, 'asqTadQuarkLinkTreatment', indent=12 )
        xmlWrite( self.fout, 'glossary', treatmentGlossary['asqTadQuarkLinkTreatment'], indent=14 )
        for construct in self.quarkProf.asqTadQuarkLinks:
            xmlWrite( self.fout, construct, self.quarkProf.asqTadQuarkLinks[construct], indent=14 )
        xmlWrite( self.fout, '/asqTadQuarkLinkTreatment', indent=12 )
        xmlWrite( self.fout, '/LinkTreatment' ,indent=10 )


#
# Algorithm lookup tables.
#
algorithmGlossary  = { 'RHMC' : 'http://www.liv.ac.uk/~urbach/ildg/algorithmGlossaries/RHMC.pdf' }


algorithmReference = { 'RHMC' : 'Phys. Rev. Lett. 98 (2007) 051601' }


algorithmExactness = { 'RHMC' : 'true' }


algorithmReweightingNeeded = { 'RHMC' : 'false' }


#
# Link treatment glossary lookup table.
#
treatmentGlossary  = { 'fat7QuarkLinkTreatment'    : 'http://www.lqcd.org/ildg/actionGlossaries/fat7QuarkLinkTreatment.pdf',
                       'projectGroupLinkTreatment' : 'http://www.lqcd.org/ildg/actionGlossaries/projectGroupLinkTreatment.pdf',
                       'asqTadQuarkLinkTreatment'  : 'http://www.lqcd.org/ildg/actionGlossaries/asqTadQuarkLinkTreatment.pdf' }
