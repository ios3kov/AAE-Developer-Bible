#!/usr/bin/env python3
"""Render reviewed source/claim records; never discover or certify APIs automatically."""
import argparse
from datetime import date
import json
from pathlib import Path
import re
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / 'sources/claim-registry.json'
OUTPUT = ROOT / 'BLOCK-5-SOURCES.md'
SHA = re.compile(r'[0-9a-f]{40}')
DIGEST = re.compile(r'[0-9a-f]{64}')


def load_registry(path=INPUT, root=ROOT):
    data = json.loads(path.read_text(encoding='utf-8'))
    if data.get('schema') != 1 or not data.get('claims'):
        raise ValueError('Expected schema 1 and nonempty claims')
    ids = set()
    for row in data['claims']:
        fields = ('id', 'claim', 'source', 'identity', 'review_date', 'sdk',
                  'host', 'panel', 'platform', 'evidence', 'limits', 'record')
        if any(not isinstance(row.get(k), str) or not row[k].strip() for k in fields):
            raise ValueError('Missing source/claim boundary field')
        if row['id'] in ids:
            raise ValueError('Duplicate claim id')
        ids.add(row['id'])
        date.fromisoformat(row['review_date'])
        parsed = urlparse(row['source'])
        if parsed.scheme != 'https' or not parsed.netloc:
            raise ValueError('Source must be an explicit HTTPS URL')
        record = (root / row['record']).resolve()
        if not record.is_relative_to(root.resolve()) or not record.is_file():
            raise ValueError('Missing or escaping review record')
        if row['evidence'] not in ('SDK-SOURCE-REVIEW', 'DOCUMENTED', 'SECONDARY', 'PROJECT-REPORTED', 'USER-REPORTED'):
            raise ValueError('Unknown technical evidence class')
        if '...' in row['identity'] or '…' in row['identity']:
            raise ValueError('Abbreviated source identity')
    for row in data.get('regenerations', []):
        if not SHA.fullmatch(row['source_git_sha']) or not SHA.fullmatch(row['generated_git_sha']):
            raise ValueError('Regeneration requires full Git SHAs')
        if not DIGEST.fullmatch(row['content_sha256']):
            raise ValueError('Regeneration requires full content digest')
        if row.get('evidence') != 'DOCS-CI-PASS':
            raise ValueError('Regeneration is documentation CI evidence only')
        date.fromisoformat(row['review_date'])
        if not row['run_url'].startswith('https://github.com/ios3kov/AAE-Developer-Bible/actions/runs/'):
            raise ValueError('Expected repository workflow evidence URL')
    return data


def cell(value):
    return value.replace('|', '&#124;').replace('\n', '<br>')


def render(data):
    lines = ['# Источники, версии и границы доказательств — блок 5', '',
             'Generated from [reviewed JSON](sources/claim-registry.json) by '
             '`python3 scripts/generate_sources_table.py`. Менять реестр, затем генерировать таблицу.', '',
             'Каждая строка относится к названной группе утверждений и указанной области review. '
             'Дата review не означает повторный запуск SDK/host проверки. SDK, host support, panel runtime '
             'и platform policy — отдельные границы. «Не относится» не означает отсутствие поддержки.', '',
             '| ID / группа | Exact source / identity | Review date | SDK baseline | Host support | Panel runtime | Platform policy | Evidence / limits / record |',
             '|---|---|---|---|---|---|---|---|']
    for r in data['claims']:
        cells = [r['id']+' / '+r['claim'], '[Source]('+r['source']+') — '+r['identity'],
                 r['review_date'], r['sdk'], r['host'], r['panel'], r['platform'],
                 r['evidence']+'; '+r['limits']+'; [review]('+r['record']+')']
        lines.append('| '+' | '.join(cell(x) for x in cells)+' |')
    lines += ['', '## Provenance регенерации документации', '',
              'Эти Git SHA и digest идентифицируют Bible и её generated outputs. '
              'Они не являются идентичностью Adobe SDK, подтверждением signing/notarization или host execution. '
              'Это фиксированные исторические записи: не записывать текущий generated SHA в его собственный source input.', '',
              '| Source-Git-SHA | Generated-SHA | Source content SHA-256 | Review / workflow | Evidence |',
              '|---|---|---|---|---|']
    for r in data.get('regenerations', []):
        lines.append('| '+' | '.join([f"`{r['source_git_sha']}`", f"`{r['generated_git_sha']}`",
            f"`{r['content_sha256']}`", f"{r['review_date']} / [run]({r['run_url']})", r['evidence']])+' |')
    lines += ['', 'Исторические run details: [VERIFICATION](VERIFICATION.md). Текущие CI identities '
              'выводит `scripts/docs_lane.py`; новые записи добавляются после проверки результата, '
              'а не автоматически получают статус технической валидации.', '',
              'Практическое сравнение источников: [Block 5 review](BLOCK-5-REVIEW-2026-10-04.md). '
              'Условия собственного текста/кода и vendor material: [NOTICE](NOTICE.md).', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--input', type=Path, default=INPUT)
    parser.add_argument('--output', type=Path, default=OUTPUT)
    args = parser.parse_args()
    content = render(load_registry(args.input))
    if args.check:
        if not args.output.is_file() or args.output.read_text(encoding='utf-8') != content:
            print('Stale source table: '+str(args.output))
            return 1
    else:
        args.output.write_text(content, encoding='utf-8')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
