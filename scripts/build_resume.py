from pathlib import Path
import html

SOURCE_DIR = Path('resumes')
OUTPUT_DIR = Path('generated')
TEMPLATE = Path('templates/resume.html')
CONFIG = Path('resume-config.yml')


def markdown_to_html(text: str) -> str:
    result = []
    for line in text.splitlines():
        escaped = html.escape(line)
        if escaped.startswith('# '):
            result.append(f'<h1>{escaped[2:]}</h1>')
        elif escaped.startswith('## '):
            result.append(f'<h2>{escaped[3:]}</h2>')
        elif escaped.startswith('### '):
            result.append(f'<h3>{escaped[4:]}</h3>')
        elif escaped.startswith('- '):
            result.append(f'<p>• {escaped[2:]}</p>')
        elif escaped.strip():
            result.append(f'<p>{escaped}</p>')
    return '\n'.join(result)


def load_mapping():
    mapping = {}
    for line in CONFIG.read_text(encoding='utf-8').splitlines():
        if line.strip().startswith('source:'):
            current = None
        if line.strip().startswith('06'):
            current = line.strip().rstrip(':')
            mapping[current] = {}
        elif 'output:' in line and current:
            mapping[current]['output'] = line.split(':', 1)[1].strip()
    return mapping


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    template = TEMPLATE.read_text(encoding='utf-8')
    for source in SOURCE_DIR.glob('*.md'):
        content = markdown_to_html(source.read_text(encoding='utf-8'))
        html_page = template.replace('{{content}}', content)
        target = OUTPUT_DIR / source.stem
        target.mkdir(exist_ok=True)
        (target / 'index.html').write_text(html_page, encoding='utf-8')


if __name__ == '__main__':
    main()
