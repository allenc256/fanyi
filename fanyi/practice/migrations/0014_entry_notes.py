# Generated by Django 4.0.5 on 2022-07-11 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0013_remove_sentence_conversation_delete_conversation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='notes',
            field=models.CharField(max_length=4096, null=True, verbose_name='notes'),
        ),
    ]