from pathlib import Path
import re


def normalize(text):
    return re.sub(r'\s+', '', text)


def main():
    failed = []
    for md in Path('resumes').glob('*.md'):
        html_file = Path('generated') / md.stem / 'index.html'
        if not html_file.exists():
            failed.append(f'{md.stem}: missing html')
            continue
        source = normalize(md.read_text(encoding='utf-8'))
        target = normalize(re.sub('<[^>]+>', '', html_file.read_text(encoding='utf-8')))
        if source not in target:
            failed.append(f'{md.stem}: mismatch')
    if failed:
        raise SystemExit('\n'.join(failed))
    print('All resumes consistent')


if __name__ == '__main__':
    main()
