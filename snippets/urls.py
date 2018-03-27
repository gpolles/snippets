from django.urls import path
from django.conf.urls import url, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^snippet/new/$', views.snippet_new, name='snippet_add'),
    url(r'^snippet/edit/(?P<uid>[0-9]+)/$', views.snippet_edit, name='snippet_edit'),
    url(r'^view/(?P<uid>[0-9]+)/$', views.snippet_view, name='snippet_view'),
    url(r'^tags/all/$', views.tags_get, name='tags_get'),
    url(r'^tags/add/$', views.tags_add, name='tags_add'),
    url(r'^comments/add/$', views.comment_add, name='comment_add'),
    url(r'^comments/delete/(?P<uid>[0-9]+)/$', views.comment_delete, 
        name='comment_delete'),
    url(r'^comments/edit/(?P<uid>[0-9]+)/$', views.comment_edit, 
        name='comment_edit'),
    url(r'^search_results/$', views.search_result_view, name='search'),
#    url(r'^search/', include('haystack.urls')),
]
