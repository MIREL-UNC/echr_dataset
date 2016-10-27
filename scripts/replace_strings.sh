#!/bin/bash
# Makes various replacements to the files to reduce vocabulary size.
# The first argument is the name of the directory that contains the input files
# with extension .txt
[ $# -ge 1 ]
for filename in $1/*.txt; do
    echo 'File ' $filename;
    echo -ne "\tReplacing numbers and dots at start of line. Matches: ";
    grep -o -P "^[0-9]+\.\s*" $filename | wc -l;
    sed -i -E "s/^[0-9]+\.\s*//g" $filename;

    # Replacing Article references like Article 47 for ARTICLE_REF
    echo -ne "\tReplacing article references. Matches: ";
    grep -o -P "Article(s*)(\s[0-9]+(\,|\sand|-|\s§)?)+" $filename | wc -l;
    sed -i -E "s/Article(s*)(\s[0-9]+(\,|\sand|-|\s§)?)+/ARTICLE_REF/g" $filename

    # Replacing section references like § 58 for SECTION_REF
    echo -ne "\tReplacing section references. Matches: ";
    grep -o -P "§(§)? [0-9]+((\sand\s|\sor\s|-)[0-9]+)*" $filename | wc -l;
    sed -i -E "s/§(§)? [0-9]+((\sand\s|\sor\s|-)[0-9]+)*/SECTION_REF/g" $filename

    # Replacing money expressions like EUR 250,633.25 for MONEY_EXP
    echo -ne "\tReplacing money references. Matches: ";
    matches=$(grep -o -P "(EUR|€|£|RUB|LTL|TRL|CZK)(\s)*([0-9]+,)*[0-9]+\.*[0-9]+" $filename | wc -l);
    echo -ne $matches " + ";
    grep -o -P "([0-9]+,)*[0-9]+\.*[0-9]+(\seuros|\sroubles|\sTurkish liras|\skorunas)(\s\(EUR\)|\s\(RUB\)|\s\(TRL\)|\s\(TRY\)|\s\(CZK\))?" $filename | wc -l;
    sed -i -E "s/(EUR|€|£|RUB|LTL|TRL|CZK|HUF)(\s)*([0-9]+,)*[0-9]+\.*[0-9]+/MONEY_EXP/g" $filename
    sed -i -E "s/([0-9]+,)*[0-9]+\.*[0-9]+(\seuros|\sroubles|\sTurkish liras|\skorunas)(\s\(EUR\)|\s\(RUB\)|\s\(TRL\)|\s\(TRY\)|\s\(CZK\))?/MONEY_EXP/g" $filename

    # Replacing case references like no. 58985/04 for CASE_REF
    echo -ne "\tReplacing case references. Matches: ";
    grep -o -P "no(s)?. ([0-9]+/[0-9]+((\s)*\,\s|\sand\s|\.\s|\s)*)+" $filename | wc -l;
    sed -i -E "s/no(s)?. ([0-9]+\/[0-9]+((\s)*\,\s|\sand\s|\.\s|\s)*)+/CASE_REF /g" $filename

    echo -ne "\tReplacing paragraph references. Matches: ";
    grep -o -P "paragraph(s*) [0-9]+-*[0-9]*((-|\sand\s)[0-9]+-*[0-9]*)*" $filename | wc -l;
    sed -i -E "s/paragraph(s*) [0-9]+-*[0-9]*((-|\sand\s)[0-9]+-*[0-9]*)*/PARAGRAPH_REF /g" $filename

done;

