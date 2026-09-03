# Academic site — Maria Rosaria Briglia

One self-contained HTML file. No build step, no dependencies, no framework.

## Put it online

Create a **public** repo named exactly `yourusername.github.io`, put `index.html` in the
root, and wait about a minute. It publishes at `https://yourusername.github.io` with no
settings to change. Dragging the file into the GitHub web UI is enough.

From the command line:

```sh
git init
git add index.html
git commit -m "Add academic site"
git branch -M main
git remote add origin git@github.com:yourusername/yourusername.github.io.git
git push -u origin main
```

If you'd rather use a normal repo, push there instead and set **Settings → Pages** to deploy
from `main` / `/ (root)`. The URL becomes `https://yourusername.github.io/reponame`.

Sapienza may also give you space at `di.uniroma1.it` — worth asking, since an institutional
URL carries weight on a paper. This file works unchanged wherever you host it.

## Editing

Open `index.html`. The first thing in the file is a `window.SITE` block holding every piece
of content: your statement, the four research themes, all eleven publications, and your
background. Nothing below that block needs touching.

**Adding a paper.** Copy any existing entry in `publications` and edit it. Keep them ordered
newest first — the page renders them in array order and does not sort. `status` takes
`"published"`, `"preprint"`, or `"submitted"`; only the last two draw a tag.

**Adding links to a paper.** Each entry accepts an optional `links` array:

```js
links: [
  { label: "arXiv", url: "https://arxiv.org/abs/2406.xxxxx" },
  { label: "PDF",   url: "https://..." },
  { label: "Code",  url: "https://github.com/..." }
]
```

This is the single highest-value thing you can add. Right now a reader who wants to actually
read a paper has nowhere to click.

**Research themes.** Each theme lists papers by title. The titles must match the
`publications` entries *character for character* — that's what makes them clickable and
scrolls to the paper with its abstract open. A typo silently degrades the link to plain text,
so paste rather than retype.

**Empty sections disappear.** `teaching` and `service` are empty arrays and render nothing
until you add entries. Same for the `Code` section: set `githubUser` and it appears, filled
from the GitHub API; leave it blank and it stays hidden.

## What I left out of your CV, and why

- **Home address, both phone numbers, date of birth, gender.** A public page gets scraped.
  Keep these for the PDF you send to named people.
- **Full exam lists with grades, and language certifications.** Standard on an Italian CV,
  unusual on an academic homepage — the publication list is doing that work now.
- **The soft-skills list** (proactive, problem solving, team working). These don't carry
  information on a page that has eleven papers on it.
- **The technical skills list.** I can add it back as a short line if you want it; I'd
  suggest keeping it off, since PyTorch and Linux are assumed at this level.
- **Your CV PDF.** Not included on purpose. Make a public version with the personal details
  stripped, commit it as `cv.pdf`, then set `links.cv` to `"cv.pdf"`.

## Three things in your CV worth fixing

1. **Two papers are dated 2025 but list ICLR 2026 as the venue** — *What is Adversarial
   Training for Diffusion Models?* and *Implicit Inversion turns CLIP into a Decoder*. I kept
   your years verbatim, so they currently sort below the 2026 entries. If ICLR 2026 is right,
   change `year` to `"2026"` for both.
2. **Your M.Sc. entry still reads as in progress**, with an expected graduation date of
   September 2023 and a "minimum expected grade" of 110. Two years stale. I rewrote it as
   completed but left the final grade out, since I don't know what it was — worth adding.
3. **Two awards didn't make it across**: the courses reserved for excellent students (2023),
   and the recognition for an outstanding academic career, which I folded into the B.Sc.
   note. If you'd like an Awards section of its own, say so.

## Notes

- Fonts come from Google Fonts (Faustina and Archivo). To drop that dependency, delete the
  two `preconnect` tags and the stylesheet link — the CSS falls back to system fonts.
- A dark palette follows the visitor's system setting. The print stylesheet hides the
  navigation and the disk and collapses abstracts, so the page prints as a clean CV-like
  summary.
- The Poincaré disk is computed, not drawn: geodesics are circular arcs orthogonal to the
  boundary, and dragging applies a Möbius isometry. It degrades to a static figure under
  `prefers-reduced-motion`.
