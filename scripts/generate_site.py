#!/usr/bin/env python3
"""
LedgerLearning static site generator.

Reads backups/ledgerlearning.WordPress.2026-10-02.xml and generates:
  1. Balancing Act book pages  →  docs/books/balancing-act-financial-systems-textbook/...
  2. Blog post pages           →  docs/YYYY/MM/DD/slug/index.html

Usage:
    python3 scripts/generate_site.py
"""

import os
import re
import sys
from html import unescape
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────────
SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT   = os.path.dirname(SCRIPT_DIR)
WXR_PATH    = os.path.join(REPO_ROOT, 'backups', 'ledgerlearning.WordPress.2026-10-02.xml')
DOCS_DIR    = os.path.join(REPO_ROOT, 'docs')

TOC_BASE = 'books/balancing-act-financial-systems-textbook/on-line-balancing-act-text-book'

# Slugs that live inside the appendices/ subdirectory
APPENDICES_SLUGS = {'appendix-1-accounting-model', 'appendix-2-event-driven-business-modeling', 'appendices'}

# ── Book Structure & Order ───────────────────────────────────────────────────

BOOK_STRUCTURE = [
    {
        'title': 'Front Matter',
        'items': [
            ('on-line-balancing-act-text-book', 'Table of Contents'),
            ('dedication', 'Dedication and Copyright'),
            ('preface', 'Preface'),
        ]
    },
    {
        'title': 'Part 1: The Pearl',
        'part_slug': 'part-1-the-pearl',
        'items': [
            ('introduction', 'Chapter 1: Introduction'),
            ('the-problem', 'Chapter 2: The Problem'),
            ('the-solution', 'Chapter 3: The Solution'),
        ]
    },
    {
        'title': 'Part 2: The Professor',
        'part_slug': 'the-professor',
        'items': [
            ('computers', 'Chapter 4: Computers'),
            ('accounting', 'Chapter 5: Accounting'),
            ('business-events', 'Chapter 6: Business Events'),
            ('resources-and-agents', 'Chapter 7: Resources and Agents'),
            ('real-analysis-method', 'Chapter 8: REAL Analysis Method'),
            ('the-ivory-tower', 'Chapter 9: The Ivory Tower'),
        ]
    },
    {
        'title': 'Part 3: The Partner',
        'part_slug': 'the-partner',
        'items': [
            ('chapter-10-reality', 'Chapter 10: Reality'),
            ('chapter-11-consulting', 'Chapter 11: Consulting'),
            ('chapter-12-types-of-computers-and-processes', 'Chapter 12: Types of Computers and Processes'),
            ('chapter-13-business-system-architecture', 'Chapter 13: Business System Architecture'),
            ('chapter-14-reporting', 'Chapter 14: Reporting'),
            ('chapter-15-operational-versus-informational', 'Chapter 15: Operational Versus Informational'),
            ('chapter-16-data-warehousing', 'Chapter 16: Data Warehousing'),
            ('chapter-17-programming-tools', 'Chapter 17: Programming Tools'),
            ('chapter-18-input-output', 'Chapter 18: Input/Output'),
            ('chapter-19-select-sort-summarize', 'Chapter 19: Select, Sort, Summarize'),
            ('chapter-20-parallelism-and-platform', 'Chapter 20: Parallelism and Platform'),
            ('chapter-21-erp-reporting', 'Chapter 21: ERP Reporting'),
            ('chapter-22-order-of-operations', 'Chapter 22: Order of Operations'),
        ]
    },
    {
        'title': 'Part 4: The Projects',
        'part_slug': 'part-4-the-projects',
        'items': [
            ('chapter-23-development', 'Chapter 23: Development'),
            ('chapter-24-skyscrapers', 'Chapter 24: Skyscrapers'),
            ('chapter-25-find-the-event-file', 'Chapter 25: Find the Event File'),
            ('chapter-26-balance-the-event-file', 'Chapter 26: Balance the Event File'),
            ('chapter-27-find-more-detailed-events', 'Chapter 27: Find More Detailed Events'),
            ('chapter-28-define-reference-data', 'Chapter 28: Define Reference Data'),
            ('chapter-29-iteratively-view-results', 'Chapter 29: Iteratively View Results'),
            ('chapter-30-assess-reporting-needs', 'Chapter 30: Assess Reporting Needs'),
            ('chapter-31-estimate-the-data-basis', 'Chapter 31: Estimate the Data Basis'),
            ('chapter-32-define-summary-structures', 'Chapter 32: Define Summary Structures'),
            ('chapter-33-define-processes', 'Chapter 33: Define Processes'),
            ('chapter-34-consider-complex-joins', 'Chapter 34: Consider Complex Joins'),
            ('chapter-35-model-the-repository', 'Chapter 35: Model the Repository'),
            ('chapter-36-optimize-for-performance', 'Chapter 36: Optimize For Performance'),
            ('chapter-37-maintain-focus', 'Chapter 37: Maintain Focus'),
        ]
    },
    {
        'title': 'Part 5: The Programmer',
        'part_slug': 'part-5-the-programmer',
        'items': [
            ('chapter-38-abends', 'Chapter 38: Abends'),
            ('chapter-39-the-copy-only-view', 'Chapter 39: The Copy Only View'),
            ('chapter-40-extract-only-view', 'Chapter 40: Extract Only View'),
            ('chapter-41-look-ups', 'Chapter 41: Look-ups'),
            ('chapter-42-reference-file-phase', 'Chapter 42: Reference File Phase'),
            ('chapter-43-extract-files', 'Chapter 43: Extract Files'),
            ('chapter-44-sort', 'Chapter 44: Sort'),
            ('chapter-45-sort-user-exits', 'Chapter 45: Sort User Exits'),
            ('chapter-46-format-phase', 'Chapter 46: Format Phase'),
            ('chapter-47-look-at-it-go', 'Chapter 47: "Look At It Go"'),
            ('chapter-48-multi-threading', 'Chapter 48: Multi-Threading'),
            ('chapter-49-control-and-contention', 'Chapter 49: Control and Contention'),
            ('chapter-50-piping-tokens-and-the-write-verb', 'Chapter 50: Piping, Tokens, and the Write Verb'),
            ('chapter-15-exits', 'Chapter 51: Exits'),
            ('chapter-52-common-key-data-buffering', 'Chapter 52: Common Key Data Buffering'),
            ('chapter-53-spin-offs', 'Chapter 53: Spin-offs'),
            ('chapter-54-crisis', 'Chapter 54: Crisis'),
        ]
    },
    {
        'title': 'Part 6: The Platform',
        'part_slug': 'part-6-the-platform',
        'items': [
            ('chapter-55-transition', 'Chapter 55: Transition'),
            ('chapter-56-walkabout', 'Chapter 56: Walkabout'),
            ('chapter-57-the-general-ledger', 'Chapter 57: The General Ledger'),
            ('chapter-58-the-arrangement-ledger', 'Chapter 58: The Arrangement Ledger'),
            ('chapter-59-accounting-rules', 'Chapter 59: Accounting Rules'),
            ('chapter-60-reclassification', 'Chapter 60: Reclassification'),
            ('chapter-61-support-processes', 'Chapter 61: Support Processes'),
            ('chapter-62-calculation-engines-and-reporting', 'Chapter 62: Calculation Engines and Reporting'),
            ('chapter-63-go-live', 'Chapter 63: Go Live'),
        ]
    },
    {
        'title': 'Part 7: The Plan',
        'part_slug': 'part7-the-plan',
        'items': [
            ('chapter-64-promotion', 'Chapter 64: Promotion'),
            ('chapter-65-start-with-finance', 'Chapter 65: Start with Finance'),
            ('chapter-66-expand-to-risk', 'Chapter 66: Expand to Risk'),
            ('chapter-67-beyond-finance-and-risk', 'Chapter 67: Beyond Finance and Risk'),
            ('chapter-68-partnership', 'Chapter 68: Partnership'),
        ]
    },
    {
        'title': 'Part 8: Appendices',
        'part_slug': 'appendices',
        'items': [
            ('appendix-1-accounting-model', 'Appendix 1: Accounting Model'),
            ('appendix-2-event-driven-business-modeling', 'Appendix 2: Event Driven Business Modeling'),
        ]
    },
    {
        'title': 'Back Matter',
        'items': [
            ('acknowledgements', 'Acknowledgements'),
            ('selected-bibliography', 'Selected Bibliography'),
            ('about-the-mentors', 'About the Mentors'),
            ('about-the-author', 'About the Author'),
        ]
    },
]

