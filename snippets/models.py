from django.db import models
from django.contrib.auth.models import User

import json

MODELVERSION = '0.0.1'
import re

TAG_RE = re.compile(r'<[^>]+>')

def strip_html(text):
    return TAG_RE.sub('', text)


# Create your models here.
class Language(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    codemirror_mode = models.TextField(null=False, default='', blank=True)
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    color = models.CharField(max_length=30, null=False, blank=True,
                             default="#cccccc")
    def __str__(self):
        return self.name

class Snippet(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)    
    title = models.CharField(max_length=200, null=False, 
                             default='', blank=False)
    content = models.TextField(null=False, default='', blank=True)
    description = models.TextField(null=False, default='', blank=True)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL,
                                 null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True)
    history = models.TextField(default='[]', blank=True, editable=False)

    def get_history(self):
        return json.loads(self.history)

    def __str__(self):
        return self.title

    def search_text(self):
        tagtext = ' '.join([ tag.name for tag in self.tags.all() ])
        text = " ".join([ 
            self.title, 
            strip_html(self.description), 
            tagtext 
        ])
        return text

class Comment(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)  
    snippet = models.ForeignKey(Snippet, 
                                on_delete=models.CASCADE)  
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField(null=False, default='', blank=False)
