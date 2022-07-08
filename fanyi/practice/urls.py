from django.urls import path

from . import views

app_name = 'practice'
urlpatterns = [
    path('convo/<int:pk>/', views.ConvoView.as_view(), name='convo'),
    path('convo/first/', views.convo_first, name='convo_first'),
    path('convo/last/', views.convo_last, name='convo_last'),
    path('convo/random/', views.convo_random, name='convo_random'),
]
