from pathlib import Path
import html
import re


def normalize(text):
    text = html.unescape(text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'(?m)^\s*#{1,6}\s+', '', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'(?m)^\s*-\s+', '', text)
    return re.sub(r'\s+', '', text)


def main():
    failed = []
    for md in Path('resumes').glob('*.md'):
        html_file = Path('generated') / md.stem / 'index.html'
        if not html_file.exists():
            failed.append(f'{md.stem}: missing html')
            continue
        source = normalize(md.read_text(encoding='utf-8'))
        target = normalize(html_file.read_text(encoding='utf-8'))
        if source not in target:
            failed.append(f'{md.stem}: mismatch')
    if failed:
        raise SystemExit('\n'.join(failed))
    print('All resumes consistent')


if __name__ == '__main__':
    main()
