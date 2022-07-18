from django.urls import path

from . import views

app_name = 'practice'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('transcript/<int:transcript_pk>', views.TranscriptView.as_view(), name='transcript'),
    path('entry/<int:entry_pk>', views.entry, name='entry'),
    path('entry/<int:entry_pk>/vocab/<int:pk>/add', views.AddVocabView.as_view(), name='vocab_add'),
    path('entry/<int:entry_pk>/vocab/<int:pk>/remove', views.RemoveVocabView.as_view(), name='vocab_remove'),
    path('vocab/<int:pk>', views.UpdateVocabView.as_view(), name='vocab_edit'),
]
