from django.urls import path

from . import views

app_name = 'practice'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('convo/<int:pk>/', views.ConvoView.as_view(), name='convo'),
    path('random/', views.random, name='random'),
]
