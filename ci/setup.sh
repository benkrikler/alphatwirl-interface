#!/usr/bin/env bash
export PYTHONPATH=$PWD:$PYTHONPATH
# get alphatwirl from master branch
pip install -U git+https://github.com/benkrikler/alphatwirl.git \
  flake8 pyyaml pandas

make install
