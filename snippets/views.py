from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from haystack.query import SearchQuerySet
from django.core.paginator import Paginator, InvalidPage
from django.db.models import Count
from django.http import Http404
import traceback, time
import datetime
import json
from .models import *
from .forms import *
from .ajax import *
from .utils import basic_serialize, clean_html

def index(request):
    query_tags = request.GET.get('tags', '').split(',')
    try:
        query_tags = [int(x) for x in query_tags]
    except ValueError:
        query_tags = []
    selected = Snippet.objects.all()
    for q in query_tags:
        selected = selected.filter(tags__id=q)
    selected = selected.order_by('-date')
    p = request.GET.get('p', 1)
    paginator = Paginator(selected, 25) # Show 25 snippets per page
    try:
        page = paginator.get_page(p)
    except InvalidPage:
        return Http404('Not found')

    tags = Tag.objects.annotate(Count('snippet'))
    tags = tags.filter(snippet__count__gt=0)

    context = {
        'page': page,
        'query_tags': query_tags,
        'query_tags_string': ','.join([str(x) for x in query_tags]),
        'tags': tags.order_by('-snippet__count'),
    }
    return render(request, 'snippets/index.html', context)
# Create your views here.

@login_required(login_url='/snippets/accounts/login/')
def snippet_new(request):
    if request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            s = form.save(commit=False)
            s.author = request.user

            # clean description from weird stuff
            s.description = clean_html(s.description)

            # substitute \r\n with \n
            s.content = "\n".join(s.content.splitlines())
            
            # we need an ID to actually set relationships, save to get one
            s.save()
            
            # get the tags
            taglist = request.POST.get('tagslist').split(';')
            if taglist != ['']:
                tags = [int(i) for i in taglist]
            else:
                tags = []

            s.tags.set( Tag.objects.filter(id__in=tags) )
            
            # finally, set the first history item
            hitem = basic_serialize(s)
            hitem.update({
                'hist_modelversion': MODELVERSION, 
                'hist_action': 'created',
                'hist_timestamp': int(time.time()),
            })
            s.history = json.dumps( [ hitem ] )
            s.save()
            return ajax_confirm({'id': s.id})

    context = {
        'tags': Tag.objects.all(),
        'languages': Language.objects.all(),
        'form': SnippetForm(),
    }
    return render(request, 'snippets/forms/snippet_new.html', context)

def snippet_edit(request, uid):
    snippet = get_object_or_404(Snippet, pk=uid)
    history = json.loads(snippet.history)
    if request.method == 'POST':
        try:
            form = SnippetForm(request.POST, instance=snippet)
            if form.is_valid():
                s = form.save(commit=False)

                # clean description from weird stuff
                s.description = clean_html(s.description)

                # substitute \r\n with \n
                s.content = "\n".join(s.content.splitlines())
                
                # get the tags
                taglist = request.POST.get('tagslist').split(';')
                if taglist != ['']:
                    tags = [int(i) for i in taglist]
                else:
                    tags = []

                s.tags.set( Tag.objects.filter(id__in=tags) )
                
                # finally, set the first history item
                hitem = basic_serialize(s)
                hitem.update({
                    'hist_modelversion': MODELVERSION, 
                    'hist_action': 'edited',
                    'hist_timestamp': int(time.time()),
                    'username': request.user.username,
                })
                history.append(hitem)

                s.history = json.dumps( history )
                s.save()
                return ajax_confirm({'id': s.id})
        except:
            return ajax_error(traceback.format_exc())
            raise
    context = {
        'tags': Tag.objects.all(),
        'languages': Language.objects.all(),
        'form': SnippetForm(instance=snippet),
        'snippet': snippet,
    }
    return render(request, 'snippets/forms/snippet_edit.html', context)

def tags_get(request):
    return ajax_confirm({ 'tags': [ basic_serialize(t) for t in Tag.objects.all() ]})

@login_required(login_url='/snippets/accounts/login/')
def tags_add(request):
    if request.method == 'POST':
        try:
            curr_names = { t.name for t in Tag.objects.all() }
            added_tags = []
            for x in request.POST.getlist('names[]'):    
                if not isinstance(x, str):
                    raise ValueError()
                if x not in curr_names:
                    nt = Tag(name=x)
                    nt.save()
                    added_tags.append(nt)
            return ajax_confirm({ 
                'tags': [ basic_serialize(t) for t in added_tags ],
            })
        except:
            return ajax_error(traceback.format_exc());
    return ajax_error(traceback.format_exc());

def snippet_view(request, uid):
    snip = get_object_or_404(Snippet, pk=uid)
    context = {
        'snippet': snip,
    }
    return render(request, 'snippets/snippet_view.html', context)

@login_required(login_url='/snippets/accounts/login/')
def comment_add(request):
    if request.method == 'POST':
        try:
            snippet = Snippet.objects.get(pk=request.POST.get('snippet'))
            c = Comment(
                author=request.user, 
                snippet=snippet, 
                content=clean_html( request.POST.get('content') ) 
            )
            c.save()
            return ajax_confirm({ 
                'id': c.id,
                'author': c.author.username,
                'content': c.content,
                'date': str(c.date),
            })
        except:
            return ajax_error(traceback.format_exc());
    return ajax_error(traceback.format_exc());

@login_required(login_url='/snippets/accounts/login/')
def comment_delete(request, uid):
    if request.method == 'POST':
        try:
            c = Comment.objects.get(pk=uid, author=request.user)
            c.delete()
            return ajax_confirm({'uid': uid})
        except:
            return ajax_error(traceback.format_exc());
    return ajax_error(traceback.format_exc());

@login_required(login_url='/snippets/accounts/login/')
def comment_edit(request, uid):
    if request.method == 'POST':
        try:
            c = Comment.objects.get(pk=uid, author=request.user)
            c.content = clean_html( request.POST.get('content') )
            c.date = datetime.datetime.now()
            c.save()
            return ajax_confirm({ 
                'id': c.id,
                'author': c.author.username,
                'content': c.content,
                'date': str(c.date),
            })
        except:
            return ajax_error(traceback.format_exc());
    return ajax_error(traceback.format_exc());


def search_request(request):
    N = 20
    query = request.GET.get('q')
    p = request.GET.get('p', 0)
    res = SearchQuerySet().filter(content=query)
    n_pages = len(res) // N
    if len(res) % N != 0:
        n_pages += 1
    
    snippets = [ 
        basic_serialize( 
            Snippet.objects.get( pk=r.django_id )
        ) for r in res[ N * p : N * (p + 1) ] 
    ]
    return ajax_confirm({
        'query': q,
        'page': p,
        'results': snippets,
        'numpages': n_pages
    })

def search_result_view(request):

    query = request.GET.get('q')
    p = request.GET.get('p', 1)
    res = SearchQuerySet().filter(content=query)
    
    paginator = Paginator(res, 25) # Show 25 contacts per page
    try:
        page = paginator.get_page(p)
    except InvalidPage:
        return Http404('Not found')

    context = {
        'page': page,
        'query': query,
    }
    
    return render(request, 'snippets/search_results.html', context)