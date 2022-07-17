from django.db import models
from django.utils.translation import gettext_lazy as _

class Transcript(models.Model):
    title = models.CharField(max_length=256)
    author = models.CharField(max_length=256, null=True)
    url = models.CharField(max_length=2048, null=True)
    date_published = models.DateField(null=True)
    date_added = models.DateField(auto_now_add=True)
    last_viewed = models.DateTimeField(null=True)

    def __str__(self):
        return self.title

class Entry(models.Model):
    class Difficulty(models.IntegerChoices):
        NONE = 0, _('None')
        EASY = 1, _('Easy')
        MEDIUM = 2, _('Medium')
        HARD = 3, _('Hard')

    transcript = models.ForeignKey(Transcript, on_delete=models.CASCADE)
    index = models.IntegerField()
    start_ms = models.IntegerField('start (ms)', null=True)
    end_ms = models.IntegerField('end (ms)', null=True)
    text_en = models.TextField('text (english)')
    notes = models.TextField('notes', null=True, blank=True)
    difficulty = models.IntegerField(choices=Difficulty.choices, default=Difficulty.NONE)

    class Meta:
        ordering = ['index']

    def __str__(self):
        s = self.text_en[:60]
        if len(self.text_en) > 60:
            s += '...'
        return s

class Translation(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    index = models.IntegerField()
    source = models.CharField(max_length=256)
    text_cn_traditional = models.TextField('text (traditional)')
    text_cn_simplified = models.TextField('text (simplified)', null=True)
    text_cn_pinyin = models.TextField('text (pinyin)')

    class Meta:
        ordering = ['index']
