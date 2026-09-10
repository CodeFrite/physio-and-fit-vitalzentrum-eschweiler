#!/usr/bin/env python3
"""Concatenate src/*.html into the deployable index.html."""
import io, glob, os

ORDER = ['01-head','02-chrome','10-home','20-praxis','30-training','40-kurse','50-firma-mitglied','60-zeiten-kontakt','70-stellen',
         '75-datenschutz','80-footer','90-script']

parts = []
for name in ORDER:
    p = 'src/%s.html' % name
    if not os.path.exists(p):
        raise SystemExit('missing part: ' + p)
    parts.append(io.open(p, encoding='utf-8').read())

doc = '\n'.join(parts)

ds = io.open('build/datenschutz-body.html', encoding='utf-8').read()
assert '<!--DATENSCHUTZ_BODY-->' in doc
doc = doc.replace('<!--DATENSCHUTZ_BODY-->', ds)

io.open('index.html', 'w', encoding='utf-8').write(doc)
print('index.html:', len(doc), 'bytes,', doc.count('<section class="page"'), 'pages')
