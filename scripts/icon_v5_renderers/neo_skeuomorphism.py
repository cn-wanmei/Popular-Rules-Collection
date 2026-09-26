from .common import image_tag,shell

def render(image_href: str,title: str)->str:
    defs='''<filter id="press"><feDropShadow dx="0" dy="16" stdDeviation="14" flood-opacity=".16"/></filter><linearGradient id="metal" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF"/><stop offset=".48" stop-color="#E5EBF4"/><stop offset="1" stop-color="#C8D3E1"/></linearGradient>'''
    body=f'''<rect width="512" height="512" rx="110" fill="#DDE5EF"/><rect x="58" y="58" width="396" height="396" rx="96" fill="url(#metal)" stroke="#FFF" stroke-width="8" filter="url(#press)"/><rect x="94" y="94" width="324" height="324" rx="76" fill="#DCE4EE" stroke="#B6C3D2" stroke-width="7"/><path d="M118 126H364M118 386H352" stroke="#FFF" stroke-width="8" stroke-linecap="round" opacity=".8"/><path d="M124 358V154M388 350V162" stroke="#B4C1D1" stroke-width="6" stroke-linecap="round" opacity=".75"/>{image_tag(image_href,x=132,y=132,size=248)}'''
    return shell(body,title,defs)