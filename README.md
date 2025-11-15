# Supplemental Linux From Scratch (SLFS)

This book is dedicated to supplementing an LFS, MLFS, BLFS, and/or GLFS x86-64
system by providing packages not found in the other LFS books.

This book boasts several libraries and utilities not covered in the `*LFS`
books. On top of that, it also provides: SVR4-related tooling, binary-only
application support, many graphical environments for both Wayland and X.org,
both computer and video game console emulators, general gaming software, and
more.

# Where to read

Go to https://glfs-book.github.io/slfs/ and start going through the book!

The book online is rolling release but there is a stable version in the SLFS
source via the stable branch.

You can switch to it by running the following command:

```Bash
git checkout stable
```

Then render the book with `make STAB=release [other options]`.

There are also [Releases](https://github.com/glfs-book/slfs/releases) that
you can download. All of them contain both the SysV and Systemd editions of the
book, chunked HTML.

# Installation

How do I convert these XML files to HTML myself? You need to have some software
installed that deal with these conversions. Please read the `INSTALL.md` file to
determine what programs you need to install and where to get instructions to
install that software.

After that, you can build the HTML with a simple `make` command.
You can change the revision, ie. systemd vs sysv by adding `REV=<rev>` to the
`make` command. `<rev>` can be:
- `sysv` (default)
- `systemd`

Example: `make REV=systemd`.

The default target (sysv) builds the HTML in `~/public_html/slfs`,
whereas for systemd, it would be in `~/public_html/slfs-systemd`.
It will by default make each package and section its own page then link
everything together for a smooth experience.

You can set a path to the themes by running `make THEME_PATH=<path>`. The
default is `stylesheets/lfs-xsl`. You can find more at
https://github.com/glfs-book/lfs-themes.

The dark theme is also the default, but you can switch the theme by
running `make THEME=<theme>`. `<theme>` can equal:
- `light`
- `dark`

Note that if you set `THEME_PATH`, you can set `THEME` to more
than just what the available options are shown above, but only the available
themes that are in that path.
