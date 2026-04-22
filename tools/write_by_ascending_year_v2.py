import bibtexparser
import pandas as pd
import sys

def write_ascending_order_year(target_bib):

	library = bibtexparser.parse_file(target_bib) # or bibtexparser.parse_file("my_file.bib")
	bibtexparser.write_file("ascending.bib", library)


if __name__ == "__main__":
	target_bib = sys.argv[1]
	write_ascending_order_year(target_bib)
