#! /bin/bash

sudo docker run -a stdout -a stdin --network host --name $1 -e TEXT=$2 -e N=$3 edge
