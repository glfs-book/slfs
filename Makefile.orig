# vim:ts=3
# Makefile for LFS_QOL Book generation.
# By Tushar Teredesai <tushar@linuxfromscratch.org>
# Edited by Zeckma <zeckma.tech@gmail.com>
# 2004-01-31

# When rendering for the stable release from the stable branch, invoke
# STAB=release to make.
-include local.mk

# Adjust these to suit your installation, or include the variables
# you wish to change in local.mk, which must be created manually.
LFS_QOL_THEME  ?= dark
RENDERTMP      := $(shell mktemp -d)
HTML_ROOT      ?= $(HOME)/public_html
DUMP_ROOT      ?= $(HOME)
CHUNK_QUIET    ?= 1
ROOT_ID         =
SHELL           = /bin/bash

ALLXML := $(filter-out $(RENDERTMP)/%, \
	$(wildcard *.xml */*.xml */*/*.xml */*/*/*.xml */*/*/*/*.xml))
ALLXSL := $(filter-out $(RENDERTMP)/%, \
	$(wildcard *.xsl */*.xsl */*/*.xsl */*/*/*.xsl */*/*/*/*.xsl))

ifdef V
  Q =
else
  Q = @
endif

ifndef REV
  REV = sysv
endif
ifneq ($(REV), sysv)
  ifneq ($(REV), systemd)
    $(error REV must be 'sysv' (default) or 'systemd')
  endif
endif

# Used in the book, does not actually change if the book will render for the
# stable git hash, just changes if text for stable release is rendered or not.
ifndef STAB
  STAB = development
endif
ifneq ($(STAB), development)
  ifneq ($(STAB), release)
    $(error STAB must be 'development' (default) or 'release')
  endif
endif

ifeq ($(REV), sysv)
  BASEDIR         ?= $(HTML_ROOT)/lfs-qol
  PDF_OUTPUT      ?= lfs-qol.pdf
  NOCHUNKS_OUTPUT ?= lfs-qol.html
  DUMPDIR         ?= $(DUMP_ROOT)/lfs-qol-commands
  LFS_QOLHTML     ?= lfs-qol-html.xml
  LFS_QOLHTML2    ?= lfs-qol-html2.xml
  LFS_QOLFULL     ?= lfs-qol-full.xml
else
  BASEDIR         ?= $(HTML_ROOT)/lfs-qol-systemd
  PDF_OUTPUT      ?= lfs-qol-sysd.pdf
  NOCHUNKS_OUTPUT ?= lfs-qol-sysd.html
  DUMPDIR         ?= $(DUMP_ROOT)/lfs-qol-sysd-commands
  LFS_QOLHTML     ?= lfs-qol-systemd-html.xml
  LFS_QOLHTML2    ?= lfs-qol-systemd-html2.xml
  LFS_QOLFULL     ?= lfs-qol-systemd-full.xml
endif

lfs-qol: html wget-list

