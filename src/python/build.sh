#!/bin/bash
# vim: set et fenc=utf-8 ff=unix sts=0 sw=2 ts=2 :
if [ -f *.deb ]; then
  rm *.deb
fi
if [ -f *.rpm ]; then
  rm *.rpm
fi
fpm -s python -t deb setup.py
fpm -s python -t rpm setup.py
