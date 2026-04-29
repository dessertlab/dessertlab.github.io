#!/usr/bin/env python3
"""Migrate monolithic .bib files to individual per-entry files.

Before: bib/pubs_journal.bib  (all journal entries in one file)
After:  bib/journal/<key>.bib (one file per entry)

Run from the repo root with the Python that has bibtexparser:
    python tools/migrate_bib_to_individual.py
"""
from __future__ import annotations

import os
import re

import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.customization import convert_to_unicode


SOURCES = [
    ("bib/pubs_journal.bib",    "bib/journal"),
    ("bib/pubs_conference.bib", "bib/conference"),
    ("bib/pubs_editorial.bib",  "bib/editorial"),
    ("bib/pubs_book.bib",       "bib/book"),
]


def entry_to_bibtex(entry: dict) -> str:
    db = BibDatabase()
    db.entries = [dict(entry)]
    writer = BibTexWriter()
    writer.order_entries_by = None
    writer.indent = "  "
    writer.comma_first = False
    return bibtexparser.dumps(db, writer).strip()


def safe_filename(key: str) -> str:
    """Sanitize a bibtex key to a safe filename (no colons, slashes, etc.)."""
    return re.sub(r"[^\w\-]", "_", key)


def main() -> None:
    root = os.getcwd()

    for bib_rel, out_dir_rel in SOURCES:
        bib_path = os.path.join(root, bib_rel)
        out_dir = os.path.join(root, out_dir_rel)

        if not os.path.exists(bib_path):
            print(f"SKIP (not found): {bib_path}")
            continue

        parser = BibTexParser(common_strings=True)
        parser.ignore_nonstandard_types = False
        parser.homogenize_fields = False
        parser.interpolate_strings = True
        parser.customization = convert_to_unicode

        with open(bib_path, "r", encoding="utf-8") as fh:
            db = bibtexparser.load(fh, parser)

        os.makedirs(out_dir, exist_ok=True)
        written = 0
        for entry in db.entries:
            key = entry.get("ID") or entry.get("id") or ""
            if not key:
                print(f"  WARNING: entry with no key in {bib_path}, skipping")
                continue
            filename = safe_filename(key) + ".bib"
            out_path = os.path.join(out_dir, filename)
            with open(out_path, "w", encoding="utf-8") as fh:
                fh.write(entry_to_bibtex(entry) + "\n")
            written += 1

        print(f"{os.path.basename(bib_path)} -> {out_dir_rel}/  ({written} files)")


if __name__ == "__main__":
    main()
