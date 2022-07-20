# Generated by Django 4.0.5 on 2022-07-17 21:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0019_rename_date_added_vocab_date_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vocab',
            name='date_created',
        ),
        migrations.AddField(
            model_name='vocab',
            name='time_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]