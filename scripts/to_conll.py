"""Script to pass to CoNLL format a document downloaded using the crawler.

The output format is
word_token \t POS tag

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
    parser.add_argument('-i', '--input_filepath', type=unicode)
    parser.add_argument('-o', '--output_filepath', type=unicode)

    return parser.parse_args()


def write_document(document, output_file):
    """Tokenizes and saves the document."""
    for paragraph in document['sentences']:
        for sentence in nltk.tokenize.sent_tokenize(paragraph):
            words = nltk.tokenize.word_tokenize(sentence)
            for word, tag in nltk.pos_tag(words):
                output_file.write(
                    (u'{}\t{}\n'.format(word, tag)).encode('utf-8'))
            output_file.write(u'\n')


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
