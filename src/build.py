import re, pathlib, html
from services_data import SERVICES, BOOK_URL, PHONE
import seo

SITE = seo.load_site()

root = pathlib.Path(__file__).parent
index = (root / "index.html").read_text()
style = re.search(r"<style>\n(.*?)</style>", index, re.S).group(1)
fonts = re.search(r'(<link rel="stylesheet" href="https://fonts.googleapis.com[^>]+>)', index).group(1)

EXTRA_CSS = """
  /* Inner pages */
  .hydra-hero { background: linear-gradient(160deg, var(--plum-deep) 0%, var(--plum) 70%, #2C2340 100%); }
  .hero-art canvas { width: 100%; max-width: 440px; height: auto; display: block; margin-inline: auto; }
  .crumbs { font-size: 0.8rem; color: var(--on-plum-muted); display: flex; gap: 0.5rem; flex-wrap: wrap; }
  .crumbs a { color: var(--gold); text-decoration: none; }
  .concerns { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0.5rem 1.2rem; }
  .concerns li { display: flex; gap: 0.6rem; align-items: baseline; color: var(--ink-soft); }
  .concerns li::before { content: ""; width: 8px; height: 8px; background: var(--aqua); transform: rotate(45deg); flex: none; position: relative; top: -1px; }
  .tiers { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.2rem; align-items: stretch; }
  .tier { background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); padding: 1.6rem; display: grid; gap: 0.8rem; align-content: start; min-width: 0; }
  .tier h3 { font-size: 1.9rem; display: flex; justify-content: space-between; gap: 0.6rem; align-items: baseline; }
  .tier .price { font-family: var(--font-body); font-size: 1rem; color: var(--gold-deep); white-space: nowrap; font-variant-numeric: tabular-nums; }
  .tier .tag { color: var(--aqua); }
  .tier.featured { border-color: var(--aqua); box-shadow: var(--shadow); position: relative; }
  .tier-lede { color: var(--ink-soft); }
  .includes { list-style: none; margin: 0; padding: 0.8rem 0 0; border-top: 1px solid var(--line); display: grid; gap: 0.4rem; font-size: 0.97rem; }
  .includes li::before { content: "+ "; color: var(--aqua); font-weight: 600; }
  .tier-for { font-size: 0.9rem; color: var(--ink-soft); border-top: 1px solid var(--line); padding-top: 0.8rem; }
  .steps { list-style: none; margin: 0; padding: 0; display: grid; gap: 0; max-width: 820px; }
  .steps li { display: grid; grid-template-columns: 48px 1fr; gap: 1.2rem; padding-block: 1.1rem; border-bottom: 1px solid var(--line); min-width: 0; }
  .steps li:last-child { border-bottom: 0; }
  .step-n { font-family: var(--font-display); font-size: 1.9rem; color: var(--aqua); line-height: 1; }
  .steps h3 { font-size: 1.2rem; display: flex; flex-wrap: wrap; gap: 0.6rem; align-items: center; margin-bottom: 0.25rem; }
  .steps p { color: var(--ink-soft); font-size: 0.97rem; }
  .pill { font-family: var(--font-body); font-size: 0.66rem; letter-spacing: 0.16em; text-transform: uppercase; font-weight: 600; color: var(--aqua); border: 1px solid var(--aqua); border-radius: 999px; padding: 0.15rem 0.55rem; }
  .faq { display: grid; gap: 0.2rem; }
  .faq details { border-bottom: 1px solid var(--line); padding: 0.6rem 0; }
  .faq summary { cursor: pointer; font-weight: 500; font-size: 1.05rem; list-style: none; display: flex; justify-content: space-between; gap: 1rem; align-items: baseline; }
  .faq summary::-webkit-details-marker { display: none; }
  .faq summary::after { content: "+"; color: var(--aqua); font-size: 1.3rem; line-height: 1; flex: none; }
  .faq details[open] summary::after { content: "–"; }
  .faq p { color: var(--ink-soft); padding-top: 0.5rem; font-size: 0.98rem; }
  .faq a { color: var(--aqua); }
  .price-table { width: 100%; border-collapse: collapse; max-width: 720px; font-variant-numeric: tabular-nums; }
  .price-table th, .price-table td { text-align: left; padding: 0.7rem 0; border-bottom: 1px solid var(--line); vertical-align: top; }
  .price-table th { font-size: 0.72rem; letter-spacing: 0.2em; text-transform: uppercase; color: var(--gold-deep); font-weight: 500; }
  .price-table td:last-child, .price-table th:last-child { text-align: right; white-space: nowrap; padding-left: 1rem; }
  .price-table td:last-child { font-family: var(--font-display); font-size: 1.25rem; color: var(--plum); }
  :root[data-theme="dark"] .price-table td:last-child { color: var(--gold); }
  @media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) .price-table td:last-child { color: var(--gold); } }
  .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 2.5rem; }
  .two-col h3 { font-size: 1.25rem; margin-bottom: 0.6rem; }
  .checks { list-style: none; margin: 0; padding: 0; display: grid; gap: 0.5rem; color: var(--ink-soft); }
  .checks li { display: flex; gap: 0.6rem; align-items: baseline; }
  .checks li::before { content: "—"; color: var(--gold-deep); flex: none; }
  @media (max-width: 820px) { .two-col { grid-template-columns: 1fr; gap: 1.8rem; } }
  .more { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 0.8rem; }
  .more a { display: block; text-decoration: none; color: var(--fg); border: 1px solid var(--line); border-radius: var(--radius); padding: 0.9rem 1rem; background: var(--surface); font-weight: 500; font-size: 0.95rem; }
  .more a:hover { border-color: var(--gold); }
  .more a span { display: block; font-size: 0.78rem; color: var(--ink-soft); font-weight: 400; margin-top: 0.15rem; }
"""

