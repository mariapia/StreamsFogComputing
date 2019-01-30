#!/usr/bin/env bash

for i in $@
do
    sudo docker stop $i
done