# Full ordered chapter list for prev/next navigation
BOOK_ORDER = [
    # front matter
    'on-line-balancing-act-text-book',   # TOC (index)
    'dedication',
    'preface',
    # part 1
    'part-1-the-pearl',
    'introduction',
    'the-problem',
    'the-solution',
    # part 2
    'the-professor',
    'computers',
    'accounting',
    'business-events',
    'resources-and-agents',
    'real-analysis-method',
    'the-ivory-tower',
    # part 3
    'the-partner',
    'chapter-10-reality',
    'chapter-11-consulting',
    'chapter-12-types-of-computers-and-processes',
    'chapter-13-business-system-architecture',
    'chapter-14-reporting',
    'chapter-15-operational-versus-informational',
    'chapter-16-data-warehousing',
    'chapter-17-programming-tools',
    'chapter-18-input-output',
    'chapter-19-select-sort-summarize',
    'chapter-20-parallelism-and-platform',
    'chapter-21-erp-reporting',
    'chapter-22-order-of-operations',
    # part 4
    'part-4-the-projects',
    'chapter-23-development',
    'chapter-24-skyscrapers',
    'chapter-25-find-the-event-file',
    'chapter-26-balance-the-event-file',
    'chapter-27-find-more-detailed-events',
    'chapter-28-define-reference-data',
    'chapter-29-iteratively-view-results',
    'chapter-30-assess-reporting-needs',
    'chapter-31-estimate-the-data-basis',
    'chapter-32-define-summary-structures',
    'chapter-33-define-processes',
    'chapter-34-consider-complex-joins',
    'chapter-35-model-the-repository',
    'chapter-36-optimize-for-performance',
    'chapter-37-maintain-focus',
    # part 5
    'part-5-the-programmer',
    'chapter-38-abends',
    'chapter-39-the-copy-only-view',
    'chapter-40-extract-only-view',
    'chapter-41-look-ups',
    'chapter-42-reference-file-phase',
    'chapter-43-extract-files',
    'chapter-44-sort',
    'chapter-45-sort-user-exits',
    'chapter-46-format-phase',
    'chapter-47-look-at-it-go',
    'chapter-48-multi-threading',
    'chapter-49-control-and-contention',
    'chapter-50-piping-tokens-and-the-write-verb',
    'chapter-15-exits',       # Chapter 51 (slug mismatch in WP)
    'chapter-52-common-key-data-buffering',
    'chapter-53-spin-offs',
    'chapter-54-crisis',
    # part 6
    'part-6-the-platform',
    'chapter-55-transition',
    'chapter-56-walkabout',
    'chapter-57-the-general-ledger',
    'chapter-58-the-arrangement-ledger',
    'chapter-59-accounting-rules',
    'chapter-60-reclassification',
    'chapter-61-support-processes',
    'chapter-62-calculation-engines-and-reporting',
    'chapter-63-go-live',
    # part 7
    'part7-the-plan',
    'chapter-64-promotion',
    'chapter-65-start-with-finance',
    'chapter-66-expand-to-risk',
    'chapter-67-beyond-finance-and-risk',
    'chapter-68-partnership',
    # part 8 appendices
    'appendices',
    'appendix-1-accounting-model',
    'appendix-2-event-driven-business-modeling',
    # back matter
    'acknowledgements',
    'selected-bibliography',
    'about-the-mentors',
    'about-the-author',
]

