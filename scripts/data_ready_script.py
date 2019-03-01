# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase

import re, os, sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'permission.settings'
django.setup()

from language.models import CommentInfo, Facebook, Sort, SortData
from language.db import connectDB


# Create your tests here.


def product_dict(product_id):
    return {
        222: "g66",
        12: "h55",
        18: "h52",
    }.get(product_id)


def get_raw_data():
    sort_name = 'BUG'
    infos = CommentInfo.objects.filter(comment_type=sort_name)
    sort, created = Sort.objects.get_or_create(name=sort_name)

    query_set_list = []
    for info in infos:
        product_code = product_dict(info.product_id)
        if info.product_id != 12 or info.comment_id in []:
            continue
        try:
            facebook = Facebook.objects.get(pk=info.comment_id)
            query_set_list.append(
                SortData(content=facebook.content, comment_id=facebook.unique_id, post_date=facebook.post_date,
                         source=facebook.source, sort=sort, product=product_code))
            print facebook.content, info.comment_id
            print "-" * 100
        except Facebook.DoesNotExist:
            print "找不到原数据", "=" * 50, info.comment_id
    # SortData.objects.bulk_create(query_set_list)


if __name__ == '__main__':
    get_raw_data()