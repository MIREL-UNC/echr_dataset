"""Common functions for distance measure."""

import jsonlines
import logging
logging.basicConfig(level=logging.INFO, filename='.log-bow')
import numpy
import os
import pickle
import re
import subprocess
import tqdm

from nltk.tokenize import sent_tokenize
from sklearn.manifold import TSNE
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

MAX_TSNE_SAMPLE = 1000


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
                result.extend(document['sentences'])
    return result


def read_wiki_documents(input_filepath):
    """Returns a list with the wikipedia documents."""
    total_docs = get_document_number(input_filepath)
    result = []
    with open(input_filepath, 'r') as input_file:
        for line in tqdm.tqdm(input_file.readlines(), total=total_docs):
            result.extend(sent_tokenize(line.decode('utf-8')))
    return result


def read_datasets(echr_dirpath, wiki_filepath):
    logging.info('Reading ECHR documents')
    echr_documents = read_echr_documents(echr_dirpath)  # ~1GB
    logging.info('Reading Wikipedia documents')
    wiki_documents = read_wiki_documents(wiki_filepath)  # ~1GB
    x_matrix = numpy.array(echr_documents + wiki_documents, dtype=unicode)
    y_vector = numpy.array(
        [0] * len(echr_documents) + [1] * len(wiki_documents))

    return shuffle(x_matrix, y_vector)



def log_report(predictions, y_test):
    """Logs the classification_report and confusion matrix."""
    target_names = ['ECHR', 'Wikipedia']
    logging.info('Classification report')
    logging.info(classification_report(y_test, predictions, digits=3,
                                       target_names=target_names))
    logging.info('Confusion matrix')
    for row in confusion_matrix(y_test, predictions):
        logging.info('\t'.join([str(count) for count in row]))


def evaluate(classifier, x_matrix, y_vector):
    """Trains and applies the classifier to x_matrix, y_vector."""
    logging.info('Splitting dataset')
    x_train, x_test, y_train, y_test = train_test_split(
        x_matrix, y_vector, test_size=0.33)

    logging.info('Training classifier')
    classifier.fit(x_train, y_train)

    logging.info('Train performance')
    predictions = classifier.predict(x_train)
    log_report(predictions, y_train)

    logging.info('Test performance')
    predictions = classifier.predict(x_test)
    log_report(predictions, y_test)


def save_tsne(x_matrix, y_vector, output_filename):
    """Transforms x_matrix in 2D with tsne and saves it in output_filename."""
    logging.info('Calculating t-sne vectors.')
    tsne_model = TSNE(n_components=2)
    if x_matrix.shape[0] > MAX_TSNE_SAMPLE:
        vectors = x_matrix[:MAX_TSNE_SAMPLE]
        labels = y_vector[:MAX_TSNE_SAMPLE]
    else:
        vectors = x_matrix
        labels = y_vector
    if hasattr(vectors, 'toarray'):
        vectors = vectors.toarray()
    vectors = tsne_model.fit_transform(vectors)

    logging.info('Saving t-sne vectors')
    with open(output_filename, 'w') as output_file:
        output = {'vectors': vectors, 'labels': labels}
        pickle.dump(output, output_file)
