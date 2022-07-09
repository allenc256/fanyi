from django.contrib import admin

from .models import Conversation, Sentence
from .models import Transcript, Entry

class SentenceInline(admin.StackedInline):
    model = Sentence

class ConversationAdmin(admin.ModelAdmin):
    inlines = [SentenceInline]

admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Sentence)

class EntryInline(admin.StackedInline):
    model = Entry

class TranscriptAdmin(admin.ModelAdmin):
    inlines = [EntryInline]

admin.site.register(Transcript, TranscriptAdmin)
