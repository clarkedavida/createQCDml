# 
# QCDmlGaugeAction.py                                                               
# 
# D. Clarke 
# 
# The ensemble metadata vary depending on the gauge action and quark action. Here
# we implement some gauge-action-specific classes and methods. 
#

from QCDmlUtils import xmlWrite


class gluonAction:

    """ There are certain metadata that all quark actions have in common. Some actions are
        in some sense special cases of other actions, which lends itself well to a class
        structure. More specific actions will inherit from this gluonAction class. """

    def __init__(self, fout, gluonProf):
        self.fout      = fout
        self.gluonProf = gluonProf

    def writeImprovement(self):
        pass


class treeSymanzikAction(gluonAction):

    """ Structures special to tree-level-improved action. """

    def writeImprovement(self):
        xmlWrite( self.fout, 'normalisation', self.gluonProf.normalization, indent=10 )
        for c in self.gluonProf.symanzikCoeffs:
            xmlWrite( self.fout, c, self.gluonProf.symanzikCoeffs[c], indent=10 )

#
# The QCDml schema often requires a 'glossary' entry. Here we store standard glossary entries, to
# keep the user from having to look it up.
#
glossaryDict = { 'treelevelSymanzikGluonAction' : 'http://www.lqcd.org/ildg/actionGlossaries/treelevelSymanzikGluonAction.pdf' }
