from tqdm.auto import tqdm
import pandas as pd


def generate_pickle(start_day=1, end_day=21):
    """
    对原始txt文件进行粗处理：
    - 约束数据格式（类别、数值、时间）
    - 连接辅助表，重设列标签
    """

    assert 1 <= end_day <= 21

    # 辅助表格，常用APP类别
    # 发现：原始表格存在重复值
    app = pd.read_csv('../Datasets/app_class.csv',
                      header=None).drop_duplicates()
    app.columns = ['appid', 'app_class']

    # 约束数据格式
    # 便于对NaN进行EDA，增加了一笔虚拟资料
    app = pd.concat([pd.DataFrame({"appid": [-404], "app_class": ['NaN']}), app],
                    ignore_index=True)
    app['app_class'] = app['app_class'].astype('category')
    app['appid'] = app['appid'].astype('category')

    for i in tqdm(range(start_day, end_day + 1)):
        # 读取初赛数据集
        df = pd.read_csv(f'../Datasets/day{str(i).zfill(2)}.txt', header=None)

        # 设置列标签
        df.columns = ['uid', 'appid', 'app_type', 'start_day', 'start_time',
                      'end_day', 'end_time', 'duration', 'up_flow', 'down_flow']

        # 连接辅助表，仅
        df = df.merge(app, on='appid', how='left')
        df['app_class'] = df['app_class'].fillna('NaN')

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
