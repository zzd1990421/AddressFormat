import re

road_num_pattern = re.compile(r"^(\w+[(大道)路])(\d+号)")
def GetRoadNumByRegex(addr):
	m = road_num_pattern.match(addr)
	if m:
		return m.group(1),m.group(2)
	return "",""