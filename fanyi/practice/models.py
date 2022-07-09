from django.db import models

class Conversation(models.Model):
    name = models.CharField(max_length=256)
    date_added = models.DateTimeField()
    date_viewed = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.name}'

class Sentence(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    index = models.IntegerField()
    speaker = models.CharField(max_length=256)
    text_en = models.CharField('text (english)', max_length=4096)
    text_cn_traditional = models.CharField('text (traditional)', max_length=4096)
    text_cn_simplified = models.CharField('text (simplified)', max_length=4096)
    text_cn_pinyin = models.CharField('text (pinyin)', max_length=4096)

    def __str__(self):
        return f'{self.name}'

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
    transcript = models.ForeignKey(Transcript, on_delete=models.CASCADE)
    index = models.IntegerField()
    start_ms = models.IntegerField('start (ms)', null=True)
    end_ms = models.IntegerField('end (ms)', null=True)
    text_en = models.CharField('text (english)', max_length=4096)
    text_cn_traditional = models.CharField('text (traditional)', max_length=4096)
    text_cn_simplified = models.CharField('text (simplified)', max_length=4096, null=True)
    text_cn_pinyin = models.CharField('text (pinyin)', max_length=4096)

    def __str__(self):
        s = self.text_en[:60]
        if len(self.text_en) > 60:
            s += '...'
        return s
