# vim:ts=3
# Makefile for SLFS Book generation.
# By Tushar Teredesai <tushar@linuxfromscratch.org>
# Edited by Zeckma <zeckma.tech@gmail.com>
# 2004-01-31

# When rendering for the stable release from the stable branch, invoke
# STAB=release to make.
-include local.mk

# Adjust these to suit your installation, or include the variables
# you wish to change in local.mk, which must be created manually.
AUTO_CLEAN  ?= 1
THEME       ?= dark
THEME_PATH  ?= stylesheets/lfs-xsl
RENDERTMP   := $(shell mktemp -d)
HTML_ROOT   ?= $(HOME)/public_html
DUMP_ROOT   ?= $(HOME)
CHUNK_QUIET ?= 1
SHELL        = /bin/bash

ALLXML := $(shell find . -mindepth 1 -name '*.xml' ! -path '$(RENDERTMP)/*')
ALLXSL := $(shell find . -mindepth 1 -name '*.xsl' ! -path '$(RENDERTMP)/*')

ifdef V
  Q =
else
  Q = @
endif

CLEAN = rm -rf $(RENDERTMP)
ifeq ($(AUTO_CLEAN), 0)
  CLEAN =
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
  BASEDIR         ?= $(HTML_ROOT)/slfs
  DUMPDIR         ?= $(DUMP_ROOT)/slfs-commands
  SLFSHTML        ?= slfs-html.xml
  SLFSHTML2       ?= slfs-html2.xml
  SLFSFULL        ?= slfs-full.xml
else
  BASEDIR         ?= $(HTML_ROOT)/slfs-systemd
  DUMPDIR         ?= $(DUMP_ROOT)/slfs-sysd-commands
  SLFSHTML        ?= slfs-systemd-html.xml
  SLFSHTML2       ?= slfs-systemd-html2.xml
  SLFSFULL        ?= slfs-systemd-full.xml
endif

slfs: html wget-list

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
	@echo "                       '$(HTML_ROOT)/slfs' if REV=sysv (or unset)"
	@echo "                       or to"
	@echo "                       '$(HTML_ROOT)/slfs-systemd' if REV=systemd"
	@echo ""
	@echo "  V=<val>              If <val> is a non-empty value, all"
	@echo "                       steps to produce the output is shown."
	@echo "                       Default is unset."
	@echo ""
	@echo "  THEME_PATH=<path>    Sets the path of themes (CSS files)."
	@echo "                       'stylesheets/lfs-xsl' is the default."
	@echo ""
	@echo "  THEME=<theme>        Sets the theme of the book, ie. light/dark."
	@echo "                       The dark theme is the default."
	@echo ""
	@echo "Targets:"
	@echo "  help                 Show this help text."
	@echo ""
	@echo "  slfs                 Builds targets 'html' and 'wget-list'."
	@echo ""
	@echo "  html                 Builds the HTML pages of the book."
	@echo ""
	@echo "  wget-list            Produces a list of all packages to download."
	@echo "                       Output is BASEDIR/wget-list"
	@echo ""
	@echo "  validate             Runs validation checks on the XML files."
	@echo ""
	@echo "  test-links           Runs validation checks on URLs in the book."
	@echo "                       Produces a file named BASEDIR/bad_urls containing"
	@echo "                       URLS which are invalid and a BASEDIR/good_urls"
	@echo "                       containing all valid URLs."
	@echo ""

all: slfs
world: all dump-commands test-links

