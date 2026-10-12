"""Shared SEO helpers: reads the SITE config out of index.html (single source of truth) and
builds schema.org JSON-LD for the home page, the two location pages and the service pages."""
import json, re, subprocess, pathlib

ROOT = pathlib.Path(__file__).parent
DOMAIN = "https://farrahsthreading.com"
ORG_ID = f"{DOMAIN}/#organization"
WEBSITE_ID = f"{DOMAIN}/#website"
BRAND = "Farrah's Threading & Beauty Studio"
LOGO = f"{DOMAIN}/logo-mark.png"
SHARE = f"{DOMAIN}/share.jpg"

# Fixed facts that are not in the editable SITE block
GEO = {"harrisburg-pike": (40.057943, -76.333909)}   # from the Apple Business Connect listing
FOUNDED = "2011"


def load_site():
    """Evaluate the `const SITE = {...};` block from index.html with node and return it as a dict."""
    src = (ROOT / "index.html").read_text()
    m = re.search(r"const SITE = (\{.*?\n  \});", src, re.S)
    js = "const SITE = " + m.group(1) + "; process.stdout.write(JSON.stringify(SITE));"
    out = subprocess.run(["node", "-e", js], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def hours_spec(rows):
    days = {"Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday", "Thu": "Thursday", "Fri": "Friday", "Sat": "Saturday", "Sun": "Sunday"}
    order = list(days)
    def to24(t):
        m = re.match(r"^(\d{1,2})(?::(\d{2}))?\s*(am|pm)$", t.strip(), re.I)
        if not m: return None
        h = int(m.group(1)) % 12
        if m.group(3).lower() == "pm": h += 12
        return f"{h:02d}:{m.group(2) or '00'}"
    out = []
    for label, span in rows:
        if re.search("closed", span, re.I): continue
        parts = re.split(r"[–-]", span)
        if len(parts) != 2: continue
        opens, closes = to24(parts[0]), to24(parts[1])
        if not opens or not closes: continue
        lab = [p.strip()[:3] for p in re.split(r"[–-]", label)]
        i = order.index(lab[0]); j = order.index(lab[1]) if len(lab) > 1 else i
        out.append({"@type": "OpeningHoursSpecification", "dayOfWeek": [days[d] for d in order[i:j + 1]], "opens": opens, "closes": closes})
    return out


def postal(loc):
    zip_m = re.search(r"\d{5}", loc["address"][1])
    return {"@type": "PostalAddress", "streetAddress": loc["address"][0], "addressLocality": "Lancaster",
            "addressRegion": "PA", "postalCode": zip_m.group(0) if zip_m else None, "addressCountry": "US"}


def location_id(loc):
    return f"{DOMAIN}/#{loc['slug']}"


def location_node(loc, site, services):
    """BeautySalon node for one studio. `services` = list of (name, url) offered there."""
    same = [u for _, u in loc.get("links", []) if u and "g.page" not in u and "maps.apple" not in u]
    node = {
        "@type": "BeautySalon",
        "@id": location_id(loc),
        "name": f"{BRAND} – {loc['name']}",
        "alternateName": BRAND,
        "url": f"{DOMAIN}/{loc['slug']}.html",
        "image": SHARE,
        "logo": LOGO,
        "telephone": loc.get("phone") or site["phone"],
        "email": site.get("email") or None,
        "address": postal(loc),
        "hasMap": loc["mapsUrl"],
        "openingHoursSpecification": hours_spec(loc.get("hours", [])),
        "priceRange": "$$",
        "currenciesAccepted": "USD",
        "parentOrganization": {"@id": ORG_ID},
        "areaServed": {"@type": "City", "name": "Lancaster", "containedInPlace": {"@type": "State", "name": "Pennsylvania"}},
        "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": n, "url": u}} for n, u in services],
    }
    if loc["slug"] in GEO:
        lat, lng = GEO[loc["slug"]]
        node["geo"] = {"@type": "GeoCoordinates", "latitude": lat, "longitude": lng}
    if same: node["sameAs"] = same
    return {k: v for k, v in node.items() if v not in (None, "", [])}


def org_node(site):
    return {
        "@type": ["Organization", "BeautySalon"],
        "@id": ORG_ID,
        "name": BRAND,
        "legalName": site["legalName"],
        "url": DOMAIN + "/",
        "logo": {"@type": "ImageObject", "url": LOGO},
        "image": SHARE,
        "telephone": site["phone"],
        "email": site.get("email") or None,
        "foundingDate": FOUNDED,
        "description": "Hand-shaped eyebrow threading, facial threading, eyebrow and lash tinting, brow lamination, lash lifts, eyelash extensions, waxing, custom facials, HydraFacial and henna in Lancaster, Pennsylvania.",
        "sameAs": [u for u in [site.get("instagram"), site.get("facebook"), site.get("tiktok"), site.get("google")] if u],
        "areaServed": {"@type": "City", "name": "Lancaster", "containedInPlace": {"@type": "State", "name": "Pennsylvania"}},
        "address": postal(site["locations"][0]),
        "location": [{"@id": location_id(l)} for l in site["locations"]],
        "subOrganization": [{"@id": location_id(l)} for l in site["locations"]],
    }


def website_node():
    return {"@type": "WebSite", "@id": WEBSITE_ID, "url": DOMAIN + "/", "name": BRAND, "publisher": {"@id": ORG_ID}, "inLanguage": "en-US"}


def webpage_node(url, name, desc, about=None):
    n = {"@type": "WebPage", "@id": url, "url": url, "name": name, "description": desc, "isPartOf": {"@id": WEBSITE_ID}, "inLanguage": "en-US", "primaryImageOfPage": SHARE}
    if about: n["about"] = about
    return n


def breadcrumbs(items):
    """items = [(name, url), ...] in order."""
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, **({"item": u} if u else {})} for i, (n, u) in enumerate(items)]}


def service_node(name, desc, url, site, where, category=None):
    locs = site["locations"] if where == "both" else [site["locations"][0]]
    return {
        "@type": "Service",
        "@id": url + "#service",
        "name": name,
        "serviceType": name,
        "category": category or "Beauty",
        "description": desc,
        "url": url,
        "provider": {"@id": ORG_ID},
        "areaServed": {"@type": "City", "name": "Lancaster", "containedInPlace": {"@type": "State", "name": "Pennsylvania"}},
        "availableAtOrFrom": [{"@id": location_id(l)} for l in locs],
        "hoursAvailable": hours_spec(locs[0].get("hours", [])) if where != "both" else None,
    }


def clean(obj):
    if isinstance(obj, dict): return {k: clean(v) for k, v in obj.items() if v not in (None, "", [], {})}
    if isinstance(obj, list): return [clean(v) for v in obj]
    return obj


def ld(graph):
    data = {"@context": "https://schema.org", "@graph": [clean(n) for n in graph]}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False).replace("</", "<\\/") + "</script>"


def service_catalog(services, where):
    """(name, url) pairs for the services offered at a studio ('pike' = everything, 'both' = both-studio services)."""
    rows = [(s["nav"], f"{DOMAIN}/{s['slug']}.html") for s in services if where == "pike" or s.get("where") == "both"]
    if where == "pike": rows.append(("HydraFacial", f"{DOMAIN}/hydrafacial.html"))
    return rows
