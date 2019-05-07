#encoding = utf-8
import simple_proxy;
import header;

if __name__ == "__main__":
    # 爬取前10页
    # xici = simple_proxy.ProxyIPWormXiCi("https");
    # xici.get_pages_ips(xici.start_page, 10);
    xici = simple_proxy.ProxyIPWormXiCi("https", header.proxy);
    xici.get_pages_ips(84, xici.end_page);

    #225