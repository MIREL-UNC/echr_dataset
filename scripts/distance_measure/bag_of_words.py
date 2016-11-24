"""Script to preprocess and classify documents with bag of words features."""

import argparse
import logging
logging.basicConfig(level=logging.INFO, filename='.log-bow')

import numpy
import utils


from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


def parse_arguments():
    """Returns the stdin arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--echr-dirpath', type=unicode,
                        help='Directory with the jl (replaced) files. Documents'
                        ' must be separated by a blank line.')
    parser.add_argument('--wiki-filepath', type=unicode,
                        help='File with the wikipedia documents. Each document'
                        ' is in a line of the file.')
    parser.add_argument('--output_filename', type=unicode,
                        help='File path to save the output')
    parser.add_argument('--save_tsne', action="store_true",
                        help='Save two dimension tsne vectors.')
    parser.add_argument('--lr', action="store_true",
                        help='Use logistic regression classifier')

    return parser.parse_args()


def main():
    """Main function of script."""
    args = parse_arguments()
    numpy.set_printoptions(suppress=True)

    x_matrix, y_vector = utils.read_datasets(args.echr_dirpath,
                                             args.wiki_filepath)

    features = [('word_count', CountVectorizer(max_features=10**5)),
                ('tfidf', TfidfTransformer())]
    feature_pipeline = Pipeline(features)
    transformed_matrix = feature_pipeline.fit_transform(x_matrix)
    del x_matrix

    if args.lr:
        classifier = LogisticRegression()
    else:
        classifier = SGDClassifier(loss='hinge', penalty='l2', alpha=1e-2,
                                   n_iter=5, random_state=42, n_jobs=-1)

    utils.evaluate(classifier, transformed_matrix, y_vector)

    if args.save_tsne:
        utils.save_tsne(transformed_matrix, y_vector, args.output_filename)


if __name__ == '__main__':
    main()

