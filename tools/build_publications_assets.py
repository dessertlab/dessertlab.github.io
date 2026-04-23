#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from collections import defaultdict
from html import escape
from pathlib import Path

import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter

ROOT = Path(__file__).resolve().parent.parent

SOURCES = [
    {
        "bib": ROOT / "bib" / "pubs_journal.bib",
        "include": ROOT / "_includes" / "pubs_journal.html",
        "category": "journal",
        "css_class": "jpaper",
    },
    {
        "bib": ROOT / "bib" / "pubs_conference.bib",
        "include": ROOT / "_includes" / "pubs_conference.html",
        "category": "conference",
        "css_class": "cpaper",
    },
    {
        "bib": ROOT / "bib" / "pubs_editorial.bib",
        "include": ROOT / "_includes" / "pubs_editorial.html",
        "category": "editorial",
        "css_class": "vpaper",
    },
    {
        "bib": ROOT / "bib" / "pubs_book.bib",
        "include": ROOT / "_includes" / "pubs_book.html",
        "category": "book",
        "css_class": "bpaper",
    },
]

JSON_OUT = ROOT / "assets" / "publications.json"


def norm(value: str | None) -> str:
    return re.sub(r"\s+", " ", (value or "")).strip()


def strip_latex(value: str) -> str:
    value = norm(value)
    value = value.replace("{", "").replace("}", "")
    value = value.replace("~", " ")
    value = value.replace("\\&", "&")
    value = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?(?:\{[^}]*\})?", " ", value)
    value = re.sub(r"\\.", " ", value)
    return norm(value)


def html_text(value: str | None) -> str:
    return escape(strip_latex(value or ""))


def format_authors(author_field: str) -> str:
    if not author_field:
        return ""
    authors = [a.strip() for a in author_field.split(" and ") if a.strip()]
    formatted = []
    for author in authors:
        if "," in author:
            last, first = [x.strip() for x in author.split(",", 1)]
            formatted.append(f"{first} {last}".strip())
        else:
            formatted.append(author)
    return ", ".join(formatted)


def bibtex_string(entry: dict) -> str:
    db = BibDatabase()
    db.entries = [dict(entry)]
    writer = BibTexWriter()
    writer.order_entries_by = None
    writer.indent = "  "
    writer.comma_first = False
    return bibtexparser.dumps(db, writer).strip()


def parse_bib(path: Path) -> list[dict]:
    parser = BibTexParser(common_strings=True)
    parser.ignore_nonstandard_types = False
    parser.homogenize_fields = False
    parser.interpolate_strings = True
    with path.open("r", encoding="utf-8") as fh:
        db = bibtexparser.load(fh, parser=parser)
    return db.entries


def year_key(entry: dict) -> int:
    year = norm(str(entry.get("year", "")))
    return int(year) if year.isdigit() else -1


def title_key(entry: dict) -> str:
    return strip_latex(entry.get("title", "")).lower()


def details_line(entry: dict, category: str) -> str:
    parts: list[str] = []

    primary = (
        entry.get("journal")
        or entry.get("booktitle")
        or entry.get("publisher")
        or entry.get("series")
    )
    if primary:
        parts.append(strip_latex(str(primary)))

    volume = norm(str(entry.get("volume", "")))
    if volume:
        parts.append(f"vol: {volume}")

    number = norm(str(entry.get("number", "")))
    if number:
        parts.append(f"no: {number}")

    pages = norm(str(entry.get("pages", "")))
    if pages:
        parts.append(f"pages: {pages}")

    year = norm(str(entry.get("year", "")))
    if year:
        parts.append(year)

    return ", ".join(parts)


def entry_url(entry: dict) -> str:
    for key in ("url", "doi"):
        value = norm(str(entry.get(key, "")))
        if not value:
            continue
        if key == "doi" and not value.lower().startswith("http"):
            return f"https://doi.org/{value}"
        return value
    return ""


