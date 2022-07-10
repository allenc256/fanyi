from django.contrib import admin

from .models import Transcript, Entry, Translation

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
