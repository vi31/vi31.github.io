import os, re, random, sys

ICONS = '/home/claude/doodle/lib/node_modules/lucide-static/icons'
OUT = '/home/claude/doodle/out'

SETS = {
    'about': ['user-round','mail','map-pin','graduation-cap','briefcase','coffee','heart','send','phone','at-sign','file-user','hand','smile','globe','calendar','book-open','award','message-circle','camera','music','plane','mountain','house','handshake','sparkles','contact','id-card','languages','tree-pine','bike','sun','headphones'],
    'home': ['laptop', 'pen-tool', 'pencil', 'message-circle', 'users', 'lightbulb', 'code',
             'coffee', 'book-open', 'search', 'sparkles', 'mouse-pointer-2', 'layout-dashboard',
             'git-branch', 'presentation', 'sticky-note', 'monitor', 'notebook-pen', 'puzzle',
             'rocket', 'graduation-cap', 'mic', 'brain', 'target', 'handshake', 'messages-square',
             'keyboard', 'palette', 'headphones', 'calendar'],
    'projects': ['laptop', 'monitor', 'code', 'terminal', 'git-branch', 'layers', 'layout-dashboard',
                 'rocket', 'puzzle', 'database', 'smartphone', 'cpu', 'wrench', 'package',
                 'square-kanban', 'chart-line', 'workflow', 'bot', 'users', 'cloud', 'braces',
                 'git-pull-request', 'flask-conical', 'component', 'server', 'mouse-pointer-2',
                 'app-window', 'blocks', 'bug', 'keyboard'],
    'teardowns': ['search', 'scan-search', 'microscope', 'layers', 'wrench', 'scissors', 'ruler',
                  'mouse-pointer-click', 'eye', 'list-checks', 'split', 'smartphone', 'thumbs-up',
                  'thumbs-down', 'lightbulb', 'target', 'puzzle', 'clipboard-list', 'zoom-in',
                  'app-window', 'message-circle-question', 'route', 'gauge', 'scale', 'star',
                  'panels-top-left', 'hand', 'funnel', 'flag', 'circle-help'],
    'blog': ['pencil', 'pen-line', 'pen-tool', 'notebook-pen', 'book-open', 'quote', 'message-circle',
             'type', 'feather', 'newspaper', 'coffee', 'bookmark', 'highlighter', 'file-text',
             'lightbulb', 'rss', 'sticky-note', 'text-cursor', 'library', 'mail', 'notebook',
             'eraser', 'heading', 'list', 'glasses', 'send', 'message-square-text', 'at-sign',
             'scroll-text', 'paperclip'],
}

MODES = {
    # (purple, green, opacity)
    'dark': ('#BFA0FF', '#C8F55A', 0.46),
    'light': ('#6B3FD9', '#5A8A00', 0.4),
}

N, CELL = 6, 80
TILE = N * CELL


def inner(name):
    p = os.path.join(ICONS, name + '.svg')
    if not os.path.exists(p):
        return None
    s = open(p).read()
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    m = re.search(r'<svg[^>]*>(.*)</svg>', s, flags=re.S)
    return re.sub(r'\s*\n\s*', '', m.group(1)).strip()


def filler(rnd, x, y, col):
    k = rnd.choice(['dot', 'plus', 'ring', 'dash'])
    if k == 'dot':
        return f'<circle cx="{x}" cy="{y}" r="1.8" fill="{col}" stroke="none"/>'
    if k == 'ring':
        return f'<circle cx="{x}" cy="{y}" r="3.2" stroke="{col}"/>'
    if k == 'plus':
        return f'<path d="M{x-4} {y}h8M{x} {y-4}v8" stroke="{col}"/>'
    a = rnd.choice([-1, 1])
    return f'<path d="M{x-5} {y+3*a}q2.5 {-6*a} 5 {-3*a}t5 {-3*a}" stroke="{col}"/>'


def build(setname, mode, seed):
    rnd = random.Random(seed)
    purple, green, op = MODES[mode]
    names = [n for n in SETS[setname] if inner(n)]
    missing = [n for n in SETS[setname] if not inner(n)]
    if missing:
        print('missing', setname, missing, file=sys.stderr)
    rnd.shuffle(names)
    pool = (names * 3)[:32]
    # avoid same icon adjacent: simple reshuffle of second pass
    parts = []
    fills = []
    S = 60  # diagonal lattice: points where (a+b) is even -> rows run at 45 degrees
    i = 0
    for a in range(8):
        for b in range(8):
            px, py = a * S + S / 2, b * S + S / 2
            if (a + b) % 2 == 0:
                name = pool[i]; i += 1
                col = purple if ((a - b) // 2 + (1 if rnd.random() < .15 else 0)) % 2 == 0 else green
                cx = px + rnd.uniform(-7, 7); cy = py + rnd.uniform(-7, 7)
                rot = rnd.uniform(-24, 24)
                sc = rnd.choice([1.1, 1.25, 1.25, 1.4])
                parts.append(
                    f'<g transform="translate({cx:.1f} {cy:.1f}) rotate({rot:.0f}) scale({sc}) translate(-12 -12)" '
                    f'stroke="{col}" stroke-width="{1.75/sc:.2f}">{inner(name)}</g>')
            elif rnd.random() > .25:
                fills.append(filler(rnd, round(px + rnd.uniform(-6, 6), 1), round(py + rnd.uniform(-6, 6), 1),
                                    rnd.choice([purple, green])))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{TILE}" height="{TILE}" viewBox="0 0 {TILE} {TILE}" '
           f'fill="none" stroke-linecap="round" stroke-linejoin="round" opacity="{op}">'
           f'<g stroke-width="1.5">{"".join(fills)}</g>{"".join(parts)}</svg>')
    fn = os.path.join(OUT, f'doodle-{setname}-{mode}.svg')
    open(fn, 'w').write(svg)
    return fn


for si, s in enumerate(SETS):
    for m in MODES:
        print(build(s, m, 31 + si), os.path.getsize(os.path.join(OUT, f'doodle-{s}-{m}.svg')))
