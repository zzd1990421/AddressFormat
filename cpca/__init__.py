# -*- coding: utf-8 -*-
# __init__.py


from .structures import AddrMap, Pca
from .structures import P,C,A
from .regex_format import *
import jieba
import json

jieba.load_userdict("dict/address_dict.txt")
jieba.load_userdict("dict/town_dict.txt")

VERSION = (0, 4, 4)

__version__ = ".".join([str(x) for x in VERSION])


def _data_from_csv() -> (AddrMap, AddrMap, AddrMap, dict, dict):
    # 区名及其简写 -> 相关pca元组
    area_map = AddrMap()
    # 城市名及其简写 -> 相关pca元组
    city_map = AddrMap()
    # (省名全称, 区名全称) -> 相关pca元组
    province_area_map = AddrMap()
    # 省名 -> 省全名
    province_map = {}
    # (省名, 市名, 区名) -> (纬度,经度)
    latlng = {}
    # 数据约定:国家直辖市的sheng字段为直辖市名称, 省直辖县的city字段为空
    from pkg_resources import resource_stream

    with resource_stream('cpca.resources', 'pca.csv') as pca_stream:
        from io import TextIOWrapper
        import csv
        text = TextIOWrapper(pca_stream, encoding='utf8')
        pca_csv = csv.DictReader(text)
        for record_dict in pca_csv:
            latlng[(record_dict['sheng'], record_dict['shi'], record_dict['qu'])] = \
                (record_dict['lat'], record_dict['lng'])

            _fill_province_map(province_map, record_dict)
            _fill_area_map(area_map, record_dict)
            _fill_city_map(city_map, record_dict)
            _fill_province_area_map(province_area_map, record_dict)

    return area_map, city_map, province_area_map, province_map, latlng


def _fill_province_area_map(province_area_map: AddrMap, record_dict):
    pca_tuple = (record_dict['sheng'], record_dict['shi'], record_dict['qu'])
    key = (record_dict['sheng'], record_dict['qu'])
    # 第三个参数在此处没有意义, 随便给的
    province_area_map.append_relational_addr(key, pca_tuple, P)


def _fill_area_map(area_map: AddrMap, record_dict):
    area_name = record_dict['qu']
    pca_tuple = (record_dict['sheng'], record_dict['shi'], record_dict['qu'])
    area_map.append_relational_addr(area_name, pca_tuple, A)
    if area_name.endswith('市'):
        area_map.append_relational_addr(area_name[:-1], pca_tuple, A)


def _fill_city_map(city_map: AddrMap, record_dict):
    city_name = record_dict['shi']
    pca_tuple = (record_dict['sheng'], record_dict['shi'], record_dict['qu'])
    city_map.append_relational_addr(city_name, pca_tuple, C)
    if city_name.endswith('市'):
        city_map.append_relational_addr(city_name[:-1], pca_tuple, C)
    # 特别行政区
    # elif city_name == '香港特别行政区':
    #     city_map.append_relational_addr('香港', pca_tuple, C)
    # elif city_name == '澳门特别行政区':
    #     city_map.append_relational_addr('澳门', pca_tuple, C)
    

def _fill_province_map(province_map, record_dict):
    sheng = record_dict['sheng']
    if sheng not in province_map:
        province_map[sheng] = sheng
        # 处理省的简写情况
        # 普通省分 和 直辖市
        if sheng.endswith('省') or sheng.endswith('市'):
            province_map[sheng[:-1]] = sheng
        # 自治区
        elif sheng == '新疆维吾尔自治区':
            province_map['新疆'] = sheng
        elif sheng == '内蒙古自治区':
            province_map['内蒙古'] = sheng
        elif sheng == '广西壮族自治区':
            province_map['广西'] = sheng
            province_map['广西省'] = sheng
        elif sheng == '西藏自治区':
            province_map['西藏'] = sheng
        elif sheng == '宁夏回族自治区':
            province_map['宁夏'] = sheng
        # 特别行政区
        # elif sheng == '香港特别行政区':
        #     province_map['香港'] = sheng
        # elif sheng == '澳门特别行政区':
        #     province_map['澳门'] = sheng


area_map, city_map, province_area_map, province_map, latlng = _data_from_csv()

# 直辖市
munis = {'北京市', '天津市', '上海市', '重庆市'}


def is_munis(city_full_name):
    return city_full_name in munis


