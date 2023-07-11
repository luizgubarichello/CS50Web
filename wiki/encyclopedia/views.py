from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
import random
from markdown2 import Markdown

from . import util


markdowner = Markdown()


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "s_id": 0
    })


def random_entry(request):
    return redirect("entry", entry=random.choice(util.list_entries()))


def entry(request, entry):
    entry_content = util.get_entry(entry)
    if entry_content != None:
        entry_content = markdowner.convert(entry_content)
    return render(request, "encyclopedia/entry.html", {
        "entry": entry,
        "entry_content": entry_content
    })


def edit_page(request, entry):
    if request.method=="POST":
        np = request.POST

        if not np["edit_body"]:
            return render(request, "encyclopedia/edit.html", {
                "msg": "All fields are required."
            })

        util.save_entry(entry, np["edit_body"])

        return redirect("entry", entry=entry)

    return render(request, "encyclopedia/edit.html", {
        "entry": entry,
        "entry_content": util.get_entry(entry)
    })


def new_page(request):
    if request.method=="POST":
        np = request.POST

        if not np["entry_title"] or not np["entry_body"]:
            return render(request, "encyclopedia/new_page.html", {
                "msg": "All fields are required."
            })

        if np["entry_title"] in util.list_entries():
            return render(request, "encyclopedia/new_page.html", {
                "msg": "The submitted title already exists!"
            })

        util.save_entry(np["entry_title"], np["entry_body"])

        return redirect("index")

    return render(request, "encyclopedia/new_page.html", {
        "msg": ""
    })


def search(request):
    query = request.GET.get("q", "")
    entries = util.list_entries()
    total_entries = len(entries)

    if query in entries:
        return redirect("entry", entry=query)

    for entry in reversed(entries):
        if str(query).lower() not in str(entry).lower():
            entries.remove(entry)

    s_id = 0
    if len(entries) != total_entries:
        s_id = 1

    return render(request, "encyclopedia/index.html", {
        "entries": entries,
        "s_id": s_id
    })
