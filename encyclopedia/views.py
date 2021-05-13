import re
from random import choice

from django.shortcuts import render, redirect
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect

from urllib.parse import urlencode

from . import util
from markdown2 import Markdown

markdowner = Markdown()

class FormInput(forms.Form):
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class":"form-control mt-1 mb-4", "id":"exampleFormControlInput1", "placeholder":"Enter the page title"}))
    content = forms.CharField(required=False, widget=forms.Textarea(attrs={"class":"form-control mt-1", "id":"exampleFormControlTextarea1", "rows":"8", "placeholder":"Enter the page content in word / using markdown syntax"}))

def index(request):
    if request.method == "GET":
        msg_alert = request.GET.get("value","")
        title_entry = request.GET.get("entry","")
    else:
        pass

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "newentry_added": msg_alert,
        "newentry": title_entry,
        "count": None,
        "encyclopedia": True
    })

def page(request, entryname):
    page = util.get_entry(entryname)
    if page is not None:
        entries = util.list_entries()
        for entry in entries:
            result = re.match(entryname.upper(), entry.upper())
            if result:
                final_entry = entry
                break
            else:
                pass

        return render(request, "encyclopedia/entrypage.html", {
            "header": markdowner.convert(f"# {final_entry}"),
            "entrycontext": markdowner.convert(re.sub(f"^# {final_entry}","", page)),
            "title": final_entry
            })

    else:
        return render(request, "encyclopedia/index.html", {
            "search_noresult": True,
            "entry": entryname
            })

def search(request):
    value = request.GET.get("search_input","")
    value_content = util.get_entry(value)
    if value_content is not None:
        entries = util.list_entries()
        for entry in entries:
            result = re.match(value.upper(), entry.upper())
            if result:
                final_entry = entry
                break
            else:
                pass

        return render(request, "encyclopedia/entrypage.html", {
            "header": markdowner.convert(f"# {final_entry}"),
            "entrycontext": markdowner.convert(re.sub(f"^# {final_entry}","", value_content)),
            "title": final_entry
            })

    elif value == "":
        return render(request, "encyclopedia/index.html", {
            "search_ntg": True,
            "search": True
            })
    else:
        update_entry = []
        entries = util.list_entries()
        modified_value = value.upper()
        for entry in entries:
            result = re.match(f'^{modified_value}', entry.upper())
            if result:
                update_entry.append(entry)
            else:
                pass
        
        return render(request, "encyclopedia/index.html", {
            "entries": update_entry,
            "search_result": True,
            "value": value,
            "count": len(update_entry),
            "search": True
            })
       
def newPage(request):
    if request.method == "POST":
        forms = FormInput(request.POST)
        if forms.is_valid():
            title = forms.cleaned_data["title"]
            content = forms.cleaned_data["content"]
            full_content = f"# {title}\n\n{content}"
            if util.get_entry(title) is None:
                util.save_entry(title, full_content)
                return HttpResponseRedirect(reverse("entrypage", kwargs={"entryname": title}))
            else:
                form = FormInput(initial={'title': title, 'content': content})
                return render(request, "encyclopedia/newpage.html", {
                    "form": form,
                    "entry_exist": True
                })     
        else:
            return render(request, "encyclopedia/newpage.html", {
            "form": FormInput(),
            "invalid": True
            })     

    else:
        return render(request, "encyclopedia/newpage.html", {
        "form": FormInput()
    })     

def editPage(request):
    if request.POST.get("edit","") == "True":
        title = request.POST.get("title","")
        content = util.get_entry(title)
        modified_content = re.sub(f"^# {title}(\n)*","", content)
        form = FormInput(initial={'title': title, 'content': modified_content})
        return render(request, "encyclopedia/editpage.html", {
            "form": form,
            "title": title
        })    
    else:
        original_title = request.POST.get("origin","")
        forms = FormInput(request.POST)
        if forms.is_valid():
            title = forms.cleaned_data["title"]
            content = forms.cleaned_data["content"]
            full_content = f"# {title}\n\n{content}"
            if util.get_entry(title) is None:
                util.save_entry(title, full_content)
                url = '{}?{}&entry={}'.format('/', 'value=True', title)
                return redirect(url)
            elif title.upper() == original_title.upper():
                util.save_entry(title, full_content)
                return HttpResponseRedirect(reverse("entrypage", kwargs={"entryname": title}))
            else:
                form = FormInput(initial={'title': title, 'content': content})
                return render(request, "encyclopedia/editpage.html", {
                    "form": form,
                    "title": original_title,
                    "entry_exist": True,
                    "edited_title": forms.cleaned_data["title"]
                })     
        else:
            return render(request, "encyclopedia/editpage.html", {
            "form": FormInput(),
            "invalid": True
            })     

def randomPage(request):
    randompage = choice(util.list_entries())
    return HttpResponseRedirect(reverse("entrypage", kwargs={"entryname": randompage}))

