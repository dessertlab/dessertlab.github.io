import bibtexparser
import pandas as pd
import sys
import re

def get_title(entry):

	title_field = entry['title']
	title_field = entry.fields_dict["title"].value
	title_field = re.sub('\s+',' ', title_field)
	title_field = title_field.replace('{', '')
	title_field = title_field.replace('}', '')
	
	return title_field 

def analyze(target_bib_1, target_bib_2):

	library_to_check = bibtexparser.parse_file(target_bib_1) # or bibtexparser.parse_file("my_file.bib")
	library_target = bibtexparser.parse_file(target_bib_2) # or bibtexparser.parse_file("my_file.bib")

	print("######### BIB FILE to check missing entries: " + target_bib_1)
	print(f"Parsed {len(library_to_check.blocks)} blocks, including:"
	  f"\n\t{len(library_to_check.entries)} entries"
	    f"\n\t{len(library_to_check.comments)} comments"
	    f"\n\t{len(library_to_check.strings)} strings and"
	    f"\n\t{len(library_to_check.preambles)} preambles")

	print("######### BIB FILE TARGET: " + target_bib_2)
	print(f"Parsed {len(library_target.blocks)} blocks, including:"
	  f"\n\t{len(library_target.entries)} entries"
	    f"\n\t{len(library_target.comments)} comments"
	    f"\n\t{len(library_target.strings)} strings and"
	    f"\n\t{len(library_target.preambles)} preambles")


	# get list of titles
	for entry in library_to_check.entries:
		title_to_check = get_title(entry)
		found = False
		for entry_target in library_target.entries:
			title_target = get_title(entry_target)
			if title_to_check.casefold() in title_target.casefold():
				found = True
		if found == False:
			print ("TITLE: " + title_to_check + " FOUND: " + str(found))

if __name__ == "__main__":
	target_bib_1 = sys.argv[1]
	target_bib_2 = sys.argv[2]
	analyze(target_bib_1, target_bib_2)
	
