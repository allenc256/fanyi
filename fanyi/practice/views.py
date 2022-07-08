from django.shortcuts import redirect
from django.views import generic
from random import choice

from .models import Conversation

class ConvoView(generic.DetailView):
    template_name = 'practice/convo.html'
    model = Conversation
    context_object_name = 'convo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        next = Conversation.objects.only('pk').filter(pk__gt=context['convo'].pk).order_by('pk').first()
        if next:
            context['next_convo_id'] = next.pk
        prev = Conversation.objects.only('pk').filter(pk__lt=context['convo'].pk).order_by('-pk').first()
        if prev:
            context['prev_convo_id'] = prev.pk
        return context

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
