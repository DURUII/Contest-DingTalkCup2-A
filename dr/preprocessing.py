from typing import Dict
from tqdm.auto import tqdm

import numpy as np
import random
import pandas as pd
import ydata_profiling

import scienceplots
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib

import torch
import os

pd.plotting.register_matplotlib_converters()
sns.set_style("whitegrid")
sns.set_palette("RdBu")
sns.set(
    rc={'text.usetex': True},
    font="serif",
    font_scale=1.2
)

# 辅助表格，常用APP类别
# 发现：原始表格存在重复值
app = pd.read_csv('../Datasets/app_class.csv', header=None).drop_duplicates()
app.columns = ['appid', 'app_class']

# 约束数据格式
app['appid'] = app['appid'].astype('category')
app['app_class'] = app['app_class'].astype('category')

# 打印行列数
print('app:', app.shape)

for i in tqdm(range(1, 22)):
    # 读取初赛数据集
    df = pd.read_csv(f'../Datasets/day{str(i).zfill(2)}.txt', header=None)

    # 设置列标签
    df.columns = ['uid', 'appid', 'app_type', 'start_day', 'start_time',
                  'end_day', 'end_time', 'duration', 'up_flow', 'down_flow']

    # 连接辅助表
    df = df.merge(app, on='appid', how='left')

    # 约束数据格式
    df['appid'] = df['appid'].astype('category')
    df['uid'] = df['uid'].astype('category')
    df['app_type'] = df['app_type'].astype('category')
    df['start_time'] = pd.to_datetime(df['start_time'], format="%H:%M:%S")
    df['end_time'] = pd.to_datetime(df['end_time'], format="%H:%M:%S")

    # 使用 pandas.Timestamp 将 `day` 和 `time` 合并
    df['start_time_new'] = df.apply(
        lambda x: x['start_time'] + pd.Timedelta(x['start_day'] - 1, unit='D'), axis=1)
    df['end_time_new'] = df.apply(
        lambda x: x['end_time'] + pd.Timedelta(x['end_day'] - 1, unit='D'), axis=1)

    # 使用 pickle 存储
    df = df[['uid', 'app_type', 'app_class', 'start_time_new',
            'end_time_new', 'duration', 'up_flow', 'down_flow']]
    df.to_pickle(f'../Datasets/day{str(i).zfill(2)}_new.pkl')