myumap = {
    '南关区': '长春市',
    '南山区': '深圳市',
    '宝山区': '上海市',
    '市辖区': '东莞市',
    '普陀区': '上海市',
    '朝阳区': '北京市',
    '河东区': '天津市',
    '白云区': '广州市',
    '西湖区': '杭州市',
    '铁西区': '沈阳市'
}


def transform(location_strs, umap=myumap, index=[], cut=True, lookahead=8, pos_sensitive=False, open_warning=True):
    """将地址描述字符串转换以"省","市","区"信息为列的DataFrame表格
        Args:
            locations:地址描述字符集合,可以是list, Series等任意可以进行for in循环的集合
                      比如:["徐汇区虹漕路461号58号楼5楼", "泉州市洛江区万安塘西工业区"]
            umap:自定义的区级到市级的映射,主要用于解决区重名问题,如果定义的映射在模块中已经存在，则会覆盖模块中自带的映射
            index:可以通过这个参数指定输出的DataFrame的index,默认情况下是range(len(data))
            cut:是否使用分词，默认使用，分词模式速度较快，但是准确率可能会有所下降
            lookahead:只有在cut为false的时候有效，表示最多允许向前看的字符的数量
                      默认值为8是为了能够发现"新疆维吾尔族自治区"这样的长地名
                      如果你的样本中都是短地名的话，可以考虑把这个数字调小一点以提高性能
            pos_sensitive:如果为True则会多返回三列，分别提取出的省市区在字符串中的位置，如果字符串中不存在的话则显示-1
            open_warning: 是否打开umap警告, 默认打开
        Returns:
            一个Pandas的DataFrame类型的表格，如下：
               |省    |市   |区    |地址                 |
               |上海市|上海市|徐汇区|虹漕路461号58号楼5楼  |
               |福建省|泉州市|洛江区|万安塘西工业区        |
    """

    from collections.abc import Iterable

    if not isinstance(location_strs, Iterable):
        from .exceptions import InputTypeNotSuportException
        raise InputTypeNotSuportException(
            'location_strs参数必须为可迭代的类型(比如list, Series等实现了__iter__方法的对象)')

    import pandas as pd

    result = pd.DataFrame([_handle_one_record(addr, umap, cut, lookahead, pos_sensitive, open_warning) for addr in location_strs], index=index) \
             if index else pd.DataFrame([_handle_one_record(addr, umap, cut, lookahead, pos_sensitive, open_warning) for addr in location_strs])
    # 这句的唯一作用是让列的顺序好看一些
    if pos_sensitive:
        return result.loc[:, ('省', '市', '区', '地址', '省_pos', '市_pos', '区_pos')]
    else:
        return result.loc[:, ('省', '市', '区', '地址')]

def parseAddr(addr, umap=myumap, index=[], cut=False, lookahead=8, pos_sensitive=False, open_warning=True):
    result = _handle_one_record(addr, umap, cut, lookahead, pos_sensitive, open_warning)
    # 获取乡镇
    dz = result["地址"]
    if dz is not None and dz!="":
        xz,new_addr = parseXZ(dz)
        if xz!="":
            result["乡镇"] = xz
            result["地址"] = new_addr

    # 根据正则获取道路和道路号码
    road,road_num = GetRoadNumByRegex(result["地址"])
    if road!="" and road_num!="":
        result["道路"] = road
        result["道路号"] = road_num
        result["地址"] = result["地址"][len(road)+len(road_num):]

    # 根据正则获取组和组号
    zu,zu_num = GetZuAndNum(result["地址"])
    if zu!="" and zu_num!="":
        result["组"] = zu
        result["组号"] = zu_num
        result["地址"] = result["地址"][:len(result["地址"])-len(zu)-len(zu_num)]
        

    return result

def parseXZ(addr):
    seg_list = jieba.lcut(addr, cut_all=False)
    
    if len(seg_list)>0 and isXZ(seg_list[0]):
        return seg_list[0],addr[len(seg_list[0]):]
    return "",""

def isXZ(value):
    if value.endswith("镇") or value.endswith("乡") or value.endswith("旗"):
        return True
    return False

