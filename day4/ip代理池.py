import requests
from lxml import etree
# 获得本机ip地址
check_url='http://www.httpbin.org/ip'
host_ip=requests.get(check_url).text
# id代理池：
class Pool(object):
# 属性（有什么）：
# 一个存放ip地址的容器（一定是可用ip）
# 阈值（决定定量）
    def __init__(self,yuzhi):
        self.db=DB('ips1.txt')
        self.yuzhi=yuzhi
        self.pagenum=1
# 方法（能做什么）：
# 1. 检验ip地址可用性
    def check_ip(self,ip):
        try:# 获得目标ip地址
            target_ip=requests.get(check_url,proxies=ip).text
            if target_ip!=host_ip:
                return True
        except:
            pass
        # 出现异常为不可用
        return False
# 2. 采集ip地址
    def crawl_ip(self,url):
        html=etree.HTML(requests.get(url,headers={
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}).text)
        for tr in html.xpath('//tr')[1:]:
            # ./ 从当前对象开始选择
            tds = tr.xpath('./td/text()')
            ip = {tds[5].lower(): tds[5].lower()+'://'+tds[0] + ':' + tds[1]}
            print(ip)
            if self.check_ip(ip):
                self.db.save(str(ip))
        self.pagenum+=1
# 3. 获取ip地址
    def get_ip(self):
        #return self.db.get_ip() 不删
        # 删除ip
        ip=self.db.get_ip()
        self.db.delete_ip(ip)
        self.check_ip_by_yuzhi()
        return ip
# 4. 定期检测ip地址可用性
    def check_ip_by_time(self):
        #1.获取所有ip地址
        ips=self.db.get_all()
        #2.检测ip地址可用性
        for ip in ips:
        #3.不可用的ip地址删除
            if not self.check_ip(ip):
                self.db.delete_ip(ip)
        # #4.判断ip地址是否满足阈值
        self.check_ip_by_yuzhi()
        # count=self.db.get_count()
        # #5.不满足，则重新采集新的ip地址
        # if count<self.yuzhi:
        #     url='https://www.xicidaili.com/nn/'+str(self.pagenum)
        #     self.crawl_ip(url)
# 5. 定量检测ip地址可用性
    def check_ip_by_yuzhi(self):
        #1. 获取ip地址的数量
        count=self.db.get_count()
        #2. 判断数量是否满足阈值
        while count<self.yuzhi:
        #3. 不满足，则重新采集新的ip地址
            url = 'https://www.xicidaili.com/nn/' + str(self.pagenum)
            self.crawl_ip(url)
# 容器对象
class DB(object):
    def __init__(self,filename):
        self.filename=filename
# 方法：
# 1. 存ip
    def save(self,ip):
        with open(self.filename,'a')as w:
            w.write(ip+'\n')
# 2. 取ip
    def get_ip(self):
        with open(self.filename,'r')as r:
            return r.readline()
# 3. 删除ip
    def delete_ip(self,target_ip):
        with open(self.filename,'r')as r:
            ips=r.readlines()
        with open(self.filename,'w')as w:
            for ip in ips:
                if target_ip==ip:
                    continue
                else:
                    w.write(ip)
# 4. 获取所有ip地址数量
    def get_count(self):
        with open(self.filename, 'r')as r:
            return len(r.readlines())
# 5. 获取所有ip地址
    def get_all(self):
        with open(self.filename, 'r')as r:
            return r.readlines()

if __name__ == '__main__':
    pool=Pool(10)
    ip=pool.get_ip()
    print(ip)