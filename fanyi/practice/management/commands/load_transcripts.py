import json
from django.core.management.base import BaseCommand, CommandError
from django.utils.dateparse import parse_date
from django.db import transaction
from pathlib import Path
from tqdm import tqdm
from practice.models import Transcript

class Command(BaseCommand):
    help = 'loads transcript JSON into the database'

    def add_arguments(self, parser):
        parser.add_argument('path', metavar='PATH', type=str, help='path to transcript JSON file')

    def handle(self, *args, **options):
        path = Path(options['path'])

        if not path.is_file():
            raise CommandError(f'not a file: {path}')

        with path.open('rt') as f:
            transcripts_json = json.load(f)

        with transaction.atomic():
            for transcript_json in tqdm(transcripts_json):
                transcript = Transcript(
                    title=transcript_json['title'],
                    author=transcript_json.get('author'),
                    url=transcript_json.get('url'),
                    date_published=parse_date(transcript_json.get('publish_date')),
                )
                transcript.save()

                for entry_idx, entry_json in enumerate(transcript_json['entries']):
                    transcript.entry_set.create(
                        index=entry_idx,
                        start_ms=entry_json.get('start_ms'),
                        end_ms=entry_json.get('end_ms'),
                        text_en=entry_json.get('text_en'),
                        text_cn_traditional=entry_json.get('text_cn_traditional'),
                        text_cn_simplified=entry_json.get('text_cn_simplified'),
                        text_cn_pinyin=entry_json.get('text_cn_pinyin'),
                    )