def _handle_one_record(addr, umap, cut, lookahead, pos_sensitive, open_warning):
    """处理一条记录"""
    src_addr = addr
    # 空记录
    if not isinstance(addr, str) or addr == '' or addr is None:
        empty = {'省': '', '市': '', '区': ''}
        if pos_sensitive:
            empty['省_pos'] = -1
            empty['市_pos'] = -1
            empty['区_pos'] = -1
        return empty

    # 地名提取
    pca, addr = _extract_addr(addr, cut, lookahead)

    _fill_city(pca, umap, open_warning,src_addr)

    _fill_province(pca)

    result = pca.propertys_dict(pos_sensitive)
    result["乡镇"] = ""
    result["道路"] = ""
    result["道路号"] = ""
    result["地址"] = addr
    result["组"] = ""
    result["组号"] = ""
    
    # 去除剩余地址中以省市区开头的部分
    for x in range(1,10):
        x = 0
        if addr.startswith(result["省"]):
            addr = addr[len(result["省"]):]
            result["地址"] = addr
        elif addr.startswith(result["市"]):
            addr = addr[len(result["市"]):]
            result["地址"] = addr
        elif addr.startswith(result["区"]):
            addr = addr[len(result["区"]):]
            result["地址"] = addr
        else:
            break

    return result

def _fill_province(pca):
    """填充省"""
    if (not pca.province) and pca.city and (pca.city in city_map):
        pca.province = city_map.get_value(pca.city, P)


def _fill_city(pca, umap, open_warning,addr):
    if not pca.city and not pca.province and not pca.area:
        return
    """填充市"""
    if not pca.city:
        # 从 区 映射
        if pca.area:
            # 从umap中映射
            if umap.get(pca.area):
                pca.city = umap.get(pca.area)
                return
            if pca.area in area_map and area_map.is_unique_value(pca.area):
                pca.city = area_map.get_value(pca.area, C)
                return

        # 从 省,区 映射
        if pca.area and pca.province:
            newKey = (pca.province, pca.area)
            if newKey in province_area_map and province_area_map.is_unique_value(newKey):
                pca.city = province_area_map.get_value(newKey, C)
                return

        if open_warning:
            import logging
            logging.warning("%s 无法映射, 建议添加进umap中", addr)


def _extract_addr(addr, cut, lookahead):
    """提取地址中的省,市,区名称
       Args:
           addr:原始地址字符串
           cut: 是否分词
       Returns:
           [sheng, shi, qu, (sheng_pos, shi_pos, qu_pos)], addr
    """
    return _jieba_extract(addr) if cut else _full_text_extract(addr, lookahead)


def _jieba_extract(addr):
    """基于结巴分词进行提取"""
    result = Pca()

    pos = 0
    truncate = 0

    def _set_pca(pca_property, name, full_name):
        """pca_property: 'province', 'city' or 'area'"""
        if not getattr(result, pca_property):
            setattr(result, pca_property, full_name)
            setattr(result, pca_property + "_pos", pos)
            if is_munis(full_name):
                setattr(result, "province_pos", pos)
            nonlocal truncate
            if pos == truncate:
                truncate += len(name)

    for word in jieba.cut(addr):
        # 优先提取低级别行政区 (主要是为直辖市和特别行政区考虑)
        if word in area_map:
            _set_pca('area', word, area_map.get_full_name(word))
        elif word in city_map:
            _set_pca('city', word, city_map.get_full_name(word))
        elif word in province_map:
            _set_pca('province', word, province_map[word])
        
        pos += len(word)

    return result, addr[truncate:]


def _full_text_extract(addr, lookahead):
    """全文匹配进行提取"""

    result = Pca()

    truncate = 0

    def _set_pca(pca_property, pos, name, full_name):
        """pca_property: 'province', 'city' or 'area'"""
        def _defer_set():
            if not getattr(result, pca_property):
                setattr(result, pca_property, full_name)
                setattr(result, pca_property + "_pos", pos)
                if is_munis(full_name):
                    setattr(result, "province_pos", pos)
                nonlocal truncate
                if pos == truncate:
                    truncate += len(name)
            return len(name)
        return _defer_set

    # i为起始位置
    i = 0
    while i < len(addr):
        # 用于设置pca属性的函数
        defer_fun = None
        # l为从起始位置开始的长度,从中提取出最长的地址
        for length in range(1, lookahead + 1):
            if i + length > len(addr):
                break
            word = addr[i:i + length]
            # 优先提取低级别的行政区 (主要是为直辖市和特别行政区考虑)
            if word in area_map:
                defer_fun = _set_pca('area', i, word, area_map.get_full_name(word))
                continue
            elif word in city_map:
                defer_fun = _set_pca('city', i, word, city_map.get_full_name(word))
                continue
            elif word in province_map:
                defer_fun = _set_pca('province', i, word, province_map[word])
                continue

        if defer_fun:
            i += defer_fun()
        else:
            i += 1

    return result, addr[truncate:]