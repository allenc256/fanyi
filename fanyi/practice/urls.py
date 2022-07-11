from django.urls import path

from . import views

app_name = 'practice'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('transcript/<int:transcript_pk>', views.TranscriptView.as_view(), name='transcript'),
    path('notes/<int:pk>', views.NotesView.as_view(), name='notes'),
]
