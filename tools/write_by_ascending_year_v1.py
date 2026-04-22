import bibtexparser
import pandas as pd
import sys
from bibtexparser.bwriter import BibTexWriter, SortingStrategy

def write_ascending_order_year(target_lib):

	with open(target_lib) as bibtex_file:
	    library = bibtexparser.load(bibtex_file)

	#pubs_bibtex = bibtexparser.bwriter.to_bibtex(library)
	writer = BibTexWriter()
	#writer.contents = ['entries']
	writer.order_entries_by = ('year',)
	writer.order_sorting = SortingStrategy.ALPHABETICAL_DESC
	pubs_bibtex = bibtexparser.dumps(library, writer)
	#print(result)
	with open("ascending.bib", "w") as file:
		file.write(pubs_bibtex)

if __name__ == "__main__":
	target_lib = sys.argv[1]
	write_ascending_order_year(target_lib)
