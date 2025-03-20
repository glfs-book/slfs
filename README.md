# Linux From Scratch - Quality of Life (LFS-QOL)

This book is dedicated to documenting the installation of some packages on an
LFS system that do not appear in LFS, MLFS, BLFS, and GLFS.

This book boasts several libraries and utilities not covered in the `*LFS`
books. On top of that, it also provides: SVR4-related tooling, binary-only
application support, many graphical environments for both Wayland and X.org,
both computer and video game console emulators, general gaming software, and
more.

# Where to read

Go to https://glfs-book.github.io/lfs-qol/ and start going through the book!

The book online is rolling release but there is a stable version in the LFS QOL
source via the stable branch.

You can switch to it by running the following command:

```Bash
git checkout stable
```

Then render the book with `make STAB=release [other options]`.

There are also [Releases](https://github.com/glfs-book/lfs-qol/releases) that
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

The default target (sysv) builds the HTML in `~/public_html/lfs-qol`,
whereas for systemd, it would be in `~/public_html/lfs-qol-systemd`.
It will by default make each package and section its own page then link
everything together for a smooth experience.

You can set a path to LFS QOL themes by running
`make LFS_QOL_THEME_PATH=<path>`. The default is `stylesheets/lfs-xsl`.

The dark theme is also the default, but you can switch the theme by
running `make LFS_QOL_THEME=<theme>`. `<theme>` can equal:
- `light`
- `dark`

Note that if you set `LFS_QOL_THEME_PATH`, you can set `LFS_QOL_THEME` to more
than just what the available options are shown above, but only the available
themes that are in that path.
