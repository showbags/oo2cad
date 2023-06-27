#!/bin/bash

dimen=$(xdpyinfo | grep dimensions | sed -r 's/^[^0-9]*([0-9]+x[0-9]+).*$/\1/')

IFS='x'

#Read the split words into an array based on space delimiter
read -a xy <<< "$dimen"

w="${xy[0]}"
h="${xy[1]}"
w2=$(echo "$w/2" | bc)
blender --window-geometry $w2 0 $w2 $h -P oo2cad.py
