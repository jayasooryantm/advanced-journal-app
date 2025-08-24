from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import JournalEntry
from .forms import JournalEntryForm
from journal_app.apps.qdrant_integration.client import upsert_entry, search_entries, delete_entry


def entry_list(request):
    entries = JournalEntry.objects.all()
    return render(request, 'entries/entry_list.html', {'entries': entries})


def entry_detail(request, pk):
    entry = get_object_or_404(JournalEntry, pk=pk)
    return render(request, 'entries/entry_detail.html', {'entry': entry})


def entry_create(request):
    if request.method == "POST":
        form = JournalEntryForm(request.POST)
        if form.is_valid():
            entry = form.save()
            upsert_entry(entry.id, entry.content)  # Add to Qdrant
            return redirect('entry_list')
    else:
        form = JournalEntryForm()
    return render(request, 'entries/entry_form.html', {'form': form})


def entry_update(request, pk):
    entry = get_object_or_404(JournalEntry, pk=pk)
    if request.method == "POST":
        form = JournalEntryForm(request.POST, instance=entry)
        if form.is_valid():
            entry = form.save()
            upsert_entry(entry.id, entry.content)  # Update in Qdrant
            return redirect('entry_detail', pk=entry.pk)
    else:
        form = JournalEntryForm(instance=entry)
    return render(request, 'entries/entry_form.html', {'form': form})


def entry_delete(request, pk):
    entry = get_object_or_404(JournalEntry, pk=pk)
    if request.method == "POST":
        entry_id = entry.id
        entry.delete()
        delete_entry(entry_id)
        return redirect('entry_list')
    return render(request, 'entries/entry_confirm_delete.html', {'entry': entry})


def entry_search(request):
    query = request.GET.get("query", "")
    results = []
    if query:
        qdrant_results = search_entries(query)
        entry_ids = [r.payload["entry_id"] for r in qdrant_results]
        results = JournalEntry.objects.filter(id__in=entry_ids)
    # Return JSON for AJAX
    return JsonResponse({
        "results": [
            {
                "id": entry.id,
                "title": entry.title,
                "content": entry.content,
                "created_at": entry.created_at.strftime("%b %d, %Y %H:%M"),
            }
            for entry in results
        ]
    })
