#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter


SOURCES = [
    ("bib/pubs_journal.bib", "journal", "jpaper"),
    ("bib/pubs_conference.bib", "conference", "cpaper"),
    ("bib/pubs_editorial.bib", "editorial", "vpaper"),
    ("bib/pubs_book.bib", "book", "bpaper"),
]


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


def entry_to_bibtex(entry: dict) -> str:
    db = BibDatabase()
    db.entries = [dict(entry)]

    writer = BibTexWriter()
    writer.order_entries_by = None
    writer.indent = "  "
    writer.comma_first = False

    return bibtexparser.dumps(db, writer).strip()


def load_bib_entries(path: Path, category: str, css_class: str) -> list[dict]:
    parser = BibTexParser(common_strings=True)
    parser.ignore_nonstandard_types = False
    parser.homogenize_fields = False
    parser.interpolate_strings = True

    with path.open("r", encoding="utf-8") as handle:
        bib_db = bibtexparser.load(handle, parser=parser)

    result: list[dict] = []

    for entry in bib_db.entries:
        title = normalize_space(entry.get("title", ""))
        authors = normalize_space(entry.get("author", ""))
        year = normalize_space(str(entry.get("year", "")))
        key = entry.get("ID") or entry.get("id") or ""

        item = {
            "id": key,
            "entry_type": normalize_space(entry.get("ENTRYTYPE", "")),
            "category": category,
            "css_class": css_class,
            "source_file": str(path),
            "title": title,
            "authors": authors,
            "year": year,
            "search_text": strip_latex_for_search(f"{title} {authors} {year}").lower(),
            "bibtex": entry_to_bibtex(entry),
        }
        result.append(item)

    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="assets/publications.json",
        help="Output JSON file path",
    )
    args = parser.parse_args()

    items: list[dict] = []
    for rel_path, category, css_class in SOURCES:
        path = Path(rel_path)
        if not path.exists():
            raise FileNotFoundError(f"Missing BibTeX source: {path}")
        items.extend(load_bib_entries(path, category, css_class))

    items.sort(
        key=lambda item: (
            -(int(item["year"]) if item["year"].isdigit() else -1),
            item["title"].lower(),
            item["id"].lower(),
        )
    )

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(items, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Wrote {len(items)} entries to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
