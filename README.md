# European Court of Human Rights (ECHR) dataset

Crawler project in Python to download documents from the European Court of Human Rights site and extract clean text and metadata.

The base site we are querying is http://hudoc.echr.coe.int/eng. Only document
in English will be downloaded.


To run the crawler, execute the following commands:
```
$ cd document_crawler
$ scrapy crawl echr
```

## Output format
The files are extracted by default in jsonlines format. See the **Set output path** section for details about how and where these files are stored. Each document is represented as a json entry with the following fields:

 - name: The name present on the link that opens the document.
 - doctype
 - sentences: A list with the paragraphs of the file in order, as they were separated in the original page. To reconstruct the file, join the sentences using new lines.
 - original_id: The id assigned to the document by the webpage.
 - language: ISO code for the document language. So far, only ENG.
 - conclusion
 - originatingbody
 - application
 - title: Scraped title of the document.


## Extract raw text only
The json files can be converted to a list of documents with the following command:
```
$ jq -r '.sentences | .+ ["***DOCUMENT END***"] | .[]' output_file.jl
```
where the string `***DOCUMENT END***` will be added at the end of each document.

## Limit number of documents
Optionally, you can pass a limit argument that indicated the number of documents to download.
```
$ scrapy crawl echr -a limit=100
```
The default value is 10, with a minimum number of request per pages of 50.

## Set output path
The scraper has a pipeline to save the output in jsonline format into multiple files overly large files. The default limit is 1M document paragraphs in a single output file. This option is active by default, to set the name of the directory to store the files use the option `output_path`:
```
$ scrapy crawl echr -a limit=100 -a output_path='your_directory/file_prefix'
```
The output will be stored in files: `your_directory/file_prefix-N.jl`, where N is the file number starting from 0.

This output process can be deactivated. In the `ITEM_PIPELINES` settings, remove `document_crawler.pipelines.MultipleJsonLinePipeline`.

Check the scrapy documentation to see other options like output redirection and format. We recommended the jsonline format, that handles correctly big volumes of data:
```
$ scrapy crawl echr -a limit=100 -o output_path/output_file.jl
```

To change the number of sentences stored in each file, edit the constant `MAX_SENTENCES_PER_FILE` in the `pipeline.py` file.


## Postprocess
To prepare the documents to be input to a NLP system, we provide some scripts. For example, to extract pos tags and transform the sentences to a tsv format run:
```
$ scripts/to_conll.py --input_filepath="original_file.jl" --output_filepath="output_file.conll"
```


## Rquirements

The NLTK library requires the dowload of tokenizer package. In iptyhon console run:

```
>>> import nltk
>>> nltk.download('averaged_perceptron_tagger')
>>> nltk.dowload('punkt')
```

See `requirements.txt` for general python requirements.
