from .common import image_tag,shell

def render(image_href: str,title: str)->str:
    defs='''<filter id="mbe-shadow"><feDropShadow dx="0" dy="10" stdDeviation="8" flood-opacity=".16"/></filter>'''
    body=f'''<rect width="512" height="512" rx="116" fill="#FFFDF8"/><path d="M88 184c-12-72 52-128 118-104 48-56 140-22 142 48 76 0 126 90 72 148 24 82-58 152-130 114-58 58-164 30-176-40-82 2-128-80-26-166z" fill="#F4F7FF" stroke="#111827" stroke-width="12" filter="url(#mbe-shadow)" stroke-linejoin="round"/><circle cx="110" cy="128" r="12" fill="#7C3AED"/><circle cx="402" cy="152" r="12" fill="#06B6D4"/><circle cx="406" cy="382" r="12" fill="#EC4899"/><path d="M98 122L62 92M408 116l36-32M106 396l-36 32M402 398l38 28" stroke="#111827" stroke-width="10" stroke-linecap="round"/>{image_tag(image_href,x=142,y=142,size=228)}'''
    return shell(body,title,defs)