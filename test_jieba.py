# -*- coding: UTF-8 -*-
import jieba

jieba.load_userdict("dict/address_dict.txt")
seg_list = jieba.cut("东吴北路35号", cut_all=False)
for x in seg_list:
	print(x)