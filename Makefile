# targets that aren't filenames
.PHONY: all clean deploy build serve

all: build

BIBBLE = bibble

_includes/pubs_editorial.php: bib/pubs_editorial.bib bib/publications_editorial.tmpl
	mkdir -p _includes
	$(BIBBLE) $+ > $@

_includes/pubs_book.php: bib/pubs_book.bib bib/publications_book.tmpl
	mkdir -p _includes
	$(BIBBLE) $+ > $@

_includes/pubs_journal.php: bib/pubs_journal.bib bib/publications_journal.tmpl
	mkdir -p _includes
	$(BIBBLE) $+ > $@

_includes/pubs_conference.php: bib/pubs_conference.bib bib/publications_conference.tmpl
	mkdir -p _includes
	$(BIBBLE) $+ > $@

build: _includes/pubs_editorial.php _includes/pubs_book.php _includes/pubs_journal.php _includes/pubs_conference.php
	jekyll build

# you can configure these at the shell, e.g.:
# SERVE_PORT=5001 make serve
# SERVE_HOST ?= 192.168.100.5
# SERVE_PORT ?= 4000

serve: _includes/pubs_editorial.php _includes/pubs_book.php _includes/pubs_journal.php _includes/pubs_conference.php
	jekyll serve --port $(SERVE_PORT) --host $(SERVE_HOST)

clean:
	$(RM) -r _site/* _includes/pubs_editorial.php _includes/pubs_book.php _includes/pubs_journal.php _includes/pubs_conference.php
	jekyll clean

deploy: clean build
	$(RSYNC) _site/ $(DEPLOY_HOST):$(DEPLOY_PATH)
