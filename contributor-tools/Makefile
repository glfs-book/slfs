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

all: prep src man
src: prep build-docstubgen
man: prep build-docstubgen-manpage
install: src install-docstubgen install-docstubgen-compat-symlink
install-man: man install-docstubgen-man
World: all install install-man

clean:
	rm -rf $(OBJDIR)

prep:
	mkdir -p $(OBJDIR)/docstubgen

build-docstubgen-manpage: $(OBJDIR)/docstubgen/docstubgen.1
$(OBJDIR)/docstubgen/docstubgen.1: docstubgen/docstubgen.1.xml FRC
	xsltproc --output $(OBJDIR)/docstubgen/ $(XSLSTYLESHEET) docstubgen/docstubgen.1.xml

build-docstubgen: $(OBJDIR)/docstubgen/docstubgen $(OBJDIR)/docstubgen/docstubgen-checkfile
$(OBJDIR)/docstubgen/docstubgen: docstubgen/docstubgen FRC
	cp docstubgen/docstubgen $(OBJDIR)/docstubgen/

$(OBJDIR)/docstubgen/docstubgen-checkfile: docstubgen/docstubgen-checkfile FRC
	cp docstubgen/docstubgen-checkfile $(OBJDIR)/docstubgen/

install-docstubgen:
	sed -e 's=#prefix#="$(PREFIX)"=g' -e 's=#libexecdir#="$(LIBEXECDIR)"=g' -i $(OBJDIR)/docstubgen/docstubgen
	install -m755 -d $(DESTDIR)$(PREFIX)/$(BINDIR)
	install -m755 $(OBJDIR)/docstubgen/docstubgen $(DESTDIR)$(PREFIX)/$(BINDIR)
	install -m755 -d $(DESTDIR)$(PREFIX)/$(LIBEXECDIR)
	install -m755 $(OBJDIR)/docstubgen/docstubgen-checkfile $(DESTDIR)$(PREFIX)/$(LIBEXECDIR)

install-docstubgen-man: build-docstubgen-manpage
	install -m755 -d $(DESTDIR)$(PREFIX)/$(SHAREDIR)/man/man1
	install -m644 $(OBJDIR)/docstubgen/docstubgen.1 $(DESTDIR)$(PREFIX)/$(SHAREDIR)/man/man1

install-docstubgen-compat-symlink: install-docstubgen
	ln -sf docstubgen $(DESTDIR)$(PREFIX)/$(BINDIR)/generate-doc-stub.py

FRC:
