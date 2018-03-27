from django_elasticsearch_dsl import DocType, Index, fields
from .models import Snippet
import xml.etree
from elasticsearch_dsl import analyzer

def strip_html(text):
    ''.join(xml.etree.ElementTree.fromstring(text).itertext())

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

        

        # Ignore auto updating of Elasticsearch when a model is saved
        # or deleted:
        # ignore_signals = True
        # Don't perform an index refresh after every update (overrides global setting):
        # auto_refresh = False
        # Paginate the django queryset used to populate the index with the specified size
        # (by default there is no pagination)
        # queryset_pagination = 5000
