# pdia, a Python library for NAEP Process Data
Proncounced like wikipedia without wiki.

----

The `pdia` (*P*rocess *D*ata *i*n *A*ssessment) library began in 2015 as an internal tool at Educational Testing Service (ETS) to transform and analyze process data (aka observables or action logs) from the NAEP digitally-based assessments (DBAs). It provides functions to read the NAEP process data from a variety sources, convert and parse them to Pandas data frames, and visualize and report on the data. As the NAEP process data becoming more accessible to the educatinal researchers, the development of `pdia` is now to this public GitHub repository, under the MIT license. 

Our goal is to offer the research community an official, standardized, and high-quality tool -- the same codebase supporting operational NAEP assessments -- to jumpstart their investigations. The public release focuses on the most time-consuming and error-prone aspects of working with NAEP process data, namely parsing the process data logs to extract and transform feature values. This is challenging not only for 3rd-party researchers but also for the operational program, as the NAEP assessment and data structure evolve from one year to the next. We sometimes have to create and maintain different code branches for different years' data.  

Most data scientists will use `pdia` in a Jupyter notebook environment, for which we provide a `Dockerfile` that standardizes a python3 environment with Jupyter and all the necessary libraries. The library is also used in production, where for example, we used AWS Lambda functions with `pdia` to process a year's worth of NAEP operational data. This dual-focus on research flexibility and production scalability drives many design decisions of `pdia`, which may not always be intuitive at the outset. 

----

# Installation

`pdia` can be used in several ways:
- Docker: this is how we use `pdia` in our data science team; **recommended**
- python installation via setup.py or pip install
- AWS Lambda

### Recommended: docker installation

We provide the "official" `Dockerfile` that defines the standardized development environment we use in our NAEP operational work. This is based on the official Jupyter docker container with `pdia` and other frequently used statistical, ML, and plotting libraries pre-installed. 

Here are three ways you can build/use the `pdia` docker:
- You can build the docker container from the `Dockerfile` following the standard `docker build` steps. 
- Or you can pull the pre-built docker image from https://cloud.docker.com/u/naep/repository/docker/naep/pdia
- To make it even easier for users, we provided shell (or Windows .bat) scripts for different operating systems under the `docker` folder. Double-click the appropriate script for your OS, you will be prompted to choose among a few different `pdia` environments in the terminal. Make a choice (**always choose `py3`**), and a Jupyter notebook will automatically start in your default browser on your computer. The Jupyter notebook server runs off the docker container you chose; if this is the first time you launch the docker image, it will be automatically pulled down. 

### Standard python install

Because `pdia` is a standard python library, you don't need docker to install it on your computer. You can do this in two ways.

- download the source from this Github repository, then do `python setup.py install`. 
- run something like `pip install --user git+https://github.com/NAEPDEV/pdia.git@2019-math` to directly install a particular branch from Github. This method works inside a Jupyter Notebook if you add `!` before the shell command.

Either way, you want to make sure you have activated the right python environment before you install. We recommend using `conda` to manage your virtualenv. You want to use a python3 for this.

### AWS Lambda

- TODO: [add text]

----
# Data Sources, Data Processing, etc.

- the 2019 NAEP Data Mining 2019 Competition (https://sites.google.com/view/dataminingcompetition2019/home)
- TODO: additional data releases and data sources

----

# Development

This library is maintained by the NAEP Process Data team at ETS, under MIT license. Please fork, report issues, and do pull requests.

## GitPod support

The current repository supports in-browser editing, testing, and PR using `GitPod`. This can be done through the following URL http://gitpod.io/#https://github.com/NAEPDEV/pdia. This will launch a docker (see `.\Dockerfile-gitpod`) with `pdia` and other required libraries installed for gitpod. 

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
cd $pdia_root$
sphinx-apidoc -o ./docs/source -f -e .
cd ./docs
make html
```  
----

 Contact: Gary Feng (gary.feng@gmail.com). 
