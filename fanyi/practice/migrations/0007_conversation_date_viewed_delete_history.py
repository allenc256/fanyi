# Generated by Django 4.0.5 on 2022-07-09 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0006_remove_conversation_view_count_history'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='date_viewed',
            field=models.DateTimeField(null=True),
        ),
        migrations.DeleteModel(
            name='History',
        ),
    ]
