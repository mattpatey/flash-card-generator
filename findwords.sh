#!/usr/bin/env bash

DICTIONARY=$1
WORDS_FILE=$2

for line in `cat $WORDS_FILE`; do
    echo "--- Searching for $line ---";
    grep -i "^$line" $DICTIONARY;
    if [ $? -ne 0 ]; then
        echo "No matches found";
    fi;
    echo "";
done
