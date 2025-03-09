#!/usr/bin/python3

# Quick doc stub generator script.
# Warning: doesn't do *all* the work for you.
# Review output manually after the script finishes.
# (C) Seal Sealy, 2025

import os
import sys
import itertools

libdocflag = False
def checklib(i, f):
	return not (libdocflag and (".a" in os.path.basename(os.path.join(i, 
		f)) or ".so" in os.path.basename(os.path.join(i, f))))

if len(sys.argv) < 3:
	print("Usage: generate-doc-stub.py pkgname folder1 <folder2> <folder3> ...")
	print("Set the DOCSTUBGEN_DOCUMENT_LIBRARIES environment variable to also \
automatically generate doc stubs for libraries. Warning: automatically documenting \
libraries is EXPERIMENTAL AND PRONE TO FALSE POSITIVES.")
	sys.exit(1)

if not os.path.isdir(sys.argv[2]):
	print("Error: nonexistent folder1")
	sys.exit(1)

if os.getenv('DOCSTUBGEN_DOCUMENT_LIBRARIES'):
	libdocflag = True

# sublist structure
# [<symlink name>, 's', <symlink target>]
# OR
# [<file name>, 'f', 'FILLER']

filelist = [['calprog', 'f'], ['diff3prog', 'f'], ['diffh', 'f']]
for d in range(len(sys.argv)):
	if d == 0 or d == 1:
		continue
	i = sys.argv[d]
	if not os.path.isdir(i):
		print(f"Error: nonexistent folder {i}")
		sys.exit(1)
	for f in os.listdir(i):
		if os.path.islink(os.path.join(i, f)):
			if os.path.isfile(os.path.normpath(os.path.join(os.path.dirname(os.path.join(i, \
					f)), os.readlink(os.path.join(i, f))))):
				if libdocflag:
					if checklib(i, f):
						filelist.append([f, 's', os.path.basename(os.readlink( \
							os.path.join(i, f)))])
				else:
					filelist.append([f, 's', os.path.basename(os.readlink(os.path.join(i, \
							f)))])
		elif os.path.isfile(os.path.join(i, f)):
			if libdocflag:
				if checklib(i, f):
					filelist.append([f, 'f', 'FILLER'])
			else:
				filelist.append([f, 'f', 'FILLER'])

filelist.sort()
filelist = list(filelist for filelist,_ in itertools.groupby(filelist))
filelist = sorted(filelist, key=lambda e: e[0])

if libdocflag:
	liblist = []
	for d in range(len(sys.argv)):
		if d == 0 or d == 1:
			continue
		i = sys.argv[d]
		if not os.path.isdir(i):
			print(f"Error: nonexistent folder {i}")
			sys.exit(1)
		for f in os.listdir(i):
			if os.path.islink(os.path.join(i, f)):
				if os.path.isfile(os.path.normpath(os.path.join(os.path.dirname(os.path.join(i, \
						f)), os.readlink(os.path.join(i, f))))):
					continue
			elif os.path.isfile(os.path.join(i, f)) and '.a' in os.path.basename(os.path.join(i, f)):
				liblist.append([f, 'f', 'FILLER'])
			elif os.path.isfile(os.path.join(i, f)) and '.so' in os.path.basename(os.path.join(i, f)):
				tmplst = f.split('.')
				tmp = tmplst[0]
				for h in tmplst[1:]:
					# isdigit only works for positive integers and doesn't work with floats
					# but it should do, shared object naming doesn't involve floats or
					# negative integers
					if not h.isdigit():
						tmp = tmp + '.' + h
				liblist.append([tmp, 'f', 'FILLER'])

	liblist.sort()
	liblist = list(liblist for liblist,_ in itertools.groupby(liblist))
	liblist = sorted(liblist, key=lambda e: e[0])

print('''  <sect2 role="content">
    <title>Contents</title>

    <segmentedlist>
      <segtitle>Installed Programs</segtitle>
      <segtitle>Installed Libraries</segtitle>
      <segtitle>Installed Directories</segtitle>

      <seglistitem>
        <seg>''')
tmp = '          '
for i in filelist:
	if i[1] == 'f':
		tmp2 = tmp + i[0] + ', '
	elif i[1] == 's':
		tmp2 = tmp + i[0] + f' (link to {i[2]})' + ', ' 
	#print(tmp2)
	if len(tmp2) <= 80:
		tmp = tmp2
	else:
		print(tmp)
		tmp3 = tmp2.split(', ')
		tmp = '          ' + tmp3[-2] + ', '
		tmp2 = ', '.join(tmp3[:-2])
print(tmp2, end='')
print('''
        </seg>
        <seg>''')
if not libdocflag:
	print('          TODO')
else:
	tmp = '          '
	for i in liblist:
		tmp2 = tmp + i[0] + ', '
		#print(tmp2)
		if len(tmp2) <= 80:
			tmp = tmp2
		else:
			print(tmp)
			tmp = '          '
			tmp2 = tmp2[80:]
	print(tmp2, end='')
	print()
print('''        </seg>
        <seg>
          TODO
        </seg>
      </seglistitem>
    </segmentedlist>

    <variablelist>
      <bridgehead renderas="sect3">Short Descriptions</bridgehead>
      <?dbfo list-presentation="list"?>
      <?dbhtml list-presentation="table"?>
''', end='')

for g in filelist:
	if g[1] == 'f':
		i = g[0]
		print(f'''
      <varlistentry id="{i}">
        <term><command>{i}</command></term>
        <listitem>
          <para>
            TODO
          </para>
          <indexterm zone="{sys.argv[1]} {i}">
            <primary sortas="b-{i}">{i}</primary>
          </indexterm>
        </listitem>
      </varlistentry>
''', end='')
	elif g[1] == 's':
		i = g[0]
		l = g[2]
		print(f'''
      <varlistentry id="{i}">
        <term><command>{i}</command></term>
        <listitem>
          <para>
            is a symlink pointing to <command>{l}</command>
          </para>
          <indexterm zone="{sys.argv[1]} {i}">
            <primary sortas="b-{i}">{i}</primary>
          </indexterm>
        </listitem>
      </varlistentry>
''', end='')

if libdocflag:
	for g in liblist:
		i = g[0]
		# yes this is a hack
		# but i can't figure out how rsplit works, I'm tired and it's 11:49PM
		if '.a' in i:
			f = i[:-2]
		elif '.so' in i:
			f = i[:-3]
		else:
			f = i
		print(f'''
      <varlistentry id="{f}">
        <term><filename class="libraryfile">{i}</filename></term>
        <listitem>
          <para>
            TODO
          </para>
          <indexterm zone="{sys.argv[1]} {f}">
            <primary sortas="c-{f}">{i}</primary>
          </indexterm>
        </listitem>
      </varlistentry>
''', end='')

print('''
    </variablelist>

  </sect2>
''')
