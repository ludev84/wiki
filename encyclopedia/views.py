from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect


import markdown2
from . import util


class searchForm(forms.Form):
    search = forms.CharField(label="Search")


class newEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    new_entry = forms.CharField(widget=forms.Textarea, label="New entry")


def index(request):
    return render(
        request,
        "encyclopedia/index.html",
        {"entries": util.list_entries(), "search_form": searchForm()},
    )


def entry(request, entry):
    entry_md = util.get_entry(entry)
    if entry_md:
        entry_md = markdown2.markdown(entry_md)
    return render(
        request,
        "encyclopedia/entry.html",
        {"entry": entry_md, "title": entry, "search_form": searchForm()},
    )


def search(request):
    entries = []
    if request.method == "POST":
        s_form = searchForm(request.POST)
        if s_form.is_valid():
            search = s_form.cleaned_data["search"].lower()
            entries = list(map(lambda entry: entry.lower(), util.list_entries()))
            if search in entries:
                return HttpResponseRedirect(reverse("entry", args=[search]))
            entries = list(
                filter(lambda entry: search in entry.lower(), util.list_entries())
            )
        else:
            return render(request, "index", {"search_form": s_form})
    else:
        s_form = searchForm(request.POST)
    return render(
        request,
        "encyclopedia/search.html",
        {"entries": entries, "search_form": s_form},
    )


def new(request):
    if request.method == "POST":
        n_form = newEntryForm(request.POST)

    else:
        n_form = newEntryForm()
    return render(
        request,
        "encyclopedia/new.html",
        {"new_entry_form": n_form, "search_form": searchForm()},
    )
