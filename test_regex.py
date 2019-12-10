# -*- coding: UTF-8 -*-

import re
from cpca import *

# pattern = re.compile(r"[村浜区片][第]*(\w+组)(\d+号)$")

addr = "刘村村泾西第9组65号"
zu,zu_num = GetZuAndNum(addr)
print("原始地址:",addr)
print("获取到组:",zu)
print("获取到组号:",zu_num)
