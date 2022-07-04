from django.contrib import admin

from .models import Conversation, Sentence

admin.site.register(Conversation)
admin.site.register(Sentence)
