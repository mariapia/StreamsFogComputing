#!/usr/bin/env bash

gnome-terminal -x "python3 /home/mariapia/PycharmProject/FogComputing/main.py cloud-node"
gnome-terminal -x "python3 /home/mariapia/PycharmProject/FogComputing/main.py fog-node"
gnome-terminal -x "python3 /home/mariapia/PycharmProject/FogComputing/main.py text-generator /home/mariapia/PycharmProject/FogComputing/prova.txt --n 10"
gnome-terminal -x "python3 /home/mariapia/PycharmProject/FogComputing/main.py text-generator /home/mariapia/PycharmProject/FogComputing/text1.txt --n 10"