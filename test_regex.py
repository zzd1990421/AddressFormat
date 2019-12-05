# -*- coding: UTF-8 -*-

import re

pattern = re.compile(r"[村浜](\d+组)(\d+号)$")

m = pattern.search('长瑞村戴浜5组11号')
if m:
	print(m.group(1),m.group(2))
else:
	print("not match")
