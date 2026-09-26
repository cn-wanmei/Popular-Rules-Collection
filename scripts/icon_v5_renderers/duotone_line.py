from .common import image_tag,shell

def render(image_href: str,title: str)->str:
    defs='''<linearGradient id="duo" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#111827"/><stop offset=".5" stop-color="#4F46E5"/><stop offset="1" stop-color="#06B6D4"/></linearGradient>'''
    body=f'''<rect width="512" height="512" rx="110" fill="#FFF"/><path d="M96 172V112h60M356 112h60v60M416 340v60h-60M156 400H96v-60" fill="none" stroke="#111827" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/><path d="M116 256h280M256 116v280" fill="none" stroke="url(#duo)" stroke-width="8" stroke-linecap="round" stroke-dasharray="18 16"/><circle cx="256" cy="256" r="134" fill="none" stroke="#CBD5E1" stroke-width="5"/>{image_tag(image_href,x=144,y=144,size=224,opacity=.94)}'''
    return shell(body,title,defs)