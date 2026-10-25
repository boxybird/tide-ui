"""Render the additive review with existing kit styles and one decision source."""
from pathlib import Path
from html import escape
import json
ROOT=Path(__file__).resolve().parent

def output():
    data=json.loads((ROOT/'decisions.json').read_text(encoding='utf-8'))
    rows=[]
    for item in data['decisions']:
        reuse=', '.join(item['reuse']) or 'No new kit block'
        rows.append('<tr><th scope="row">'+escape(item['pattern'])+'</th><td><strong>'+escape(item['decision'])+'</strong><p>'+escape(item['contract'])+'</p><p>Reuse: '+escape(reuse)+'</p></td><td>'+escape(item['hostOwns'])+'</td></tr>')
    states=['<tr>'+''.join(('<th scope="row">' if i==0 else '<td>')+escape(value)+('</th>' if i==0 else '</td>') for i,value in enumerate(row))+'</tr>' for row in data['states']]
    html=(ROOT/'templates/review.html').read_text(encoding='utf-8')
    html=html.replace('{{DECISIONS}}','\n'.join(rows)).replace('{{STATES}}','\n'.join(states)).replace('{{EXAMPLE}}',escape((ROOT/'examples/combined-form.html.txt').read_text(encoding='utf-8')))
    assert '{{' not in html
    return html

if __name__=='__main__':
    (ROOT/'index.html').write_text(output(),encoding='utf-8',newline='\n')
    print('Review generated; existing kit and prototype sources are untouched.')
