from django.http import HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from django.urls import reverse
from django.db import transaction
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render

import operator
from functools import reduce

from .models import Transcript, Entry, Vocab
from .forms import EntryEditForm, EntryVocabForm

class IndexView(generic.list.ListView):
    template_name = 'practice/index.html'
    model = Transcript
    paginate_by = 20

    def get_queryset(self):
        return Transcript.objects.annotate(entry_count=Count('entry')) \
            .annotate(note_count=Count('entry', filter=Q(entry__notes__isnull=False) & ~Q(entry__notes=''))) \
            .annotate(vocab_count=Count('entry__vocab'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent'] = Transcript.objects.annotate(entry_count=Count('entry')) \
            .annotate(note_count=Count('entry', filter=Q(entry__notes__isnull=False) & ~Q(entry__notes=''))) \
            .annotate(vocab_count=Count('entry__vocab')) \
            .filter(last_viewed__isnull=False) \
            .order_by('-last_viewed')[:10]
        return context

class TranscriptView(generic.list.ListView):
    template_name = 'practice/transcript.html'
    model = Entry
    paginate_by = 20

    def get_queryset(self):
        qs = Entry.objects.filter(transcript=self.kwargs['transcript_pk'])

        if self._is_notes_only():
            qs = qs.filter(Q(notes__isnull=False) & ~Q(notes=''))

        min_difficulty = self._min_difficulty()
        if min_difficulty > 0:
            qs = qs.filter(Q(difficulty__gte=min_difficulty))
            
        return qs.prefetch_related('vocab_set') \
            .order_by('index') \
            .all() \
            .prefetch_related('translation_set')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        transcript = Transcript.objects.get(pk=self.kwargs['transcript_pk'])
        context['transcript'] = transcript
        context['transcript_next'] = Transcript.objects.only('pk') \
            .filter(pk__gt=self.kwargs['transcript_pk']) \
            .order_by('pk') \
            .first()
        context['transcript_prev'] = Transcript.objects.only('pk') \
            .filter(pk__lt=self.kwargs['transcript_pk']) \
            .order_by('-pk') \
            .first()

        context['notes_only'] = self._is_notes_only()
        context['notes_only_toggle'] = not context['notes_only']

        context['difficulties'] = Entry.Difficulty.choices
        context['min_difficulty'] = self._min_difficulty()

        context['last_viewed'] = transcript.last_viewed
        transcript.last_viewed = timezone.now()
        transcript.save()

        return context

    def _is_notes_only(self):
        return self.request.GET.get('notes_only', '').lower() in ('t', 'true')

    def _min_difficulty(self):
        return int(self.request.GET.get('min_difficulty', 0))

class UpdateVocabView(generic.edit.UpdateView):
    template_name = 'practice/vocab.html'
    model = Vocab
    fields = ['phrase', 'translation']

    def get_success_url(self):
        return self.request.GET.get('next', reverse('practice:index'))

class AddVocabView(generic.edit.UpdateView):
    model = Vocab
    fields = []

    @transaction.atomic
    def form_valid(self, form):
        entry = get_object_or_404(Entry, pk=self.kwargs['entry_pk'])
        vocab = get_object_or_404(Vocab, pk=self.kwargs['pk'])
        vocab.time_last_modified = timezone.now()
        vocab.entries.add(entry)
        vocab.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.request.GET.get('next', reverse('practice:index'))

class RemoveVocabView(generic.edit.UpdateView):
    model = Vocab
    fields = []

    def form_valid(self, form):
        entry = get_object_or_404(Entry, pk=self.kwargs['entry_pk'])
        vocab = get_object_or_404(Vocab, pk=self.kwargs['pk'])
        vocab.entries.remove(entry)
        vocab.save()

        # Garbage collect unattached entries.
        Vocab.objects.annotate(entry_count=Count('entries')).filter(entry_count=0).delete()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.request.GET.get('next', reverse('practice:index'))

class SearchVocabView(generic.list.ListView):
    template_name = 'practice/vocab/search.html'
    model = Vocab
    paginate_by = 20

    def get_queryset(self):
        qs = Vocab.objects.annotate(entry_count=Count('entries')) \
            .filter(~Q(entries__pk__exact=self.kwargs['entry_pk']))
        query = self.request.GET.get('query', None)
        if query:
            qs = qs.filter(Q(phrase__icontains=query) | Q(translation__icontains=query))
        return qs

def entry(request, entry_pk):
    if request.method == 'GET':
        return entry_GET(request, entry_pk)
    elif request.method == 'POST' and request.POST['form'] == 'edit_form':
        return entry_POST_edit(request, entry_pk)
    elif request.method == 'POST' and request.POST['form'] == 'vocab_form':
        return entry_POST_vocab(request, entry_pk)
    else:
        raise NotImplementedError()

def entry_GET(request, entry_pk):
    entry = get_object_or_404(Entry, pk=entry_pk)
    edit_form = EntryEditForm(instance=entry)
    vocab_form = EntryVocabForm(initial=request.GET)
    context = {'vocab_form': vocab_form, 'edit_form': edit_form, 'entry': entry}

    qs = Vocab.objects.annotate(entry_count=Count('entries')) \
        .filter(~Q(entries__pk__exact=entry.pk))
    phrase = request.GET.get('phrase', '')
    translation = request.GET.get('translation', '')
    filters = []
    if phrase:
        filters.append(Q(phrase__icontains=phrase))
    if translation:
        filters.append(Q(translation__icontains=translation))
    if filters:
        qs = qs.filter(reduce(operator.or_, filters))
    context['matches'] = qs[:20]

    return render(request, 'practice/entry.html', context)

def entry_POST_edit(request, entry_pk):
    entry = get_object_or_404(Entry, pk=entry_pk)
    vocab_form = EntryVocabForm()
    edit_form = EntryEditForm(request.POST, instance=entry)
    context = {'vocab_form': vocab_form, 'edit_form': edit_form, 'entry': entry}

    if edit_form.is_valid():
        edit_form.save()
        return HttpResponseRedirect(request.GET.get('next', reverse('practice:index')))

    return render(request, 'practice/entry.html', context)

def entry_POST_vocab(request, entry_pk):
    entry = get_object_or_404(Entry, pk=entry_pk)
    vocab_form = EntryVocabForm(request.POST)
    edit_form = EntryEditForm(instance=entry)
    context = {'vocab_form': vocab_form, 'edit_form': edit_form, 'entry': entry}

    if vocab_form.is_valid():
        entry.vocab_set.create(
            phrase=vocab_form.cleaned_data['phrase'],
            translation=vocab_form.cleaned_data['translation'])
        return HttpResponseRedirect(request.GET.get('next', reverse('practice:index')))

    return render(request, 'practice/entry.html', context)
