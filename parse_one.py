# -*- coding: UTF-8 -*-
# location_str = ["徐汇区虹漕路461号58号楼5楼", "泉州市洛江区万安塘西工业区", "朝阳区北苑华贸城"]
import cpca
import sys

if len(sys.argv)<2:
	print("error")
else:
	print(cpca.parseAddr(sys.argv[1]))