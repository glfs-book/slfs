#!/usr/bin/python3

# Quick doc stub generator script.
# Warning: doesn't do *all* the work for you.
# Review output manually after the script finishes.
# (C) Seal Sealy, 2025

import os
import sys
import itertools

if len(sys.argv) < 3:
	print("Usage: generate-doc-stub.py pkgname folder1 <folder2> <folder3>")
	sys.exit(1)

if not os.path.isdir(sys.argv[2]):
	print("Error: nonexistent folder1")
	sys.exit(1)

# sublist structure
# [<symlink name>, 's', <symlink target>]
# OR
# [<file name>, 'f', 'FILLER']

filelist1 = []
for f in os.listdir(sys.argv[2]):
	if os.path.islink(os.path.join(sys.argv[2], f)):
		if os.path.isfile(os.path.normpath(os.path.join(os.path.dirname(os.path.join(sys.argv[2], \
				f)), os.readlink(os.path.join(sys.argv[2], f))))):
			filelist1.append([f, 's', os.path.basename(os.readlink(os.path.join(sys.argv[2], f)))])
	elif os.path.isfile(os.path.join(sys.argv[2], f)):
		filelist1.append([f, 'f', 'FILLER'])

if len(sys.argv) > 3:
	filelist2 = []
	for f in os.listdir(sys.argv[3]):
        	if os.path.islink(os.path.join(sys.argv[3], f)):
                	if os.path.isfile(os.path.normpath(os.path.join(os.path.dirname(os.path.join(sys.argv[3], \
                        	        f)), os.readlink(os.path.join(sys.argv[3], f))))):
                        	filelist2.append([f, 's', os.path.basename(os.readlink(os.path.join(sys.argv[3], f)))])
        	elif os.path.isfile(os.path.join(sys.argv[3], f)):
                	filelist2.append([f, 'f', 'FILLER'])
else:
	filelist2 = []

if len(sys.argv) > 4:
	filelist3 = []
	for f in os.listdir(sys.argv[4]):
		if os.path.islink(os.path.join(sys.argv[4], f)):
			if os.path.isfile(os.path.normpath(os.path.join(os.path.dirname(os.path.join(sys.argv[4], \
					f)), os.readlink(os.path.join(sys.argv[4], f))))):
				filelist3.append([f, 's', os.path.basename(os.readlink(os.path.join(sys.argv[4], f)))])
		elif os.path.isfile(os.path.join(sys.argv[4], f)):
			filelist3.append([f, 'f', 'FILLER'])
else:
	filelist3 = []

filelist = filelist1 + filelist2 + filelist3

filelist.sort()
filelist = list(filelist for filelist,_ in itertools.groupby(filelist))
filelist = sorted(filelist, key=lambda e: e[0])

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
		tmp = '          '
		tmp2 = tmp2[80:]
print(tmp2, end='')
print('''
        </seg>
        <seg>
          TODO
        </seg>
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
print('''
    </variablelist>

  </sect2>
''')
