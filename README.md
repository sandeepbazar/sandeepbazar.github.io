# sandeepbazar.github.io

Homepage for **[Sandeep Bazar](https://www.linkedin.com/in/sandeepbazar/)**: <https://sandeepbazar.github.io/>

This is the GitHub **user site**, which is why the repository has to be named
`sandeepbazar.github.io` exactly. An account gets one of these, and it owns the root of the
domain. Every other repository with Pages enabled becomes a project site nested underneath it.

A single hand-written `index.html`: no framework, no build step, no tracker. The only external
request is the IBM Plex webfont from Google Fonts. GitHub Actions publishes the repository root
to Pages on every push to `main`.

## The site map

| URL | Repo | What it is |
|---|---|---|
| `/` | `sandeepbazar.github.io` | This homepage. Was previously `/About/`. |
| `/About/` | `About` | Redirects here. Kept so older links and printed resumes still resolve. |
| `/blogs/` | `blogs` | Long-form writing |
| `/ocm-mcp-server/` | `ocm-mcp-server` | Project documentation |
| `/ai-roadmap-365/` | `ai-roadmap-365` | The curriculum |

Each row is a separate repository and a separate Pages deployment. They cannot share one
navigation bar without duplicating the markup into every repo, so the header nav here uses
in-page anchors for this site's own sections and plain outbound links for the others.

## Layout

| Path | What it is |
|------|------------|
| `index.html` | The whole site: markup, styles and the career chart script |
| `assets/profile.jpg` | Hero headshot (800x800). Replace this file to change the photo. |
| `assets/running.jpg` | Photo for the endurance section |
| `.github/workflows/pages.yml` | Static deploy to GitHub Pages |

## Editing

**Career chart.** The plot and the mobile milestone list are both generated from two arrays
near the bottom of `index.html`: `STEPS` (role changes, as `{year, level, label}`) and `MARKS`
(milestones). Edit those and both views stay in sync. There is no hand-drawn SVG path to
maintain.

**Resume.** Do not put one here. Every variant `build_resumes.py` produces carries a phone
number, an email address and a full postal location in its header, and anything in this
repository is publicly downloadable and indexable. Resumes stay in the jobs project, under
`Apply/`, which is not a git repository and never leaves the machine. Recruiters are pointed at
LinkedIn instead.

## Checks worth repeating after an edit

- No horizontal scroll at 375 px wide.
- Readable in both light and dark colour schemes.
- `prefers-reduced-motion` disables the chart draw-on and scroll reveals.
- Keyboard focus is visible, and every chart milestone is reachable by Tab.
- The canonical link and the two Open Graph URLs still point at the root, not at `/About/`.
- No email address, phone number, postal location or resume PDF anywhere in the repository:

```sh
grep -rn -iE "gmail|9545|tel:|mailto:|maharashtra|pune" . --exclude-dir=.git
```