ART_JS = r"""
  (function () {
    const c = document.getElementById("art"); if (!c) return;
    const ctx = c.getContext("2d"); const W = c.width, H = c.height;
    const css = getComputedStyle(document.documentElement);
    const gold = css.getPropertyValue("--gold").trim() || "#C9A36A", aqua = css.getPropertyValue("--aqua").trim() || "#6FC2DE", blush = css.getPropertyValue("--blush").trim() || "#E7B6BE", cream = "#F6EEE4";
    ctx.lineCap = "round"; ctx.lineJoin = "round";
    const stroke = (color, w, a) => { ctx.strokeStyle = color; ctx.lineWidth = w; ctx.globalAlpha = a === undefined ? 1 : a; };
    const diamond = (x, y, s, color) => { ctx.fillStyle = color; ctx.globalAlpha = 1; ctx.beginPath(); ctx.moveTo(x, y - s); ctx.lineTo(x + s, y); ctx.lineTo(x, y + s); ctx.lineTo(x - s, y); ctx.closePath(); ctx.fill(); };
    const drop = (x, y, s, color) => { ctx.fillStyle = color; ctx.globalAlpha = 1; ctx.beginPath(); ctx.moveTo(x, y - s * 1.3); ctx.bezierCurveTo(x + s, y - s * 0.2, x + s * 0.9, y + s, x, y + s); ctx.bezierCurveTo(x - s * 0.9, y + s, x - s, y - s * 0.2, x, y - s * 1.3); ctx.fill(); };
    // a brow: many short hair strokes along an arch
    const brow = (x0, y0, w, up, dir) => {
      const n = 46;
      for (let i = 0; i <= n; i++) {
        const u = i / n; const x = x0 + dir * u * w; const y = y0 - Math.sin(u * Math.PI * 0.92) * 44 + u * u * 22;
        const len = 10 + 16 * Math.sin(u * Math.PI); const ang = (up ? -1.25 : -0.55) + (dir > 0 ? u * 1.1 : -u * 1.1);
        stroke(gold, 1.5, 0.55 + 0.45 * Math.sin(u * Math.PI)); ctx.beginPath(); ctx.moveTo(x, y + 6); ctx.lineTo(x + Math.cos(ang) * len * (dir > 0 ? 1 : -1), y + 6 + Math.sin(ang) * len); ctx.stroke();
      }
    };
    const thread = (pts, color, w) => { stroke(color || blush, w || 1.4, 0.9); ctx.beginPath(); ctx.moveTo(pts[0][0], pts[0][1]); for (let i = 1; i + 2 < pts.length; i += 3) ctx.bezierCurveTo(pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1], pts[i+2][0], pts[i+2][1]); ctx.stroke(); };
    const eye = (cx, cy, w, h) => { stroke(gold, 1.6, 0.9); ctx.beginPath(); ctx.moveTo(cx - w, cy); ctx.quadraticCurveTo(cx, cy - h * 2, cx + w, cy); ctx.quadraticCurveTo(cx, cy + h * 1.2, cx - w, cy); ctx.stroke(); };
    const lashes = (cx, cy, w, curl, count, len, color) => {
      for (let i = 0; i < count; i++) {
        const u = (i + 0.5) / count; const x = cx - w + u * 2 * w; const y = cy - Math.sin(u * Math.PI) * 2 * 0.5 * 30; // along upper lid
        const l = len * (0.5 + Math.sin(u * Math.PI)); const tilt = (u - 0.5) * 1.1;
        stroke(color, 1.6, 0.9); ctx.beginPath(); ctx.moveTo(x, y); ctx.quadraticCurveTo(x + Math.sin(tilt) * l * 0.6, y - l * 0.7, x + Math.sin(tilt) * l + curl * l * 0.6, y - l); ctx.stroke();
      }
    };
    const kind = c.dataset.art;
    if (kind === "brow" || kind === "tint") {
      brow(60, 190, 150, false, 1); brow(390, 190, 150, false, -1);
      thread([[20, 250],[120, 120],[260, 120],[330, 250],[360, 300],[420, 240],[430, 210]], blush, 1.4);
      diamond(20, 250, 5, blush);
      if (kind === "tint") { drop(225, 150, 9, aqua); drop(248, 120, 6, blush); drop(205, 118, 5, gold); }
    } else if (kind === "lamination") {
      const x0 = 70, w = 300;
      for (let i = 0; i <= 60; i++) { const u = i / 60; const x = x0 + u * w; const y = 215 - Math.sin(u * Math.PI * 0.9) * 48 + u * u * 26; const len = 18 + 26 * Math.sin(u * Math.PI); stroke(gold, 1.6, 0.5 + 0.5 * Math.sin(u * Math.PI)); ctx.beginPath(); ctx.moveTo(x, y + 10); ctx.quadraticCurveTo(x + 4, y - len * 0.5, x + 14, y - len); ctx.stroke(); }
      thread([[30, 300],[130, 290],[230, 300],[300, 310],[360, 290],[400, 280],[420, 285]], blush, 1.2);
      diamond(400, 160, 5, aqua); diamond(60, 150, 4, blush);
    } else if (kind === "lashes" || kind === "lashtint" || kind === "extensions") {
      eye(220, 200, 150, 34);
      const n = kind === "extensions" ? 40 : 26; const len = kind === "extensions" ? 62 : 48; const curl = kind === "lashes" ? 0.6 : 0.25;
      lashes(220, 174, 136, curl, n, len, kind === "lashtint" ? cream : gold);
      if (kind === "extensions") lashes(220, 174, 120, 0.35, 18, 78, blush);
      if (kind === "lashtint") { drop(360, 110, 9, aqua); drop(385, 140, 6, blush); }
      ctx.fillStyle = gold; ctx.globalAlpha = 0.9; ctx.beginPath(); ctx.arc(220, 206, 22, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = "#2B0C22"; ctx.beginPath(); ctx.arc(220, 206, 11, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = cream; ctx.beginPath(); ctx.arc(228, 198, 3.5, 0, Math.PI * 2); ctx.fill();
    } else if (kind === "wax") {
      ctx.save(); ctx.translate(220, 190); ctx.rotate(-0.35);
      ctx.fillStyle = blush; ctx.globalAlpha = 0.95; ctx.beginPath(); ctx.roundRect(-120, -34, 240, 68, 18); ctx.fill();
      stroke(gold, 1.4, 0.9); ctx.beginPath(); ctx.roundRect(-104, -20, 208, 40, 12); ctx.stroke();
      ctx.restore();
      for (let i = 0; i < 14; i++) { const x = 90 + i * 20; const y = 270 + Math.sin(i) * 6; stroke(gold, 1.3, 0.5); ctx.beginPath(); ctx.moveTo(x, y); ctx.quadraticCurveTo(x + 4, y - 12, x + 2, y - 22); ctx.stroke(); }
      diamond(360, 100, 6, aqua); diamond(70, 120, 4, gold); diamond(390, 280, 4, blush);
    } else if (kind === "facial") {
      stroke(gold, 1.6, 0.9); ctx.beginPath(); ctx.moveTo(250, 60); ctx.bezierCurveTo(300, 70, 330, 120, 322, 170); ctx.bezierCurveTo(340, 176, 336, 200, 318, 204); ctx.bezierCurveTo(312, 250, 280, 300, 230, 310); ctx.bezierCurveTo(200, 316, 180, 300, 172, 280); ctx.stroke();
      stroke(gold, 1.2, 0.7); ctx.beginPath(); ctx.moveTo(262, 140); ctx.quadraticCurveTo(286, 130, 302, 144); ctx.stroke();
      for (let i = 0; i < 5; i++) { const a = -1.1 + i * 0.32; const r = 130; const x = 130 + Math.cos(a) * r, y = 200 + Math.sin(a) * r; drop(x, y, 7 + (i % 2) * 3, i % 2 ? aqua : blush); }
      stroke(aqua, 1.2, 0.6); ctx.beginPath(); ctx.arc(130, 200, 108, -1.3, 0.25); ctx.stroke();
      diamond(380, 90, 5, blush); diamond(60, 300, 4, gold);
    } else if (kind === "henna") {
      const paisley = (x, y, s, rot) => { ctx.save(); ctx.translate(x, y); ctx.rotate(rot); stroke(gold, 1.5, 0.95); ctx.beginPath(); ctx.moveTo(0, -s); ctx.bezierCurveTo(s * 0.9, -s, s * 0.9, s * 0.6, 0, s * 0.8); ctx.bezierCurveTo(-s * 0.9, s * 0.6, -s * 0.9, -s * 0.2, 0, -s); ctx.stroke(); stroke(blush, 1.2, 0.9); ctx.beginPath(); ctx.moveTo(0, -s * 0.55); ctx.bezierCurveTo(s * 0.5, -s * 0.55, s * 0.5, s * 0.3, 0, s * 0.45); ctx.bezierCurveTo(-s * 0.5, s * 0.3, -s * 0.5, -s * 0.1, 0, -s * 0.55); ctx.stroke(); for (let i = 0; i < 7; i++) { const a = -1.9 + i * 0.5; ctx.fillStyle = aqua; ctx.globalAlpha = 1; ctx.beginPath(); ctx.arc(Math.cos(a) * s * 1.15, Math.sin(a) * s * 1.15, 2.4, 0, Math.PI * 2); ctx.fill(); } ctx.restore(); };
      paisley(220, 170, 70, -0.5); paisley(110, 250, 36, 0.6); paisley(340, 250, 36, -1.4);
      thread([[40, 320],[120, 300],[200, 330],[260, 330],[330, 310],[390, 330],[420, 320]], gold, 1.2);
      for (let i = 0; i < 9; i++) { ctx.fillStyle = gold; ctx.globalAlpha = 0.9; ctx.beginPath(); ctx.arc(60 + i * 40, 60 + (i % 2) * 10, 2.2, 0, Math.PI * 2); ctx.fill(); }
    } else if (kind === "makeup") {
      ctx.save(); ctx.translate(150, 230); ctx.rotate(-0.8);
      stroke(gold, 1.6, 0.95); ctx.beginPath(); ctx.roundRect(-8, -150, 16, 170, 8); ctx.stroke();
      ctx.fillStyle = blush; ctx.globalAlpha = 0.95; ctx.beginPath(); ctx.ellipse(0, 40, 18, 34, 0, 0, Math.PI * 2); ctx.fill();
      ctx.restore();
      stroke(gold, 1.6, 0.95); ctx.beginPath(); ctx.moveTo(240, 210); ctx.bezierCurveTo(270, 180, 300, 182, 320, 200); ctx.bezierCurveTo(340, 182, 370, 180, 400, 210); ctx.bezierCurveTo(370, 250, 270, 250, 240, 210); ctx.stroke();
      stroke(blush, 1.2, 0.8); ctx.beginPath(); ctx.moveTo(244, 212); ctx.quadraticCurveTo(320, 222, 396, 212); ctx.stroke();
      diamond(410, 120, 5, aqua); diamond(70, 90, 4, blush); diamond(300, 300, 4, gold);
    }
  })();
"""

