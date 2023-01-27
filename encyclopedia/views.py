from django.shortcuts import render
from django.http import HttpResponse
from markdown2 import Markdown
from django import forms
from . import util
import random

mark_down = Markdown()
entries = util.list_entries()

class Edit(forms.Form):
    textarea= forms.CharField(widget=forms.Textarea(), label='')

class Post(forms.Form):
    title= forms.CharField(label="Title")
    textarea= forms.CharField(widget=forms.Textarea(), label='')

class Search(forms.Form):
    item = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'myfieldclass', 'placeholder': 'Search'
    }))

def index(request):
    searched_entry = []
    if request.method == "POST":
        this_form = Search(request.POST)
        if this_form.is_valid():
            this_item = this_form.cleaned_data["item"]
            for j in entries:
                if this_item in entries:
                    this_page = util.get_entry(this_item)
                    converted_page = mark_down.convert(this_page)

                    context = {
                        'content': converted_page,
                        'title': this_item,
                        'form': Search()
                    }
                    return render(request, "encyclopedia/entry.html", context)
                else:
                    context = {
                        'form': Search(),
                        'entries': entries,
                        'input': this_item
                    }
                    return render(request, "encyclopedia/error.html", context)

                if this_item.lower() in j.lower():
                    searched_entry.append(j)
                    context = {
                        'searched': searched_entry,
                        'form': Search()
                    }
            return render(request, "encyclopedia/search.html", context)
        else:
            return render(request, "encyclopedia/index.html", {"form": form})
    else:
        return render(request, "encyclopedia/index.html",{
            "entries": util.list_entries(), "form":Search()
        })

def create(request):
    if request.method == 'POST':
        this_form = Post(request.POST)
        if this_form.is_valid():
            title = this_form.cleaned_data["title"]
            this_textarea = form.cleaned_data["textarea"]
            if title in entries:
                return render(request, "encyclopedia/error.html",{
                    "form": Search(),
                    "message": "This page already exist!"
                })
            else:
                util.save_entry(title, this_textarea)
                this_page = util.get_entry(title)
                converted_page = mark_down.convert(this_page)

                context = {
                    'form': Search(),
                    'content': converted_page,
                    'title': title
                }
                return render(request, "encyclopedia/entry.html", context)
        else:
            return render(request, "encyclopedia/create.html",{
                "form": Search(),
                "post": Post()
            })
    else:
        return render(request, "encyclopedia/create.html",{
            "form": Search(),
            "post": Post()
        })

def random_page(request):
    if request.method == 'GET':
        num = random.randint(0, len(entries)- 1)
        page_random = entries[num]
        this_page = util.get_entry(page_random)
        converted_page = mark_down.convert(this_page)
        
        context = {
            'form': Search(),
            'title': page_random,
            'content': converted_page,
        }
        return render(request, "encyclopedia/entry.html", context)

def edit(request, title):
    if request.method == 'GET':
        this_page = util.get_entry(title)

        context = {
            'form': Search(),
            'edit': Edit(initial={'textarea': this_page}),
            'title': title
        }
        return render(request, "encyclopedia/edit.html", context)
    else:
        form = Edit(request.POST)
        if form.is_valid():
            this_textarea = form.cleaned_data["textarea"]
            util.save_entry(title, this_textarea)
            this_page = util.get_entry(title)
            converted_page = mark_down.convert(this_page)

            context = {
                'form': Search(),
                'title': title,
                'content': converted_page
            }
            return render(request, "encyclopedia/entry.html", context)

# https://github.com/trentm/python-markdown2
# https://stackoverflow.com/questions/62855513/using-markdown2-with-django
# https://stackoverflow.com/questions/66914241/how-do-i-get-user-input-from-search-bar-to-display-in-a-page-django
# https://stackoverflow.com/questions/15799328/django-typeerror-querydict-object-is-not-callable/15799415
# https://www.geeksforgeeks.org/render-html-forms-get-post-in-django/
# https://django.cowhite.com/blog/working-with-url-get-post-parameters-in-django/
# https://hakibenita.com/django-markdown
# https://docs.djangoproject.com/en/3.0/ref/urlresolvers/#reverse
# https://stackoverflow.com/questions/6011146/django-urls-regex-for-query-string
# https://docs.djangoproject.com/en/3.2/ref/request-response/
# https://adriennedomingus.medium.com/working-with-urls-in-python-django-81192e4115c9
# https://github.com/LeoZorzoli/Wiki/blob/master/encyclopedia/views.py

def wiki(request, title):
    if title in entries:
        this_title = util.get_entry(title)
        this_page = mark_down.convert(this_title)
        context = {
            'content': this_page, 
            'title': title,
            'form': Search()
        }
        return render(request, 'encyclopedia/entry.html', context)
    else:
        return render(request,'encyclopedia/error.html',{
            "message": "The requested page was not found. Try again.",
            "form": Search()
        }) #show error page