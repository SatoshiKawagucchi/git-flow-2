# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals


def print_number(upper_count):
    """
    1から引数までの数字を表示する

    :type upper_count: int
    """
    if not upper_count:
      raise ValueError

    print('start')
    for i in xrange(upper_count):
      print(i + 1)

    print('end')


# 数字を表示する
print_number(10)
