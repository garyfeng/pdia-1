#!/bin/bash

cd "${0%/*}"

# Select the repository version. To be updated if new branches are made available.
read -p "Which version of pdia would you like to use? (1=master, 2=2018xval, 3=py3, 0=test) " -n 1 -r
if [[ $REPLY =~ ^[1]$ ]]
then
  export PDJTAG=master
elif [[ $REPLY =~ ^[2]$ ]]
then
  export PDJTAG=2018xval
elif [[ $REPLY =~ ^[3]$ ]]
then
  export PDJTAG=py3
elif [[ $REPLY =~ ^[0]$ ]]
then
  export PDJTAG=test
fi

# Find a number to use to designate the container, in case multiple are running.
NUM=1
while [ $(docker ps -q -f name=pdj-$NUM | wc -l) -gt 0 ]
do
  NUM=$(expr 1 + $NUM)
done

# Ensure that the latest version is being used
# This will fail if you do not have access to pdia/docked-jupyter as a collaborator
docker pull pdia/docked-jupyter:$PDJTAG

# Run the container mounted into the current working directory
docker run -p $(expr 8887 + $NUM):8888 -h CONTAINER \
    -d -it --rm --name pdj-$NUM-$PDJTAG \
    --mount type=bind,source="$(pwd)",target="/home/jovyan/work" \
    pdia/docked-jupyter:$PDJTAG jupyter notebook --NotebookApp.token='pdia'

# Give it 5 seconds before opening localhost
# If it still does not work, it most likely just needs to refresh
echo "Now running; please wait"
sleep 5

open http://localhost:$(expr 8887 + $NUM)/?token=pdia

# Press any key to stop the container, which is automatically removed
read -n1 -r -p "Press any key to clean up..." key
docker stop pdj-$NUM-$PDJTAG
