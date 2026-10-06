"""Generate the profile's self-contained animated SVG artwork.

Daily updates use only Python's standard library. Pillow is portrait-only.
"""
from datetime import date, timedelta
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PROFILE = json.loads((ROOT / 'profile.json').read_text())
FONT = 'ui-monospace,SFMono-Regular,Menlo,Consolas,monospace'


def frame(width, height, title):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">', f'<title>{escape(title)}</title>', '<style>text{font-family:' + FONT + '}@media(prefers-reduced-motion:reduce){animate{display:none}}</style>', '<rect width="100%" height="100%" rx="14" fill="#0d1117" stroke="#30363d"/>']


def text(x, y, value, size=13, color='#e6edf3'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}">{escape(str(value))}</text>'


def save(name, parts):
    (ROOT / name).write_text('\n'.join(parts + ['</svg>']) + '\n')
    print('Generated', name)


def info():
    p = frame(490, 302, 'Ahmed Khafaji — terminal profile')
    p += [text(22, 30, '$ neofetch', 14, '#39d353'), '<path d="M20 45H470" stroke="#30363d"/>', text(22, 76, PROFILE['display_name'], 23)]
    rows = [('now', PROFILE['role']), ('prev', PROFILE['previous']), ('stack', ' · '.join(PROFILE['stack'][:4])), ('also', ' · '.join(PROFILE['stack'][4:])), ('github', '@' + PROFILE['username']), ('contact', PROFILE['contact'])]
    for i, (key, value) in enumerate(rows):
        y = 112 + i * 29
        p += ['<g>', text(22, y, key, 12, '#39d353'), text(100, y, value, 12), f'<animate attributeName="opacity" values="0;1" dur="0.35s" begin="{i*.13}s" fill="freeze"/>', '</g>']
    save('info-card.svg', p)


def portrait():
    from PIL import Image, ImageOps, ImageEnhance, ImageDraw
    image = Image.open(ROOT / 'data/avatar.png').convert('RGB')
    image = ImageOps.grayscale(image)
    ImageDraw.floodfill(image, (0, 0), 255, thresh=22)
    image = ImageEnhance.Contrast(image).enhance(1.35)
    image = image.resize((76, 43))
    ramp = '@%#*+=-:. '
    p = frame(490, 302, 'Animated monochrome ASCII portrait of Ahmed Khafaji')
    p += [text(18, 25, '$ cat portrait.txt', 12, '#39d353')]
    for row in range(43):
        line = ''.join(ramp[min(9, image.getpixel((col,row))*10//256)] for col in range(76))
        p += [f'<defs><clipPath id="row{row}"><rect width="490" height="302"><animate attributeName="width" from="0" to="490" dur="0.2s" begin="{row*.025}s" fill="freeze"/></rect></clipPath></defs>', f'<text x="18" y="{43+row*5.6:.1f}" font-size="5.7" textLength="454" lengthAdjust="spacingAndGlyphs" fill="#c9d1d9" xml:space="preserve" clip-path="url(#row{row})">{escape(line)}</text>']
    save('ahmed-ascii.svg', p)


class Calendar(HTMLParser):
    def __init__(self):
        super().__init__(); self.days = {}; self.target = None; self.words = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'td' and a.get('data-date'):
            self.days[a.get('id', a['data-date'])] = dict(date=a['data-date'], level=int(a.get('data-level',0)), count=0)
        if tag == 'tool-tip':
            self.target = a.get('for'); self.words = []
    def handle_data(self, value):
        if self.target: self.words.append(value)
    def handle_endtag(self, tag):
        if tag == 'tool-tip':
            match = re.search(r'([\d,]+) contributions?', ' '.join(self.words))
            if match and self.target in self.days:
                self.days[self.target]['count'] = int(match[1].replace(',',''))
            self.target = None


def fetch():
    user = PROFILE['username']
    if not re.fullmatch(r'[A-Za-z0-9-]{1,39}', user): raise ValueError('Invalid username')
    req = Request(f'https://github.com/users/{user}/contributions', headers={'User-Agent':'profile-art','Accept':'text/html'})
    with urlopen(req, timeout=30) as response: body = response.read().decode()
    parser = Calendar(); parser.feed(body)
    days = sorted(parser.days.values(), key=lambda d:d['date'])
    if len(days) < 350: raise ValueError('Incomplete contribution calendar; refusing to overwrite')
    if any(d['level'] > 0 and d['count'] == 0 for d in days): raise ValueError('Missing contribution counts')
    longest = streak = 0; previous = None
    active = set()
    for d in days:
        dt = date.fromisoformat(d['date'])
        if d['count']:
            active.add(dt); streak = streak+1 if previous == dt-timedelta(days=1) else 1
            longest = max(longest, streak); previous = dt
    cursor = date.today()
    if cursor not in active: cursor -= timedelta(days=1)
    current = 0
    while cursor in active: current += 1; cursor -= timedelta(days=1)
    best = max(days, key=lambda d:d['count'])
    payload = dict(username=user, total_last_year=sum(d['count'] for d in days), days=days, stats=dict(current_streak=current, longest_streak=longest, best_day=best['date'], best_day_count=best['count']))
    (ROOT/'data/contributions.json').write_text(json.dumps(payload,indent=2)+'\n')
    print('Fetched', len(days), 'days;', payload['total_last_year'], 'contributions')


def heatmap():
    data = json.loads((ROOT/'data/contributions.json').read_text())
    days = data['days']; first = date.fromisoformat(days[0]['date'])
    origin = first-timedelta(days=(first.weekday()+1)%7)
    palette = ['#161b22','#0e4429','#006d32','#26a641','#39d353']
    p = frame(1000, 260, 'GitHub contribution calendar for '+data['username'])
    p += [text(24, 31, '$ ./contributions.sh', 16, '#39d353')]
    months = set()
    for d in days:
        dt = date.fromisoformat(d['date']); col = (dt-origin).days//7; row=(dt.weekday()+1)%7
        x=60+col*17; y=72+row*17
        if dt.day <= 7 and (dt.year,dt.month) not in months:
            months.add((dt.year,dt.month)); p.append(text(x,61,dt.strftime('%b'),10,'#8b949e'))
        p += [f'<rect x="{x}" y="{y}" width="12" height="12" rx="3" fill="{palette[max(0,min(4,d["level"]))]}"><title>{d["date"]}: {d["count"]} contributions</title><animate attributeName="opacity" values="0;1" dur="0.3s" begin="{(col+row)*.012:.3f}s" fill="freeze"/></rect>']
    for row,label in [(1,'Mon'),(3,'Wed'),(5,'Fri')]: p.append(text(24,82+row*17,label,10,'#8b949e'))
    stats=data['stats']
    p += [text(24,222,f'{data["total_last_year"]:,} contributions in the last year',18), text(24,245,f'Current streak: {stats["current_streak"]} days  ·  Longest streak: {stats["longest_streak"]} days',12,'#8b949e'),text(806,222,'Less',10,'#8b949e')]
    for i,color in enumerate(palette): p.append(f'<rect x="{838+i*19}" y="212" width="12" height="12" rx="3" fill="{color}"/>')
    p.append(text(936,222,'More',10,'#8b949e'))
    save('contrib-heatmap.svg',p)


if __name__ == '__main__':
    {'fetch':fetch,'heatmap':heatmap,'info':info,'portrait':portrait}[sys.argv[1]]()
