#!/bin/bash

#clean_codes.bash

awk "NR > 1 && NF!=0" < postal_codes > postal_codes_clean.txt