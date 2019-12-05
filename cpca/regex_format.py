import re
import cn2an

road_num_pattern = re.compile(r"^(\w+[(大道)路])(\d+号)")
zu_num_pattern = re.compile(r"(\d+组)(\d+号)$")

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
		return m.group(1),m.group(2)
	return "",""
