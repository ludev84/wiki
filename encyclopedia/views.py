from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect


import markdown2
from . import util


class searchForm(forms.Form):
    search = forms.CharField(label="Search")


def index(request):
    return render(
        request,
        "encyclopedia/index.html",
        {"entries": util.list_entries(), "form": searchForm()},
    )


def entry(request, entry):
    entry_md = util.get_entry(entry)
    if entry_md:
        entry_md = markdown2.markdown(entry_md)
    return render(
        request,
        "encyclopedia/entry.html",
        {"entry": entry_md, "title": entry},
    )


def search(request):
    if request.method == "POST":
        form = searchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data["search"].lower()
            entries = list(map(lambda entry: entry.lower(), util.list_entries()))
            if search in entries:
                return HttpResponseRedirect(reverse("entry", args=[search]))
            entries_filtered = list(
                filter(lambda entry: search in entry.lower(), util.list_entries())
            )
            return render(
                request,
                "encyclopedia/search.html",
                {"entries": entries_filtered, "form": form},
            )
        else:
            return render(request, "index", {"form": form})
