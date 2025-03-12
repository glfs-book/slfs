# Makefile for LFS-QOL Contributor Tools
# (C) Seal Sealy (seal331) 2025

XSLSTYLESHEET ?= /usr/share/xml/docbook/xsl-stylesheets-nons-1.79.2/manpages/docbook.xsl
DESTDIR ?=
OBJDIR ?= obj

all: build-docstubgen-manpage
install: install-docstubgen install-docstubgen-compat-symlink
World: all install

clean:
	rm -rf $(OBJDIR)/docstubgen

build-docstubgen-manpage: $(OBJDIR)/docstubgen/docstubgen.1
$(OBJDIR)/docstubgen/docstubgen.1: docstubgen/docstubgen.1.xml
	mkdir -p $(OBJDIR)/docstubgen/
	xsltproc --output $(OBJDIR)/docstubgen/ $(XSLSTYLESHEET) docstubgen/docstubgen.1.xml
	cp docstubgen/docstubgen $(OBJDIR)/docstubgen/
	cp docstubgen/checkfile.sh $(OBJDIR)/docstubgen/

install-docstubgen: build-docstubgen-manpage
	install -m755 -d $(DESTDIR)/usr/bin
	install -m755 $(OBJDIR)/docstubgen/docstubgen $(DESTDIR)/usr/bin
	install -m755 -d $(DESTDIR)/usr/libexec
	install -m755 $(OBJDIR)/docstubgen/checkfile.sh $(DESTDIR)/usr/libexec
	install -m755 -d $(DESTDIR)/usr/share/man/man1
	install -m644 $(OBJDIR)/docstubgen/docstubgen.1 $(DESTDIR)/usr/share/man/man1

install-docstubgen-compat-symlink: install-docstubgen
	ln -sf docstubgen /usr/bin/generate-doc-stub.py
