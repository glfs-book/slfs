<div align="center">
  <img src="https://github.com/glfs-book/slfs/blob/trunk/images/slfs-logo.svg?raw=true" width="25%">
  <h1>SLFS</h1>
</div>

<h2 align="center">
Supplemental Linux From Scratch
</h2>

This book supplements an LFS, MLFS, BLFS, and/or GLFS x86-64 system by providing
packages not found in the other LFS books.

SLFS boasts several libraries and utilities not covered in the other `*LFS`
books, including SVR4-related tooling, binary-only application support, many
graphical environments for both Wayland and X11, emulators, games and gaming
software, system utilities, and more.

## Where to read

Go to https://glfs-book.github.io/slfs/ and start going through the book!

The online book is rolling release but there is a stable version in the SLFS
source via the stable branch. You can switch to it by running the following
command:

```Bash
git checkout stable
```

Then render the book with `make STAB=release [other options]`.

There are also [releases](https://github.com/glfs-book/slfs/releases) available
for download. These contain both the SysV and Systemd editions of the book as
chunked HTML.

## Installation

How do I convert these XML files to HTML myself? You need to have some software
installed that deal with these conversions. Please read
[INSTALL.md](./INSTALL.md) to determine which programs you need to install and
where to get instructions to install that software.

You can then build the HTML with a simple `make` command. You can change the
revision by passing `REV=<rev>` to the `make` command. `<rev>` can be:
- `sysv` (default)
- `systemd`

Example: `make REV=systemd`

You can switch the theme by passing `THEME=<theme>` to the `make` command.
`<theme>` can equal:
- `dark` (default)
- `light`
- any theme in `THEME_PATH`

Example: `make THEME=dark`

You can set the theme path by passing `THEME_PATH=<path>` to the `make` command.
The default is `stylesheets/lfs-xsl`. More themes are available at
https://github.com/glfs-book/lfs-themes.

Example: `make THEME_PATH=../lfs-themes/themes THEME=whitepink`

The default target (sysv) builds the HTML in `~/public_html/slfs`,
whereas for systemd, it would be in `~/public_html/slfs-systemd`.
It will by default make each package and section its own page then link
everything together for a smooth experience.

There are also more variables that can be set which can be used to specify
where the rendered output goes, where temporary files are located, the
stability type of the render, and more.

An important thing to be aware of is by default, what is set as RENDERTMP
(`mktemp -d` by default) will be removed after every file has been
converted to a new format (HTML, wget-list, command scripts, etc.) by default.
If you need to keep the directory for whatever reason, pass `AUTO_CLEAN=0` when
running `make`.

Example: `make RENDERTMP=~/tmp AUTO_CLEAN=0`
