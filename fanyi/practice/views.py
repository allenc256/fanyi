from django.shortcuts import redirect
from django.views import generic
from random import choice

from .models import Conversation, Sentence

class IndexView(generic.ListView):
    template_name = 'practice/index.html'
    model = Conversation
    paginate_by = 20

class ConvoView(generic.DetailView):
    template_name = 'practice/convo.html'
    model = Conversation
    context_object_name = 'convo'

def random(request):
    all_ids = Conversation.objects.values_list('pk', flat=True)
    random_id = choice(all_ids)
    return redirect(f'/practice/convo/{random_id}/')

# def convo(request, convo_id):
#     convo = get_object_or_404(Conversation, pk=convo_id)
#     return render(request, 'practice/convo.html', {'convo': convo})
