#
# QCDmlGaugeAction.py
#
# D. Clarke
#
# The ensemble metadata vary depending on the gauge action and quark action. Here
# we implement some gauge-action-specific classes and methods.
#
import xml.etree.ElementTree as ET


class gluonAction:

    """ There are certain metadata that all quark actions have in common. Some actions are
        in some sense special cases of other actions, which lends itself well to a class
        structure. More specific actions will inherit from this gluonAction class. """

    def __init__(self, gluonProf):
        self.gluonProf = gluonProf

    def writeImprovement(self, parent):
        pass


class treeSymanzikAction(gluonAction):

    """ Structures special to tree-level-improved action. """

    def writeImprovement(self, parent):
        ET.SubElement(parent, 'normalisation').text = str(self.gluonProf.normalization)
        for c in self.gluonProf.symanzikCoeffs:
            ET.SubElement(parent, c).text = str(self.gluonProf.symanzikCoeffs[c])

#
# The QCDml schema requires a 'glossary' entry. Here we store standard glossary entries, to
# keep the user from having to look it up.
#
glossaryDict = { 'treelevelSymanzikGluonAction' : 'http://www.lqcd.org/ildg/actionGlossaries/treelevelSymanzikGluonAction.pdf' }
