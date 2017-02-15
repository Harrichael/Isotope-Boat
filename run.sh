#!/bin/bash

# Place your compile and execute script here.
# You can write any bash script that will run on campus linux machines.
# The below script will compile and execute the example.cpp program.

# compile the program
g++ -W -Wall -pedantic-errors example.cpp -o example

# execute the program
./example 
