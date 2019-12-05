# -*- coding: UTF-8 -*-

import re

pattern = re.compile(r"^(\w+[(大道)路])(\d+)号")

m = pattern.match('港城大道108号xx')
if m:
	print(m.group(1),m.group(2))

m = pattern.match('港城大路108号xx')
if m:
	print(m.group(1),m.group(2))
