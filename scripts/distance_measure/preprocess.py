"""Script to preprocess and classify documents."""

import argparse
import jsonlines
import logging
logging.basicConfig(level=logging.INFO, filename='.log-preprocess')
import numpy
import os
import re
import subprocess
import tqdm


from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.utils import shuffle


def parse_arguments():
    """Returns the stdin arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--echr-dirpath', type=unicode)
    parser.add_argument('--wiki-filepath', type=unicode)

    return parser.parse_args()


def get_document_number(filepath):
    """Returns the number of documents in filepath without opening it."""
    return int(subprocess.check_output(["wc", "-l", filepath]).split()[0])


def get_input_files(input_dirpath, pattern):
    """Returns the names of the files in input_dirpath that matches pattern."""
    all_files = os.listdir(input_dirpath)
    for filename in all_files:
        if re.match(pattern, filename) and os.path.isfile(os.path.join(
                input_dirpath, filename)):
            yield os.path.join(input_dirpath, filename)


def read_echr_documents(input_dirpath):
    """Returns a list of documents"""
    filepaths = get_input_files(input_dirpath, r'.*jl')
    result = []
    for filepath in filepaths:
        total_docs = get_document_number(filepath)
        with jsonlines.open(filepath) as reader:
            for document in tqdm.tqdm(reader, total=total_docs):
                result.append(' '.join(document['sentences']))
    return result


def read_wiki_documents(input_filepath):
    """Returns a list with the wikipedia documents."""
    total_docs = get_document_number(input_filepath)
    with open(input_filepath, 'r') as input_file:
        result = [line for line in tqdm.tqdm(
            input_file.readlines(), total=total_docs)]
    return result


def log_report(predictions, y_test):
    """Logs the classification_report and confusion matrix."""
    target_names = ['ECHR', 'Wikipedia']
    logging.info('Classification report')
    logging.info(classification_report(y_test, predictions, digits=3,
                                       target_names=target_names))
    logging.info('Confusion matrix')
    for row in confusion_matrix(y_test, predictions):
        logging.info('\t'.join([str(count) for count in row]))



def evaluate(pipeline, x_matrix, y_vector):
    """Trains and applies the pipeline to x_matrix, y_vector."""
    logging.info('Splitting dataset')
    x_train, x_test, y_train, y_test = train_test_split(
        x_matrix, y_vector, test_size=0.33)

    logging.info('Training classifier')
    pipeline.fit(x_train, y_train)

    logging.info('Getting predictions')
    predictions = pipeline.predict(x_test)
    log_report(predictions, y_test)


def main():
    """Main function of script."""
    args = parse_arguments()

    logging.info('Reading ECHR documents')
    echr_documents = read_echr_documents(args.echr_dirpath)  # ~1GB
    logging.info('Reading Wikipedia documents')
    wiki_documents = read_wiki_documents(args.wiki_filepath)  # ~1GB

    x_matrix = numpy.array(echr_documents + wiki_documents)
    y_vector = numpy.array(
        [0] * len(echr_documents) + [1] * len(wiki_documents))

    x_matrix, y_vector = numpy.shuffle(x_matrix, y_vector)

    pipeline = Pipeline([
        ('word_count', CountVectorizer(max_features=10**5)),
        ('tfidf', TfidfTransformer()),
        ('classifier', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-2,
                                  n_iter=5, random_state=42, n_jobs=-1))
    ])




if __name__ == '__main__':
    main()
