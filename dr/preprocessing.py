from tqdm.auto import tqdm
import pandas as pd
import os


def generate_pickle_origin(start_day=1, end_day=21):
    # 读取类型数据
    app = pd.read_csv(
        filepath_or_buffer='../Datasets/app_class.csv',
        header=None
    ).drop_duplicates()

    # 更新列标签
    app.columns = ['appid', 'app_class']

    # 新增一笔虚拟资料（NaN）
    app = pd.concat(
        objs=[pd.DataFrame({"appid": [-404], "app_class": ['NaN']}), app],
        ignore_index=True
    )

    # 约束数据格式
    app['app_class'] = app['app_class'].astype('category')
    app['appid'] = app['appid'].astype('category')

    # 初赛数据集day1～21
    for i in tqdm(range(start_day, end_day + 1)):
        # 读取监测数据
        df = pd.read_csv(
            filepath_or_buffer=f'../Datasets/day{str(i).zfill(2)}.txt',
            header=None
        ).drop_duplicates()

        # 更新列标签
        df.columns = ['uid', 'appid', 'app_type', 'start_day', 'start_time',
                      'end_day', 'end_time', 'duration', 'up_flow', 'down_flow']

        # 新增app_class，对于所属类别未知的APP，类别记作NaN
        df = df.merge(app, on='appid', how='left')
        df['app_class'] = df['app_class'].fillna('NaN')

        # 约束数据格式
        df['appid'] = df['appid'].astype('category')
        df['uid'] = df['uid'].astype('category')
        df['app_type'] = df['app_type'].astype('category')

        # df['start_time'] = pd.to_datetime(df['start_time'], format="%H:%M:%S")
        # df['end_time'] = pd.to_datetime(df['end_time'], format="%H:%M:%S")
        # 使用 pandas.Timestamp 将 `day` 和 `time` 合并
        # df['start_time_new'] = df.apply(
        #     lambda x: x['start_time'] + pd.Timedelta(x['start_day'] - 1, unit='D'), axis=1)
        # df['end_time_new'] = df.apply(
        #     lambda x: x['end_time'] + pd.Timedelta(x['end_day'] - 1, unit='D'), axis=1)

        df = df[['uid', 'appid', 'app_type', 'app_class', 'start_day', 'start_time',
                 'end_day', 'end_time', 'duration', 'up_flow', 'down_flow']]

        # 使用 pickle 存储
        df.to_pickle(f'../Datasets/day{str(i).zfill(2)}.pkl')


def generate_pickle_1(start_day=1, end_day=21):
    """
    数据融合：day01~day21
    建立特征：连接辅助表，新增app_class
    清洗数据：异常值、缺失值、重复值
    """

    # 读取类型数据
    app = pd.read_csv(
        filepath_or_buffer='../Datasets/app_class.csv',
        header=None
    ).drop_duplicates()

    # 更新列标签
    app.columns = ['appid', 'app_class']

    # 新增一笔虚拟资料（NaN）
    app = pd.concat(
        objs=[pd.DataFrame({"appid": [-404], "app_class": ['NaN']}), app],
        ignore_index=True
    )

    # 约束数据格式
    app['app_class'] = app['app_class'].astype('category')
    app['appid'] = app['appid'].astype('category')

    # 初赛数据集day1～21
    for i in tqdm(range(start_day, end_day + 1)):
        # 读取监测数据
        df = pd.read_csv(
            filepath_or_buffer=f'../Datasets/day{str(i).zfill(2)}.txt',
            header=None
        ).drop_duplicates()

        # 更新列标签
        df.columns = ['uid', 'appid', 'app_type', 'start_day', 'start_time',
                      'end_day', 'end_time', 'duration', 'up_flow', 'down_flow']

        # 问题：start_day为负数，甚至持续时间长达一千年
        df = df.query('start_day >=0 & duration <= 9159')

        # 新增app_class，对于所属类别未知的APP，类别记作NaN
        df = df.merge(app, on='appid', how='left')
        df['app_class'] = df['app_class'].fillna('NaN')
        # 问题：app_type 列存在中文
        df['app_class'] = df['app_class'].replace({'用户': 'usr', '预装': 'sys'})

        # 约束数据格式
        df['appid'] = df['appid'].astype('category')
        df['uid'] = df['uid'].astype('category')
        df['app_type'] = df['app_type'].astype('category')

        # df['start_time'] = pd.to_datetime(df['start_time'], format="%H:%M:%S")
        # df['end_time'] = pd.to_datetime(df['end_time'], format="%H:%M:%S")
        # 使用 pandas.Timestamp 将 `day` 和 `time` 合并
        # df['start_time_new'] = df.apply(
        #     lambda x: x['start_time'] + pd.Timedelta(x['start_day'] - 1, unit='D'), axis=1)
        # df['end_time_new'] = df.apply(
        #     lambda x: x['end_time'] + pd.Timedelta(x['end_day'] - 1, unit='D'), axis=1)

        df = df[['uid', 'appid', 'app_type', 'app_class', 'start_day', 'start_time',
                 'end_day', 'end_time', 'duration', 'up_flow', 'down_flow']]

        # 使用 pickle 存储
        df.to_pickle(f'../Datasets/day{str(i).zfill(2)}.pkl')


def generate_features(start_day=1, end_day=21):
    for i in tqdm(range(start_day, end_day + 1)):
        df = pd.read_pickle(f'../Datasets/day{str(i).zfill(2)}.pkl')
