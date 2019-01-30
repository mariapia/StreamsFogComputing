#! /bin/bash

sudo docker run -a stdout -a stdin --network host --name $1 fog
