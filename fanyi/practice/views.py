from django.shortcuts import redirect
from django.views import generic
from django.utils import timezone
from random import choice

from .models import Conversation, Transcript, Entry

class ConvoView(generic.DetailView):
    template_name = 'practice/convo.html'
    model = Conversation
    context_object_name = 'convo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        convo = context['convo']

        next = Conversation.objects.only('pk').filter(pk__gt=convo.pk).order_by('pk').first()
        if next:
            context['next_convo_id'] = next.pk
        prev = Conversation.objects.only('pk').filter(pk__lt=convo.pk).order_by('-pk').first()
        if prev:
            context['prev_convo_id'] = prev.pk

        sents = sorted(convo.sentence_set.all(), key=lambda sent: sent.index)
        speaker_idxs = {}
        for sent in sents:
            if sent.speaker not in speaker_idxs:
                speaker_idxs[sent.speaker] = len(speaker_idxs)
            sent.speaker_idx = speaker_idxs[sent.speaker]
        context['sents'] = sents

        context['date_viewed'] = convo.date_viewed
        convo.date_viewed = timezone.now()
        convo.save()

        return context

class RecentView(generic.list.ListView):
    template_name = 'practice/recent.html'
    model = Conversation
    paginate_by = 20

    def get_queryset(self):
        return Conversation.objects.filter(date_viewed__isnull=False).order_by('-date_viewed').all()

def convo_random(request):
    all_ids = Conversation.objects.values_list('pk', flat=True)
    random_id = choice(all_ids)
    return redirect(f'/practice/convo/{random_id}/')

def convo_first(request):
    first = Conversation.objects.order_by('pk').first()
    return redirect(f'/practice/convo/{first.pk}/')

def convo_last(request):
    last = Conversation.objects.order_by('-pk').first()
    return redirect(f'/practice/convo/{last.pk}/')

class IndexView(generic.list.ListView):
    template_name = 'practice/index.html'
    model = Transcript
    paginate_by = 20

    def get_queryset(self):
        return Transcript.objects.filter(last_viewed__isnull=False).order_by('-last_viewed').all()

class TranscriptView(generic.list.ListView):
    template_name = 'practice/transcript.html'
    model = Entry
    paginate_by = 20

    def get_queryset(self):
        return Entry.objects.filter(transcript=self.kwargs['transcript_pk']).order_by('index').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transcript = Transcript.objects.get(pk=self.kwargs['transcript_pk'])
        context['transcript'] = transcript
        context['last_viewed'] = transcript.last_viewed
        transcript.last_viewed = timezone.now()
        transcript.save()
        return context

