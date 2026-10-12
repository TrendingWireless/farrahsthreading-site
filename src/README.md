# Site source

Everything on the live site is generated from this folder. Edit here, rebuild, copy the result up one level, commit.

| File | What it holds |
|---|---|
| `index.html` | The homepage (hero, services cards, locations, gift cards, about, careers, contact). The `const SITE = {...}` block near the bottom is the editable config: phone, email, social links, booking/gift-card form links, and both locations' addresses, hours and links. The services cards in this file are reused on the two location pages. |
| `services_data.py` | Content for each service page: headline, intro, facts, what it is, who it's for, what to expect, prep/aftercare, FAQ, SEO title/description, and `where` (`both` = both studios, `pike` = Harrisburg Pike only). |
| `hydrafacial-body.html` | Body of the HydraFacial page. |
| `build.py` | Builds the service pages, the HydraFacial page and the two location pages (`LOC_COPY` at the bottom holds the location-page wording). |
| `seo.py` | Structured data (schema.org) helpers. |
| `build_dist.py` | Assembles the deployable site into `dist/`: wraps the homepage, copies pages and logos, makes favicons, sitemap, robots.txt, 404 page, CNAME. |
| `logo-*.png`, `share.jpg` | Logo files and the link-preview image. |

## Rebuild and publish

```bash
cd src
python3 build.py && python3 build_dist.py
cp -r dist/. ..
cd .. && git add -A && git commit -m "Describe the change" && git push
```

GitHub Pages republishes `main` within a minute or two of the push.

Needs Python 3 with Pillow (`pip install pillow`) and Node (used to read the `SITE` block out of `index.html`).
