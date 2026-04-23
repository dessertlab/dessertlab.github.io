.PHONY: all build serve clean deploy publications-assets

all: build

BIBBLE ?= bibble
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

_includes/pubs_editorial.html: bib/pubs_editorial.bib bib/publications_editorial.tmpl
	mkdir -p _includes
	$(BIBBLE) $+ > $@

_includes/pubs_book.html: bib/pubs_book.bib bib/publications_book.tmpl
	mkdir -p _includes
	$(BIBBLE) $+ > $@

_includes/pubs_journal.html: bib/pubs_journal.bib bib/publications_journal.tmpl
	mkdir -p _includes
	$(BIBBLE) $+ > $@

_includes/pubs_conference.html: bib/pubs_conference.bib bib/publications_conference.tmpl
	mkdir -p _includes
	$(BIBBLE) $+ > $@

$(PUBLICATIONS_JSON): bib/pubs_editorial.bib bib/pubs_book.bib bib/pubs_journal.bib bib/pubs_conference.bib tools/build_publications_json.py
	mkdir -p assets
	$(PYTHON) tools/build_publications_json.py --output $@

build: publications-assets
	$(JEKYLL) build

serve: publications-assets
	$(JEKYLL) serve --port $(SERVE_PORT) --host $(SERVE_HOST)

clean:
	rm -rf _site
	rm -f $(PUBS_INCLUDES) $(PUBLICATIONS_JSON)
	$(JEKYLL) clean

deploy: clean build
	$(RSYNC) _site/ $(DEPLOY_HOST):$(DEPLOY_PATH)