def head(title, desc, slug="", extra=""):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="https://farrahsthreading.com/{slug}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://farrahsthreading.com/{slug}">
<meta property="og:image" content="https://farrahsthreading.com/share.jpg">
<meta property="og:image:secure_url" content="https://farrahsthreading.com/share.jpg">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Farrah's Threading & Beauty Studio logo">
<meta property="og:site_name" content="Farrah's Threading & Beauty Studio">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://farrahsthreading.com/share.jpg">
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
{style}{EXTRA_CSS}</style>
{extra}
</head>
<body>
"""

def header(current):
    cur = lambda s: ' aria-current="page"' if current == s else ""
    return f"""<header class="site-header">
  <div class="wrap nav">
    <a class="brand" href="index.html" aria-label="Farrah's Threading & Beauty Studio, home">
      <img class="brand-mark" src="logo-mark.png" alt="" width="54" height="56">
      <span class="brand-text">
        <span class="brand-name">Farrah's</span>
        <span class="brand-sub">Threading &amp; Beauty Studio</span>
      </span>
    </a>
    <button class="nav-toggle" id="navToggle" aria-expanded="false" aria-controls="navLinks">Menu</button>
    <ul class="nav-links" id="navLinks">
      <li><a href="index.html#services"{cur('services')}>Services</a></li>
      <li><a href="hydrafacial.html"{cur('hydrafacial')}>HydraFacial</a></li>
      <li><a href="index.html#locations">Locations</a></li>
      <li><a href="index.html#gift">Gift cards</a></li>
      <li><a href="index.html#about">About</a></li>
      <li><a href="index.html#contact">Contact</a></li>
      <li><a class="btn btn-gold" id="navCta" href="{BOOK_URL}" target="_blank" rel="noopener">Request appointment</a></li>
    </ul>
  </div>
