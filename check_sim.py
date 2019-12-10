# -*- coding: utf-8 -*-
import sys
import synonyms

if len(sys.argv)<3:
	print("error")
else:
	v1 = sys.argv[1]
	v2 = sys.argv[2]
	r = synonyms.compare(v1, v2, seg=True)
	print('词语1:',v1)
	print('词语2:',v2)
	print('相似度',r)