#!/usr/bin/env python3
"""Static i18n site generator for the Ketut Bali Driver landing page.

Reads tools/template.html + tools/i18n/<lang>.json and writes one page per
language (English at the site root, others under /<lang>/), plus sitemap.xml.

Usage: python3 tools/build.py
"""
import json
from pathlib import Path
from string import Template
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://djomobil.github.io/personal-driver-bali/"
LANG_ORDER = ["en", "fr", "de", "ru", "zh"]

WA_PATH = (
    '<path fill="currentColor" d="M12 2a10 10 0 0 0-8.66 15L2 22l5.16-1.32A10 10 0 1 0 12 2Zm0 '
    "18.2c-1.5 0-2.96-.4-4.24-1.16l-.3-.18-3.06.79.81-2.98-.2-.31A8.16 8.16 0 1 1 12 20.2Zm4.48-6"
    ".1c-.24-.12-1.45-.71-1.67-.8-.22-.08-.39-.12-.55.13-.16.24-.63.79-.77.95-.14.16-.28.18-.53.0"
    "6a6.7 6.7 0 0 1-3.35-2.93c-.25-.43.25-.4.72-1.34.08-.16.04-.3-.02-.42-.06-.12-.55-1.33-.76-1"
    ".82-.2-.48-.4-.42-.55-.42h-.47c-.16 0-.43.06-.65.3-.22.25-.85.83-.85 2.03s.87 2.36 1 2.52c.1"
    "2.16 1.72 2.62 4.16 3.68.58.25 1.03.4 1.39.51.58.19 1.11.16 1.53.1.47-.07 1.45-.6 1.65-1.17."
    '2-.57.2-1.06.14-1.17-.06-.1-.22-.16-.47-.28Z"/>'
)
WA_ICON = f'<svg class="ico" viewBox="0 0 24 24" aria-hidden="true">{WA_PATH}</svg>'
WA_ICON_BIG = f'<svg viewBox="0 0 24 24" aria-hidden="true">{WA_PATH}</svg>'


def lang_url(code: str) -> str:
    return BASE if code == "en" else f"{BASE}{code}/"


def build():
    template = Template((ROOT / "tools" / "template.html").read_text(encoding="utf-8"))
    langs = {
        code: json.loads((ROOT / "tools" / "i18n" / f"{code}.json").read_text(encoding="utf-8"))
        for code in LANG_ORDER
    }

    hreflangs = "\n".join(
        f'  <link rel="alternate" hreflang="{c}" href="{lang_url(c)}">' for c in LANG_ORDER
    ) + f'\n  <link rel="alternate" hreflang="x-default" href="{BASE}">'

    for code, t in langs.items():
        prefix = "" if code == "en" else "../"
        canonical = lang_url(code)

        lang_options = "\n".join(
            f'      <option value="{lang_url(c) if c != code else "#"}"'
            f'{" selected" if c == code else ""}>{langs[c]["lang_name"]}</option>'
            for c in LANG_ORDER
        )
        footer_langs = " · ".join(
            f'<a href="{lang_url(c)}" lang="{c}">{langs[c]["lang_name"]}</a>'
            for c in LANG_ORDER if c != code
        )

        faq_html = "\n".join(
            "      <details>\n"
            f"        <summary>{item['q']}</summary>\n"
            f"        <p>{item['a']}</p>\n"
            "      </details>"
            for item in t["faq"]
        )
        faq_jsonld = json.dumps(
            {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": item["q"],
                        "acceptedAnswer": {"@type": "Answer", "text": item["a"]},
                    }
                    for item in t["faq"]
                ],
            },
            ensure_ascii=False,
            indent=2,
        )

        values = dict(t)
        values.pop("faq")
        for key in ("wa_generic", "wa_book", "wa_price1", "wa_price2", "wa_price3", "wa_price4"):
            values[key] = quote(t[key], safe="")
        values.update(
            prefix=prefix,
            base=BASE,
            canonical=canonical,
            hreflangs=hreflangs,
            lang_options=lang_options,
            footer_langs=footer_langs,
            faq_html=faq_html,
            faq_jsonld=faq_jsonld,
            waicon=WA_ICON,
            waicon_big=WA_ICON_BIG,
        )

        out = ROOT / "index.html" if code == "en" else ROOT / code / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(template.substitute(values), encoding="utf-8")
        print(f"wrote {out.relative_to(ROOT)}")

    alternates = "\n".join(
        f'    <xhtml:link rel="alternate" hreflang="{c}" href="{lang_url(c)}"/>' for c in LANG_ORDER
    ) + f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}"/>'
    urls = "\n".join(
        "  <url>\n"
        f"    <loc>{lang_url(c)}</loc>\n"
        "    <changefreq>monthly</changefreq>\n"
        f"    <priority>{'1.0' if c == 'en' else '0.9'}</priority>\n"
        f"{alternates}\n"
        "  </url>"
        for c in LANG_ORDER
    )
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        f"{urls}\n"
        "</urlset>\n",
        encoding="utf-8",
    )
    print("wrote sitemap.xml")


if __name__ == "__main__":
    build()
