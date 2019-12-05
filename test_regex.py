# -*- coding: UTF-8 -*-

import re
from cpca import *

pattern = re.compile(r"[村浜区片][第]*(\w+组)(\d+号)$")

zu,zu_num = GetZuAndNum("刘村村泾西第九组65号")
print(zu)
print(zu_num)
