# Makefile for LFS-QOL Contributor Tools
# (C) Seal Sealy (seal331) 2025

XSL_PATH ?= /usr/share/xml/docbook/xsl-stylesheets-nons-1.79.2
XSLSTYLESHEET ?= $(XSL_PATH)/manpages/docbook.xsl
DESTDIR ?=
PREFIX ?= /usr/local
BINDIR ?= bin
LIBEXECDIR ?= libexec
SHAREDIR ?= share
OBJDIR ?= obj

all: man
man: build-docstubgen-manpage
install: install-docstubgen install-docstubgen-compat-symlink
install-man: install-docstubgen-man
World: all install install-man

clean:
	rm -rf $(OBJDIR)

build-docstubgen-manpage: $(OBJDIR)/docstubgen/docstubgen.1
$(OBJDIR)/docstubgen/docstubgen.1: docstubgen/docstubgen.1.xml
	mkdir -p $(OBJDIR)/docstubgen/
	xsltproc --output $(OBJDIR)/docstubgen/ $(XSLSTYLESHEET) docstubgen/docstubgen.1.xml
	cp docstubgen/docstubgen $(OBJDIR)/docstubgen/
	cp docstubgen/checkfile.sh $(OBJDIR)/docstubgen/

install-docstubgen:
	install -m755 -d $(DESTDIR)$(PREFIX)/$(BINDIR)
	install -m755 $(OBJDIR)/docstubgen/docstubgen $(DESTDIR)$(PREFIX)/$(BINDIR)
	install -m755 -d $(DESTDIR)$(PREFIX)/$(LIBEXECDIR)
	install -m755 $(OBJDIR)/docstubgen/checkfile.sh $(DESTDIR)$(PREFIX)/$(LIBEXECDIR)

install-docstubgen-man: build-docstubgen-manpage
	install -m755 -d $(DESTDIR)$(PREFIX)/$(SHAREDIR)/man/man1
	install -m644 $(OBJDIR)/docstubgen/docstubgen.1 $(DESTDIR)$(PREFIX)/$(SHAREDIR)/man/man1

install-docstubgen-compat-symlink: install-docstubgen
	ln -sf docstubgen $(DESTDIR)$(PREFIX)/$(BINDIR)/generate-doc-stub.py
