#!/bin/sh
cd examples
PYTHONPATH=.. ../env/bin/python ../bin/maxdoc --output-format=html index.mdoc out.html && cat out.html
