# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import jsonlines
import logging


DEFAULT_OUTPUT_FILEPATH = 'output'
MAX_SENTENCES_PER_FILE = 10**6


class MultipleJsonLinePipeline(object):
    """Pipeline to save items in jsonline, with a limit of elements per file.
    """
    def __init__(self):
        # Number of sentences written in the current file
        self.current_sentences_count = 0
        self.current_file_number = 0
        self.item_counter = 0
        # Json line writer
        self.writer = None
        # Base path of the outout file. Each output file will be generated
        # appending the file number and the extension name '.jl' to this
        # attribute.
        self.base_output_filename = ''

    def _reopen_writer(self):
        """Opens a new writer. Closes old writer instance if open."""
        if self.writer:
            self.writer.close()
            self.current_file_number += 1
        output_filepath = '{}-{}.jl'.format(self.base_output_filename,
                                            self.current_file_number)
        self.writer = jsonlines.open(output_filepath, mode='w')

    def open_spider(self, spider):
        """Method called when the spider is opened. Opens output file."""
        self.base_output_filename = getattr(spider, 'output_path',
                                            DEFAULT_OUTPUT_FILEPATH)
        self._reopen_writer()

    def close_spider(self, _):
        """Method called when the spider is closed. Close open file."""
        self.writer.close()

    def process_item(self, item, _):
        """Saves each produced item."""
        self.item_counter += 1
        if not self.item_counter % 1000:
            logging.info('Processing document number {}'.format(
                self.item_counter))
        if len(item['sentences']) == 0:
            logging.info(u'No sentences in document {} {}'.format(
                item['name'], item['original_id']))
            return
        self.current_sentences_count += len(item['sentences'])
        self.writer.write(dict(item))
        if self.current_sentences_count > MAX_SENTENCES_PER_FILE:
            self.current_sentences_count = 0
            logging.info('Saving to new file ({})'.format(
                self.current_file_number))
            self._reopen_writer()
        return item
