
from lxml import etree

# 解析单个主机扫描记录
def ParseOneHostXml(xml):
    # 获取主机信息
    host = xml.xpath("./address/@addr")[0]
    print("Host: %s" % host)
    ports_info = []
    ports = xml.xpath("./ports//port")
    # print(ports)
    for port_info in ports:
        tmp = {}
        tmp['protocol'] = port_info.xpath("./@protocol")[0]
        tmp['port'] = port_info.xpath("./@portid")[0]
        tmp['stat'] = port_info.xpath("./state/@state")[0]
        service = port_info.xpath("./service/@name")
        if service:
            tmp['service'] = service[0]
        else:
            tmp['service'] = "unknow"
        product = port_info.xpath("./service/@product")
        if product:
            tmp['product'] = product[0]
        else:
            tmp['product'] = "unknow"

        ports_info.append(tmp)

        print("Protocol：%s\tPort：%s\tStat：%s\tService：%s\tProduct：%s" %
              (tmp['protocol'], tmp['port'], tmp['stat'], tmp['service'], tmp['product'])
              )
    return host,ports_info


# 解析多个主机扫描记录
def ParseHostsXml(xml):
    hosts = xml.xpath("//host")
    hosts_info = {}    # 存储每个host对应的端口开放信息
    for host_info in hosts:
        host,ports_info = ParseOneHostXml(host_info)
        hosts_info[host] = ports_info

    return hosts_info


# ParseOneHostXml(xml)


keys = []   # 用于限制title输出次数及操作字典中对应数据
# 随机解析字典并输出到文件
def ParsePortsInfo(host,ports_info):
    # ports_info 数据格式为 [{},{}...]
    with open("test.csv","a+",encoding="utf-8") as f:
        if not keys:
            for key in ports_info[0].keys():
                keys.append(key)
            f.write('host,' + ','.join(keys) + "\n")
        for port_info in ports_info:
            tmp = []
            for key in keys:
                tmp.append(port_info.get(key))
            f.write(host+ ',' + ','.join(tmp) + "\n")
    print(keys)

# 输出所有的字段
def randomParse(hosts_info):
    for host, ports_info in hosts_info.items():
        ParsePortsInfo(host,ports_info)


# 自定义字段解析ParseHostsXml结果
def customParse(hosts_info):
    with open("result.csv", "a+", encoding="utf-8") as f:
        # 自定义port信息输出字段及顺序
        keys = ["port","protocol","stat","service","product"]

        # 判断是否存在目标输出文件或目标文件是否为空，以避免重复输出表头
        if not os.path.exists("result.csv") or not os.stat("result.csv").st_size:
            f.write('host,' + ','.join(keys) + "\n")

        for host, ports_info in hosts_info.items():
            if not ports_info:
                tmp = ['None','None','None','None','None']
                f.write(host + ',' + ','.join(tmp) + "\n")
            for port_info in ports_info:
                tmp = []
                for key in keys:
                    tmp.append(port_info.get(key))
                f.write(host + ',' + ','.join(tmp) + "\n")

if __name__ == "__main__":

    try:
        xmlFile = sys.argv[1]
    except Exception as e:
        print("命令格式：python nmap_xml2csv.py xml文件名")
        exit()    
    
    print("正在解析 %s " % xmlFile)
    # xml = etree.parse('nmap_test.xml')
    xml = etree.parse(xmlFile)

    hosts_info = ParseHostsXml(xml)
    # print(hosts_info)
    customParse(hosts_info)

# x = xml.xpath("//hosts/ports/port/service/@adsf")
# print(x)