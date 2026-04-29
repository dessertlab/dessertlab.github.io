#!/usr/bin/env python3
"""Generate static HTML includes for the publications page from BibTeX files.

Replaces the PHP-based pubs_*.html includes with static HTML so the site
works on GitHub Pages (no PHP server required). The generated HTML is
structurally identical to what bibtexbrowser.php produced at runtime.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.customization import convert_to_unicode


# ---------------------------------------------------------------------------
# BibTeX loading
# ---------------------------------------------------------------------------

def load_entries(bib_path: Path) -> list[dict]:
    """Load BibTeX entries from a directory of individual .bib files, sorted by year descending."""
    if not bib_path.exists():
        return []
    entries: list[dict] = []
    for f in sorted(bib_path.glob("*.bib")):
        parser = BibTexParser(common_strings=True)
        parser.ignore_nonstandard_types = False
        parser.homogenize_fields = False
        parser.interpolate_strings = True
        parser.customization = convert_to_unicode
        with f.open("r", encoding="utf-8") as fh:
            db = bibtexparser.load(fh, parser)
        entries.extend(db.entries)
    entries.sort(
        key=lambda e: -(int(e["year"]) if e.get("year", "").strip().isdigit() else 0)
    )
    return entries


# ---------------------------------------------------------------------------
# Field helpers
# ---------------------------------------------------------------------------

def field(entry: dict, key: str) -> str:
    """Return a cleaned field value (strips residual braces, normalises whitespace)."""
    val = entry.get(key, "") or ""
    val = val.replace("{", "").replace("}", "")
    val = re.sub(r"\s+", " ", val).strip()
    return val


def paper_url(entry: dict) -> str:
    """Return the best URL to the paper (url field, then DOI-derived)."""
    url = field(entry, "url")
    if url:
        return url
    doi = field(entry, "doi")
    if doi:
        return doi if doi.startswith("http") else f"https://doi.org/{doi}"
    return ""


def format_authors(raw: str) -> str:
    """Convert BibTeX author string → display form ('Last First, Last2 First2')."""
    raw = raw.replace("{", "").replace("}", "")
    parts = re.split(r"\s+and\s+", raw, flags=re.IGNORECASE)
    out = []
    for part in parts:
        part = re.sub(r"\s+", " ", part).strip()
        if "," in part:
            last, first = part.split(",", 1)
            out.append(f"{last.strip()} {first.strip()}")
        else:
            out.append(part)
    return ", ".join(out)


# ---------------------------------------------------------------------------
# HTML fragment helpers
# ---------------------------------------------------------------------------

def assets_html(entry: dict) -> str:
    """Render the pubassets div (bibtex popup button + DOI link)."""
    doi = field(entry, "doi")
    bib = entry_to_bibtex(entry)
    parts = []
    if bib:
        escaped_bib = html.escape(bib)
        parts.append(
            f'<a href="javascript:void(0)" class="bibtex-btn" data-toggle="tooltip" '
            f'data-placement="top" title="BibTeX entry" '
            f'data-bibtex="{escaped_bib}">'
            f'<i class="fa fa-quote-right"></i></a>'
        )
    if doi:
        doi_url = doi if doi.startswith("http") else f"https://doi.org/{doi}"
        parts.append(
            f'<a href="{html.escape(doi_url)}" data-toggle="tooltip" '
            f'data-placement="top" title="DOI" target="_blank" rel="noopener">'
            f'<i class="fa fa-cloud-download"></i></a>'
        )
    return '<div class="pubassets">' + "".join(parts) + "</div>"


def item_open(css_class: str, year: str, prev_year: str | None) -> list[str]:
    """Return the opening div for a publication entry, with optional year header."""
    lines = [f'<div class="item mix {css_class}" data-year={html.escape(year)}>']
    if year != prev_year:
        lines.append(f"<h2> {html.escape(year)} </h2>")
    return lines


def title_html(entry: dict) -> str:
    return (
        f'<h4 class="pubtitle"> '
        f'<strong>{html.escape(field(entry, "title"))}</strong></h4>'
    )


def authors_html(entry: dict) -> str:
    raw = entry.get("author", "") or ""
    if not raw:
        return ""
    return f'<div class="pubauthor">{html.escape(format_authors(raw))}</div>'


# ---------------------------------------------------------------------------
# Per-type renderers
# ---------------------------------------------------------------------------

def render_journal(entries: list[dict]) -> str:
    out: list[str] = []
    prev_year: str | None = None
    for entry in entries:
        year = field(entry, "year")
        out += item_open("jpaper", year, prev_year)
        prev_year = year

        out.append('<div class="pubmain">')
        out.append(assets_html(entry))
        out.append(title_html(entry))
        out.append(authors_html(entry))

        venue: list[str] = []
        if v := field(entry, "journal"):
            venue.append(html.escape(v))
        if v := field(entry, "volume"):
            venue.append(f"vol: {html.escape(v)}")
        if v := field(entry, "pages"):
            venue.append(f"pages: {html.escape(v)}")
        if year:
            venue.append(html.escape(year))
        out.append(f'<div>{", ".join(venue)}</div>')

        if doi := field(entry, "doi"):
            doi_url = doi if doi.startswith("http") else f"https://doi.org/{doi}"
            out.append(f'<div class="doi"><a href="{html.escape(doi_url)}" target="_blank" rel="noopener">DOI: {html.escape(doi)}</a></div>')
        if pub := field(entry, "publisher"):
            out.append(f'<div class="publisher">{html.escape(pub)}</div>')

        out.append(
            '<div class="pubcite">'
            '<span class="btn btn-success">Journal Papers</span>'
            "</div>"
        )
        out.append("</div>")  # pubmain
        out.append("</div>")  # item
    return "\n".join(out)


def render_conference(entries: list[dict]) -> str:
    out: list[str] = []
    prev_year: str | None = None
    for entry in entries:
        year = field(entry, "year")
        out += item_open("cpaper", year, prev_year)
        prev_year = year

        out.append('<div class="pubmain">')
        out.append(assets_html(entry))
        out.append(title_html(entry))
        out.append(authors_html(entry))

        if bt := field(entry, "booktitle"):
            out.append(f"<div>{html.escape(bt)}</div>")
        if doi := field(entry, "doi"):
            doi_url = doi if doi.startswith("http") else f"https://doi.org/{doi}"
            out.append(f'<div class="doi"><a href="{html.escape(doi_url)}" target="_blank" rel="noopener">DOI: {html.escape(doi)}</a></div>')

        out.append(
            '<div class="pubcite">'
            '<span class="btn btn-warning">Conference Papers</span>'
            "</div>"
        )
        out.append("</div>")
        out.append("</div>")
    return "\n".join(out)


def render_editorial(entries: list[dict]) -> str:
    out: list[str] = []
    prev_year: str | None = None
    for entry in entries:
        year = field(entry, "year")
        out += item_open("vpaper", year, prev_year)
        prev_year = year

        out.append('<div class="pubmain">')
        out.append(assets_html(entry))
        out.append(title_html(entry))
        out.append(authors_html(entry))

        if bt := field(entry, "booktitle"):
            out.append(f"<div>{html.escape(bt)}</div>")

        out.append(
            '<div class="pubcite">'
            '<span class="btn btn-primary">Editorials</span>'
            "</div>"
        )
        out.append("</div>")
        out.append("</div>")
    return "\n".join(out)


def render_book(entries: list[dict]) -> str:
    out: list[str] = []
    prev_year: str | None = None
    for entry in entries:
        year = field(entry, "year")
        out += item_open("bpaper", year, prev_year)
        prev_year = year

        out.append('<div class="pubmain">')
        out.append(assets_html(entry))
        out.append(title_html(entry))
        out.append(authors_html(entry))

        pub_parts: list[str] = []
        if v := field(entry, "publisher"):
            pub_parts.append(html.escape(v))
        if v := field(entry, "booktitle"):
            pub_parts.append(html.escape(v))
        if v := field(entry, "journal"):
            pub_parts.append(html.escape(v))
        if pub_parts:
            out.append(f'<div>{", ".join(pub_parts)}</div>')

        out.append(
            '<div class="pubcite">'
            '<span class="btn btn-danger">Books &amp; Book Chapters</span>'
            "</div>"
        )
        out.append("</div>")
        out.append("</div>")
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

SOURCES: list[tuple[str, str, str, str, object]] = [
    ("bib/journal",    "_includes/pubs_journal.html",    "journal",   "jpaper", render_journal),
    ("bib/conference", "_includes/pubs_conference.html", "conference","cpaper", render_conference),
    ("bib/editorial",  "_includes/pubs_editorial.html",  "editorial", "vpaper", render_editorial),
    ("bib/book",       "_includes/pubs_book.html",       "book",      "bpaper", render_book),
]

JSON_OUT = "assets/publications.json"


def entry_to_bibtex(entry: dict) -> str:
    db = BibDatabase()
    db.entries = [dict(entry)]
    writer = BibTexWriter()
    writer.order_entries_by = None
    writer.indent = "  "
    writer.comma_first = False
    return bibtexparser.dumps(db, writer).strip()


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", (value or "")).strip()


def strip_latex_for_search(value: str) -> str:
    value = normalize_space(value)
    value = value.replace("{", "").replace("}", "")
    value = value.replace("~", " ")
    value = value.replace("\\&", "&")
    value = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?(?:\{[^}]*\})?", " ", value)
    value = re.sub(r"\\.", " ", value)
    return normalize_space(value)


def build_json_record(entry: dict, category: str, css_class: str) -> dict:
    title = normalize_space(entry.get("title", ""))
    authors = normalize_space(entry.get("author", ""))
    year = normalize_space(str(entry.get("year", "")))
    key = entry.get("ID") or entry.get("id") or ""
    return {
        "id": key,
        "entry_type": normalize_space(entry.get("ENTRYTYPE", "")),
        "category": category,
        "css_class": css_class,
        "title": title,
        "authors": authors,
        "year": year,
        "search_text": strip_latex_for_search(f"{title} {authors} {year}").lower(),
        "bibtex": entry_to_bibtex(entry),
    }


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    all_json: list[dict] = []

    for bib_rel, out_rel, category, css_class, renderer in SOURCES:
        bib_path = root / bib_rel   # now a directory
        out_path = root / out_rel
        if not bib_path.exists():
            print(f"ERROR: missing BibTeX directory: {bib_path}")
            return 1
        entries = load_entries(bib_path)
        content = renderer(entries)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(content + "\n", encoding="utf-8")
        print(f"Wrote {len(entries)} entries -> {out_path.name}")
        all_json.extend(build_json_record(e, category, css_class) for e in entries)

    all_json.sort(key=lambda e: (
        -(int(e["year"]) if e["year"].isdigit() else -1),
        e["title"].lower(),
        e["id"].lower(),
    ))
    json_path = root / JSON_OUT
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(all_json, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(all_json)} records -> {json_path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
