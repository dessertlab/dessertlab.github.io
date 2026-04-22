import bibtexparser
import pandas as pd
import sys

def clean(target_bib):
	library = bibtexparser.parse_file(target_bib) # or bibtexparser.parse_file("my_file.bib")

	print(f"Parsed {len(library.blocks)} blocks, including:"
	  f"\n\t{len(library.entries)} entries"
	    f"\n\t{len(library.comments)} comments"
	    f"\n\t{len(library.strings)} strings and"
	    f"\n\t{len(library.preambles)} preambles")

	cleaned_library = bibtexparser.Library()

	for entry in library.blocks:
		if not isinstance(entry, bibtexparser.model.DuplicateBlockKeyBlock):
			cleaned_library.add(entry)
		else:
			key = entry.key
			print(key + " is DUPLICATED, do not add")

	bibtexparser.write_file("cleaned.bib", cleaned_library)

if __name__ == "__main__":
	target_bib = sys.argv[1]
	print("Target lib : " + target_bib)
	clean(target_bib)
	