</header>
"""

FOOTER = f"""<footer>
  <div class="wrap">
    <img class="footer-logo" src="logo-full-dark.png" alt="Farrah's Threading & Beauty Studio" width="200" height="192">
    <div class="footer-text">
      <div><strong>Farrah's Threading &amp; Beauty Studio L.L.C.</strong> · Lancaster, Pennsylvania</div>
      <div><a href="harrisburg-pike.html" style="color:inherit">1360A Harrisburg Pike</a> · <a href="park-city-center.html" style="color:inherit">621 Park City Center</a> · <a href="tel:+17174337774" style="color:inherit;text-decoration:none">{PHONE}</a> · <a href="https://g.page/r/CbGpJmRZDTYFEBM/review" target="_blank" rel="noopener" style="color:var(--gold)">Leave a Google review</a></div>
      <div>HydraFacial® and Vortex-Fusion® are registered trademarks of their owner; Farrah's is an independent HydraFacial provider. · © <span id="year">2026</span></div>
    </div>
  </div>
</footer>
"""

NAV_JS = """
  const t = document.getElementById("navToggle"), l = document.getElementById("navLinks");
  t.addEventListener("click", () => { const open = l.classList.toggle("open"); t.setAttribute("aria-expanded", String(open)); t.textContent = open ? "Close" : "Menu"; });
  document.getElementById("year").textContent = String(new Date().getFullYear());
