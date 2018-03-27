from django.forms.models import model_to_dict
from django.db import models
from datetime import datetime
import json
import lxml.html, lxml.html.clean 

def basic_serialize(obj):
    md = model_to_dict(obj)
    for key, val in md.items():
        if isinstance(val, datetime):
            md[key] = str(val)
        if isinstance(val, list):
            for i in range(len(val)):
                if isinstance(val[i], models.Model):
                    val[i] = str(val[i])
    md['model'] = obj.__class__.__name__
    return md

def json_basic_serialize(obj):
    return json.dumps( basic_serialize(obj) )
    
def clean_html(input_html):
    cleaner = lxml.html.clean.Cleaner()
    cleaner.javascript = True # remove js injections
    cleaner.style = True      # remove stylesheets
    cleaner.inline_style = False # allow inline styles
    cleaner.frames = True     # remove frames
    cleaner.embedded = True   # remove embedded content
    cleaner.safe_attrs_only = False # allow other kind of attributes for 
                                    # math and images and stuff.
    cleaner.remove_unknown_tags = False
    
    return lxml.html.tostring(
        cleaner.clean_html(
            lxml.html.fromstring(input_html)
        )
    ).decode("utf-8")

import re

TAG_RE = re.compile(r'<[^>]+>')

def html_to_clean_lowercase(text):
    # while removing tags, it will also remove spacing
    # this will add spaces (maybe a lot) between stuff
    # separated by html tags
    text = text.replace('<', ' <')
    text = lxml.html.tostring(
            lxml.html.fromstring(text),
            method='text', 
            encoding='unicode'
    )
    # collapse whitespaces and punctuation. Note that
    # it will leave only letters, digits and underscores
    rex = re.compile(r'\W+')
    text = rex.sub(' ', text).lower().strip()
    return text
    