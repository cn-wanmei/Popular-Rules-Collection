from __future__ import annotations

import base64

def xml_escape(value: str) -> str:
    return str(value).replace('&','&amp;').replace(chr(34),'&quot;').replace('<','&lt;').replace('>','&gt;')

def svg_data_url(content: bytes, kind: str) -> str:
    mime={'svg':'image/svg+xml','png':'image/png','webp':'image/webp','ico':'image/x-icon','jpg':'image/jpeg'}[kind]
    return 'data:' + mime + ';base64,' + base64.b64encode(content).decode('ascii')

def image_tag(href: str, *, x: int, y: int, size: int, opacity: float = 1.0, extra: str = '') -> str:
    return (f'<image href="{href}" x="{x}" y="{y}" width="{size}" height="{size}" '
            f'preserveAspectRatio="xMidYMid meet" opacity="{opacity}" {extra}/>')

def shell(body: str, title: str, defs: str = '') -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" role="img" aria-label="{xml_escape(title)}"><defs>{defs}</defs>{body}</svg>'''