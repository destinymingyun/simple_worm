#encoding = utf-8;
__all__ = ("IP_Model", "IP_Queue");
import queue;
from save import save_csv;

class IP_Model(object):
    '''保存代理ip的全部内容'''
    def __init__(self):
        self._country = None;
        self._addres = None;

    @property
    def country(self):
        '''
        代理服务器所在国家
        '''
        return self._country;

    @country.setter
    def country(self, ip_country):
        if ip_country != None:
            self._country = ip_country;
        else:
            self._country = None;

    @property
    def ip(self):
        '''
        代理服务器的ip
        '''
        return self._ip;

    @ip.setter
    def ip(self, new_ip):
        self._ip = new_ip;

    @property
    def port(self):
        '''
        访问端口号
        '''
        return self._port;

    @port.setter
    def port(self, new_port):
        self._port = new_port;

    @property
    def addres(self):
        '''
        服务器所在省地址
        '''
        return self._addres;

    @addres.setter
    def addres(self, new_addres):
        if new_addres != None:
            self._addres = new_addres;
        else:
            self._addres = None;

    @property
    def http_type(self):
        '''
        请求类型
        '''
        return self._http_type;

    @http_type.setter
    def http_type(self, type):
        self._http_type = type;

    @property
    def velocity(self):
        '''服务器速度'''
        return self._velocity;

    @velocity.setter
    def velocity(self, http_velocity):
        self._velocity = http_velocity;

    @property
    def anonymous(self):
        return self._anonymous;

    @anonymous.setter
    def anonymous(self, anonymous_text):
        if anonymous_text == "高匿" or anonymous_text == "True":
            self._anonymous = True;
        else:
            self._anonymous= False;

    def __str__(self):
        '''
        重新__str__方法，
        :return: 返回格式化的IP_Model属性内容生成的字符串
        '''
        return (
            "| country: {} |\n"
            "| ip: {} |\n"
            "| port: {} |\n"
            "| address: {} |\n"
            "| http_type: {} |\n"
            "| velocity: {}|\n"
            "| anonymous: {} |\n"
                .format(self.country, self.ip, self.port, self.addres, self.http_type, self.velocity, self.anonymous)
        );

    def to_dict(self):
        return {
            "country" : self.country,
            "ip" : self.ip,
            "port" : self.port,
            "addres" : self.addres,
            "http_type" : self.http_type,
            "velocity" : self.velocity,
            "anonymous": self.anonymous
        };

    def from_dict(self, dict):
        self.country = dict.get("country");
        self.ip = dict.get("ip");
        self.port = dict.get("port");
        self.addres = dict.get("addres");
        self.http_type = dict.get("http_type");
        self.velocity = dict.get("velocity");
        if dict.get("anonymous") == "True":
            self.anonymous = True;
        else:
            self.anonymous = False;

    def get_ip_proxies(self):
        proxies = None;
        if self.http_type == "https":
            proxies = { "https" : "{}:{}".format(self.ip, self.port)};
        else:
            proxies = {"http": "{}:{}".format(self.ip, self.port)};
        return proxies;

class IP_Queue(object):
    '''
    初始化ip队列
    :param http_type: http请求类型
    :param queue_size: 队列长度,默认为30个
    '''
    def __init__(self, http_type, queue_size = 30):
        self.http_type = http_type;
        self.http_queue = queue.Queue(queue_size);
        self.https_queue = queue.Queue(queue_size);
        self.init_queue();

    @property
    def http_type(self):
        return self._http_type;

    @http_type.setter
    def http_type(self, value):
        if value == "http" or value == "https":
            self._http_type = value;
        else:
            raise RuntimeError("无效类型");

    @property
    def ip_generator(self):
        return self._ip_generator;

    def init_generator(self, read_func = save_csv.read_csv):
        path = self.http_type+"_ips_info.csv";
        self._ip_generator = read_func(path);

    def init_queue(self):
        '''
        初始化队列指向对应类型的队列
        :return:
        '''
        self.queue = None;
        if self.http_type == "http":
            self.queue = self.http_queue;
        else:
            self.queue = self.https_queue;

    def replenish_ips(self):
        '''
        装填ip到ip队列中
        :return:
        '''
        if self.queue.full():
            return self.queue;
        count = self.queue.maxsize - self.queue.qsize();
        for i in range(count):
            self.queue.put(self.ip_generator.__next__());
        return self.queue;

    def get_ip(self):
        '''
        返回一个ip对应的ip_model类型
        :return: 返回ip_model
        '''
        if self.queue.empty():
            self.replenish_ips();
        # print(self.queue.qsize())
        ip = IP_Model();
        ip.from_dict(self.queue.get());
        return ip;

if __name__ == "__main__":
    ips = IP_Queue("https");
    ips.init_generator();
    print(ips.get_ip());