def slug_to_url(slug):
    """Return the URL path (relative to docs/) for a book page slug."""
    if slug == 'on-line-balancing-act-text-book':
        return f'{TOC_BASE}/'
    if slug in APPENDICES_SLUGS:
        return f'{TOC_BASE}/appendices/{slug}/' if slug != 'appendices' else f'{TOC_BASE}/appendices/'
    return f'{TOC_BASE}/{slug}/'

def slug_to_file(slug):
    """Return the file path (relative to docs/) for a book page."""
    if slug == 'on-line-balancing-act-text-book':
        return os.path.join(DOCS_DIR, TOC_BASE, 'index.html')
    if slug in APPENDICES_SLUGS:
        if slug == 'appendices':
            return os.path.join(DOCS_DIR, TOC_BASE, 'appendices', 'index.html')
        return os.path.join(DOCS_DIR, TOC_BASE, 'appendices', slug, 'index.html')
    return os.path.join(DOCS_DIR, TOC_BASE, slug, 'index.html')

def toc_depth(slug):
    """How many levels deep from docs/ root for CSS path."""
    if slug == 'on-line-balancing-act-text-book':
        return 3
    if slug in APPENDICES_SLUGS and slug != 'appendices':
        return 5
    return 4

# Map of all book slugs to their canonical absolute URL
SLUG_MAP = {s: '/' + slug_to_url(s) for s in BOOK_ORDER}
SLUG_MAP['on-line-balancing-act-text-book'] = f'/{TOC_BASE}/'

