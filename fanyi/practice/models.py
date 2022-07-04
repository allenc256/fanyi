from django.db import models

class Conversation(models.Model):
    date_added = models.DateTimeField()

class Sentence(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    index = models.IntegerField()
    speaker = models.CharField(max_length=256)
    text_en = models.CharField('text (english)', max_length=4096)
    text_cn_traditional = models.CharField('text (traditional)', max_length=4096)
    text_cn_simplified = models.CharField('text (simplified)', max_length=4096)
    text_cn_pinyin = models.CharField('text (pinyin)', max_length=4096)

    def __str__(self):
        return f'{self.speaker}: {self.text_en}'
