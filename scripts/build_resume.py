from pathlib import Path

SOURCE_DIR = Path('resumes')
OUTPUT_DIR = Path('generated')
TEMPLATE = Path('templates/resume.html')


def markdown_to_html(text: str) -> str:
    lines = []
    for line in text.splitlines():
        if line.startswith('# '):
            lines.append(f'<h1>{line[2:]}</h1>')
        elif line.startswith('## '):
            lines.append(f'<h2>{line[3:]}</h2>')
        elif line.startswith('### '):
            lines.append(f'<h3>{line[4:]}</h3>')
        elif line.strip():
            lines.append(f'<p>{line}</p>')
    return '\n'.join(lines)


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    template = TEMPLATE.read_text(encoding='utf-8')
    for source in SOURCE_DIR.glob('*.md'):
        html = template.replace('{{content}}', markdown_to_html(source.read_text(encoding='utf-8')))
        target = OUTPUT_DIR / source.stem
        target.mkdir(exist_ok=True)
        (target / 'index.html').write_text(html, encoding='utf-8')


if __name__ == '__main__':
    main()
