from django.shortcuts import render
from django import forms

from . import util
from markdown2 import Markdown

class NewEntry(forms.Form):
    newentry = forms.CharField(label="A", max_length=50, widget=forms.TextInput(attrs={"placeholder":"Search Encyclopedia"}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, entryname):
    return render(request, "encyclopedia/entrypage.html", {
        "entrycontext": util.get_entry(entryname),
        "entry": entryname
    })

def search(request):
    if request.post == "post":
        return render(request, "encyclopedia/search_event.html", {})
    else:
        return render()