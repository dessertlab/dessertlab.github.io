import bibtexparser
import pandas as pd
import sys

def analyze(target_bib):
	library = bibtexparser.parse_file(target_bib) # or bibtexparser.parse_file("my_file.bib")

	print(f"Parsed {len(library.blocks)} blocks, including:"
	  f"\n\t{len(library.entries)} entries"
	    f"\n\t{len(library.comments)} comments"
	    f"\n\t{len(library.strings)} strings and"
	    f"\n\t{len(library.preambles)} preambles")

if __name__ == "__main__":
	target_bib = sys.argv[1]
	print("Target lib : " + target_bib)
	analyze(target_bib)
	