"""

def li(items): return "".join(f"<li>{i}</li>" for i in items)

def service_page(s, all_services):
    walkin = s["booking"] == "walkin"
    primary = ('<a class="btn btn-gold" href="index.html#locations">Find a location</a>' if walkin
               else f'<a class="btn btn-gold" href="{BOOK_URL}" target="_blank" rel="noopener">Request an appointment</a>')
    secondary = '<a class="btn btn-outline" href="#steps">What to expect</a>'
    fl = list(s["facts"]); fl[1] = (["Both studios", "Harrisburg Pike &amp; Park City Center"] if s.get("where") == "both" else ["Harrisburg Pike studio", "1360A Harrisburg Pike only"])
    facts = "".join(f'<div class="fact"><strong>{f[0]}</strong><span>{f[1]}</span></div>' for f in fl)
    steps = "".join(f'<li><span class="step-n">{i+1}</span><div><h3>{t}</h3><p>{d}</p></div></li>' for i, (t, d) in enumerate(s["steps"]))
    rows = "".join(f"<tr><td>{n}</td><td>{p}</td></tr>" for n, p in s["prices"])
    faq = "".join(f'<details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(s["faq"]))
    others = [o for o in all_services if o["slug"] != s["slug"]]
    more = "".join(f'<a href="{o["slug"]}.html">{o["nav"]}<span>{o["category"]}{" · Harrisburg Pike only" if o.get("where") == "pike" else ""}</span></a>' for o in others)
    more += '<a href="hydrafacial.html">HydraFacial<span>Facials · Harrisburg Pike only</span></a>'
    link = f'<p style="margin-top:1rem"><a class="service-link" href="{s["link"][1]}">{s["link"][0]}</a></p>' if s.get("link") else ""
    where_note = ("Offered at both studios: Harrisburg Pike and Park City Center." if s.get("where") == "both"
                  else "Offered at our Harrisburg Pike studio, 1360A Harrisburg Pike. Not available at Park City Center.")
    walk_note = (f'<p class="note" style="margin-top:1rem">{where_note} Threading is walk-in only, first come, first served. No appointment needed.</p>' if walkin
                 else f'<p class="note" style="margin-top:1rem">{where_note} By appointment: send a request and we\'ll call or text to confirm, or call {PHONE}.</p>')
    plain_name = re.sub(r"<[^>]+>", "", s["h1"]).replace("&amp;", "&")
    body = f"""{header('services')}
