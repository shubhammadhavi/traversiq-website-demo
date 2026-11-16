#!/usr/bin/env python3
"""Builds the Traversiq Global site from _source/template.html.

Edit template.html (shared layout + all page content) or policy-content.html,
then run:   python3 _source/build.py
It rewrites every page in the site root. Upload the site root to GitHub Pages.
"""
import html
import json
import re
from datetime import date
from pathlib import Path

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
SITE = "https://traversiq.com"

# One entry per real URL. `service` / `dest` pre-fill the enquiry desk on that page.
PAGES = {
    "home": {
        "path": "/",
        "title": "Traversiq Global | US Visas, Passports & Tours — Panvel",
        "desc": "Direct US F1 & B1/B2 visa interview prep, Schengen & global visas, Passport & Tatkaal desk, and custom holidays in Taloja, Panvel, Navi Mumbai.",
        "service": "US F1 / B1-B2 Visa & Interview Prep",
        "dest": "",
    },
    "us-visa": {
        "path": "/us-visa/",
        "crumb": "US Visas",
        "title": "US F1 & B1/B2 Visa Prep in Panvel | Traversiq Global",
        "desc": "US F1 student and B1/B2 visitor visa coaching, DS-160 & social media check, 214(b) refusal review, and mock interviews by Shubham Madhavi.",
        "service": "US F1 / B1-B2 Visa & Interview Prep",
        "dest": "USA (F1 Student / B1-B2 Visitor Visa)",
    },
    "global-visas": {
        "path": "/global-visas/",
        "crumb": "Global Visas",
        "title": "Schengen, UAE & UK Visa Assistance | Traversiq Global",
        "desc": "Schengen Europe cover letters, VFS biometric slot booking, UAE e-Visas, and UK/Australia/Canada visitor visa filings in Panvel, Navi Mumbai.",
        "service": "Schengen / UK / Global Tourist Visa",
        "dest": "Schengen / Dubai / UK / Global Tourist Visa",
    },
    "passport": {
        "path": "/passport-services/",
        "crumb": "Passports",
        "title": "Passport & Tatkaal Desk in Panvel | Traversiq Global",
        "desc": "Online Passport Seva filing, Tatkaal slot monitoring, Police Clearance Certificate (PCC), and pre-PSK document check in Taloja, Panvel.",
        "service": "Indian Passport / Tatkaal / PCC",
        "dest": "Taloja / Panvel / Navi Mumbai Passport Seva",
    },
    "flights": {
        "path": "/flights-holidays/",
        "crumb": "Flights & Tours",
        "title": "Student Flights & Custom Tour Packages | Traversiq Global",
        "desc": "Student extra-baggage flight tickets and custom family holiday packages to Thailand, Dubai, Bali, Vietnam, Europe, Kashmir, and Kerala.",
        "service": "Flights & Custom Holiday Package",
        "dest": "Student Flight Ticket / Custom Family Tour",
    },
}

POLICY = {
    "path": "/privacy-terms/",
    "crumb": "Privacy & Terms",
    "title": "Privacy, Terms & Refund Policy | Traversiq Global",
    "desc": "How Traversiq Global handles your personal data and documents, our document integrity policy, consultancy fee terms, and refund and cancellation rules.",
}

template = (SRC / "template.html").read_text(encoding="utf-8")
use_compiled_css = (ROOT / "assets" / "site.css").exists()


def esc(text):
    return html.escape(text, quote=True)


def breadcrumb_ld(page):
    if "crumb" not in page:
        return ""
    data = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": page["crumb"], "item": SITE + page["path"]},
        ],
    }
    return '    <script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>\n"