# ── helpers ──────────────────────────────────────────────────────────────────

def read_wxr():
    with open(WXR_PATH, 'r', encoding='utf-8', errors='replace') as f:
        return f.read()

def extract_cdata(pattern, text, default=''):
    m = re.search(pattern + r'><!\[CDATA\[(.*?)\]\]>', text, re.DOTALL)
    return m.group(1).strip() if m else default

def extract_tag(pattern, text, default=''):
    m = re.search(r'<' + pattern + r'>(.*?)</' + pattern + r'>', text, re.DOTALL)
    return m.group(1).strip() if m else default

def strip_fusion_shortcodes(html):
    """Remove Avada/Fusion builder wrapper shortcodes, keep inner HTML."""
    html = re.sub(r'\[fusion_builder_container[^\]]*\]', '', html)
    html = re.sub(r'\[/fusion_builder_container\]', '', html)
    html = re.sub(r'\[fusion_builder_row[^\]]*\]', '', html)
    html = re.sub(r'\[/fusion_builder_row\]', '', html)
    html = re.sub(r'\[fusion_builder_column[^\]]*\]', '', html)
    html = re.sub(r'\[/fusion_builder_column\]', '', html)
    html = re.sub(r'\[fusion_text[^\]]*\]', '', html)
    html = re.sub(r'\[/fusion_text\]', '', html)
    html = re.sub(r'\[fusion_title[^\]]*\](.*?)\[/fusion_title\]', r'<h2>\1</h2>', html, flags=re.DOTALL)
    html = re.sub(r'\[fusion_separator[^\]]*\]', '<hr>', html)
    html = re.sub(r'\[[^\]]{1,120}\]', '', html)
    return html.strip()

def fix_all_book_links(html):
    """Rewrite any link targeting Balancing Act to its canonical absolute URL."""
    def repl_href(m):
        url = m.group(1)
        # Separate anchor if present
        anchor = ''
        if '#' in url:
            url, anchor = url.split('#', 1)
            anchor = '#' + anchor
        clean = url.replace('https://ledgerlearning.com', '').replace('http://ledgerlearning.com', '').split('?')[0].strip('/')
        if not clean:
            return m.group(0)

        # Check last segment or whole segment for a known slug
        segments = clean.split('/')
        last = segments[-1]
        if last in SLUG_MAP:
            return f'href="{SLUG_MAP[last]}{anchor}"'
        if clean in SLUG_MAP:
            return f'href="{SLUG_MAP[clean]}{anchor}"'
        return m.group(0)

    return re.sub(r'href=[\"\']([^\"\']+)[\"\']', repl_href, html)

