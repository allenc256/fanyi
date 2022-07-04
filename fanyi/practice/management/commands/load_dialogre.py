from django.core.management.base import BaseCommand, CommandError
from practice.models import Conversation, Sentence
import json
from pathlib import Path

class Command(BaseCommand):
    help = 'loads DialogRE (https://github.com/nlpdata/dialogre/) conversations into the database'

    def add_arguments(self, parser):
        parser.add_argument('path_en', metavar='PATH_EN', type=str, help='path to DialogRE English JSON file')
        parser.add_argument('path_cn', metavar='PATH_CN', type=str, help='path to DialogRE Chinese JSON file')

    def handle(self, *args, **options):
        path_en, path_cn = Path(options['path_en']), Path(options['path_cn'])

        if not path_en.is_file():
            raise CommandError(f'not a file: {path_en}')
        if not path_cn.is_file():
            raise CommandError(f'not a file: {path_cn}')

        with path_en.open('rt') as f:
            json_en = json.load(f)
        with path_cn.open('rt') as f:
            json_cn = json.load(f)

        if len(json_en) != len(json_cn):
            raise CommandError(f'datasets are of differing lengths: {len(json_en)} vs {len(json_cn)}')

        convo_en = json_en[0][0]
        convo_cn = json_cn[0][0]
        