<main id="top">
  <section class="hero on-plum hydra-hero">
    <div class="wrap">
      <div class="hero-grid">
        <div class="hero-copy">
          <p class="crumbs"><a href="index.html">Home</a> › <a href="index.html#services">Services</a> › {s["category"]}</p>
          <h1>{s["h1"]}</h1>
          <p class="lede">{s["lede"]}</p>
          <div class="hero-actions">{primary}{secondary}</div>
        </div>
        <div class="hero-art" aria-hidden="true"><canvas id="art" data-art="{s["art"]}" width="440" height="340"></canvas></div>
      </div>
      <div class="hero-facts">{facts}</div>
    </div>
  </section>

  <section class="band">
    <div class="wrap about-grid">
      <div>
        <p class="eyebrow">What it is</p>
        <h2 style="margin:0.6rem 0 1.2rem">How it works.</h2>
        <p class="lede">{s["what"]}</p>
        {link}
      </div>
      <div class="story">
        <h3>Good for</h3>
        <ul class="concerns">{li(s["good_for"])}</ul>
        {walk_note}
      </div>
    </div>
  </section>

  <section id="steps">
    <div class="wrap">
      <div class="section-head"><p class="eyebrow">Your visit</p><h2>What to expect.</h2></div>
      <ol class="steps">{steps}</ol>
    </div>
  </section>

  <section class="band">
    <div class="wrap two-col">
      <div><h3>Before your visit</h3><ul class="checks">{li(s["prep"])}</ul></div>
      <div><h3>Afterward</h3><ul class="checks">{li(s["after"])}</ul></div>
    </div>
  </section>

  <section>
    <div class="wrap split">
      <div>
        <p class="eyebrow">Good to know</p>
        <h2>Questions we hear most.</h2>
        <p class="lede">Anything else, call or text us at {PHONE}.</p>
        <div class="hero-actions" style="margin-top:1.2rem">{primary}<a class="btn btn-ghost" href="index.html#gift">Give it as a gift</a></div>
      </div>
      <div class="faq">{faq}</div>
    </div>
  </section>

  <section class="band">
    <div class="wrap">
      <div class="section-head"><p class="eyebrow">More at Farrah's</p><h2>Other services.</h2></div>
      <div class="more">{more}</div>
    </div>
  </section>
