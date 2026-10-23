# pigrosoft.com

The company site for Pigrosoft. Plain HTML and CSS, no build step, hosted on GitHub Pages.

## What is here

| File | What it is |
| --- | --- |
| `index.html` | The whole home page: welcome, tools, company, help, contact |
| `impressum.html`, `datenschutz.html` | Legal notice and privacy page, English and German |
| `404.html` | The page GitHub Pages shows for a missing URL |
| `assets/style.css` | All the styling, with the colours named at the top (paper, ink, rose, burgundy) |
| `assets/pigrun.js` | PIGRUN.EXE, the runner game under the welcome window. It plays itself until someone clicks, and stores nothing |
| `brand/pigrosoft/` | The brand kit files, never edited: wordmarks (ink, paper, accent), the animated pig GIF and the two profile pictures |
| `assets/pig.svg`, `assets/pig-awake.svg` | The small pig used for the favicon, and the awake pig for the click on the home page |
| `tools/make_logo.py` | Draws the pig and the tool icons on a pixel grid |
| `CNAME` | Tells GitHub Pages the site answers to pigrosoft.com |

## Changing things

Edit the HTML, push to `main`, then copy `main` onto the branch the live site is built from with `git push origin main:gh-pages`. The site updates about a minute later.

To add a tool, copy one `<li>` in the Tools window in `index.html` and change the name, the sentence and the link.

To change the pig, edit the shapes in `tools/make_logo.py` and run `python3 tools/make_logo.py` from the repo root (it needs Pillow). It rewrites the SVGs, the favicon and the touch icon.

## Hosting

GitHub Pages serves the `gh-pages` branch from the root folder, and `main` is the working copy. To publish straight from `main` and drop the extra branch, open the repository settings, go to Pages, and set the source to "Deploy from a branch", `main`, `/ (root)`. The custom domain is `pigrosoft.com`, set by the `CNAME` file. Once DNS points here, tick "Enforce HTTPS" on the same settings page.

DNS at the registrar (Porkbun):

| Type | Name | Value |
| --- | --- | --- |
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | pigrosoft.github.io |

## Credits

Pixelify Sans (SIL Open Font License) is served from this repo and used only for the lettering inside the PIGRUN.EXE game, so the site makes no third-party requests.
