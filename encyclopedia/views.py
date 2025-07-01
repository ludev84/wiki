from django.shortcuts import render


import markdown2
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def entry(request, entry):
    entry_md = util.get_entry(entry)
    if entry_md:
        entry_md = markdown2.markdown(entry_md)
    return render(
        request,
        "encyclopedia/entry.html",
        {"entry": entry_md, "title": entry},
    )