help:
	@echo ""
	@echo "make <parameters> <targets>"
	@echo ""
	@echo "Parameters:"
	@echo ""
	@echo "  REV=<rev>            Build variation of book"
	@echo "                       Valid values for REV are:"
	@echo "                       * sysv    - Build book for SysV"
	@echo "                       * systemd - Build book for systemd"
	@echo "                       Defaults to 'sysv'"
	@echo ""
	@echo "  BASEDIR=<dir>        Put the output in directory <dir>."
	@echo "                       Defaults to"
	@echo "                       '$(HTML_ROOT)/lfs-qol' if REV=sysv (or unset)"
	@echo "                       or to"
	@echo "                       '$(HTML_ROOT)/lfs-qol-systemd' if REV=systemd"
	@echo ""
	@echo "  V=<val>              If <val> is a non-empty value, all"
	@echo "                       steps to produce the output is shown."
	@echo "                       Default is unset."
	@echo ""
	@echo "  LFS_QOL_THEME=<theme> Sets the theme of the book, ie. light/dark."
	@echo "                        The dark theme is the default."
	@echo ""
	@echo "Targets:"
	@echo "  help                 Show this help text."
	@echo ""
	@echo "  lfs-qol              Builds targets 'html' and 'wget-list'."
	@echo ""
	@echo "  html                 Builds the HTML pages of the book."
	@echo ""
	@echo "  pdf                  Builds the book as a PDF file."
	@echo ""
	@echo "  wget-list            Produces a list of all packages to download."
	@echo "                       Output is BASEDIR/wget-list"
	@echo ""
	@echo "  nochunks             Builds the book as a one-pager. The output"
	@echo "                       is a large single HTML page containing the"
	@echo "                       whole book."
	@echo ""
	@echo "                       Parameter NOCHUNKS_OUTPUT=<filename> controls"
	@echo "                       the name of the HTML file."
	@echo ""
	@echo "  validate             Runs validation checks on the XML files."
	@echo ""
	@echo "  test-links           Runs validation checks on URLs in the book."
	@echo "                       Produces a file named BASEDIR/bad_urls containing"
	@echo "                       URLS which are invalid and a BASEDIR/good_urls"
	@echo "                       containing all valid URLs."
	@echo ""

all: lfs-qol nochunks
world: all dump-commands test-links