def fill(doc, page, robots="index, follow", canonical=True):
    """Fill the per-page placeholders and pick the Tailwind source."""
    url = SITE + page["path"]
    if use_compiled_css:
        doc, n = re.subn(r"[ \t]*<!--@tw-cdn-->.*?<!--@/tw-cdn-->\n", "", doc, flags=re.S)
        doc = doc.replace("{{BREADCRUMB_LD}}", '{{BREADCRUMB_LD}}    <link rel="stylesheet" href="/assets/site.css">\n')
    else:
        doc = re.sub(r"[ \t]*<!--@/?tw-cdn-->\n", "", doc)
    values = {
        "{{TITLE}}": esc(page["title"]),
        "{{DESC}}": esc(page["desc"]),
        "{{CANONICAL_TAG}}": f'    <link rel="canonical" href="{url}">' if canonical else "",
        "{{ROBOTS}}": robots,
        "{{URL}}": url,
        "{{BREADCRUMB_LD}}": breadcrumb_ld(page),
        "{{SERVICE}}": esc(page.get("service", "")),
        "{{DEST}}": esc(page.get("dest", "")),
    }
    for key, value in values.items():
        doc = doc.replace(key, value)
    assert "{{" not in doc.split("<body", 1)[0], "unfilled placeholder in <head>"
    return doc


def render_service_page(key):
    page = PAGES[key]

    def pick(match):
        return match.group(2) if key in match.group(1).split(",") else ""

    doc = re.sub(r"[ \t]*<!--@only ([\w,-]+)-->(.*?)<!--@end-->\n?", pick, template, flags=re.S)
    # highlight this page in the desktop nav
    doc = doc.replace(
        f'data-nav="{key}" class="nav-tab hover:text-navy',
        f'data-nav="{key}" aria-current="page" class="nav-tab text-navy border-b-2 border-gold',
    )
    doc = fill(doc, page)
    assert len(re.findall(r"<h1\b", doc)) == 1, f"{key}: expected exactly one <h1>"
    return doc


HEAD = template.split("</head>", 1)[0] + "</head>\n"

SIMPLE_BODY = """<body class="font-sans antialiased selection:bg-navy selection:text-white">

    <header class="bg-white border-b border-slate-200 shadow-sm">
        <div class="max-w-5xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between gap-4">
            <a href="/" class="font-serif font-bold text-base sm:text-lg text-navy tracking-tight whitespace-nowrap">TRAVERSIQ GLOBAL</a>
            <nav aria-label="Main Navigation" class="flex items-center gap-4 text-xs font-semibold text-slate-700">
                <a href="/us-visa/" class="hidden sm:inline hover:text-navy">US Visas</a>
                <a href="/global-visas/" class="hidden sm:inline hover:text-navy">Global Visas</a>
                <a href="/passport-services/" class="hidden sm:inline hover:text-navy">Passports</a>
                <a href="/flights-holidays/" class="hidden sm:inline hover:text-navy">Flights &amp; Tours</a>
                <a href="/" class="px-3 py-2 rounded-lg bg-navy hover:bg-navyLight text-white font-bold">Home</a>
            </nav>
        </div>
    </header>

    <main class="max-w-3xl mx-auto px-4 sm:px-6 py-10 md:py-14">
{{MAIN}}
    </main>

    <footer class="bg-navy text-slate-300 py-8 border-t-4 border-gold text-xs">
        <div class="max-w-5xl mx-auto px-4 sm:px-6 space-y-3">
            <p><strong class="text-white font-serif tracking-wide">TRAVERSIQ GLOBAL</strong> • ISP 10, Plot No. 88, Near CNG Pump, Opp. Aditya Birla, Taloja, Panvel, Navi Mumbai, Maharashtra 410208</p>
            <p class="flex flex-wrap gap-x-5 gap-y-2 font-semibold text-amber-300">
                <a href="/" class="hover:underline">Overview</a>
                <a href="/us-visa/" class="hover:underline">US Visa Consultation</a>
                <a href="/global-visas/" class="hover:underline">Global Visas</a>
                <a href="/passport-services/" class="hover:underline">Passport Desk</a>
                <a href="/flights-holidays/" class="hover:underline">Flights &amp; Tours</a>
                <a href="/privacy-terms/" class="hover:underline">Privacy, Terms &amp; Refunds</a>
            </p>
            <p class="text-slate-400">&copy; <span id="year"></span> Traversiq Global. All rights reserved.</p>
        </div>
    </footer>

    <script>document.getElementById('year').textContent = new Date().getFullYear();</script>
</body>
</html>
"""