def clean_wp_content(html):
    """Cleanup WordPress HTML for static rendering: shortcodes, images, and links."""
    html = strip_fusion_shortcodes(html)
    # Fix media image paths
    html = re.sub(r'(?:https?://ledgerlearning\.com)?/wp-content/uploads/', '/assets/images/', html)
    # Fix book links
    html = fix_all_book_links(html)
    # Fix general absolute site links
    html = re.sub(r'https?://ledgerlearning\.com/', '/', html)
    return html

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def write_html(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  wrote {os.path.relpath(path, REPO_ROOT)}')

# ── shared nav / footer ──────────────────────────────────────────────────────

def nav_html(depth=0, active='books'):
    def link(href, label, key):
        cls = ' class="active"' if active == key else ''
        return f'<li><a href="/{href}"{cls}>{label}</a></li>'

    return f"""  <header class="site-header">
    <input type="checkbox" id="nav-toggle" class="nav-toggle-input">
    <div class="container nav-container">
      <a href="/" class="brand">
        <div class="brand-text">
          <span class="brand-title">LedgerLearning</span>
          <span class="brand-subtitle">by Kip Twitchell</span>
        </div>
      </a>
      <label for="nav-toggle" class="nav-toggle-btn">
        <span class="icon-open">&#9776;</span>
        <span class="icon-close">&times;</span>
      </label>
      <nav>
        <ul class="nav-links">
          {link('', 'Home', 'home')}
          {link('vlog.html', 'Topics', 'vlog')}
          {link('episodes.html', 'All Episodes', 'episodes')}
          {link('books.html', 'Books', 'books')}
          {link('whitepapers.html', 'White Papers', 'whitepapers')}
          {link('courses.html', 'Courses', 'courses')}
          {link('blog.html', 'Blog', 'blog')}
          {link('about.html', 'About', 'about')}
          <li><a href="https://sharealedger.org/membership.html" target="_blank" rel="noopener" class="nav-btn-highlight">Join Sharealedger</a></li>
        </ul>
      </nav>
    </div>
  </header>"""

def footer_html(depth=0):
    return f"""  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <h4>LedgerLearning</h4>
          <p>Educational gateway for financial systems, accounting history, and ledger innovation.</p>
          <p style="margin-top: 8px;">A project of <a href="https://sharealedger.org" style="color: rgba(255,255,255,0.7);">Sharealedger, NFP</a></p>
          <p style="font-size: 0.78rem; color: rgba(255,255,255,0.4); margin-top: 8px;">&copy; 2016&ndash;2026 Kip M. Twitchell. All rights reserved.</p>
        </div>
        <div class="footer-col">
          <h5>Books</h5>
          <ul>
            <li><a href="/books.html">Books Overview</a></li>
            <li><a href="/books/balancing-act-financial-systems-textbook/on-line-balancing-act-text-book/">Balancing Act</a></li>
            <li><a href="/books/metric-engine/">Metric Engine</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h5>Sharealedger</h5>
          <ul>
            <li><a href="https://sharealedger.org" target="_blank" rel="noopener">Sharealedger.org</a></li>
            <li><a href="https://sharealedger.org/membership.html" target="_blank" rel="noopener">Join (Free)</a></li>
            <li><a href="https://github.com/sharealedger-org" target="_blank" rel="noopener">GitHub</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <div>&copy; 2016&ndash;2026 Kip M. Twitchell. All rights reserved.</div>
        <div><a href="/about.html">About</a></div>
      </div>
    </div>
  </footer>"""

def css_link(depth=0):
    return '  <link rel="stylesheet" href="/assets/css/style.css">'

# ── Side Panel TOC Builder ───────────────────────────────────────────────────

def render_sidebar(current_slug):
    """Render the sticky Table of Contents sidebar for book pages."""
    parts = []
    parts.append('    <aside class="book-sidebar" aria-label="Book Table of Contents">')
    parts.append('      <div class="book-sidebar-header">')
    parts.append(f'        <a href="/{TOC_BASE}/" class="book-sidebar-title">')
    parts.append('          <strong>Balancing Act</strong>')
    parts.append('          <span class="book-sidebar-subtitle">Table of Contents</span>')
    parts.append('        </a>')
    parts.append('      </div>')
    parts.append('      <nav class="book-sidebar-nav">')

    for group in BOOK_STRUCTURE:
        parts.append('        <div class="book-sidebar-group">')
        title = group['title']
        if 'part_slug' in group:
            pslug = group['part_slug']
            purl = '/' + slug_to_url(pslug)
            active_cls = ' class="active"' if current_slug == pslug else ''
            parts.append(f'          <div class="book-sidebar-group-title"><a href="{purl}"{active_cls}>{title}</a></div>')
        else:
            parts.append(f'          <div class="book-sidebar-group-title">{title}</div>')

        parts.append('          <ul class="book-sidebar-list">')
        for islug, ititle in group['items']:
            iurl = '/' + slug_to_url(islug)
            active_cls = ' class="active"' if current_slug == islug else ''
            parts.append(f'            <li><a href="{iurl}"{active_cls}>{ititle}</a></li>')
        parts.append('          </ul>')
        parts.append('        </div>')

    parts.append('      </nav>')
    parts.append('    </aside>')
    return '\n'.join(parts)

def render_mobile_toc(current_slug):
    """Render the mobile collapsible TOC dropdown for narrow screens."""
    parts = []
    parts.append('      <details class="book-toc-toggle">')
    parts.append('        <summary>📖 Table of Contents</summary>')
    parts.append('        <nav class="book-toc-mobile-nav">')

    for group in BOOK_STRUCTURE:
        parts.append('          <div class="book-toc-mobile-group">')
        title = group['title']
        if 'part_slug' in group:
            pslug = group['part_slug']
            purl = '/' + slug_to_url(pslug)
            active_cls = ' class="active"' if current_slug == pslug else ''
            parts.append(f'            <strong><a href="{purl}"{active_cls}>{title}</a></strong>')
        else:
            parts.append(f'            <strong>{title}</strong>')

        parts.append('            <ul>')
        for islug, ititle in group['items']:
            iurl = '/' + slug_to_url(islug)
            active_cls = ' class="active"' if current_slug == islug else ''
            parts.append(f'              <li><a href="{iurl}"{active_cls}>{ititle}</a></li>')
        parts.append('            </ul>')
        parts.append('          </div>')

    parts.append('        </nav>')
    parts.append('      </details>')
    return '\n'.join(parts)

# ── Book page builder ─────────────────────────────────────────────────────────

def build_book_pages(items_by_slug):
    print('\n── Balancing Act book pages ──────────────────────────────────────')

    order = BOOK_ORDER

    for i, slug in enumerate(order):
        if slug not in items_by_slug:
            print(f'  SKIP (not in WXR): {slug}')
            continue

        item = items_by_slug[slug]
        title_raw = extract_tag('title', item)
        title = unescape(re.sub(r'<!\[CDATA\[|\]\]>', '', title_raw)).strip()
        body_raw = extract_cdata('content:encoded', item)
        body = clean_wp_content(body_raw) if body_raw else '<p><em>(No content)</em></p>'

        depth = toc_depth(slug)

        # prev / next navigation
        prev_slug = order[i - 1] if i > 0 else None
        next_slug = order[i + 1] if i < len(order) - 1 else None

        def nav_item(s, direction):
            if not s or s not in items_by_slug:
                return ''
            t_raw = extract_tag('title', items_by_slug[s])
            t = unescape(re.sub(r'<!\[CDATA\[|\]\]>', '', t_raw)).strip()
            url = '/' + slug_to_url(s)
            lbl = '&larr; Previous' if direction == 'prev' else 'Next &rarr;'
            cls = 'prev' if direction == 'prev' else 'next'
            return f'<a href="{url}" class="{cls}"><span class="label">{lbl}</span>{t}</a>'

        chapter_nav = f"""<nav class="chapter-nav">
          {nav_item(prev_slug, 'prev')}
          {nav_item(next_slug, 'next')}
        </nav>"""

        toc_link = f'/{TOC_BASE}/'
        canonical = f'https://ledgerlearning.com/{slug_to_url(slug)}'
        sidebar_html = render_sidebar(slug)
        mobile_toc_html = render_mobile_toc(slug)

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — Balancing Act | LedgerLearning</title>
  <link rel="canonical" href="{canonical}">
{css_link(depth)}
</head>
<body>

{nav_html(depth, 'books')}

  <header class="page-header cream">
    <div class="container" style="max-width: 1240px;">
      <p style="font-size:0.8rem; color:var(--text-muted); margin-bottom:6px;">
        <a href="{toc_link}">Balancing Act</a> &rsaquo;
      </p>
      <h1 class="page-title">{title}</h1>
    </div>
  </header>

  <main class="book-container">

{sidebar_html}

    <div class="book-main">
{mobile_toc_html}

      <article class="prose">
{body}
      </article>

      {chapter_nav}

      <div class="callout mt-24" style="border-left-color: var(--ll-brown);">
        <p>
          <strong>Printable edition:</strong> The full PDF of <em>Balancing Act</em> (v1.5, 2015) is
          available to <a href="https://sharealedger.org/membership.html" target="_blank" rel="noopener"><strong>Sharealedger members</strong></a>
          (free to join).
        </p>
      </div>

    </div>

  </main>

{footer_html(depth)}

</body>
</html>"""

        write_html(slug_to_file(slug), html)

    # Also write redirect stubs for direct appendix URLs if requested without /appendices/
    for app_slug in ['appendix-1-accounting-model', 'appendix-2-event-driven-business-modeling']:
        direct_stub_path = os.path.join(DOCS_DIR, TOC_BASE, app_slug, 'index.html')
        target_url = f'/{TOC_BASE}/appendices/{app_slug}/'
        stub_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0; url={target_url}">
  <link rel="canonical" href="https://ledgerlearning.com{target_url}">
  <title>Redirecting…</title>
</head>
<body>
  <p>Redirecting to <a href="{target_url}">{target_url}</a>…</p>
</body>
</html>"""
        write_html(direct_stub_path, stub_html)


# ── Blog post builder ─────────────────────────────────────────────────────────

def build_post_pages(content):
    print('\n── Blog post pages ───────────────────────────────────────────────')

    items = re.findall(r'<item>(.*?)</item>', content, re.DOTALL)
    posts = []
    for item in items:
        pt = re.search(r'<wp:post_type><!\[CDATA\[(.*?)\]\]>', item)
        if not pt or pt.group(1) != 'post': continue
        status = re.search(r'<wp:status><!\[CDATA\[(.*?)\]\]>', item)
        if not status or status.group(1) != 'publish': continue

        slug_m   = re.search(r'<wp:post_name><!\[CDATA\[(.*?)\]\]>', item)
        date_m   = re.search(r'<wp:post_date><!\[CDATA\[(.*?)\]\]>', item)
        title_m  = re.search(r'<title>(.*?)</title>', item)
        body_m   = re.search(r'<content:encoded><!\[CDATA\[(.*?)\]\]>', item, re.DOTALL)
        excerpt_m = re.search(r'<excerpt:encoded><!\[CDATA\[(.*?)\]\]>', item, re.DOTALL)

        slug    = slug_m.group(1)   if slug_m    else 'post'
        date    = date_m.group(1)   if date_m    else '2000-01-01 00:00:00'
        title   = title_m.group(1)  if title_m   else ''
        body    = body_m.group(1)   if body_m    else ''
        excerpt = excerpt_m.group(1) if excerpt_m else ''

        title   = unescape(re.sub(r'<!\[CDATA\[|\]\]>', '', title)).strip()
        date    = date[:10]

        posts.append((date, slug, title, body, excerpt))

    posts.sort()

    for i, (date, slug, title, body, excerpt) in enumerate(posts):
        try:
            dt = datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            dt = datetime(2000, 1, 1)

        yyyy = dt.strftime('%Y')
        mm   = dt.strftime('%m')
        dd   = dt.strftime('%d')
        date_display = dt.strftime('%B %-d, %Y')

        url_path = f'{yyyy}/{mm}/{dd}/{slug}/'
        file_path = os.path.join(DOCS_DIR, yyyy, mm, dd, slug, 'index.html')
        canonical = f'https://ledgerlearning.com/{url_path}'

        depth = 4

        body_clean = clean_wp_content(body)

        if not excerpt:
            excerpt = re.sub(r'<[^>]+>', '', body_clean)[:200].strip()
            if len(excerpt) == 200:
                excerpt += '…'
        else:
            excerpt = re.sub(r'<[^>]+>', '', excerpt)[:300].strip()

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — LedgerLearning</title>
  <meta name="description" content="{excerpt[:160]}">
  <link rel="canonical" href="{canonical}">
{css_link(depth)}
</head>
<body>

{nav_html(depth, 'blog')}

  <header class="page-header cream">
    <div class="container">
      <p style="font-size:0.8rem; color:var(--text-muted); margin-bottom:6px;">
        <a href="/blog.html">Blog</a> &rsaquo;
      </p>
      <h1 class="page-title">{title}</h1>
      <p class="page-subtitle" style="font-size:0.85rem;">{date_display}</p>
    </div>
  </header>

  <main class="container content-single">
    <div class="prose">
{body_clean}
    </div>

    <div style="margin-top: 40px; padding-top: 24px; border-top: 1px solid var(--ll-border);">
      <a href="/blog.html" class="btn btn-brown btn-sm">&larr; All Posts</a>
    </div>

  </main>

{footer_html(depth)}

</body>
</html>"""

        write_html(file_path, html)

    print(f'  {len(posts)} post pages written')


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    print(f'Reading WXR: {WXR_PATH}')
    content = read_wxr()

    items = re.findall(r'<item>(.*?)</item>', content, re.DOTALL)
    items_by_slug = {}
    for item in items:
        pt = re.search(r'<wp:post_type><!\[CDATA\[(.*?)\]\]>', item)
        if not pt or pt.group(1) != 'page': continue
        slug_m = re.search(r'<wp:post_name><!\[CDATA\[(.*?)\]\]>', item)
        if slug_m:
            items_by_slug[slug_m.group(1)] = item

    build_book_pages(items_by_slug)
    build_post_pages(content)

    print('\nDone.')

if __name__ == '__main__':
    main()