html: $(BASEDIR)/index.html
$(BASEDIR)/index.html: $(RENDERTMP)/$(LFS_QOLHTML) version wget-list
	@echo "Generating chunked XHTML files..."
	$(Q)xsltproc --nonet                                    \
                --stringparam chunk.quietly $(CHUNK_QUIET) \
                --stringparam rootid "$(ROOT_ID)"          \
                --stringparam base.dir $(BASEDIR)/         \
                stylesheets/lfs-qol-chunked.xsl            \
                $(RENDERTMP)/$(LFS_QOLHTML)

	@echo "Copying CSS code, images, and patches..."
	$(Q)if [ ! -e $(BASEDIR)/stylesheets ]; then \
      mkdir -p $(BASEDIR)/stylesheets;          \
   fi;

	$(Q)cp stylesheets/lfs-xsl/$(LFS_QOL_THEME).lfs.css $(BASEDIR)/stylesheets/lfs.css
	$(Q)sed -i 's|../stylesheet|stylesheet|' $(BASEDIR)/index.html

	$(Q)if [ ! -e $(BASEDIR)/images ]; then \
      mkdir -p $(BASEDIR)/images;          \
   fi;
	$(Q)cp images/*.png $(BASEDIR)/images

	$(Q)cd $(BASEDIR)/; sed -e "s@../images@images@g"           \
                           -i *.html

	$(Q)if [ ! -e $(BASEDIR)/patches ]; then \
		mkdir -p $(BASEDIR)/patches;          \
   fi;
	$(Q)cp -r patches/* $(BASEDIR)/patches

	@echo "Running Tidy and obfuscate.sh on chunked XHTML..."
	$(Q)for filename in `find $(BASEDIR) -name "*.html"`; do       \
      tidy -config tidy.conf $$filename;                          \
      true;                                                       \
      bash obfuscate.sh $$filename;                               \
      sed -i -e "1,20s@text/html@application/xhtml+xml@g" $$filename; \
   done;

	$(Q)rm -rf $(RENDERTMP)

pdf: validate wget-list
	@echo "Generating profiled XML for PDF..."
	$(Q)xsltproc --nonet \
						--stringparam profile.condition pdf   \
						--output $(RENDERTMP)/lfs-qol-pdf.xml \
						stylesheets/lfs-xsl/profile.xsl       \
						$(RENDERTMP)/$(LFS_QOLFULL)

	@echo "Generating FO file..."
	$(Q)xsltproc --nonet										 \
					--stringparam rootid "$(ROOT_ID)"	 \
					--output $(RENDERTMP)/lfs-qol-pdf.fo \
					stylesheets/lfs-qol-pdf.xsl          \
					$(RENDERTMP)/lfs-qol-pdf.xml

	$(Q)sed -i -e 's/span="inherit"/span="all"/' $(RENDERTMP)/lfs-qol-pdf.fo
	$(Q)bash pdf-fixups.sh $(RENDERTMP)/lfs-qol-pdf.fo

	@echo "Generating PDF file..."
	$(Q)mkdir -p $(RENDERTMP)/images
	$(Q)cp images/*.png $(RENDERTMP)/images

	$(Q)mkdir -p $(BASEDIR)

	$(Q)fop -q $(RENDERTMP)/lfs-qol-pdf.fo $(BASEDIR)/$(PDF_OUTPUT) 2>fop.log
	@echo "$(BASEDIR)/$(PDF_OUTPUT) created"
	@echo "fop.log created"
	$(Q)rm fop.log
	@echo "fop.log destroyed"

	$(Q)rm -rf $(RENDERTMP)

nochunks: $(BASEDIR)/$(NOCHUNKS_OUTPUT)
$(BASEDIR)/$(NOCHUNKS_OUTPUT): $(RENDERTMP)/$(LFS_QOLHTML) version
	@echo "Generating non-chunked XHTML file..."
	$(Q)xsltproc --nonet                                \
                --stringparam rootid "$(ROOT_ID)"      \
                --output $(BASEDIR)/$(NOCHUNKS_OUTPUT) \
                stylesheets/lfs-qol-nochunks.xsl       \
                $(RENDERTMP)/$(LFS_QOLHTML)

	@echo "Running Tidy and obfuscate.sh on non-chunked XHTML..."
	$(Q)tidy -config tidy.conf $(BASEDIR)/$(NOCHUNKS_OUTPUT) || true
	$(Q)bash obfuscate.sh $(BASEDIR)/$(NOCHUNKS_OUTPUT)
	$(Q)sed -i -e "1,20s@text/html@application/xhtml+xml@g" $(BASEDIR)/$(NOCHUNKS_OUTPUT)

validate: $(RENDERTMP)/$(LFS_QOLFULL)
$(RENDERTMP)/$(LFS_QOLFULL): general.ent packages.ent $(ALLXML) $(ALLXSL) version
	$(Q)[ -d $(RENDERTMP) ] || mkdir -p $(RENDERTMP)

	@echo "Rendering the book for $(REV)..."
	$(Q)xsltproc --nonet                               \
                --xinclude                            \
                --output $(RENDERTMP)/$(LFS_QOLHTML2) \
                --stringparam profile.revision $(REV) \
                stylesheets/lfs-xsl/profile.xsl       \
                index.xml

	@echo "Validating the book..."
	$(Q)xmllint --nonet                             \
               --noent                             \
               --postvalid                         \
               --output $(RENDERTMP)/$(LFS_QOLFULL)   \
               $(RENDERTMP)/$(LFS_QOLHTML2)

profile-html: $(RENDERTMP)/$(LFS_QOLHTML)
$(RENDERTMP)/$(LFS_QOLHTML): $(RENDERTMP)/$(LFS_QOLFULL) version
	@echo "Generating profiled XML for XHTML..."
	$(Q)xsltproc --nonet                              \
                --stringparam profile.condition html \
                --output $(RENDERTMP)/$(LFS_QOLHTML)    \
                stylesheets/lfs-xsl/profile.xsl      \
                $(RENDERTMP)/$(LFS_QOLFULL)

wget-list: $(BASEDIR)/wget-list
$(BASEDIR)/wget-list: $(RENDERTMP)/$(LFS_QOLFULL) version
	@echo "Generating wget list for $(REV) at $(BASEDIR)/wget-list ..."
	$(Q)mkdir -p $(BASEDIR)
	$(Q)xsltproc --nonet                       \
                --output $(BASEDIR)/wget-list \
                stylesheets/wget-list.xsl     \
                $(RENDERTMP)/$(LFS_QOLFULL)

test-links: $(BASEDIR)/test-links
$(BASEDIR)/test-links: $(RENDERTMP)/$(LFS_QOLFULL) version
	@echo "Generating test-links file..."
	$(Q)mkdir -p $(BASEDIR)
	$(Q)xsltproc --nonet                        \
                --stringparam list_mode full   \
                --output $(BASEDIR)/test-links \
                stylesheets/wget-list.xsl      \
                $(RENDERTMP)/$(LFS_QOLFULL)

	@echo "Checking URLs, first pass..."
	$(Q)rm -f $(BASEDIR)/{good,bad,true_bad}_urls
	$(Q)for URL in `cat $(BASEDIR)/test-links`; do                     \
         wget --spider --tries=2 --timeout=60 $$URL >>/dev/null 2>&1; \
         if test $$? -ne 0 ; then                                     \
            echo $$URL >> $(BASEDIR)/bad_urls ;                       \
         else                                                         \
            echo $$URL >> $(BASEDIR)/good_urls 2>&1;                  \
         fi;                                                          \
   done

	@echo "Checking URLs, second pass..."
	$(Q)for URL2 in `cat $(BASEDIR)/bad_urls`; do                       \
         wget --spider --tries=2 --timeout=60 $$URL2 >>/dev/null 2>&1; \
         if test $$? -ne 0 ; then                                      \
           echo $$URL2 >> $(BASEDIR)/true_bad_urls ;                   \
         else                                                          \
           echo $$URL2 >> $(BASEDIR)/good_urls 2>&1;                   \
         fi; \
   done

bootscripts:
	@VERSION=`grep "bootscripts-version " general.ent | cut -d\" -f2`; \
   BOOTSCRIPTS="lfs-qol-bootscripts-$$VERSION";                       \
   if [ ! -e $$BOOTSCRIPTS.tar.xz ]; then                             \
     rm -rf $(RENDERTMP)/$$BOOTSCRIPTS;                               \
     mkdir $(RENDERTMP)/$$BOOTSCRIPTS;                                \
     cp -a ../bootscripts/* $(RENDERTMP)/$$BOOTSCRIPTS;               \
     rm -rf ../bootscripts/archive;                                   \
     tar  -cJhf $$BOOTSCRIPTS.tar.xz -C $(RENDERTMP) $$BOOTSCRIPTS;   \
   fi

systemd-units:
		@VERSION=`grep "systemd-units-version " general.ent | cut -d\" -f2`; \
	UNITS="lfs-qol-systemd-units-$$VERSION";                                \
	if [ ! -e $$UNITS.tar.xz ]; then                                     \
		rm -rf $(RENDERTMP)/$$UNITS;                                       \
		mkdir $(RENDERTMP)/$$UNITS;                                        \
		cp -a ../systemd-units/* $(RENDERTMP)/$$UNITS;                     \
		tar -cJhf $$UNITS.tar.xz -C $(RENDERTMP) $$UNITS;                  \
	fi

test-options:
	$(Q)xsltproc --xinclude --nonet stylesheets/test-options.xsl index.xml

dump-commands: $(DUMPDIR)
$(DUMPDIR): $(RENDERTMP)/$(LFS_QOLFULL) version
	@echo "Dumping book commands at $(DUMPDIR)..."
	$(Q)xsltproc --output $(DUMPDIR)/          \
                stylesheets/dump-commands.xsl \
                $(RENDERTMP)/$(LFS_QOLFULL)
	$(Q)touch $(DUMPDIR)
	$(Q)rm -rf $(RENDERTMP)

.PHONY: lfs-qol all world html nochunks pdf clean validate profile-html \
   wget-list test-links dump-commands bootscripts systemd-units version \
   test-options

version:
	$(Q)REV=$(REV) STAB=$(STAB) ./git-version.sh
