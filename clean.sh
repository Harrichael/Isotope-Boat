#!/bin/bash

# Remove pyc files
cd game
rm *.pyc
cd util
rm *.pyc
cd ../..

# Remove solutions
cd solutions
rm solution*.txt
cd ..
