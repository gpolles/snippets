from haystack import indexes
from .models import Snippet


class SnippetIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    title = indexes.EdgeNgramField(model_attr='title')
    tags = indexes.NgramField()

    #content_auto = indexes.EdgeNgramField(use_template=True)

    def prepare_tags(self, obj):
        return ' '.join([ tag.name for tag in obj.tags.all() ])

    def get_model(self):
        return Snippet

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()