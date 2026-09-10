#!/usr/bin/env python3
"""Single-file build for the Artifact viewer: images inlined as data URIs,
document skeleton removed (the viewer supplies its own)."""
import io, re, base64, os, mimetypes

src = io.open('index.html', encoding='utf-8').read()

def inline(m):
    path = m.group(1)
    mime = mimetypes.guess_type(path)[0] or 'image/jpeg'
    data = base64.b64encode(open(path, 'rb').read()).decode('ascii')
    return 'src="data:%s;base64,%s"' % (mime, data)

out, n = re.subn(r'src="(assets/img/[^"]+)"', inline, src)

# the viewer wraps the file in its own <!doctype>/<html>/<head>/<body>
out = re.sub(r'(?s)^.*?<meta name="viewport"[^>]*>\s*', '', out)
out = out.replace('</head>', '').replace('<body>', '')
out = out.replace('</body>', '').replace('</html>', '')
out = out.strip()

os.makedirs('dist', exist_ok=True)
io.open('dist/vitalzentrum.html', 'w', encoding='utf-8').write(out)
print('inlined %d images -> dist/vitalzentrum.html  %.2f MB' % (n, len(out.encode()) / 1e6))
print('starts with:', out[:70].replace('\n', ' '))
