from .common import image_tag,shell

def render(image_href: str,title: str)->str:
    defs='''<linearGradient id="accent" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0EA5E9"/><stop offset=".5" stop-color="#6366F1"/><stop offset="1" stop-color="#EC4899"/></linearGradient>'''
    body=f'''<rect width="512" height="512" rx="112" fill="#FFF"/><circle cx="256" cy="256" r="186" fill="#F8FAFC"/><path d="M112 362C146 394 194 412 256 412s110-18 144-50" fill="none" stroke="url(#accent)" stroke-width="10" stroke-linecap="round"/><path d="M148 126h216" stroke="#E2E8F0" stroke-width="5" stroke-linecap="round"/><circle cx="394" cy="124" r="9" fill="#111827"/>{image_tag(image_href,x=126,y=126,size=260)}'''
    return shell(body,title,defs)