def render_entry(entry: dict, css_class: str, category: str) -> str:
    title = html_text(entry.get("title", ""))
    authors = html_text(format_authors(entry.get("author", "")))
    year = html_text(str(entry.get("year", "")))
    doi_raw = norm(str(entry.get("doi", "")))
    doi_href = ""
    if doi_raw:
        doi_href = doi_raw if doi_raw.lower().startswith("http") else f"https://doi.org/{doi_raw}"

    publisher = html_text(str(entry.get("publisher", "")))
    details = html_text(details_line(entry, category))
    url = escape(entry_url(entry), quote=True)

    lines = [
        f'<div class="item {css_class}" data-year="{year}">',
        '  <div class="pubmain">',
        '    <div class="pubassets">',
    ]
    if url:
        lines.append(f'      <a href="{url}" target="_blank" rel="noopener noreferrer"><i class="fa fa-external-link"></i></a>')
    if doi_href:
        doi_esc = escape(doi_href, quote=True)
        lines.append(f'      <a href="{doi_esc}" target="_blank" rel="noopener noreferrer"><i class="fa fa-link"></i></a>')
    lines += [
        '    </div>',
        '    <div class="pubtitle">',
        f'      <strong>{title}</strong>',
        '    </div>',
    ]
    if authors:
        lines += [
            '    <div class="pubauthor">',
            f'      {authors}',
            '    </div>',
        ]
    if details:
        lines += [
            '    <div class="pubdetails">',
            f'      {details}',
            '    </div>',
        ]
    if doi_raw:
        lines += [
            '    <div class="pubdoi">',
            f'      DOI: {html_text(doi_raw)}',
            '    </div>',
        ]
    if publisher:
        lines += [
            '    <div class="pubpublisher">',
            f'      {publisher}',
            '    </div>',
        ]
    lines += [
        '  </div>',
        '</div>',
    ]
    return "\n".join(lines)


def write_include(entries: list[dict], include_path: Path, css_class: str, category: str) -> None:
    grouped: dict[int, list[dict]] = defaultdict(list)
    for entry in entries:
        grouped[year_key(entry)].append(entry)

    years = sorted(grouped.keys(), reverse=True)
    chunks: list[str] = []

    for year in years:
        display_year = str(year) if year >= 0 else "Unknown year"
        chunks.append(f'<h3 class="pubyear">{escape(display_year)}</h3>')
        for entry in sorted(grouped[year], key=title_key):
            chunks.append(render_entry(entry, css_class, category))

    include_path.parent.mkdir(parents=True, exist_ok=True)
    include_path.write_text("\n\n".join(chunks) + "\n", encoding="utf-8")


def build_json_record(entry: dict, category: str, css_class: str, source_file: str) -> dict:
    title = strip_latex(entry.get("title", ""))
    authors = format_authors(entry.get("author", ""))
    year = norm(str(entry.get("year", "")))

    return {
        "id": entry.get("ID", ""),
        "entry_type": norm(str(entry.get("ENTRYTYPE", ""))),
        "category": category,
        "css_class": css_class,
        "source_file": source_file,
        "title": title,
        "authors": authors,
        "year": year,
        "search_text": strip_latex(f"{title} {authors} {year}").lower(),
        "bibtex": bibtex_string(entry),
    }


def main() -> int:
    all_json_records: list[dict] = []

    for spec in SOURCES:
        entries = parse_bib(spec["bib"])
        write_include(entries, spec["include"], spec["css_class"], spec["category"])
        all_json_records.extend(
            build_json_record(
                entry,
                spec["category"],
                spec["css_class"],
                spec["bib"].name,
            )
            for entry in entries
        )

    all_json_records.sort(
        key=lambda item: (
            -(int(item["year"]) if item["year"].isdigit() else -1),
            item["title"].lower(),
            item["id"].lower(),
        )
    )

    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(
        json.dumps(all_json_records, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Wrote {len(all_json_records)} records to {JSON_OUT}")
    for spec in SOURCES:
        print(f"Wrote {spec['include']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
