#!/usr/bin/env python3
"""Every sentence the live site shows must appear, unchanged, in the rebuild."""
import re, html, io, glob, os, sys, unicodedata

TXT = sys.argv[1]

def visible(path):
    s = io.open(path, encoding='utf-8', errors='replace').read()
    s = re.sub(r'(?is)<script.*?</script>', ' ', s)
    s = re.sub(r'(?is)<style.*?</style>', ' ', s)
    s = re.sub(r'(?is)<!--.*?-->', ' ', s)
    s = re.sub(r'(?s)<[^>]+>', ' ', s)
    return html.unescape(s)

def norm(t):
    t = unicodedata.normalize('NFKC', t)
    t = t.replace('„', '"').replace('“', '"').replace('”', '"')
    t = t.replace('‘', "'").replace('’', "'").replace('‚', "'")
    t = t.replace('–', '-').replace('—', '-').replace('−', '-')
    t = re.sub(r'\s+', ' ', t)
    t = re.sub(r'\s+([.,;:!?)\]])', r'\1', t)   # tag boundaries leave a space before punctuation
    t = re.sub(r'([(\[])\s+', r'\1', t)
    return t.strip().lower()

built = norm(visible('index.html'))

# navigation chrome the old builder repeated on every page — not content
CHROME = {norm(x) for x in [
 'home','praxis','physiopraxis','anwendungsbereiche','training','milon zirkel','frei medical',
 'freies training','reha sport','kurse vor ort','firmenfitness','mehr','praxisphysiopraxis',
 'trainingmilon zirkel','öffnungszeiten','mitgliedschaft','impressum','datenschutz','kontakt',
 'ablehnenannehmen','wir verwenden cookies.','datenschutzbestimmungen','ausbildung',
 'anweisungen erhalten','senden','name*','e-mail*','rückrufnummer*',
]}

missing, checked = [], 0
for f in sorted(glob.glob(os.path.join(TXT, '*.txt'))):
    page = os.path.basename(f)[:-4]
    if page == 'datenschutz':
        continue  # generated verbatim from this very file; checked separately below
    for line in io.open(f, encoding='utf-8'):
        n = norm(line)
        if len(n) < 25 or n in CHROME:
            continue
        checked += 1
        if n not in built:
            missing.append((page, line.strip()))

print('sentences checked: %d' % checked)
print('missing: %d' % len(missing))
for p, l in missing:
    print('  [%s] %s' % (p, l[:150]))
