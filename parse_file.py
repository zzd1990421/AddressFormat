# -*- coding: UTF-8 -*-
# location_str = ["徐汇区虹漕路461号58号楼5楼", "泉州市洛江区万安塘西工业区", "朝阳区北苑华贸城"]
import cpca
import sys
import json
import time

result_file = open("result.txt","w",encoding='utf-8')

print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

if len(sys.argv)<2:
	print("error")
else:
	fileName = sys.argv[1]
	with open(fileName, 'r',encoding='gbk') as f:
	    print("Load str file from {}".format(fileName))
	    str1 = f.read()
	    r = json.loads(str1)
	    for x in r:
	    	if x is not None:
	    		result_file.write(x)
		    	result_file.write("\n")

		    	res = cpca.parseAddr(x)
		    	result_file.write(json.dumps(res,ensure_ascii=False))
		    	result_file.write("\n\n")
		    	
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))