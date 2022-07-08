from django.contrib import admin

from .models import Conversation, Sentence

class SentenceInline(admin.StackedInline):
    model = Sentence

class ConversationAdmin(admin.ModelAdmin):
    inlines = [SentenceInline]

admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Sentence)
