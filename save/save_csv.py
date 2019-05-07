#encoding = utf-8
import pandas;

'''
    供simple_proxy使用的保存数据函数集
'''

def to_pandas_DataFrame(ips_list):
    '''
    适配pandas 的数据类型， 将list表转换为pandas存储的数据类型
    :param page_list: 保存字典类型的列表
    :return: 返回panfas存储数据的类型
    '''
    page_map = map(lambda ip_model: ip_model.to_dict(), ips_list);
    return pandas.DataFrame(list(page_map));

def to_csv(dicts, prefix):
    '''
    :param dicts:要保存的字典
    :param prefix:保存文件的前缀名
    '''
    to_pandas_DataFrame(dicts).to_csv("./{}_ips_info.csv".format(prefix), mode="a", encoding="ANSI");

def read_csv(path="http_ips_info.csv"):
    '''
    从csv的指定行开始读取对应行数的ip内容
    :param path: csv文件路径名
    :return: 返回对应的ip_dict
    '''
    dataframe = pandas.read_csv(path, encoding="ANSI");
    for data in dataframe.iterrows():
        ip_dict = data[1].to_dict();
        yield ip_dict;
