"""Script to pass to CoNLL format a document downloaded using the crawler.

The output format is
    index \t word_token \t POS tag \t label
The index is the position of the word_token in the sentence. The label is 'O'
for words in the document, and 'O-DOC' for the document title.

Sentences are separated by blank lines.
"""

import argparse
import jsonlines
import nltk
import subprocess
import tqdm


def parse_arguments():
    """Returns the stdin arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-filepath', type=unicode)
    parser.add_argument('-o', '--output-filepath', type=unicode)

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


def main():
    """Main script function"""
    args = parse_arguments()

    total_docs = get_document_number(args.input_filepath)

    with open(args.output_filepath, 'w') as output_file:
        with jsonlines.open(args.input_filepath) as reader:
            for document in tqdm.tqdm(reader, total=total_docs):
                write_document(document, output_file)


if __name__ == '__main__':
    main()
