#!/bin/zsh

# assume running in either:
# - aoc root directory, named advent-of-code (will cd to current year)
# - aoc/year directory

if [[ $(basename $(pwd)) == "advent-of-code" ]]
then
  cd "year$(date +%Y)"
fi

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
cp ../../.template.py 1.py
