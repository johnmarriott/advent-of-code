#!/bin/zsh

# assume running in a year directory

if [[ $# == 0 ]] 
then
  day=$( date +%d )
else
  day=$1
fi

mkdir "day$day"
cd "day$day"
touch input.txt
touch sample.txt
echo "#!/usr/bin/env python" > 1.py
