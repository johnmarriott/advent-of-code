#!/bin/zsh

# assume running in a year directory

if [[ $# == 0 ]] 
then
  day=$( date +%d )
else
  day=$( printf "%02d" $1 )
fi

mkdir "day$day"
cd "day$day"
touch input.txt
touch sample.txt
echo "#!/usr/bin/env python\n\nimport fileinput\n\nlines = [line.strip() for line in fileinput.input()]" > 1.py
