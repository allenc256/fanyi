import json
import re
import opencc
import pypinyin
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.db import transaction
from pathlib import Path
from tqdm import tqdm, trange
from practice.models import Conversation, Sentence

def to_pinyin(text_cn: str) -> str:
    pinyin_list = pypinyin.pinyin(text_cn)
    pinyin_flattened = []
    for ws in pinyin_list:
        for w in ws:
            is_pinyin = w.isalpha()
            if is_pinyin and pinyin_flattened:
                pinyin_flattened.append(' ')
            pinyin_flattened.append(w)
    return ''.join(pinyin_flattened)

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

        converter = opencc.OpenCC('s2twp.json')

        convos_to_save = []
        sents_to_save = []

        count_mismatch = 0

        for convo_idx in trange(len(json_en), desc='parsing'):
            convo_en = json_en[convo_idx][0]
            convo_cn = json_cn[convo_idx][0]

            if len(convo_en) != len(convo_cn):
                count_mismatch += 1
                continue

            convo = Conversation(name=f'{path_en.name}:{convo_idx}', date_added=timezone.now())
            sents = []
            mismatched = False

            for sent_idx, (sent_en, sent_cn) in enumerate(zip(convo_en, convo_cn)):
                m_en = re.match(r'^(Speaker [^:]+): ?(.*)$', sent_en)
                m_cn = re.match(r'^(Speaker [^:]+): ?(.*)$', sent_cn)

                if not m_en or not m_cn:
                    raise CommandError(f'failed to parse sentences: "{sent_en}", "{sent_cn}"')
                if m_en.group(1) != m_cn.group(1):
                    mismatched = True
                    break

                sent = Sentence(
                    conversation=convo,
                    speaker=m_en.group(1),
                    index=sent_idx,
                    text_en=m_en.group(2),
                    text_cn_simplified=m_cn.group(2),
                    text_cn_traditional=converter.convert(m_cn.group(2)),
                    text_cn_pinyin=to_pinyin(m_cn.group(2)),
                )
                sents.append(sent)

            if mismatched:
                count_mismatch += 1
            else:
                convos_to_save.append(convo)
                sents_to_save.extend(sents)

        with transaction.atomic():
            for convo in tqdm(convos_to_save, desc='saving conversations'):
                convo.save()
            batch_size = 200
            for i in tqdm(range(0, len(sents_to_save), batch_size), desc='saving sentences'):
                Sentence.objects.bulk_create(sents_to_save[i:i + batch_size])
