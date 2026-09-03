#!/usr/bin/env python3
"""Emit a fully static index.html. JS is used only to make the disk draggable;
every word of content is in the markup, so the page works with JS disabled."""

import json, math, cmath, re, html

D = json.load(open('site.json'))
SITE_URL = "https://merybria99.github.io"

D['links']['github'] = "Merybria99"

e = html.escape


def slug(s):
    return "p-" + re.sub(r'-+$', '', re.sub(r'[^a-z0-9]+', '-', s.lower()).lstrip('-'))[:60]


# ---------------------------------------------------------------- geodesics
# Arcs orthogonal to the unit circle. For ideal endpoints p, q the centre is
# (p + q) / (1 + p.q) and the radius satisfies |c|^2 = 1 + r^2.
N_IDEAL, STEPS, SEG = 16, [5, 7], 18


def arc_d(p, q):
    dot = p.real * q.real + p.imag * q.imag
    if abs(1 + dot) < 1e-4:
        return f"M{p.real:.4f} {p.imag:.4f}L{q.real:.4f} {q.imag:.4f}"
    c = (p + q) / (1 + dot)
    r2 = abs(c) ** 2 - 1
    if r2 <= 0:
        return f"M{p.real:.4f} {p.imag:.4f}L{q.real:.4f} {q.imag:.4f}"
    r = math.sqrt(r2)
    a1, a2 = cmath.phase(p - c), cmath.phase(q - c)
    d = (a2 - a1 + math.pi) % (2 * math.pi) - math.pi
    pts = []
    for k in range(SEG + 1):
        z = c + r * cmath.exp(1j * (a1 + d * k / SEG))
        pts.append(("M" if k == 0 else "L") + f"{z.real:.4f} {z.imag:.4f}")
    return "".join(pts)


ideal = [cmath.exp(2j * math.pi * i / N_IDEAL) for i in range(N_IDEAL)]
geos = []
for band, step in enumerate(STEPS):
    for i in range(N_IDEAL):
        j = (i + step) % N_IDEAL
        cls = "geo geo-b" if band else "geo"
        geos.append(
            f'<path class="{cls}" data-a="{i}" data-b="{j}" pathLength="1" '
            f'style="animation-delay:{len(geos) * 22}ms" d="{arc_d(ideal[i], ideal[j])}"/>'
        )
GEOS = "\n      ".join(geos)


# ---------------------------------------------------------------- sections
STATUS = {"submitted": "Under submission", "preprint": "Preprint"}

VISIBLE = [p for p in D['publications'] if not p.get('hidden')]
HIDDEN = {p['title'] for p in D['publications'] if p.get('hidden')}

pubs_html = []
for p in VISIBLE:
    tag = ""
    label = STATUS.get(p.get('status'))
    if label and p['venue'] != label:
        tag = f'<span class="tag tag-{p["status"]}">{e(label)}</span>'
    links = ""
    if p.get('links'):
        items = " ".join(
            f'<a href="{e(l["url"])}" rel="noopener">{e(l["label"])}</a>' for l in p['links'])
        links = f'\n        <p class="pub-links">{items}</p>'
    pubs_html.append(f"""      <article class="pub" id="{slug(p['title'])}">
        <p class="pub-yr">{e(p['year'])}</p>
        <div>
          <h3 class="pub-t">{e(p['title'])}</h3>
          <p class="pub-v"><span>{e(p['venue'])}</span>{tag}</p>{links}
          <details class="pub-abs">
            <summary><span class="chev">&#8250;</span><span>Abstract</span></summary>
            <p>{e(p['abstract'])}</p>
          </details>
        </div>
      </article>""")
PUBS = "\n".join(pubs_html)

PUB_SUB = f"{len(VISIBLE)} papers. Abstracts expand in place."

themes_html = []
for t in D['research']:
    shown = [n for n in t['papers'] if n not in HIDDEN]
    block = ""
    if shown:
        refs = "\n            ".join(
            f'<li><a href="#{slug(n)}">{e(n)}</a></li>' for n in shown)
        block = f'\n          <ul class="theme-refs">\n            {refs}\n          </ul>'
    themes_html.append(f"""        <div class="theme">
          <h3 class="theme-h">{e(t['title'])}</h3>
          <p class="theme-b">{e(t['body'])}</p>{block}
        </div>""")
THEMES = "\n".join(themes_html)

bg_html = []
for b in D['background']:
    note = f'\n            <p class="bg-n">{e(b["note"])}</p>' if b.get('note') else ""
    bg_html.append(f"""        <li class="bg-item">
          <p class="bg-p">{e(b['period'])}</p>
          <div>
            <p class="bg-t">{e(b['title'])}</p>
            <p class="bg-o">{e(b['org'])}</p>{note}
          </div>
        </li>""")
