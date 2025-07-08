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
    content = forms.CharField(widget=forms.Textarea, label="New entry")


def _get_entries_with_lookup():
    """
    Helper function to get entries and create a case-insensitive lookup.
    Returns tuple of (original_entries, lowercase_lookup_dict)
    """
    entries = util.list_entries()
    # Create a lookup dict: lowercase_title -> original_title
    entries_lookup = {entry.lower(): entry for entry in entries}
    return entries, entries_lookup


def index(request):
    entries, _ = _get_entries_with_lookup()
    return render(
        request,
        "encyclopedia/index.html",
        {"entries": entries, "search_form": searchForm()},
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
    entries, entries_lookup = _get_entries_with_lookup()
    filtered_entries = []

    if request.method == "POST":
        s_form = searchForm(request.POST)
        if s_form.is_valid():
            search_term = s_form.cleaned_data["search"].lower()

            # Check for exact match (case-insensitive)
            if search_term in entries_lookup:
                # Redirect to the original case version
                return HttpResponseRedirect(
                    reverse("entry", args=[entries_lookup[search_term]])
                )

            # Filter entries that contain the search term
            filtered_entries = [
                entry for entry in entries if search_term in entry.lower()
            ]
        else:
            return render(request, "encyclopedia/index.html", {"search_form": s_form})
    else:
        s_form = searchForm()

    return render(
        request,
        "encyclopedia/search.html",
        {"entries": filtered_entries, "search_form": s_form},
    )


def new(request):
    entries, entries_lookup = _get_entries_with_lookup()

    if request.method == "POST":
        n_form = newEntryForm(request.POST)
        if n_form.is_valid():
            title = n_form.cleaned_data["title"]
            title_lower = title.lower()

            # Check if entry already exists (case-insensitive)
            if title_lower in entries_lookup:
                # Redirect to existing entry with original case
                # return HttpResponseRedirect(reverse("entry", args=[entries_lookup[title_lower]]))
                n_form.add_error("title", "An entry with this title already exists.")
                return render(
                    request,
                    "encyclopedia/new.html",
                    {"new_entry_form": n_form, "search_form": searchForm()},
                )
            else:
                content = n_form.cleaned_data["content"]
                util.save_entry(title, content)
                # Redirect to the new entry with the exact title provided
                return HttpResponseRedirect(reverse("entry", args=[title]))
    else:
        n_form = newEntryForm()

    return render(
        request,
        "encyclopedia/new.html",
        {"new_entry_form": n_form, "search_form": searchForm()},
    )
