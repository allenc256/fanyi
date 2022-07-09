from django.urls import path

from . import views

app_name = 'practice'
urlpatterns = [
    path('convo/<int:pk>/', views.ConvoView.as_view(), name='convo'),
    path('convo/first/', views.convo_first, name='convo_first'),
    path('convo/last/', views.convo_last, name='convo_last'),
    path('convo/random/', views.convo_random, name='convo_random'),
    path('recent/', views.RecentView.as_view(), name='recent'),
    path('', views.IndexView.as_view(), name='index'),
    path('transcript/<int:transcript_pk>', views.TranscriptView.as_view(), name='transcript'),
]
