#! /bin/bash

sudo docker build --network host -f docker_cloud -t cloud .
sudo docker build --network host -f docker_fog -t fog .
sudo docker build --network host -f docker_edge -t edge .
