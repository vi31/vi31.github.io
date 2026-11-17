# vi31.github.io

Personal portfolio for Vibha Govind Hegde. A static [Jekyll](https://jekyllrb.com) site with a custom
"Studio" design in a dark and a light theme, hosted on GitHub Pages. No pre-made theme, no CSS or JS
framework: one stylesheet (`assets/css/site.css`) and one small script (`assets/js/site.js`).

Live site: https://vi31.github.io/

## Run it locally

You need Ruby and Bundler.

```sh
bundle install
bundle exec jekyll serve      # then open http://127.0.0.1:4000/
```

If Jekyll stops with an `Invalid US-ASCII character` error, run `export LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8` first.
A warning about `faraday-retry` is harmless.

## How the site is laid out

| Path | What it is |
|---|---|
| `_config.yml` | Site title, description, links, contact-form address, collections |
| `index.html` | Home. Hero text and the "Now" line are in its front matter |
| `about.html` | About page and contact form. Text and fact tiles are in its front matter |
| `projects.html`, `teardowns.html`, `blog.html` | Listing pages |
| `_projects/`, `_teardowns/`, `_posts/` | One Markdown file per project, teardown, blog post |
| `_data/timeline.yml` | About > Experience tiles |
| `_layouts/` | Page templates (`project`, `teardown`, `post`, `page-banner`, `default`) |
| `_includes/` | Header, footer, cards, filters, previous/next |
| `assets/css/site.css` | All styles. Colours are tokens at the top |
| `assets/img/` | Logos, favicon, share image, the doodle background tiles |
| `404.html` | "Page not found" page |

## Replace the placeholders first

Anything not supplied yet is a visible `[placeholder]`. To find them all:

```sh
grep -rn "\[" _config.yml index.html about.html projects.html teardowns.html blog.html _data _projects _teardowns _posts
```

Start with these:

1. **`_config.yml`**: `description` (shown in search results and link previews), the `profiles` links (LinkedIn, email), and `form_endpoint`.
2. **`index.html`** front matter: your name, what you do, the status line, the intro and the "Now" line.
3. **`about.html`** front matter: the three paragraphs, facts, CV path, portrait.
4. **`_data/timeline.yml`**: your roles and degrees.
5. **The sample entries.** Every file in `_projects/`, `_teardowns/` and `_posts/` whose title starts with `[SAMPLE]` is a template. Edit it into a real entry or delete it.

## Adding content

### A project

Create `_projects/my-project.md`:

```yaml
---
title: "Project title"
year: "2026"                  # listing is sorted newest first by this
category: "Product design"    # becomes a filter button; keep the spelling consistent
summary: "Several sentences are fine: the problem, what you did, the outcome."
cover: /assets/img/projects/my-project/cover.jpg   # optional
accent: lime                  # lime or purple: the colour of the card's top edge
featured: true                # the first two featured projects appear on Home
role: "Designer and developer"
timeline: "Jan to Mar 2026"
team: "Solo"
tools: ["Figma", "Python"]
links:
  demo: "https://example.com"   # remove a line to hide its button
  code: "https://github.com/vi31/my-project"
---
## Problem
Write the body in Markdown. These headings are only a starting template:
rename or drop any of them.
```

### A teardown

Create `_teardowns/product-angle.md`. The blocks below the body come from the front matter, and any you leave out are skipped.

```yaml
---
title: "Product: the angle you examine"
date: 2026-11-20
product_category: "Fintech"
summary: "One sentence on the decision or feature this teardown examines."
cover: /assets/img/teardowns/product/screenshot.png
read_time: 6                  # minutes
featured: true                # shown large at the top of the Teardowns page
verdict: "Your conclusion in one sentence."
works:
  - "A strength"
does_not:
  - "A friction point"
changes:
  - title: "A recommendation"
    text: "Why, and the trade-off."
takeaway: "The broader product lesson, in two or three sentences."
---
## The user problem
Body in Markdown ("The user problem", "What they built", annotated screenshots).
```

### A blog post

Create `_posts/YYYY-MM-DD-title.md` (the date in the filename sets the date and order):

```yaml
---
title: "Post title"
date: 2026-11-20
topic: "Process"              # becomes a filter button on the Blog page
subtitle: "The one idea this post argues."
---
Opening paragraph (shown larger).

## A section heading

> A line worth pulling out (shown as a large purple quote).
```

Reading time is worked out from the word count.

### Images

Put images under `assets/img/` and refer to them by path, e.g. `/assets/img/projects/my-project/cover.jpg`.
In a Markdown body use `![Describe the image](/assets/img/...)`. Keep the alt text meaningful.
For a figure with a caption, use HTML in the Markdown:

```html
<figure>
  <img src="/assets/img/..." alt="Describe it">
  <figcaption>Caption.</figcaption>
</figure>
```

### Search and share previews

Every page uses the share image `assets/img/og-image.png`. To use a different one on a page, add
`image: /assets/img/...` to its front matter (1200 x 630 works best). Add `description:` to a
page's front matter to control its search snippet.

## Contact form

The form posts to [Formspree](https://formspree.io). Create a form there, then put its URL in `_config.yml`:

```yaml
form_endpoint: "https://formspree.io/f/abcdwxyz"
```

Until that is a real address, pressing "Send message" shows a "not connected yet" message.

## Colours, fonts and the theme

- All colours are CSS variables at the top of `assets/css/site.css`, once for dark and once for light
  (the light set appears twice, for the toggle and for visitors whose system prefers light; keep both copies identical).
- Rule of thumb: **lime = action, "now", current page. Purple = classification and depth.**
- Text must stay at 4.5:1 contrast or better. The light-theme lime text is `#4A7300` for that reason.
- Fonts (Space Grotesk and Inter) load from Google Fonts. To self-host them, download the files into
  `assets/fonts/`, add `@font-face` rules to `site.css`, and remove the Google Fonts links in `_layouts/default.html`.
- The doodle background tiles in `assets/img/doodles/` were generated by `tools/make_doodles.py` (not published with
  the site). It needs `npm i lucide-static`; edit the `ICONS` path inside it, then change density, icon size,
  colours or opacity and re-run. Avoid editing the SVGs by hand.

## Publishing

GitHub Pages builds this site from the `gh-pages` branch whenever it changes, so a push to that branch
publishes the site. Work on a branch, open a pull request, and merge when you are happy.

## Credits

Icons in the background tiles and the theme toggle are from [Lucide](https://lucide.dev) (ISC licence).
Fonts: Space Grotesk and Inter (SIL Open Font Licence), via Google Fonts.
