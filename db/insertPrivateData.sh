#!/bin/bash

for i in $(ls ./data/[0-9]*.sql); do ln -sf ../$i $(pwd)/sql/5_$(basename $i); done
