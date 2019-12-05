# -*- coding: UTF-8 -*-

import os
import json

def walkFile(file):
  for root, dirs, files in os.walk(file):
    for f in files:
      readTownJson(os.path.join(root, f))

    for d in dirs:
      walkFile(d)

def readTownJson(file_addr):
  print("read:"+file_addr)
  with open(file_addr, 'r',encoding="UTF-8") as f:
    r = json.loads(f.read())
    for v in r.values():
      result_file.write(v)
      result_file.write("\n")

result_file = open("town_dict.txt","w")
walkFile("town")

