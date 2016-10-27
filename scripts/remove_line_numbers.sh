#!/bin/bash
# Removes the line numbers in paragraphs.
# The first argument is the name of the directory that contains the input files
[ $# -ge 1 ]
for filename in $1/*; do
    echo 'File ' $filename;
    echo -ne "\tReplacing numbers and dots at start of line. Matches: ";
    grep -o -P "^[0-9]+\.\s*" $filename | wc -l;
    sed -i -E "s/^[0-9]+\.\s*//g" $filename;
    grep -o -P "\"[0-9]+\.\s*" $filename | wc -l;
    sed -i -E "s/\"[0-9]+\.\s*/\"/g" $filename;

done;

