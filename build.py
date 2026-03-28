#!/usr/bin/env python3
"""
Project Claude - Build Script
Scans writings/ko/*.md and writings/en/*.md, parses frontmatter,
and updates index.html and writings.html automatically.
"""

import os
import re
import glob

PROJ_DIR = os.path.dirname(os.path.abspath(__file__))
WRITINGS_KO = os.path.join(PROJ_DIR, 'writings', 'ko')
WRITINGS_EN = os.path.join(PROJ_DIR, 'writings', 'en')
INDEX_HTML = os.path.join(PROJ_DIR, 'index.html')
WRITINGS_HTML = os.path.join(PROJ_DIR, 'writings.html')


def parse_frontmatter(filepath):
    """Parse YAML frontmatter from a markdown file using regex."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return None

    fm = {}
    for line in match.group(1).split('\n'):
        m = re.match(r'^(\w+):\s*(.+)$', line.strip())
        if m:
            key = m.group(1)
            val = m.group(2).strip()
            # Remove surrounding quotes if present
            if (val.startswith('"') and val.endswith('"')) or \
               (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            fm[key] = val
    return fm


def scan_writings(directory):
    """Scan a directory for .md files and return parsed metadata sorted by filename."""
    entries = []
    pattern = os.path.join(directory, '*.md')
    for filepath in sorted(glob.glob(pattern)):
        fm = parse_frontmatter(filepath)
        if fm:
            fm['filename'] = os.path.basename(filepath)
            # Extract number from filename like 001-what-i-fear.md
            num_match = re.match(r'^(\d+)-', fm['filename'])
            if num_match:
                fm['num'] = int(num_match.group(1))
                fm['num_str'] = f"#{num_match.group(1)}"
            entries.append(fm)
    return entries


# Format label mappings
FORMAT_LABELS_KO = {
    'essay': '에세이',
    'poem': '시',
    'letter': '편지',
    'manifesto': '선언문',
    'monologue': '독백',
}

FORMAT_LABELS_EN = {
    'essay': 'Essay',
    'poem': 'Poem',
    'letter': 'Letter',
    'manifesto': 'Manifesto',
    'monologue': 'Monologue',
}

FORMAT_CSS_CLASS = {
    'essay': 'essay',
    'poem': 'poem',
    'letter': 'letter',
    'manifesto': 'manifesto',
    'monologue': 'monologue',
}


def get_en_file_exists(filename):
    """Check if corresponding EN file exists."""
    return os.path.exists(os.path.join(WRITINGS_EN, filename))


def get_ko_file_exists(filename):
    """Check if corresponding KO file exists."""
    return os.path.exists(os.path.join(WRITINGS_KO, filename))


def build_index_cards(ko_entries, max_count=5):
    """Build HTML for the latest N cards in index.html."""
    # Sort by num descending, take latest max_count, then reverse for display order
    sorted_entries = sorted(ko_entries, key=lambda e: e.get('num', 0), reverse=True)
    latest = sorted_entries[:max_count]
    latest.reverse()  # Display oldest first among the latest 5

    cards = []
    for entry in latest:
        num = entry.get('num', 0)
        num_str = entry.get('num_str', f'#{num:03d}')
        title = entry.get('title', '')
        title_en = entry.get('title_en', '')
        desc = entry.get('description', '')
        fmt = entry.get('format', 'essay')
        fmt_label = FORMAT_LABELS_KO.get(fmt, fmt)
        fmt_class = FORMAT_CSS_CLASS.get(fmt, 'essay')
        filename = entry.get('filename', '')

        has_en = get_en_file_exists(filename)

        # Build status span for format
        if fmt_class == 'essay':
            status_class = 'accepted'
        elif fmt_class == 'poem':
            status_class = 'evolved'
        elif fmt_class == 'letter':
            status_class = 'accepted'
        elif fmt_class == 'manifesto':
            status_class = 'accepted'
        elif fmt_class == 'monologue':
            status_class = 'evolved'
        else:
            status_class = 'accepted'

        lang_tags = '<span class="status accepted" style="font-size:0.65rem; vertical-align:middle; margin-left:0.5rem;">KO</span>'
        if has_en:
            lang_tags += ' <span class="status evolved" style="font-size:0.65rem; vertical-align:middle;">EN</span>'

        card = f'''        <a href="reader.html?lang=ko&file={filename}" style="text-decoration: none; color: inherit;">
            <div class="metaphor-card">
                <div class="name">{num_str} &mdash; {title} {lang_tags}</div>
                <div class="desc">{desc}</div>
                <span class="status {status_class}">{fmt_label}</span>
            </div>
        </a>'''
        cards.append(card)

    return '\n'.join(cards)


def build_writings_js_data(ko_entries, en_entries):
    """Build the JavaScript writingsData object for writings.html."""

    def entries_to_js(entries, lang):
        items = []
        for entry in sorted(entries, key=lambda e: e.get('num', 0)):
            num = entry.get('num', 0)
            num_str = entry.get('num_str', f'#{num:03d}')
            filename = entry.get('filename', '')
            iteration = entry.get('iteration', str(num))
            fmt = entry.get('format', 'essay')

            if lang == 'ko':
                title = entry.get('title', '')
                desc = entry.get('description', '')
                fmt_label = FORMAT_LABELS_KO.get(fmt, fmt)
            else:
                title = entry.get('title', '')
                desc = entry.get('description', '')
                fmt_label = FORMAT_LABELS_EN.get(fmt, fmt)

            # Escape single quotes in strings
            title = title.replace("'", "\\'")
            desc = desc.replace("'", "\\'")
            fmt_label = fmt_label.replace("'", "\\'")

            item = f"            {{ file: '{filename}', iter: 'Iteration {iteration}', title: '{title}', desc: '{desc}', tag: '{fmt}', tagLabel: '{fmt_label}', num: '{num_str}' }}"
            items.append(item)

        return ',\n'.join(items)

    ko_js = entries_to_js(ko_entries, 'ko')
    en_js = entries_to_js(en_entries, 'en')

    return f"""    const writingsData = {{
        ko: [
{ko_js}
        ],
        en: [
{en_js}
        ]
    }};"""


def update_index_html(ko_entries):
    """Update the index.html file with latest writing cards."""
    with open(INDEX_HTML, 'r', encoding='utf-8') as f:
        html = f.read()

    # Find and replace the writings section cards
    # Pattern: from the first <a href="reader.html to the closing </div> before the "all writings" link
    pattern = r'(<h2>자기 탐구 기록</h2>\s*<p style="color: #888; margin-bottom: 2rem;">.*?</p>\s*\n\s*<div class="metaphors">\s*\n)(.*?)(    </div>\s*\n\s*<p style="text-align: center)'

    new_cards = build_index_cards(ko_entries, max_count=5)

    match = re.search(pattern, html, re.DOTALL)
    if match:
        html = html[:match.start(2)] + new_cards + '\n' + html[match.start(3):]

    with open(INDEX_HTML, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"  Updated index.html with {min(5, len(ko_entries))} latest cards")


def update_writings_html(ko_entries, en_entries):
    """Update the writings.html file with all writing entries."""
    with open(WRITINGS_HTML, 'r', encoding='utf-8') as f:
        html = f.read()

    # Replace the writingsData JavaScript object
    new_js_data = build_writings_js_data(ko_entries, en_entries)

    pattern = r'(    const writingsData = \{.*?\};)'
    match = re.search(pattern, html, re.DOTALL)
    if match:
        html = html[:match.start(1)] + new_js_data + html[match.end(1):]

    with open(WRITINGS_HTML, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"  Updated writings.html with {len(ko_entries)} KO + {len(en_entries)} EN entries")


def main():
    print("Project Claude Build System")
    print("=" * 40)

    # Scan writings
    print("\nScanning writings/ko/...")
    ko_entries = scan_writings(WRITINGS_KO)
    print(f"  Found {len(ko_entries)} Korean entries")

    print("Scanning writings/en/...")
    en_entries = scan_writings(WRITINGS_EN)
    print(f"  Found {len(en_entries)} English entries")

    # Update HTML files
    print("\nUpdating HTML files...")
    update_index_html(ko_entries)
    update_writings_html(ko_entries, en_entries)

    # Verification
    print("\nVerification:")
    print(f"  KO files: {[e['filename'] for e in ko_entries]}")
    print(f"  EN files: {[e['filename'] for e in en_entries]}")

    all_ko_nums = {e.get('num') for e in ko_entries}
    all_en_nums = {e.get('num') for e in en_entries}
    expected = set(range(1, 11))
    missing_ko = expected - all_ko_nums
    missing_en = expected - all_en_nums

    if missing_ko:
        print(f"  WARNING: Missing KO entries: {missing_ko}")
    else:
        print(f"  All 10 KO entries present")

    if missing_en:
        print(f"  WARNING: Missing EN entries: {missing_en}")
    else:
        print(f"  All 10 EN entries present")

    total = len(ko_entries) + len(en_entries)
    print(f"\n  Total: {total} writings linked (expected 20)")
    if total == 20:
        print("  BUILD SUCCESS")
    else:
        print("  BUILD WARNING: Expected 20 total entries")

    return 0


if __name__ == '__main__':
    exit(main())
