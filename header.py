#encoding = utf-8;
__all__ = ("Header", "proxy", "html_to_dom");
import random;
import re;
from bs4 import BeautifulSoup;
import requests;
from ip_model import IP_Queue;

class Header(object):
    '''请求头构造类'''
    def __init__(self):
        self.__user_agent = [
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)", #IE
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",  #  Fire_Fox
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",  # Chrome
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",  # taobao
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",    #猎豹
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36", # 360
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2", # safarir
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0", # 搜狐
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ", # maxthon
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36" # uc
        ];

    @property
    def headers(self):
        '''返回一个伪造后的hander'''
        headers = {
            "User-agent" : self.user_agent,
        };
        return headers;

    @property
    def user_agent(self):
        index = random.randint(0, len(self.__user_agent)-1);
        return self.__user_agent[index];

    def __new__(cls):
        '''此类创建模式为单实例模式'''
        if not hasattr(cls, "__instance"):
            cls.__instance = super().__new__(cls);
            return cls.__instance;
        else:
            return cls.__instance;

def proxy(url, is_anonymous=True):
    '''
    使用代理ip访问指定服务器
    :param url: 访问的服务器ip路径
    :return: 返回生成的bs4的dom
    '''
    type = re.match(r"(.*):.*", url).group(1);
    ip_queue = None;
    if type == "http" or type == "https":
        ip_queue = IP_Queue(type);
        ip_queue.init_generator();
    else:
        raise RuntimeError("不支持此类请求");
    ip = ip_queue.get_ip();
    while ip != None:
        while ip.anonymous != is_anonymous:
            ip = ip_queue.get_ip();
        proxies = {type: "{}:{}".format(ip.ip, ip.port)};
        print("当前尝试ip主机:{}, 高匿:{}".format(proxies, ip.anonymous));
        try:
            dom = html_to_dom(url, Header().headers, proxies);
            if dom != None:
                return dom;
            else:
                print("该代理ip被访问路径拒绝");
                ip = ip_queue.get_ip();
        except Exception:
            #预留添加删除对应ip
            ip = ip_queue.get_ip();

def html_to_dom(url, header=Header().headers, proxies=None):
    '''
    简单封装下requests
    :param url: 访问url
    :param header: 伪造的请求头
    :param proxies: 是否使用代理ip
    :return:
    '''
    # if proxies != None:
    try:
        response = requests.get(url, headers=header, proxies=proxies, verify=True);
    except Exception:
        print("连接异常");
        raise Exception("连接异常");
    # else:
    #     response = requests.get(url, headers=header, verify=True);
    if response.status_code == 200:
        response.encoding = "utf-8";
        return BeautifulSoup(response.text, "html.parser");
    else:
        return None;


if __name__ == "__main__":
    dom = proxy("http://news.gzcc.cn/html/xiaoyuanxinwen/");
    print(dom);