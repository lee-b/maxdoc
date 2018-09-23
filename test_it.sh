#!/bin/bash

cd examples
USER=Larry PYTHONPATH=.. ../env/bin/python ../bin/maxdoc --renderer=html "$@" index.mdoc out.html && cat out.html

#if which xdg-open > /dev/null; then
#    if [ "$DISPLAY" != "" ]; then
#        xdg-open &> /dev/null out.html
#    fi
#fi
