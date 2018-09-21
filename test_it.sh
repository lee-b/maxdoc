#!/bin/bash

cd examples
PYTHONPATH=.. ../env/bin/python ../bin/maxdoc --output-format=html index.mdoc out.html

if [ "$DISPLAY" != "" ]; then
    xdg-open out.html
else
    cat out.html
fi
