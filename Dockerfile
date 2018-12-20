# Dockerfile v1.03.01
# Last updated 12-20-18 by Jason Xie
#
# The base image can be found here. This version features the last use of python 3.6
# http://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html
FROM jupyter/base-notebook:9e8682c9ea54

RUN pip install -U pip Cython

# Without switching users, there are some permissions problems
USER root

# Copy necessary files from this directory into temporary folder
# Use the .dockerignore file to designate exceptions
COPY . ./src/

# Move into the temporary folder for installation
WORKDIR ./src

# Install necessary libraries to successfully install pdia requirements
RUN apt-get update && apt-get install -y --no-install-recommends\
    python3-dev \
    unixodbc-dev \
    freetds-dev \
    libopenblas-dev \
    git \
    g++ && \
    rm -rf /var/lib/apt/lists/*

# Momentarily switch to the normal user to install requirements from PyPi
USER $NB_USER
RUN pip install git+https://github.com/pymssql/pymssql.git && \
    pip install -r requirements.txt
USER root

# Run setup and install punkt module as described in Wiki
# Clean up unnecessary files
RUN python setup.py install && \
    conda install -c conda-forge pyarrow && \
    conda clean -tipsy
# Exit and delete temporary folder
WORKDIR ..
RUN rm -d -r src/

# Return to normal user 'jovyan'
USER $NB_USER
