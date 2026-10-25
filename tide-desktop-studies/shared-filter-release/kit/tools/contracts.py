"""Targeted markup-contract checks. This is not a full accessibility-name engine."""
from html.parser import HTMLParser
import re

VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}


def registered_blocks(manifest):
    return ({entry['block'] for entry in manifest['components']}
            | set(manifest['compositions'])
            | {entry['block'] for entry in manifest.get('supportingBlocks',[])})


def ownership_issues(classes,manifest,private_blocks=()):
    known=registered_blocks(manifest)|set(private_blocks)|{'tide'}
    blocks={cls.split('__')[0].split('--')[0] for cls in classes}
    return ['Unregistered shared block: '+block for block in sorted(blocks-known)]


def style_ownership_issues(css,manifest):
    css=re.sub(r'/\*.*?\*/','',css,flags=re.S)
    selectors=' '.join(re.findall(r'([^{}]+)\{',css))
    entries=manifest['components']+[
        {'block':block,**contract} for block,contract in manifest.get('compositionContracts',{}).items()]
    return ['Kit-owned selectors redefined in app CSS: '+entry['block'] for entry in entries
            if entry.get('styleOwnership')=='kit'
            and re.search(r'\.'+re.escape(entry['block'])+r'(?:__[\w-]+|--[\w-]+)?(?![\w-])',selectors)]


class ContractScan(HTMLParser):
    def __init__(self):
        super().__init__();self.nodes=[];self.stack=[]
    def handle_starttag(self,tag,attrs):
        node={'tag':tag,'attrs':dict(attrs),'text':''}
        self.nodes.append(node)
        if tag not in VOID:self.stack.append(node)
    def handle_endtag(self,tag):
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i]['tag']==tag:
                del self.stack[i:];break
    def handle_data(self,data):
        if any(n['attrs'].get('aria-hidden')=='true' for n in self.stack):return
        for node in self.stack:node['text']+=data


def markup_issues(html):
    scan=ContractScan();scan.feed(html);issues=[]
    ids={n['attrs']['id']:n for n in scan.nodes if n['attrs'].get('id')}
    for node in scan.nodes:
        attrs=node['attrs'];classes=attrs.get('class','').split()
        for cls in classes:
            if '--' in cls and cls.split('--')[0] not in classes:
                issues.append('Modifier without its base class: '+cls)
        if attrs.get('tabindex','').lstrip('+').isdigit() and int(attrs['tabindex'])>0:
            issues.append('Positive tabindex changes natural focus order')
        if node['tag']=='img' and 'alt' not in attrs and attrs.get('aria-hidden')!='true':
            issues.append('Image missing an alt attribute')
        if 'aria-pressed' in attrs and node['tag']!='button' and attrs.get('role')!='button':
            issues.append('aria-pressed belongs on a toggle button')
        if node['tag'] in {'a','button'} and not (node['tag']=='a' and 'href' not in attrs):
            labelled=any(ids.get(ref,{}).get('text','').strip() for ref in attrs.get('aria-labelledby','').split())
            if not (attrs.get('aria-label','').strip() or labelled or node['text'].strip()):
                issues.append('Link/button missing an authored accessible name')
    if len([n for n in scan.nodes if n['tag']=='main'])!=1:issues.append('Document must have one main landmark')
    if len([n for n in scan.nodes if n['tag']=='h1'])!=1:issues.append('Document must have one primary h1')
    return issues
