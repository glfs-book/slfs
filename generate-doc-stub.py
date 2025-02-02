#!/usr/bin/python3

import os
import sys

if len(sys.argv) != 3:
	print("Usage: generate-doc-stub.py folder pkgname")
	sys.exit(1)

if not os.path.isdir(sys.argv[1]):
	print("Error: nonexistent folder")
	sys.exit(1)

filelist = onlyfiles = [f for f in os.listdir(sys.argv[1]) \
			if os.path.isfile(os.path.join(sys.argv[1], f))]
filelist = sorted(filelist)

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
print(tmp + tmp2, end='')
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
          <indexterm zone="{sys.argv[2]} {i}">
            <primary sortas="b-{i}">{i}</primary>
          </indexterm>
        </listitem>
      </varlistentry>
''', end='')
print('''
    </variablelist>

  </sect2>
''')
