#!/usr/bin/env python3
"""Turn the site's own Datenschutzerklärung plain text into structured HTML.
Words are never altered — only numbering markers are lifted out into <span class="sn">."""
import re, html, io, sys

SRC = sys.argv[1]
OUT = sys.argv[2]

raw = io.open(SRC, encoding='utf-8').read().split('\n')

# the policy runs from "Datenschutzerklärung" to the sentence that closes section 5
start = raw.index('Datenschutzerklärung')
end = next(i for i, l in enumerate(raw) if l.startswith('Der aktuelle Stand dieser Datenschutzerklärung'))
lines = [l.strip() for l in raw[start + 1:end + 1] if l.strip()]

HEAD = re.compile(r'^(\d+(?:\.\d+)*)\.?(?=[A-ZÄÖÜ„‚])(.+)$')
BULLET = re.compile(r'^[••]\s*(.+)$')
ALPHA = re.compile(r'^([a-h])\)\s*(.*)$')
URL = re.compile(r'https?://[^\s<>"]+')

def esc(t):
    t = html.escape(t, quote=False)
    def link(m):
        u = m.group(0)
        tail = ''
        # never swallow the sentence punctuation that follows a URL
        while u and u[-1] in '.,;:':
            tail = u[-1] + tail; u = u[:-1]
        while u.endswith(')') and u.count('(') < u.count(')'):
            tail = ')' + tail; u = u[:-1]
        return '<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>%s' % (u, u, tail)
    t = URL.sub(link, t)
    t = re.sub(r'(?<![\w.])([\w.+-]+@[\w-]+\.[\w.]+)', r'<a href="mailto:\1">\1</a>', t)
    return t

out, li = [], []

def flush():
    if li:
        out.append('<ul>' + ''.join('<li>%s</li>' % x for x in li) + '</ul>')
        li.clear()

for l in lines:
    m = BULLET.match(l)
    if m:
        li.append(esc(m.group(1)))
        continue
    m = ALPHA.match(l)
    if m and len(l) > 12:
        li.append('<span class="sn">%s)</span> %s' % (m.group(1), esc(m.group(2))))
        continue
    flush()
    m = HEAD.match(l)
    if m:
        num, title = m.group(1), m.group(2).strip()
        depth = num.count('.')
        tag = ['h3', 'h4', 'h5'][min(depth, 2)]
        out.append('<%s><span class="sn">%s</span> %s</%s>' % (tag, num, html.escape(title), tag))
        continue
    if l.endswith(':') and len(l) < 90:
        out.append('<h5>%s</h5>' % esc(l))
        continue
    out.append('<p>%s</p>' % esc(l))
flush()

io.open(OUT, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('sections:', sum(1 for o in out if o.startswith('<h3')), '| blocks:', len(out), '| bytes:', sum(len(o) for o in out))
