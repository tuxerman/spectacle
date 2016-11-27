# spectacle

Spectacle intends to permanently archive, and enable citizens quickly search over large volumes of publicly-released government documents.

Of particular interest (and original inspiration) are the thousands of documents released under the [Right to Information Act, 2005](https://en.wikipedia.org/wiki/Right_to_Information_Act,_2005).

Anyone can submit documents that they see fit to be included in the archive, while moderators review these submissions before publishing them. Once published, they are indexed by the search-backend and are served as results to anyone searching for relevant text.

Currently supports MySQL as a permanent datastore for document data, Amazon S3 as an archive for documents and ElasticSearch as the full-text-search subsystem.
