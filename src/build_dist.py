"""Assemble a standalone, host-anywhere copy of the site in dist/ (GitHub Pages, Netlify, Cloudflare Pages...)."""
import re, pathlib, shutil, html, datetime
from PIL import Image
import seo
from services_data import SERVICES

root = pathlib.Path(__file__).parent
dist = root / "dist"
if dist.exists(): shutil.rmtree(dist)
dist.mkdir()

DOMAIN = "farrahsthreading.com"
index_src = (root / "index.html").read_text()

# --- index.html: the artifact version has no skeleton; wrap it like the inner pages ---
title = re.search(r"<title>(.*?)</title>", index_src).group(1)
seo_title = "Farrah's Threading & Beauty Studio | Eyebrow Threading in Lancaster, PA"
site = seo.load_site()
desc = re.search(r'<meta name="description" content="(.*?)">', index_src).group(1)
body = index_src
body = re.sub(r"<title>.*?</title>\n", "", body, count=1)
body = re.sub(r'<meta name="description" content=".*?">\n', "", body, count=1)
body = re.sub(r'<meta property="og:title" content=".*?">\n', "", body, count=1)
body = re.sub(r'<meta property="og:description" content=".*?">\n', "", body, count=1)
fonts = re.search(r'(<link rel="stylesheet" href="https://fonts.googleapis.com[^>]+>)', body).group(1)
body = body.replace(fonts + "\n", "", 1)
body = re.sub(r'<link rel="preconnect" href="https://fonts.g[^>]+>\n', "", body)

head = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{seo_title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://{DOMAIN}/">
<meta property="og:title" content="{title} · Lancaster, PA">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://{DOMAIN}/">
<meta property="og:image" content="https://{DOMAIN}/share.jpg">
<meta property="og:image:secure_url" content="https://{DOMAIN}/share.jpg">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Farrah's Threading & Beauty Studio logo">
<meta property="og:site_name" content="Farrah's Threading & Beauty Studio">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://{DOMAIN}/share.jpg">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta name="theme-color" content="#27091F">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{fonts}
<style>
  html {{ color-scheme: light; padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }}
  body {{ margin: 0; font: 14px system-ui, sans-serif; }}
  img {{ max-width: 100%; }}
  [hidden] {{ display: none !important; }}
</style>
"""
# the artifact head only allows a <title>; our body now starts with <style>, so split head/body at <header
style_end = body.index("<header")
page_head_part = body[:style_end]   # contains <style>...</style>
page_body = body[style_end:]
home_graph = [seo.org_node(site), seo.website_node(),
              seo.webpage_node(seo.DOMAIN + "/", seo_title, desc, about={"@id": seo.ORG_ID})]
for loc in site["locations"]:
    home_graph.append(seo.location_node(loc, site, seo.service_catalog(SERVICES, "pike" if loc["slug"] == "harrisburg-pike" else "both")))
static_ld = seo.ld(home_graph).replace('<script type="application/ld+json">', '<script type="application/ld+json" id="ldjson">')
assert page_body.count('<script type="application/ld+json" id="ldjson"></script>') == 1
page_body = page_body.replace('<script type="application/ld+json" id="ldjson"></script>', static_ld)
assert page_body.count("renderSchema(); ") == 1
page_body = page_body.replace("renderSchema(); ", "")
(dist / "index.html").write_text(head + page_head_part + "</head>\n<body>\n" + page_body + "\n</body>\n</html>\n")

# --- inner pages + assets ---
pages = ["harrisburg-pike.html", "park-city-center.html", "hydrafacial.html", "threading.html", "eyebrow-tinting.html", "lash-tinting.html", "brow-lamination.html",
         "lash-lift.html", "lash-extensions.html", "waxing.html", "facials.html", "henna.html"]
for f in pages + ["logo-mark.png", "logo-full.png", "logo-full-dark.png", "share.jpg"]:
    shutil.copy(root / f, dist / f)

# --- favicons from the butterfly mark ---
mark = Image.open(root / "logo-mark.png").convert("RGBA")
bbox = mark.getbbox(); mark = mark.crop(bbox)
side = max(mark.size); sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
sq.paste(mark, ((side - mark.width) // 2, (side - mark.height) // 2), mark)
pad = int(side * 0.06); sq2 = Image.new("RGBA", (side + 2 * pad, side + 2 * pad), (0, 0, 0, 0)); sq2.paste(sq, (pad, pad), sq)
sq2.resize((180, 180), Image.LANCZOS).save(dist / "apple-touch-icon.png")
sq2.resize((32, 32), Image.LANCZOS).save(dist / "favicon-32x32.png")
sq2.resize((64, 64), Image.LANCZOS).save(dist / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])

# --- hosting files ---
(dist / "CNAME").write_text(DOMAIN + "\n")
(dist / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /src/\nSitemap: https://{DOMAIN}/sitemap.xml\n")
today = datetime.date.today().isoformat()
urls = ["", *pages]
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <url><loc>https://{DOMAIN}/{u}</loc><lastmod>{today}</lastmod><priority>{'1.0' if u == '' else '0.8'}</priority></url>\n" for u in urls) + "</urlset>\n"
(dist / "sitemap.xml").write_text(sitemap)
(dist / "404.html").write_text(f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found · Farrah's</title>
<link rel="icon" href="favicon.ico"><style>body{{margin:0;min-height:100vh;display:grid;place-items:center;background:#27091F;color:#F6EEE4;font-family:Georgia,serif;text-align:center;padding:24px}}a{{color:#C9A36A}}</style></head>
<body><div><img src="logo-mark.png" alt="" width="90"><h1 style="font-weight:500">That page isn't here.</h1><p><a href="/">Back to Farrah's Threading &amp; Beauty Studio</a></p></div></body></html>
""")
print("dist files:", sorted(p.name for p in dist.iterdir()))
