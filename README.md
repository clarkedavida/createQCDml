# QCDml Utils

To upload to ILDG, it is expected that you provide some metadata about
your configurations. There is a strict [QCDml schema](https://doi.org/10.1016/j.nuclphysbps.2004.11.116)
that should be followed, including a lot of information the user might not know, such as
the location of a "glossary". The purpose of these tools is to allow you
to write your own Python scripts streamlining this process.

The general idea is that for an ensemble, you should create a corresponding
`ensemble profile`, and similarly configurations get `configuration profiles`.
These profiles implement metadata as Python variables. You can then either
put the metadata in by hand, use one of the `QCDmlUtils` scripts, or you
can use your own script, written in whatever language you prefer, which
you then call using the `QCDmlUtil` command `shell()`. Some example profiles
can be found in the `profiles` folder. Some example usage of `QCDmlUtil`
functions can be found in `exampleQCDmlUtilScript.py`.

Most of the core tools already exist in this code. At the moment, only the HISQ
and tree-level Symanzik actions have example profiles. If ILDG wants to
use it, what is required is to extend the profiles in the `profiles` folder to
include other lattice actions. Correspondingly one might want to add
metadata-checking functions for those actions.

## Getting set up

This is a collection of Python scripts to help make QCDml metadata files.
All you need is Python 3.5+. To get started, please run
```shell
./installQCDmlUtils.bash
```
To see whether everything worked, you can then try
```shell
./testQCDml.bash
```

## What can I do with these tools?

Start by filling out a profile. Some examples can be found in the `profiles` subfolder.
An excerpt from one is:
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
The profiles have a lot of nice features, namely:
1. You have an idea of what information is required from the variable names on the LHS.
2. You can leverage Python data structures and commands, like lists and `len`, and can
do on-the-fly math, such as setting `c7Link=1/384`, where the RHS will be converted to
float by Python.
3. You can use already existing code, or write code in a language of your choice if you don't 
care for Python, by wrapping in the `shell` command. In the above example, we use a Perl script
by H. Simma to compute the time.

Once you have filled out your profiles, you can write a Python script to create, and if you like check,
the XML files. For instance:
```Python
# Some basic checks that the supplied data are reasonable.
checkConfigProfile( confInfo )
checkEnsembleProfile( ensmInfo )

# Also possible to call like: makeConfURI( collaboration, projectName, ensembleName )
URI = makeConfURI( ensmInfo )
LFN = makeDataLFN( URI, confInfo.configurationName )

# Make the ensemble and configuration XML files.
writeQCDmlEnsembleFile( ensmInfo, gActInfo, qActInfo )
writeQCDmlConfigFile( confInfo, dataLFN=LFN, markovChainURI=URI )
```
That's it, you're done! The full example is in `exampleQCDmlUtilScript.py`.