def render_simple_page(page, main_html, **head_options):
    return fill(HEAD, page, **head_options) + SIMPLE_BODY.replace("{{MAIN}}", main_html)


def policy_main():
    content = (SRC / "policy-content.html").read_text(encoding="utf-8")
    return f"""        <p class="text-xs font-bold uppercase tracking-wider text-crimson">Legal &amp; Compliance Policies</p>
        <h1 class="font-serif text-2xl sm:text-4xl font-bold text-navy mt-1 leading-snug">Privacy Policy, Terms of Service &amp; Refund Policy</h1>
        <div class="mt-8 space-y-7 text-sm text-slate-700 leading-relaxed">
{content}        </div>
        <p class="mt-10">
            <a href="/" class="text-sm font-bold text-navy hover:underline">&larr; Back to Traversiq Global</a>
        </p>"""


NOT_FOUND_MAIN = """        <p class="text-xs font-bold uppercase tracking-wider text-crimson">Error 404</p>
        <h1 class="font-serif text-2xl sm:text-4xl font-bold text-navy mt-1 leading-snug">This page could not be found.</h1>
        <p class="mt-4 text-sm text-slate-600 leading-relaxed">The link may be old or mistyped. These pages cover everything we do:</p>
        <ul class="mt-6 grid grid-cols-1 sm:grid-cols-2 gap-3 text-sm font-semibold text-navy">
            <li><a href="/" class="block px-4 py-3 rounded-lg bg-white border border-slate-300 hover:border-navy">Overview &amp; all service desks</a></li>
            <li><a href="/us-visa/" class="block px-4 py-3 rounded-lg bg-white border border-slate-300 hover:border-navy">US F1 &amp; B1/B2 visa prep</a></li>
            <li><a href="/global-visas/" class="block px-4 py-3 rounded-lg bg-white border border-slate-300 hover:border-navy">Schengen, UAE &amp; global visas</a></li>
            <li><a href="/passport-services/" class="block px-4 py-3 rounded-lg bg-white border border-slate-300 hover:border-navy">Passport &amp; Tatkaal desk</a></li>
            <li><a href="/flights-holidays/" class="block px-4 py-3 rounded-lg bg-white border border-slate-300 hover:border-navy">Flights &amp; custom tours</a></li>
            <li><a href="https://wa.me/919324666369" target="_blank" rel="noopener noreferrer" class="block px-4 py-3 rounded-lg bg-whatsapp text-white hover:bg-emerald-800">Message us on WhatsApp</a></li>
        </ul>"""


def write(path, text):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    print(f"  {path}  ({len(text) // 1024} KB)")


def main():
    print("Tailwind:", "compiled /assets/site.css" if use_compiled_css else "CDN (assets/site.css not found)")
    urls = []
    for key, page in PAGES.items():
        write(page["path"].lstrip("/") + "index.html", render_service_page(key))
        urls.append(page["path"])
    write("privacy-terms/index.html", render_simple_page(POLICY, policy_main()))
    urls.append(POLICY["path"])
    not_found = {"path": "/", "title": "Page Not Found | Traversiq Global", "desc": "This page could not be found on traversiq.com."}
    write("404.html", render_simple_page(not_found, NOT_FOUND_MAIN, robots="noindex, follow", canonical=False))

    today = date.today().isoformat()
    entries = "".join(f"  <url>\n    <loc>{SITE}{u}</loc>\n    <lastmod>{today}</lastmod>\n  </url>\n" for u in urls)
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + entries + "</urlset>\n")


if __name__ == "__main__":
    main()
