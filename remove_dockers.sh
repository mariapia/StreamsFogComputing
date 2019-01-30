#!/usr/bin/env bash

for i in $@
do
    sudo docker rm $i
done