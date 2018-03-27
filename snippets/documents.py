from django_elasticsearch_dsl import DocType, Index, fields
from .models import Snippet
import xml.etree
from elasticsearch_dsl import analyzer


# Name of the Elasticsearch index
index = Index('snippets')
# See Elasticsearch Indices API reference for available settings
index.settings(
    number_of_shards=1,
    number_of_replicas=0
)

#use a edge ngram
ngram = analyzer('ngram',
    tokenizer="ngram", 
    filter=["lowercase"],
    min_gram=3,
    max_gram=10,
    token_chars=['letter', 'digit']
)

@index.doc_type
class SnippetDocument(DocType):
    text = fields.TextField(attr='search_text', 
                            analyzer=ngram)      

    class Meta:
        model = Snippet # The model associated with this DocType

# This setting should be more conservative, when searching for Snippets.
# {
#   "index": {
#     "index": "my_idx",
#     "type": "my_type",
#     "analysis": {
#       "index_analyzer": {
#         "my_index_analyzer": {
#           "type": "custom",
#           "tokenizer": "standard",
#           "filter": [
#             "lowercase",
#             "mynGram"
#           ]
#         }
#       },
#       "search_analyzer": {
#         "my_search_analyzer": {
#           "type": "custom",
#           "tokenizer": "standard",
#           "filter": [
#             "standard",
#             "lowercase",
#             "mynGram"
#           ]
#         }
#       },
#       "filter": {
#         "mynGram": {
#           "type": "nGram",
#           "min_gram": 2,
#           "max_gram": 50
#         }
#       }
#     }
#   }
# }