html: $(BASEDIR)/index.html
$(BASEDIR)/index.html: $(RENDERTMP)/$(SLFSHTML) version wget-list
	@echo "Generating chunked XHTML files..."
	$(Q)xsltproc --nonet                                    \
                --stringparam chunk.quietly $(CHUNK_QUIET) \
                --stringparam base.dir $(BASEDIR)/         \
                stylesheets/slfs-chunked.xsl            \
                $(RENDERTMP)/$(SLFSHTML)

	@echo "Copying CSS code, images, and patches..."
	$(Q)if [ ! -e $(BASEDIR)/stylesheets ]; then \
      mkdir -p $(BASEDIR)/stylesheets;          \
   fi;

	$(Q)cp $(THEME_PATH)/$(THEME).lfs.css $(BASEDIR)/stylesheets/lfs.css
	$(Q)cp stylesheets/lfs-xsl/lfs-print.css $(BASEDIR)/stylesheets
	$(Q)sed -i 's|../stylesheet|stylesheet|' $(BASEDIR)/index.html

	$(Q)if [ ! -e $(BASEDIR)/images ]; then \
      mkdir -p $(BASEDIR)/images;          \
   fi;
	$(Q)cp images/*.{ico,png} $(BASEDIR)/images

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

	$(Q)$(CLEAN)

validate: $(RENDERTMP)/$(SLFSFULL)
$(RENDERTMP)/$(SLFSFULL): general.ent packages.ent $(ALLXML) $(ALLXSL) version
	$(Q)[ -d $(RENDERTMP) ] || mkdir -p $(RENDERTMP)
	$(Q)trap '$(CLEAN)' EXIT

	@echo "Rendering the book for $(REV)..."
	$(Q)xsltproc --nonet                               \
                --xinclude                            \
                --output $(RENDERTMP)/$(SLFSHTML2) \
                --stringparam profile.revision $(REV) \
                stylesheets/lfs-xsl/profile.xsl       \
                index.xml

	@echo "Validating the book..."
	$(Q)xmllint --nonet                             \
               --noent                             \
               --postvalid                         \
               --output $(RENDERTMP)/$(SLFSFULL)   \
               $(RENDERTMP)/$(SLFSHTML2)

profile-html: $(RENDERTMP)/$(SLFSHTML)
$(RENDERTMP)/$(SLFSHTML): $(RENDERTMP)/$(SLFSFULL) version
	@echo "Generating profiled XML for XHTML..."
	$(Q)xsltproc --nonet                              \
                --stringparam profile.condition html \
                --output $(RENDERTMP)/$(SLFSHTML)    \
                stylesheets/lfs-xsl/profile.xsl      \
                $(RENDERTMP)/$(SLFSFULL)

wget-list: $(BASEDIR)/wget-list
$(BASEDIR)/wget-list: $(RENDERTMP)/$(SLFSFULL) version
	@echo "Generating wget list for $(REV) at $(BASEDIR)/wget-list ..."
	$(Q)mkdir -p $(BASEDIR)
	$(Q)xsltproc --nonet                       \
                --output $(BASEDIR)/wget-list \
                stylesheets/wget-list.xsl     \
                $(RENDERTMP)/$(SLFSFULL)

test-links: $(BASEDIR)/test-links
$(BASEDIR)/test-links: $(RENDERTMP)/$(SLFSFULL) version
	@echo "Generating test-links file..."
	$(Q)mkdir -p $(BASEDIR)
	$(Q)xsltproc --nonet                        \
                --stringparam list_mode full   \
                --output $(BASEDIR)/test-links \
                stylesheets/wget-list.xsl      \
                $(RENDERTMP)/$(SLFSFULL)

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

	$(Q)$(CLEAN)

bootscripts:
	$(Q)trap '$(CLEAN)' EXIT
	@VERSION=`grep "bootscripts-version " general.ent | cut -d\" -f2`; \
   BOOTSCRIPTS="slfs-bootscripts-$$VERSION";                       \
   if [ ! -e $$BOOTSCRIPTS.tar.xz ]; then                             \
     rm -rf $(RENDERTMP)/$$BOOTSCRIPTS;                               \
     mkdir $(RENDERTMP)/$$BOOTSCRIPTS;                                \
     cp -a ../bootscripts/* $(RENDERTMP)/$$BOOTSCRIPTS;               \
     rm -rf ../bootscripts/archive;                                   \
     tar  -cJhf $$BOOTSCRIPTS.tar.xz -C $(RENDERTMP) $$BOOTSCRIPTS;   \
   fi

	$(Q)$(CLEAN)

systemd-units:
	$(Q)trap '$(CLEAN)' EXIT
		@VERSION=`grep "systemd-units-version " general.ent | cut -d\" -f2`; \
	UNITS="slfs-systemd-units-$$VERSION";                                \
	if [ ! -e $$UNITS.tar.xz ]; then                                     \
		rm -rf $(RENDERTMP)/$$UNITS;                                       \
		mkdir $(RENDERTMP)/$$UNITS;                                        \
		cp -a ../systemd-units/* $(RENDERTMP)/$$UNITS;                     \
		tar -cJhf $$UNITS.tar.xz -C $(RENDERTMP) $$UNITS;                  \
	fi

	$(Q)$(CLEAN)

test-options:
	$(Q)trap '$(CLEAN)' EXIT
	$(Q)xsltproc --xinclude --nonet stylesheets/test-options.xsl index.xml
	$(Q)$(CLEAN)

dump-commands: $(DUMPDIR)
$(DUMPDIR): $(RENDERTMP)/$(SLFSFULL) version
	@echo "Dumping book commands at $(DUMPDIR)..."
	$(Q)xsltproc --output $(DUMPDIR)/          \
                stylesheets/dump-commands.xsl \
                $(RENDERTMP)/$(SLFSFULL)
	$(Q)touch $(DUMPDIR)
	$(Q)$(CLEAN)

.PHONY: slfs all world html validate profile-html wget-list \
  test-links dump-commands bootscripts systemd-units version test-options

version:
	$(Q)REV=$(REV) STAB=$(STAB) ./git-version.sh
