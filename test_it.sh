#!/bin/bash

cd examples
PYTHONPATH=.. ../env/bin/python ../bin/maxdoc --renderer=html_jinja2 index.mdoc out.html && cat out.html

if which xdg-open; then
    if [ "$DISPLAY" != "" ]; then
        xdg-open &> /dev/null out.html
    fi
fi
