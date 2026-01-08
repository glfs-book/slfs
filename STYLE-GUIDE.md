# Style Guide

<!-- TODO: This is currently a stub and could use some work. -->

## 1. Text
This section sets some standards for writing text in SLFS.

### 1.1 Serial Commas
Use [serial commas](https://en.wikipedia.org/wiki/Serial_comma) (subject1,
subject2, and subject3) instead of (subject1, subject2 and subject3).

### 1.2 Indefinite Articles and Vowels
To decide whether to use 'a' or 'an', pronounce the word after the article. If
it starts with a vowel sound, use 'an'. Otherwise, use 'a'.

Consider the following sentence:
> This example is part of an SLFS style guide.

Since 'SLFS' starts with a vowel sound, specifically /ˈɛ/, the article 'an' is
preferred.

For an opposite example:
> The ICU package provides a universal set of Unicode libraries.

Since 'universal' starts with a consonant sound, specifically '/ˌj/', the
article 'a' is preferred.

## 2. Source Code
This section sets some standards for the SLFS source code.

### 2.1 Tabs
Use spaces instead of tabs in the XML files.

### 2.2 Text Wrapping
Keep character count on any given line to a maximum of 80 characters. This keep
the XML from getting ugly and unmaintainable.

There are situations where 80 characters isn't feasible, e.g. in links or code
blocks. In such situations, the limit is flexible. But if you can help it,
please keep under the 80 character limit.

## 3. Commands
This section standardizes the invocation of some common commands. This is done to
encourage consistency and correctness while also simplifying some actions.

### 3.1 Install
Some general rules and examples for using `install`:
- Where possible, prefer `install` to `cp`.
- Always pass `-v`.
- Omit spacing between flags unless necessary (e.g. installing a file with
  explicit ownership).
- Prefer explicitly setting the mode in octal permissions of the installed file
  using the `-m` flag. Generally, executable files want 755, and most other
  files want 644.
- To install a file to a directory without changing the filename, invoke
  `install -vDm755 myprogram -t /usr/bin/`. Always assume parent directories may
  not exist. Always include a trailing / to make more explicit the intent to
  install to a directory.
- To install multiple files to a directory without changing their filenames,
  invoke `install -vDm644 README LICENSE doc/*.{html,css,pdf} -t
  /usr/share/package-0.0.0/doc/`.
- To install a file to a directory and change the filename, invoke `install
  -vDm755 myprogram /usr/bin/program`.
- To install a directory, invoke `install -vdm755 /path/to/directory`.
- To install a file with explicit ownership, invoke `install -vDm644 -o someuser
  -g somegroup myfile -t /opt/package/`.
- To install an empty file, invoke `install -vDm644 /dev/null
  /usr/share/myemptyfile`.
- To install a file from a heredoc, invoke `install` like so:
```
install -vDm644 /dev/stdin /etc/package/config << EOF
# Begin configuration for package
some_option = true
# End configuration for package
EOF
```

<!-- TODO: -->
<!-- Other commands we may want to consider: -->
<!-- - `patch` -->
<!-- - `sed` -->
