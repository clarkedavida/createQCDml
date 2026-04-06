# QCDml Utils

To upload to ILDG, it is expected that you provide some metadata about
your configurations. There is a strict [QCDml schema](https://doi.org/10.1016/j.nuclphysbps.2004.11.116)
that should be followed, including a lot of information the user might not know, such as
the location of a "glossary". (One can also find more information about the ILDG specification
[here](https://gitlab.desy.de/ildg/hands-on/material/-/tree/main/howto?ref_type=heads).)
These tools are intended to be a lightweight framework to help you write Python
scripts to easily mark up xml files that comply with QCDml.

The general idea is that for an ensemble, you should create a corresponding
`ensemble profile`, and similarly configurations get `configuration profiles`.
These profiles implement metadata as Python variables. You can then either
put the metadata in by hand, use one of the `QCDmlUtils` scripts, or you
can use your own script, written in whatever language you prefer, which
you then call using the `QCDmlUtil` command `shell()`. Some example profiles
can be found in the `profiles` folder. Some example usage of `QCDmlUtil`
functions can be found in `exampleQCDmlUtilScript.py`.

WARNING: At the moment, only the HISQ
and tree-level Symanzik actions have example profiles. If ILDG wants to
use it, what is required is to extend the profiles in the `profiles` folder to
include other lattice actions. Correspondingly one might want to add
metadata-checking functions for those actions. Right now there is structure for
only some optional annotations. More may be added later.


## Getting set up

This is a collection of Python scripts to help make QCDml metadata files.
All you need is Python 3.9+. To get started, please run
```shell
./installQCDmlUtils.bash
```
To see whether everything worked, you can then try
```shell
./testQCDml.bash
```

## What can I do with these tools?

Start by filling out a skeleton. Some examples can be found in the `example` subfolder.
An excerpt from `example/confInfo.py` is:
```Python
QCDmlConfigFileName = "example_config.xml"
reference           = "myreference"
revisionNumber      = [0,1]
revisionAction      = ["generate","add"]
reviser             = ["Dr. Strangelove","Merkin Muffley"]
reviserInstitute    = ["Bielefeld University","Brookhaven National Laboratory"]
revisionDate        = ["2022-08-21T00:00:00+00:00",shell("hubert-mtime.pl")]
revisionComment     = "myrevision"
revisions           = len(revisionNumber)
```
These skeletons have a lot of nice features, namely:
1. You have an idea of what information is required from the variable names on the LHS.
2. You can leverage Python data structures and commands, like lists and `len`, and can
do on-the-fly math, such as setting `c7Link=1/384`, where the RHS will be converted to
float by Python.
3. You can use already existing code, or write code in a language of your choice if you don't 
care for Python, by wrapping in the `shell` command. In the above example, we use a Perl script
by H. Simma to compute the time.

Once you have filled out your skeletons, you can write a Python script to create, and if you like check,
the XML files. For instance:
```Python
# Some basic checks that the supplied data are reasonable.
checkConfigProfile( confInfo )
checkEnsembleProfile( ensmInfo )

URI = makeURI( ensmInfo ) # Also possible to call like: makeURI( collaboration, projectName, ensembleName )
LFN = makeLFN( ensmInfo.collaboration, ensmInfo.projectName, ensmInfo.ensembleName, confInfo.configurationName )

# Make the ensemble and configuration XML files.
writeQCDmlEnsembleFile( ensmInfo, gActInfo, qActInfo )
writeQCDmlConfigFile( confInfo, dataLFN=LFN, markovChainURI=URI )
```
That's it, you're done! The full example is in `exampleQCDmlUtilScript.py`.

## Explanation of file tree

- `example`: Contains examples how to use this code.
- `glossaries`: Some glossary PDFs from the old ILDG.
- `profile`: Contains some profiles specific to particular actions.
- `xml`: Contains QCDml2.0 schemata along with a small script for validation.
