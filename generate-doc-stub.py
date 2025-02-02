#!/usr/bin/python3

# Quick doc stub generator script.
# Warning: doesn't do *all* the work for you.
# Review output manually after the script finishes.
# (C) Seal Sealy, 2025

import os
import sys

if len(sys.argv) < 3:
	print("Usage: generate-doc-stub.py pkgname folder1 <folder2> <folder3>")
	sys.exit(1)

if not os.path.isdir(sys.argv[2]):
	print("Error: nonexistent folder1")
	sys.exit(1)

filelist1 =  [f for f in os.listdir(sys.argv[2]) \
			if os.path.isfile(os.path.join(sys.argv[2], f))]
if len(sys.argv) > 3:
	filelist2 = [f for f in os.listdir(sys.argv[3]) \
                        if os.path.isfile(os.path.join(sys.argv[3], f))]
else:
	filelist2 = []

if len(sys.argv) > 4:
	filelist3 = [f for f in os.listdir(sys.argv[4]) \
                        if os.path.isfile(os.path.join(sys.argv[4], f))]
else:
	filelist3 = []

filelist = sorted(list(set(filelist1 + filelist2 + filelist3)))

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
	tmp2 = tmp + i + ', '
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

for i in filelist:
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
print('''
    </variablelist>

  </sect2>
''')
