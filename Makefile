.PHONY: all build serve clean publications-assets

all: build

PYTHON ?= python3
JEKYLL ?= jekyll

SERVE_HOST ?= 127.0.0.1
SERVE_PORT ?= 4000

PUBS_INCLUDES = \
	_includes/pubs_editorial.html \
	_includes/pubs_book.html \
	_includes/pubs_journal.html \
	_includes/pubs_conference.html

PUBLICATIONS_JSON = assets/publications.json

publications-assets: $(PUBS_INCLUDES) $(PUBLICATIONS_JSON)

$(PUBS_INCLUDES) $(PUBLICATIONS_JSON): \
	bib/pubs_editorial.bib \
	bib/pubs_book.bib \
	bib/pubs_journal.bib \
	bib/pubs_conference.bib \
	tools/build_publications_assets.py
	mkdir -p _includes assets
	$(PYTHON) tools/build_publications_assets.py

build: publications-assets
	$(JEKYLL) build

serve: publications-assets
	$(JEKYLL) serve --port $(SERVE_PORT) --host $(SERVE_HOST)

clean:
	rm -rf _site
	rm -f $(PUBS_INCLUDES) $(PUBLICATIONS_JSON)
	$(JEKYLL) clean
