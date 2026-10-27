"""Targeted markup-contract checks. This is not a full accessibility-name engine."""
from html.parser import HTMLParser
import re

VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}


def registered_blocks(manifest):
    return ({entry['block'] for entry in manifest['components']}
            | set(manifest['compositions'])
            | {entry['block'] for entry in manifest.get('supportingBlocks',[])})


def registry_entries(manifest):
    return manifest['components']+manifest.get('supportingBlocks',[])+[
        {'block':block,**contract} for block,contract in manifest.get('compositionContracts',{}).items()]


def registry_issues(manifest,root):
    """Every public block needs a reviewable owner, recipe and behavior boundary."""
    issues=[];entries=registry_entries(manifest)
    blocks=[e['block'] for e in entries]
    for block in sorted(set(blocks)):
        if blocks.count(block)>1:issues.append('Duplicate registry owner: '+block)
    for block in manifest.get('compositions',[]):
        if block not in manifest.get('compositionContracts',{}):issues.append('Missing composition contract: '+block)
    for entry in entries:
        block=entry['block']
        for key in ('source','htmlSource','fixture','contract','behavior','styleOwnership'):
            if not isinstance(entry.get(key),str) or not entry[key].strip():issues.append(block+': missing '+key)
        if entry.get('styleOwnership') not in ('kit',):issues.append(block+': invalid styleOwnership')
        for key in ('source','htmlSource','contract'):
            if entry.get(key):
                path=(root/entry[key].split('#')[0]).resolve()
                suffix={'source':'.css','htmlSource':'.html','contract':'.md'}[key]
                if not path.is_relative_to(root.resolve()) or not path.is_file() or path.suffix!=suffix:
                    issues.append(block+': invalid '+key+' home')
        if entry.get('fixture') and ('..' in entry['fixture'].split('/') or not entry['fixture'].endswith('.html') and entry['fixture']!='library'):
            issues.append(block+': invalid fixture')
        for path in entry.get('supportingSources',[]):
            if not (root/path).is_file():issues.append(block+': invalid supporting source')
        for exception in entry.get('consumerStyleExceptions',[]):
            if not exception.get('target') or not exception.get('reason') or not exception.get('properties'):
                issues.append(block+': incomplete consumer style exception')
    return issues


def ownership_issues(classes,manifest,private_blocks=()):
    known=registered_blocks(manifest)|set(private_blocks)|{'tide'}
    blocks={cls.split('__')[0].split('--')[0] for cls in classes}
    return ['Unregistered shared block: '+block for block in sorted(blocks-known)]


def style_ownership_issues(css,manifest):
    css=re.sub(r'/\*.*?\*/','',css,flags=re.S)
    selectors=' '.join(re.findall(r'([^{}]+)\{',css))
    entries=registry_entries(manifest)
    issues=[]
    for entry in entries:
        target=r'\.'+re.escape(entry['block'])+r'(?:__[\w-]+|--[\w-]+)?(?![\w-])'
        if entry.get('styleOwnership')!='kit' or not re.search(target,selectors):continue
        exceptions=entry.get('consumerStyleExceptions',[])
        def matching_selectors(rule):
            # Commas inside :is/:where are not separate selectors. A negative
            # match such as p:not(.tide-eyebrow) does not restyle that block.
            depth=0;start=0;out=[]
            for i,char in enumerate(rule):
                depth+=(char=='(')-(char==')')
                if char==',' and depth==0:out.append(rule[start:i].strip());start=i+1
            out.append(rule[start:].strip())
            return [s for s in out if re.search(target,re.sub(r':not\([^()]*\)','',s))]
        matching=[(s,dict((k.strip(),v.strip()) for k,v in
                   (part.split(':',1) for part in body.split(';') if ':' in part)))
                  for rule,body in re.findall(r'([^{}]+)\{([^{}]*)\}',css) for s in matching_selectors(rule)]
        if not matching:continue
        def permitted(selector,declarations):
            # Reviewed property/value slots, never unrestricted overrides.
            return any(selector.endswith(rule['target']) and
                       all(name in rule['properties'] and value in rule['properties'][name]
                           for name,value in declarations.items()) for rule in exceptions)
        if not exceptions or not matching or any(not permitted(s,d) for s,d in matching):
            issues.append('Kit-owned selectors redefined in app CSS: '+entry['block'])
    return issues


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
