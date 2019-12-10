import re
import cn2an

road_num_pattern = re.compile(r"^(\w+[(大道)路])(\d+号)")
zu_num_pattern = re.compile(r"(\d+组)(\d+号)$")
unsure_zu_num_pattern = re.compile(r"[村浜区片桥]\w*[第]*(\w+组)(\d+号)$")
num_pattern = re.compile(r"\d+")

# 获取道路和道路号
def GetRoadNumByRegex(addr):
	m = road_num_pattern.match(addr)
	if m:
		return m.group(1),m.group(2)
	return "",""

# 获取组和组号
def GetZuAndNum(addr):
	m = zu_num_pattern.search(addr)
	if m:
		num = m.group(1)[:-1]
		value = cn2an.an2cn(num)
		return str(value)+"组",m.group(2)

	return getZuAndNumLast(addr)

def getZuAndNumLast(addr):
	ta = addr
	zu,zu_num = "",""
	for i in range(1,10):
		i = 0
		um = unsure_zu_num_pattern.search(ta)
		if um:
			zu = um.group(1)
			zu_num = um.group(2)
			ta = zu+zu_num
		else:
			break

	# if zu!="" and zu_num!="":
	# 	zu_str = zu[:len(zu)-1]
	# 	try:
	# 		value = cn2an.cn2an(zu_str, "strict")
	# 		value = str(value)
	# 		if num_pattern.match(value):
	# 			return value+"组",zu_num
	# 	except ValueError:
	# 		print(zu_str)
	# 		print("get zu zu_num wrong 1:"+addr)
	# 		return "",""
	# 	except TypeError:
	# 		print(zu_str)
	# 		print("get zu zu_num wrong 2:"+addr)
	# 		return "",""

	return "",""