</main>
{FOOTER}
<script>{NAV_JS}{ART_JS}</script>
</body>
</html>
"""
    title = f"{s['seo_title']} | Farrah's Threading & Beauty Studio"
    if len(title) > 72: title = f"{s['seo_title']} | Farrah's"
    desc = s["seo_desc"]
    url = f"{seo.DOMAIN}/{s['slug']}.html"
    graph = [seo.webpage_node(url, title, desc, about={"@id": url + "#service"}),
             seo.service_node(plain_name.rstrip('.'), desc, url, SITE, s.get("where", "pike"), s["category"]),
             seo.breadcrumbs([("Home", seo.DOMAIN + "/"), ("Services", seo.DOMAIN + "/#services"), (plain_name.rstrip('.'), None)])]
    return head(title, desc, f"{s['slug']}.html", seo.ld(graph)) + body

# Build service pages
for s in SERVICES:
    (root / f"{s['slug']}.html").write_text(service_page(s, SERVICES))
    print("built", s["slug"] + ".html")

# Build the HydraFacial page from its body file, with the shared header/footer
hydra_body = (root / "hydrafacial-body.html").read_text()
hydra_body = re.sub(r"<header class=\"site-header\">.*?</header>\n", header("hydrafacial"), hydra_body, count=1, flags=re.S)
hydra_body = re.sub(r"<footer>.*?</footer>\n", FOOTER, hydra_body, count=1, flags=re.S)
hydra_title = "HydraFacial in Lancaster, PA | Farrah's Threading & Beauty Studio"
hydra_desc = "HydraFacial in Lancaster, PA at Farrah's Harrisburg Pike studio: Signature, Deluxe and Platinum tiers that cleanse, exfoliate, extract and hydrate, no downtime."
hydra_url = seo.DOMAIN + "/hydrafacial.html"
hydra_graph = [seo.webpage_node(hydra_url, hydra_title, hydra_desc, about={"@id": hydra_url + "#service"}),
               seo.service_node("HydraFacial", hydra_desc, hydra_url, SITE, "pike", "Facials"),
               seo.breadcrumbs([("Home", seo.DOMAIN + "/"), ("Services", seo.DOMAIN + "/#services"), ("HydraFacial", None)])]
hydra = head(hydra_title, hydra_desc, "hydrafacial.html", seo.ld(hydra_graph)) + hydra_body + "\n</body>\n</html>\n"
(root / "hydrafacial.html").write_text(hydra)
print("built hydrafacial.html")


# ---------- Location pages ----------
LOC_COPY = {
    "harrisburg-pike": {
        "title": "Farrah's Threading & Beauty Studio, 1360A Harrisburg Pike, Lancaster PA",
        "desc": "Farrah's original Lancaster studio, 1360A Harrisburg Pike: eyebrow threading (walk in), tinting, lash lift, lamination, waxing, facials and HydraFacial.",
        "h1": "Harrisburg Pike <em>studio.</em>",
        "lede": "Our standalone studio at 1360A Harrisburg Pike in Lancaster, with the full menu: eyebrow and facial threading, eyebrow and lash tinting, lash lift, brow lamination, eyelash extensions, waxing, custom facials, HydraFacial and henna.",
        "where": "pike",
        "notes": [
            "Eyebrow threading is walk-in only, first come, first served. Everything else is by appointment: send a request online and we'll call or text to confirm.",
            "This is the only studio offering eyelash extensions, waxing, custom facials, HydraFacial and henna.",
            "Gift cards are sold here and are good at both studios.",
            "Farrah's moved here from Harrisburg in 2018; the Park City Center bar inside the mall opened in 2026.",
        ],
    },
    "park-city-center": {
        "title": "Farrah's Threading at Park City Center Mall, Lancaster PA",
        "desc": "Farrah's brow and lash bar inside Park City Center mall, Lancaster PA: eyebrow threading (walk in), tinting, lash lift and brow lamination. Open 7 days.",
        "h1": "Park City <em>Center.</em>",
        "lede": "Our brow and lash bar inside Park City Center mall, where Farrah's first opened its doors. Eyebrow threading, eyebrow tinting, lash tinting, lash lift and brow lamination, seven days a week.",
        "where": "both",
        "notes": [
            "Eyebrow threading is walk-in only, first come, first served. Tinting, lash lift and brow lamination are by appointment: send a request online and we'll call or text to confirm.",
            "Facials, HydraFacial, eyelash extensions, waxing and henna are offered at our Harrisburg Pike studio, a few minutes away.",
            "Open Sundays, unlike the Harrisburg Pike studio. Find us on the mall directory for the nearest entrance and parking.",
            "Gift cards are good at both studios.",
        ],
    },
}

# The homepage service cards, keyed by the page they link to (so the location pages show the same cards)
_grid = re.search(r'<div class="services">\n(.*?)\n      </div>', index, re.S).group(1)
HOME_CARDS = [(re.search(r'href="([a-z-]+)\.html"', card).group(1), card)
              for card in re.findall(r'<article class="service[^"]*">.*?</article>', _grid, re.S)]
BOTH_SLUGS = {s["slug"] for s in SERVICES if s.get("where") == "both"}

def service_cards(slugs_here, elsewhere_href=None):
    out = []
    for slug, card in HOME_CARDS:
        here = slug in slugs_here
        if here == bool(elsewhere_href):      # first call wants the local cards, second call the others
            continue
        card = re.sub(r'\s*<span class="where">[^<]*</span>', "", card)
        if elsewhere_href:
            card = card.replace("</article>", f'<span class="where"><a href="{elsewhere_href}" style="color:inherit;text-decoration:none">Visit Harrisburg Pike →</a></span>\n        </article>')
        out.append(card)
    return "\n".join(out)

def location_page(loc):
    c = LOC_COPY[loc["slug"]]
    other = next(l for l in SITE["locations"] if l["slug"] != loc["slug"])
    rows = [s for s in SERVICES if c["where"] == "pike" or s.get("where") == "both"]
    here = {s["slug"] for s in SERVICES} | {"hydrafacial"} if c["where"] == "pike" else BOTH_SLUGS
    cards = service_cards(here)
    if c["where"] == "pike":
        elsewhere = ""
    else:
        elsewhere = f"""
      <div class="section-head" style="margin-top:2.8rem"><p class="eyebrow">Also at Farrah's</p><h2 style="font-size:1.7rem">Offered at our <a href="{other["slug"]}.html" style="color:inherit">Harrisburg Pike studio</a>.</h2>
        <p class="lede">These services aren't available at Park City Center. Visit our Harrisburg Pike location at {other["address"][0]}, a few minutes away, or <a href="{BOOK_URL}" target="_blank" rel="noopener">request an appointment</a> there.</p></div>
      <div class="services">
        {service_cards(here, elsewhere_href=other["slug"] + ".html")}
      </div>"""
    hours = "".join(f"<dt>{h[0]}</dt><dd>{h[1]}</dd>" for h in loc["hours"])
    links = "".join(f'<a class="btn btn-ghost" href="{html.escape(u)}" target="_blank" rel="noopener">{html.escape(n)}</a>' for n, u in loc.get("links", []))
    phone = loc.get("phone") or SITE["phone"]
    tel = "+1" + re.sub(r"\D", "", phone)
    open_days = [h for h in loc["hours"] if "closed" not in h[1].lower()]
    sunday = next((h for h in loc["hours"] if h[0].startswith("Sun")), None)
    fact_days = "7 days" if sunday and "closed" not in sunday[1].lower() else "Mon–Sat"
    facts = "".join(f'<div class="fact"><strong>{a}</strong><span>{b}</span></div>' for a, b in [
        (fact_days, "a week" if fact_days == "7 days" else "closed Sunday"),
        ("Walk in", "for eyebrow threading, first come, first served"),
        (f"{len(rows) + (1 if c['where'] == 'pike' else 0)} services", "full menu" if c["where"] == "pike" else "brows &amp; lashes"),
    ])
    url = f"{seo.DOMAIN}/{loc['slug']}.html"
    graph = [seo.webpage_node(url, c["title"], c["desc"], about={"@id": seo.location_id(loc)}),
             seo.location_node(loc, SITE, seo.service_catalog(SERVICES, c["where"])),
             seo.breadcrumbs([("Home", seo.DOMAIN + "/"), ("Locations", seo.DOMAIN + "/#locations"), (loc["name"], None)])]
    body = f"""{header('locations')}
