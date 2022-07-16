from django.views import generic
from django.utils import timezone
from django.urls import reverse
from django.db.models import Count, Q

from .models import Transcript, Entry

class IndexView(generic.list.ListView):
    template_name = 'practice/index.html'
    model = Transcript
    paginate_by = 20

    def get_queryset(self):
        return Transcript.objects.annotate(entry_count=Count('entry')) \
            .annotate(note_count=Count('entry', filter=Q(entry__notes__isnull=False) & ~Q(entry__notes='')))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent'] = Transcript.objects.annotate(entry_count=Count('entry')) \
            .annotate(note_count=Count('entry', filter=Q(entry__notes__isnull=False) & ~Q(entry__notes=''))) \
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
        return qs.order_by('index') \
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
        context['last_viewed'] = transcript.last_viewed
        transcript.last_viewed = timezone.now()
        transcript.save()
        return context

    def _is_notes_only(self):
        return self.request.GET.get('notes_only', '').lower() in ('t', 'true')


class NotesView(generic.edit.UpdateView):
    template_name = 'practice/notes.html'
    model = Entry
    fields = ['notes', 'difficulty']

    def get_success_url(self):
        return self.request.GET.get('next', reverse('practice:index'))
