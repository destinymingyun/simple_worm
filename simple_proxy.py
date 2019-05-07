# encoding = utf-8
__all__ = ("ProxyIPWormXiCi");
from header import Header, html_to_dom;
from ip_model import IP_Model;
from save import save_csv
import os;

class ProxyIPWormXiCi(object):
    '''爬取代理ip'''
    def __init__(self, type, request=html_to_dom):
        self.request = request;
        self.http_type = type;
        self.name = "xici";

    @property
    def start_page(self):
        '''
        开始页
        :return:永远返回1
        '''
        return 1;

    @property
    def end_page(self):
        '''
        获取公开的高匿ip的总页数
        :return: 返回高匿ip页数
        '''
        page_dom = self.dom_tree.select(".pagination a");
        self._end_page = page_dom[-2];
        return int(self._end_page.text);

    def page_url(self, page):
        '''
        由给定整数生成对应西刺ip对应的页数的网址
        :param page: 指定的页数
        :return: 生成后的网址
        '''
        if page < 1 or page > self.end_page:
            raise RuntimeError("页数大于总页数");
        elif page == 1:
            return "https://www.xicidaili.com/{}/".format(self.type_to_url(self.http_type));
        else:
            return "https://www.xicidaili.com/{}/{}".format(self.type_to_url(self.http_type), page);

    @property
    def http_type(self):
        return self._http_type;

    @http_type.setter
    def http_type(self, type):
        '''
        根据http或https设置
        :param type: hhtp 或 https
        '''
        if not(type == "http" or type == "https"):
            raise RuntimeError("type应该为http或https");
        self._http_type = type;
        self.proxy_ip_html = "https://www.xicidaili.com/{}/".format(self.type_to_url(type));
        self.dom_tree = html_to_dom(self.proxy_ip_html, Header().headers);


    def type_to_url(self, type):
        '''
        将http或https转换为对应的西刺url片段
        :param type:
        :return:
        '''
        if type == "http":
            return "wt";
        elif type == "https":
            return "wn";
        else:
            raise RuntimeError("type应该为http或https");

    def get_page_ips(self, page):
        '''
        获取指定页的所有ip
        :param type: ip类型  http 或 https
        :param page: 爬取页面
        :return:返回该页被ip_model封装的所有ip列表
        '''
        print(self.page_url(page));
        page_dom = self.request(self.page_url(page));
        page_ips_dom = page_dom.select("table tr");
        # print(page_ips_dom[0]);
        ip_generator = (ip for ip in page_ips_dom[1:]);
        ip_list = [];
        for ip_dom in ip_generator:
            ip_info = self.get_ip_info(ip_dom);
            ip_list.append(ip_info);
        return ip_list;

    def get_ip_info(self, ip_dom):
        '''
        获取指定的ip详细信息
        :param ip_dom: 存有ip信息的html节点
        :return: 返回ip_model结构的ipo封装类
        '''
        ip_info = IP_Model();
        ip_td = ip_dom.select("td");
        country = ip_td[0].img;
        ip_info.http_type = ip_td[5].text;
        if country != None:
            ip_info.country = str(country.get("alt"));
            ip_info.addres = ip_td[3].text.split()[0];
        ip_info.ip = ip_td[1].text;
        ip_info.port = ip_td[2].text;
        anonymous = ip_td[4].text;
        if anonymous == "高匿":
            ip_info.anonymous = True;
        else:
            ip_info.anonymous = False;

        ip_info.velocity = ip_td[6].div.get("title");
        return ip_info;

    def get_pages_ips(self, start_page, end_page, save_in=save_csv.to_csv):
        '''
        获取指定开始页到结束页的所有ip(包括结束页)
        :param type: 请求为http还是https
        :param start_page: 开始页面
        :param end_page: 结束页
        :param save_in: 如何保存到文件格式，是一个回调函数，默认保存入csv
        :return:
        '''
        if start_page > end_page:
            raise RuntimeError("开始页大于结束页");
        elif start_page == end_page:
            page_list = self.get_page_ips(start_page);
            save_in(page_list, self.http_type);
        elif start_page < 1:
            raise RuntimeError("开始页小于结束页");
        elif end_page > self.end_page:
            raise RuntimeError("结束页大于总页数");
        else:
            for page in range(start_page, end_page+1):
                print("当前页:{}".format(page));
                page_list = self.get_page_ips(page);
                prefix = "{}_{}".format(self.name, self.http_type)
                save_in(page_list, prefix);
                # time.sleep(10);
        return page_list;

    def get_up_to_pages_ips(self, save_in=save_csv.to_csv()):
        '''
        返回最新的5页ip
        :return: 最新的5页ip
        '''
        prefix = "{}_{}".format(self.name, self.http_type);
        file_path = prefix + "_ips_info.csv";
        if os.path.exists(file_path):
            os.remove(file_path);
        page_list = self.get_pages_ips(self.start_page, 5, save_in);
        return page_list;

if __name__ == "__main__":
    # test = ProxyIPWormXiCi("http");
    #爬到170页
    # test.get_pages_ips(test.start_page, test.end_page);
    #
    # https_list = test.get_page_ips("https", 1);
    # http_list =  test.get_page_ips("http", 1);
    # ips = IP_List();
    # ips.https_list = https_list;
    # ips.http_list = http_list;
    # dom = proxy("http://news.gzcc.cn/html/xiaoyuanxinwen/", ips, True);
    # print(dom);
    pass;


