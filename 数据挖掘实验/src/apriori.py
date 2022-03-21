# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 14:44:20 2021

@author: Yuetian
"""

import pandas as pd
import numpy as np
from itertools import combinations
from operator import itemgetter
from time import time
import warnings
warnings.filterwarnings("ignore")
# 拿到购物栏数据

dataset = pd.read_csv('retail.csv', usecols=['items'])


# 定义自己的Aprior算法
def my_aprior(data, support_count):
    """
    Aprior关联规则挖掘
    @data: 数据
    @support_count: 项集的频度, 最小支持度计数阈值
    """
    start = time()
    # 对数据进行处理，删除多余空格
    for index, row in data.iterrows():
        data.loc[index, 'items'] = row['items'].strip()
    # 找出所有频繁一项集
    single_items = (data['items'].str.split(" ", expand = True)).apply(pd.value_counts) \
    .sum(axis = 1).where(lambda value: value > support_count).dropna()
    print("找到所有频繁一项集")
    # 创建频繁项集对照表
    apriori_data = pd.DataFrame({'items': single_items.index.astype(int), 'support_count': single_items.values, 'set_size': 1})
    # 整理数据集
    data['set_size'] = data['items'].str.count(" ") + 1
    data['items'] = data['items'].apply(lambda row: set(map(int, row.split(" "))))
    single_items_set = set(single_items.index.astype(int))
    # 循环计算，找到频繁项集
    for length in range(2, len(single_items_set) + 1):
        data = data[data['set_size'] >= length]
        d = data['items'] \
            .apply(lambda st: pd.Series(s if set(s).issubset(st) else None for s in combinations(single_items_set, length))) \
            .apply(lambda col: [col.dropna().unique()[0], col.count()] if col.count() >= support_count else None).dropna()
        if d.empty:
            break
        apriori_data = apriori_data.append(pd.DataFrame(
            {'items': list(map(itemgetter(0), d.values)), 'support_count': list(map(itemgetter(1), d.values)),
             'set_size': length}), ignore_index=True)
    print("结束搜索，总耗时%s"%(time() - start))
    return apriori_data


apriori_result = my_aprior(dataset, 5000)
for x in apriori_result:
    print(x)