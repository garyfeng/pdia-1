
Installation
============


Python Installation
-------------------

``pdia`` can be installed on ``python 3.6+``, using

    pip install https://github.com/NAEPDEV/pdia/archive/master.zip

Building Documentation
----------------------
Make sure you have Sphinx installed, using something like

    conda install sphinx

In a local git repo, using terminal:

    cd <root of your pdia repo>
    sphinx-apidoc -o ./docs/source -f -e .
    make html

This assumes you are using the ``docs/source/config.py`` and the ``./Makefile``. If not, you will
need to use the ``sphinx-quickstart`` command to get you started. See http://www.sphinx-doc.org/en/master/usage/installation.html

Process Data Overview
=====================

NAEP Process Data Formats
-------------------------

[To be added]

Data Access
-----------

[To be added]

Using pdia
==========

Data Import
-----------

See ``pdia.dataImport`` module

Data QC
-------

See ``pdia.qc`` module

Parsing ExtendedInfo
--------------------

See ``pdia.extendedInfoParser`` module

Response Reconstruction
-----------------------

See ``pdia.responseReconstruction`` module for functions to extract responses and to reconstruct responses from observable data

Utilities
---------

See ``pdia.utilis`` for utility functions

Feature Extraction and Analysis
===============================

Feature extraction is often specific to the analysis of interest, and therefore is currently not
included in the ``pdia`` library.