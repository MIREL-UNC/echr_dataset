"""Script to pass to CoNLL format documents downloaded using the crawler.

The output format is
    index \t word_token \t POS tag \t label
The index is the position of the word_token in the sentence. The label is 'O'
for words in the document, and 'O-DOC' for the document title.

Sentences are separated by blank lines.
"""

import argparse
import jsonlines
import nltk
import os
import re
import subprocess
import tqdm


def parse_arguments():
    """Returns the stdin arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-dirpath', type=unicode)
    parser.add_argument('-o', '--output-dirpath', type=unicode)

    return parser.parse_args()


def write_sentence(sentence, output_file, label):
    """Tokenizes the sentence and saves it with the given label."""
    words = nltk.tokenize.word_tokenize(sentence)
    for index, (word, tag) in enumerate(nltk.pos_tag(words)):
        line = u'{}\t{}\t{}\t{}\n'.format(index, word, tag, label)
        output_file.write(line.encode('utf-8'))
    output_file.write(u'\n')


def write_document(document, output_file):
    """Tokenizes and saves the document."""
    # Write the title
    write_sentence(document['title'], output_file, 'O-DOC')

    # Write the content
    for paragraph in document['sentences']:
        for sentence in nltk.tokenize.sent_tokenize(paragraph):
            write_sentence(sentence, output_file, 'O')


def get_document_number(filename):
    """Returns the number of documents in filename without opening it."""
    return int(subprocess.check_output(["wc", "-l", filename]).split()[0])


def get_input_files(input_dirpath, pattern):
    """Returns the names of the files in input_dirpath that matches pattern."""
    all_files = os.listdir(input_dirpath)
    for filename in all_files:
        if re.match(pattern, filename) and os.path.isfile(os.path.join(
                input_dirpath, filename)):
            yield os.path.join(input_dirpath, filename)


def main():
    """Main script function"""
    args = parse_arguments()
    filepaths = get_input_files(args.input_dirpath, r'.*jl')
    for filepath in filepaths:
        total_docs = get_document_number(filepath)
        filename = '{}.conll'.format(os.path.basename(filepath).split('.jl')[0].encode('utf-8'))
        output_filename = os.path.join(args.output_dirpath, filename.decode('utf8'))
        with open(output_filename, 'w') as output_file:
            with jsonlines.open(filepath) as reader:
                for document in tqdm.tqdm(reader, total=total_docs):
                    write_document(document, output_file)


if __name__ == '__main__':
    main()