BG = "\n".join(bg_html)

schools = "\n          ".join(
    f'<li><span>{e(s["year"])}</span><span>{e(s["name"])}, {e(s["where"])}</span></li>'
    for s in D['schools'])

SHAPES = [
    ("email",    "Email",    lambda v: "mailto:" + v,                    lambda v: v),
    ("scholar",  "Scholar",  lambda v: v,                                 lambda v: "Google Scholar"),
    ("orcid",    "ORCID",    lambda v: "https://orcid.org/" + v,          lambda v: v),
    ("github",   "GitHub",   lambda v: "https://github.com/" + v,         lambda v: v),
    ("bluesky",  "Bluesky",  lambda v: "https://bsky.app/profile/" + v,   lambda v: "@" + v),
    ("linkedin", "LinkedIn", lambda v: "https://linkedin.com/in/" + v,    lambda v: "in/" + v),
    ("cv",       "CV",       lambda v: v,                                 lambda v: "Curriculum vitae (PDF)"),
]
links = dict(D['links']); links['email'] = D['email']
rows, same_as = [], []
for key, label, href, show in SHAPES:
    v = links.get(key)
    if not v:
        continue
    url = href(v)
    rel = ' rel="me noopener"' if url.startswith("http") else ""
    if url.startswith("http"):
        same_as.append(url)
    rows.append(f'<li><span class="el-l">{label}</span>'
                f'<a href="{e(url)}"{rel}>{e(show(v))}</a></li>')
ELSEWHERE = "\n          ".join(rows)

HMETA = [f'<span>{e(D["location"])}</span>',
         f'<a href="mailto:{e(D["email"])}">{e(D["email"])}</a>']
if D['links'].get('cv'):
    HMETA.append(f'<a href="{e(D["links"]["cv"])}">Curriculum vitae</a>')

STATEMENT = "\n        ".join(f'<p>{e(s)}</p>' for s in D['statement'])

# ---------------------------------------------------------------- JSON-LD
graph = [{
    "@type": "Person",
    "@id": SITE_URL + "/#me",
    "name": D['name'],
    "url": SITE_URL,
    "email": "mailto:" + D['email'],
    "jobTitle": "PhD student",
    "affiliation": {"@type": "CollegeOrUniversity", "name": D['affiliation']},
    "alumniOf": {"@type": "CollegeOrUniversity", "name": "University of Salerno"},
    "knowsAbout": ["Adversarial robustness", "Generative model safety",
                   "Hyperbolic representation learning", "Energy-based models",
                   "Vision-language models", "Media forensics"],
    "sameAs": same_as,
}]
for p in VISIBLE:
    graph.append({
        "@type": "ScholarlyArticle",
        "headline": p['title'],
        "datePublished": p['year'],
        "author": {"@id": SITE_URL + "/#me"},
        "publication": p['venue'],
        "abstract": p['abstract'],
        "url": SITE_URL + "/#" + slug(p['title']),
    })
LD = json.dumps({"@context": "https://schema.org", "@graph": graph},
                ensure_ascii=False, indent=1)

DESC = (f"{D['name']} \u2014 {D['role']}, {D['affiliation']}. "
        "Research on the safety and robustness of generative models.")

# ---------------------------------------------------------------- template
tpl = open('template.html').read()
out = (tpl
       .replace("{{LD}}", LD)
       .replace("{{DESC}}", e(DESC))
       .replace("{{URL}}", SITE_URL)
       .replace("{{NAME}}", e(D['name']))
       .replace("{{SHORT}}", e(D['shortName']))
       .replace("{{ROLE}}", e(D['role'] + ", " + D['affiliation']))
       .replace("{{STATEMENT}}", STATEMENT)
       .replace("{{HMETA}}", "\n        ".join(HMETA))
       .replace("{{GEOS}}", GEOS)
       .replace("{{THEMES}}", THEMES)
       .replace("{{PUB_SUB}}", e(PUB_SUB))
       .replace("{{PUBS}}", PUBS)
       .replace("{{BG}}", BG)
       .replace("{{SCHOOLS}}", schools)
       .replace("{{ELSEWHERE}}", ELSEWHERE))

open('/mnt/user-data/outputs/index.html', 'w').write(out)
print("wrote index.html:", len(out), "bytes")
print("unreplaced placeholders:", re.findall(r'\{\{[A-Z_]+\}\}', out) or "none")
