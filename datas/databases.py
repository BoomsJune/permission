# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import MySQLdb
import codecs
import os

from datas import cut_word


def get_data_from_filter():
    """
    获取分类好的数据
    [(['word1','word2'],label),(['word1','word2','word3'],label)]
    """
    mysql_cn = MySQLdb.connect(host='10.250.30.158', port=3306, user='root', passwd='88888888', db='zjy_test')
    sql = "SELECT content,sort FROM language_filterdata where sort!=0 and sort!=3"
    cursor = mysql_cn.cursor()
    cursor.execute(sql)
    alldata = cursor.fetchall()
    cursor.close()
    mysql_cn.close()
    return handle_datas(alldata)


def get_filewords(file_name):
    """获取停用词"""
    filepath = os.path.dirname(os.path.realpath(__file__)) + "/dicts/"+file_name
    words = [line.strip() for line in codecs.open(filepath, 'r', 'utf-8').readlines()]
    return words


def handle_datas(datas):
    """处理好数据并分词"""
    r = '{机器型号:[\s\S]*?}|回复：[\s\S]*'
    data_list = []
    stopwords = get_filewords("stop_words.txt")
    for data in datas:
        if int(data[1]) > 3:
            label = 1
        else:
            label = 0
        words_list = []
        words = cut_word.CutWord(re.sub(r, '', data[0]), 'zh').cut()
        for word in words:
            if word not in stopwords:
                words_list.append(word)
        data_list.append((words_list, label))
    return data_list

