#!/usr/bin/env bash

from humain.constants import *

## iterate through each file whose name ends in 'jpg'
## $1 is the input file - Send the directory
## $2 is the output location - again directory
## $3 is the accepted file that should be deleted from here

cp -r $1 $2
xargs rm < $3