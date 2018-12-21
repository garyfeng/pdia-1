# pdia, a Python library for Process Data in Assessment
Proncounced like wikipedia without wiki.

```
Gary Feng, Fred Yan
Princeton, NJ
```

----


`pdia` began in 2015 as a python library to process and analyze the process data (aka observables, or action 
logs) from the NAEP digitally-based assessments (DBAs). It provides functions to read the NAEP process data from a 
variety sources, pre-process and parse them to Pandas data frames, and visualize and report on the data.

----

# Installation

## Anaconda and virtual environments

We recommend the following setup in your system:

### Python 3.x

- TODO: [ to be added ]

## installation methods

`pdia` is a standard python library but not available on `pip`. You can install in several ways. Make sure you download the right branch of `pdia`. In most cases you should use `main` but for on-going projects you may need to load a special branch.

### Recommended: docker installation

- TODO: [add text about docker]

## Generating requirements.txt

To get the precise requirements for versions of libraries, etc. We use the `pipreqs`
[library](https://github.com/bndr/pipreqs). Assuming the path
to your local pdia git directory is `$path`

```bash
pip install pipreqs
pipreqs $path
```

This will (re)generate `$path/requirements.txt` file.

## Generating code-level documents with Sphinx

`pdia` uses docstrings and `Sphinx` for documentation. To (re)generate API documents from the source code, make sure you install sphinx following [this]( https://developer.ridgerun.com/wiki/index.php/How_to_generate_sphinx_documentation_for_python_code_running_in_an_embedded_system) or other instructions.

Then

```bash
conda install sphinx

cd $pdia_root$
sphinx-apidoc -o ./docs/source -f -e .
cd ./docs
make html
```  
----

# Data Sources, Data Processing, etc.

- TODO: [add text]

----

# Development

This library is maintained by Gary Feng (gary.feng@gmail.com). Because of the differences year-over-year, we likely will maintain different branches for each year of the data rather than keeping everything backward compatible, until we can stabilize the data structure for NAEP.
