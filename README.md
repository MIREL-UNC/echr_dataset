# European Court of Human Rights (ECHR) dataset

Crawler project in Python to download documents from the European Court of Human Rights site and extract clean text.

The base site we are querying is http://hudoc.echr.coe.int/eng


To run the crawler, execute the following commands:
```
$ cd document_crawler
$ scrapy crawl echr
```

Optionally, you can pass a limit argument that indicated the number of documents to download.
```
$ scrapy crawl echr -a limit=100
```
The default value is 10, with a minimum number of request per pages of 50.

Check the scrapy documentation to see other options like output redirection and format. We recommended the jsonline format, that handles correctly big
volumes of data:
```
$ scrapy crawl echr -a limit=100 -o output_path/output_file.jl
```
