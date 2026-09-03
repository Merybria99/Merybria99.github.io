# merybria99.github.io

Personal academic site for Maria Rosaria Briglia. One self-contained HTML file,
no build step and no dependencies.

## What changed in this version

The first version rendered all of its content with JavaScript from a config
object. That was a mistake on a site whose job is to make papers findable: a
crawler that doesn't execute JS saw four headings and nothing else. Google runs
JS, but Bing, DuckDuckGo, most academic aggregators and archive.org snapshots
don't, and neither does anyone browsing with JS off.

This version is static. Every word is in the markup — 2,172 words visible with
JavaScript disabled, against roughly 30 before. Specifically:

- All content, including the eleven abstracts, is plain HTML.
- The Poincaré disk's 32 geodesics are pre-computed and written into the SVG.
  The intro animation is pure CSS. JavaScript only adds the drag, and the page
  is complete without it.
- Abstracts use native `<details>`, so they expand with no script at all.
- Research-theme paper references are real anchors, so they work as permalinks —
  `#p-not-all-latent-spaces-are-flat-hyperbolic-concept-control` links straight
  to that paper, which is handy in an email.
- Added `schema.org` JSON-LD describing you and all eleven papers, plus a
  canonical URL and Open Graph tags for link previews.

## Deploying an update

You already have the repo. To publish a change:

```sh
git add index.html
git commit -m "Update publications"
git push
```

Live in under a minute. If you uploaded through the GitHub web UI and your local
clone is now behind, run `git pull --rebase origin main` before pushing.

For a one-line change, editing the file directly on GitHub (click it, hit the
pencil icon) is entirely reasonable.

## Editing

**For small changes**, edit `index.html`. It's readable HTML — to add an arXiv
link to a paper, find its `<article class="pub">` block and add:

```html
<p class="pub-links">
  <a href="https://arxiv.org/abs/2406.xxxxx" rel="noopener">arXiv</a>
  <a href="https://github.com/Merybria99/..." rel="noopener">Code</a>
</p>
```

right after the `<p class="pub-v">` line.

**For bigger changes**, the three optional files regenerate the page:

```sh
python3 build.py    # reads site.json + template.html, writes index.html
```

`site.json` holds all the content, `template.html` the markup and styling.
Adding a paper there is cleaner than hand-editing HTML. You never have to use
this — `index.html` stands alone, and the generator is only a convenience.
If you do use it, commit the regenerated `index.html`, since that's what
GitHub Pages serves.

## Your photo, and where the disk went

The portrait sits in the hero. Rather than crowd it in next to the Poincaré
disk, the disk moved down into the *geometry of representation space* thread,
where it stops being decoration and starts illustrating the two papers next to
it. It is still draggable.

Three image files, all with metadata stripped:

| file | size | use |
|---|---|---|
| `portrait-640.jpg` | 98 KB | portrait, retina screens |
| `portrait-320.jpg` | 29 KB | portrait, standard screens |
| `og.jpg` | 71 KB | link previews on LinkedIn, Slack, WhatsApp |

The `<img>` uses `srcset`, so phones download the 29 KB file rather than the
98 KB one. All three must sit next to `index.html` in the repo root, or the
photo breaks.

Your original had no EXIF — LinkedIn had already stripped it — so there was no
GPS or device data to remove. Worth checking if you ever swap in a photo
straight off your phone, since those usually do carry coordinates. The crop also
took the passer-by out of the background.

To replace it: crop square-ish, export at 640x800 and 320x400, keep the same
filenames. Or send me a new photo.

## Papers under submission are hidden

The three papers under review are excluded from the page: *Architectural
Backdoors*, *Mind the Modality Gap*, and *Anchored Protein Engineering*. They
carry `"hidden": true` in `site.json` and are skipped everywhere — the list, the
research-thread references, and the structured data.

They are **not** left in as HTML comments. A commented-out abstract is still
readable in view-source, and a reviewer searching a distinctive phrase from your
own paper would find it on your site. Hiding it has to mean absent, not folded.

To un-hide one on acceptance, delete its `"hidden": true` line, update `venue`
and `status`, and rebuild:

```sh
python3 build.py
git add index.html site.json && git commit -m "Add accepted paper" && git push
```

If you'd rather not use the generator, copy the paper's block from an older
`index.html` and paste it into the publication list in the right year order.

Two threads now cite a single paper each, because most of their work is under
review. That reads as thin. Options when you want to address it: fold *Threats
to generative media* into the geometry thread, or leave it — the prose describes
the direction honestly without naming unpublished work, which is what a research
statement is for.

## Still open

1. **Co-authors.** The list shows titles only. An academic bibliography normally
   gives the full author line with your own name in bold. For the multi-author
   collaborations this reads as an omission.
2. **Links to the papers.** Nobody can currently read any of them from this page.
   The highest-value thing to add.
3. **Your email.** The site shows `briglia@di.uniroma1.it`, from your CV, but you
   configured git with `mariarosaria.briglia@uniroma1.it`. Pick one.
4. **Advisor and lab.** Almost every PhD page names both; yours names neither.
5. **Scholar, ORCID, LinkedIn.** `links` in `site.json` has slots waiting.
6. Two papers are dated 2025 but list ICLR 2026 as the venue — *What is
   Adversarial Training for Diffusion Models?* and *Implicit Inversion turns CLIP
   into a Decoder*. They currently sort below the 2026 entries.
7. Your M.Sc. final grade, which I left out because your CV only gave an
   expected minimum.
8. An `alt` text sanity check. I described the photo as a Renaissance palazzo
   courtyard in Rome from what I could see — correct it if it's somewhere else,
   since that text is what screen readers announce.

## Deliberately left off your CV

Home address, both phone numbers, date of birth, gender, the full exam lists,
and the soft-skills list. A public page gets scraped.

**Don't commit your current CV PDF.** Git keeps every version permanently, so
deleting it later would not remove it from a public repo's history. Strip the
personal details first, then commit it as `cv.pdf` and set `links.cv` to
`"cv.pdf"`.

## Palette

Drawn from the portrait: magenta lilies, eucalyptus foliage, warm stone.

| variable | light | dark | role |
|---|---|---|---|
| `--paper` | `#f9f2f3` | `#1a1418` | page ground |
| `--paper-deep` | `#f1e3e7` | `#221a20` | banded sections |
| `--ink` | `#2c1d28` | `#f2e8ec` | body text, a deep aubergine rather than black |
| `--ink-soft` | `#755c6a` | `#ac95a3` | secondary text |
| `--plum` | `#8f2555` | `#e895b4` | your name, section headings |
| `--sage` | `#3f6559` | `#8fbfac` | links, the cool counterpoint |
| `--rule` | `#e3d5da` | `#3a2e36` | hairlines |

The sage is doing real work: an all-rose page drifts saccharine, and the green
holds it back. Every pair passes WCAG AA in both modes — the weakest is
secondary text on the banded background at 4.83:1 against a 4.5 threshold, so
if you darken `--paper-deep` much further, darken `--ink-soft` with it.

All seven live in the `:root` block at the top of the `<style>` section, and
again in the dark-mode block below it. Changing a colour means editing both.
`--plum` and `--sage` also appear as literal hex inside the favicon data URI, so
that needs the third edit if you want it to match.

## Notes

Fonts are Faustina and Archivo from Google Fonts; delete the two `preconnect`
tags and the stylesheet link to drop that dependency and fall back to system
fonts. A dark palette follows the visitor's system setting. The print stylesheet
hides the navigation and the disk and collapses abstracts, so the page prints as
a clean summary.
