from django.contrib import admin

from .models import Conversation, Sentence
from .models import Transcript, Entry, Translation

class SentenceInline(admin.StackedInline):
    model = Sentence

class ConversationAdmin(admin.ModelAdmin):
    inlines = [SentenceInline]

admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Sentence)

class TranslationInline(admin.StackedInline):
    model = Translation

class EntryAdmin(admin.ModelAdmin):
    inlines = [TranslationInline]

class EntryInline(admin.StackedInline):
    model = Entry
    show_change_link = True

class TranscriptAdmin(admin.ModelAdmin):
    inlines = [EntryInline]

admin.site.register(Transcript, TranscriptAdmin)
admin.site.register(Entry, EntryAdmin)
