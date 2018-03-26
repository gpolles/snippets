from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Language)
admin.site.register(Tag)
admin.site.register(Snippet)
admin.site.register(Comment)