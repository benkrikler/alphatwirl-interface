#!/usr/bin/env bash
export PYTHONPATH=$PWD:$PYTHONPATH
# get alphatwirl from master branch
pip install -U git+https://github.com/alphatwirl/alphatwirl.git \
  flake8

make install