<main id="top">
  <section class="hero on-plum hydra-hero">
    <div class="wrap">
      <div class="hero-grid">
        <div class="hero-copy">
          <p class="crumbs"><a href="index.html">Home</a> › <a href="index.html#locations">Locations</a> › {loc["name"]}</p>
          <h1>{c["h1"]}</h1>
          <p class="lede">{c["lede"]}</p>
          <div class="hero-actions">
            <a class="btn btn-gold" href="{html.escape(loc["mapsUrl"])}" target="_blank" rel="noopener">Get directions</a>
            <a class="btn btn-outline" href="#services">See our services</a>
            <a class="btn btn-outline" href="{BOOK_URL}" target="_blank" rel="noopener">Request an appointment</a>
          </div>
        </div>
        <div class="hero-art" aria-hidden="true"><canvas id="art" data-art="brow" width="440" height="340"></canvas></div>
      </div>
      <div class="hero-facts">{facts}</div>
    </div>
  </section>

  <section class="band">
    <div class="wrap about-grid">
      <div>
        <p class="eyebrow">Visit us</p>
        <h2 style="margin:0.6rem 0 1.2rem">{loc["name"]}.</h2>
        <address class="addr" style="font-size:1.15rem">{"<br>".join(loc["address"])}</address>
        <p style="margin-top:0.8rem"><a href="tel:{tel}" style="color:inherit;text-decoration:none;font-size:1.15rem">{phone}</a></p>
        <div class="loc-actions" style="margin-top:1.2rem">
          <a class="btn btn-plum" href="{html.escape(loc["mapsUrl"])}" target="_blank" rel="noopener">Get directions</a>{links}
        </div>
      </div>
      <div class="story">
        <h3>Hours</h3>
        <dl class="hours">{hours}</dl>
        <p class="note" style="margin-top:1rem">Holiday hours may differ; call or text {phone} to check.</p>
      </div>
    </div>
  </section>

  <section id="services">
    <div class="wrap">
      <div class="section-head"><p class="eyebrow">Services at this studio</p><h2>What we offer here.</h2></div>
      <div class="services">
        {cards}
      </div>{elsewhere}
    </div>
  </section>

  <section class="band">
    <div class="wrap split">
      <div>
        <p class="eyebrow">Good to know</p>
        <h2>Before you come in.</h2>
        <p class="lede">Our other studio: <a href="{other["slug"]}.html">{other["name"]}</a>, {other["address"][0]}.</p>
        <div class="hero-actions" style="margin-top:1.2rem"><a class="btn btn-gold" href="{BOOK_URL}" target="_blank" rel="noopener">Request an appointment</a><a class="btn btn-ghost" href="index.html#gift">Gift cards</a></div>
      </div>
      <div><ul class="concerns" style="grid-template-columns:1fr">{li(c["notes"])}</ul></div>
    </div>
  </section>
</main>
{FOOTER}
<script>{NAV_JS}{ART_JS}</script>
</body>
</html>
"""
    return head(c["title"], c["desc"], f"{loc['slug']}.html", seo.ld(graph)) + body

for loc in SITE["locations"]:
    (root / f"{loc['slug']}.html").write_text(location_page(loc))
    print("built", loc["slug"] + ".html")
