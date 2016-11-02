"""Script to preprocess and classify documents with word embedding features."""


import argparse
import gensim
import logging
logging.basicConfig(level=logging.INFO, filename='.log-bow')
import numpy

import utils

from nltk.tokenize import word_tokenize
from sklearn.linear_model import SGDClassifier
from tqdm import tqdm


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
    parser.add_argument('--gensim_save', action="store_true",
                        help='Indicates if the word vector model was saved as '
                        'a generic gensim model.')
    parser.add_argument('--model_filepath', type=unicode,
                        help='File path of the word vector model.')

    return parser.parse_args()


def get_document_vectors(x_matrix, w2v_model):
    """Transform the documents in x_matrix into an average of word vectors."""
    result = []
    for sentence in tqdm(x_matrix, total=x_matrix.shape[0]):
        vector = numpy.zeros((w2v_model.layer1_size,))
        words = word_tokenize(sentence)
        for word in words:
            vector += w2v_model[word]
        result.append(vector)
    return numpy.vstack(result)


def main():
    """Main function of script."""
    args = parse_arguments()
    numpy.set_printoptions(suppress=True)

    x_matrix, y_vector = utils.read_datasets(args.echr_dirpath,
                                             args.wiki_filepath)

    logging.info('Reading word vectors')
    if args.gensim_save:
        w2v_model = gensim.utils.SaveLoad.load(args.model_filepath)
    else:
        w2v_model = gensim.models.Word2Vec.load_word2vec_format(
            args.model_filepath, binary=True)

    logging.info('Transforming matrix')
    transformed_matrix = get_document_vectors(x_matrix, w2v_model)
    del x_matrix
    del w2v_model

    classifier = SGDClassifier(loss='hinge', penalty='l2', alpha=1e-2,
                               n_iter=5, random_state=42, n_jobs=-1)

    utils.evaluate(classifier, transformed_matrix, y_vector)

    if args.save_tsne:
        utils.save_tsne(transformed_matrix, y_vector, args.output_filename)


if __name__ == '__main__':
    main()
