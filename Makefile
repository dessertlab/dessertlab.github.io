.PHONY: all build serve clean publications-assets repo-meta


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

$(PUBS_INCLUDES) $(PUBLICATIONS_JSON): $(wildcard bib/pubs_*.bib) tools/build_publications_html.py
	mkdir -p _includes assets
	$(PYTHON) tools/build_publications_html.py

repo-meta:
	$(PYTHON) tools/fetch_repos.py $(if $(GITHUB_TOKEN),--token $(GITHUB_TOKEN),)

build: publications-assets repo-meta
	$(JEKYLL) build

serve: publications-assets repo-meta
	$(JEKYLL) serve --port $(SERVE_PORT) --host $(SERVE_HOST)

clean:
	rm -rf _site
	rm -f $(PUBS_INCLUDES) $(PUBLICATIONS_JSON)
	$(JEKYLL) clean
