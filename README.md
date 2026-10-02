# pigrosoft.com

The company site for Pigrosoft. Plain HTML and CSS, no build step, hosted on GitHub Pages.

## What is here

| File | What it is |
| --- | --- |
| `index.html` | The whole home page: welcome, tools, company, help, contact |
| `impressum.html`, `datenschutz.html` | Legal notice and privacy page, English and German |
| `404.html` | The page GitHub Pages shows for a missing URL |
| `assets/style.css` | All the styling, with the colours named at the top |
| `assets/pig.svg`, `assets/pig-awake.svg` | The logo, asleep and awake |
| `assets/pig-animated.svg`, `assets/pig-animated.gif` | The snoozing loop: breathing, Zs and an ear flick |
| `assets/pig-profile-pink.png`, `assets/pig-profile-mulberry.png` | Square pictures for round avatars |
| `assets/logo.png`, `assets/og.png` | Pig plus wordmark, and the link preview image |
| `tools/make_logo.py` | Draws the pig and the tool icons on a pixel grid |
| `CNAME` | Tells GitHub Pages the site answers to pigrosoft.com |

## Changing things

Edit the HTML and push to `main`. The site updates about a minute later.

To add a tool, copy one `<li>` in the Tools window in `index.html` and change the name, the sentence and the link.

To change the pig, edit the shapes in `tools/make_logo.py` and run `python3 tools/make_logo.py` from the repo root (it needs Pillow). It rewrites the SVGs, the favicon and the touch icon.

## Hosting

GitHub Pages serves the `main` branch from the root folder. In the repository settings, under Pages, the source is "Deploy from a branch", `main`, `/ (root)`, and the custom domain is `pigrosoft.com` with "Enforce HTTPS" ticked.

DNS at the registrar:

| Type | Name | Value |
| --- | --- | --- |
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | pigrosoft.github.io |

## Credits

Headings use [Pixelify Sans](https://github.com/eifetx/Pixelify-Sans) under the SIL Open Font License, served from this repo so the site makes no third-party requests.
