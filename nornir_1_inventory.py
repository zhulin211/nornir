# https://nornir.readthedocs.io/en/latest/tutorial/inventory.html
from nornir import InitNornir
from nornir.core.inventory import Host
from pprint import pprint

nr = InitNornir(config_file="config.yaml")

# 要求的格式
print('-'*50 + '打印Host schema' + '-'*50)
pprint(Host.schema(), indent=4)

# {   'connection_options': {   '$connection_type': {   'extras': {   '$key': '$value'},
#                                                       'hostname': 'str',
#                                                       'password': 'str',
#                                                       'platform': 'str',
#                                                       'port': 'int',
#                                                       'username': 'str'}},
#     'data': {'$key': '$value'},
#     'groups': ['$group_name'],
#     'hostname': 'str',
#     'name': 'str',
#     'password': 'str',
#     'platform': 'str',
#     'port': 'int',
#     'username': 'str'}

print('-'*50 + '打印Hosts' + '-'*50)
pprint(nr.inventory.hosts)
pprint(nr.inventory.hosts['csr1'])

print('-'*50 + '打印Groups' + '-'*50)
pprint(nr.inventory.groups)
pprint(nr.inventory.groups['iosxe_routers'])

# csr1从group获取data
print('-'*50 + '打印csr1信息(从group得到信息)' + '-'*50)
csr1 = nr.inventory.hosts['csr1']
print(type(csr1))
print(csr1.keys())
print(csr1['site'])

# csr2从default获取data
print('-'*50 + '打印csr2信息(从default得到信息)' + '-'*50)
csr2 = nr.inventory.hosts['csr2']
print(type(csr2))
print(csr2.keys())
print(csr2['site'])

# 不同的过滤方案
print('-'*50 + '过滤方案一' + '-'*50)
print(nr.filter(site="beijing").inventory.hosts.keys())

print('-'*50 + '过滤方案二' + '-'*50)
print(nr.filter(site="beijing", type="router").inventory.hosts.keys())

print('-'*50 + '过滤方案三' + '-'*50)
print(nr.filter(site="beijing").filter(type="router").inventory.hosts.keys())

print('-'*50 + '过滤方案四' + '-'*50)
filter1 = nr.filter(site="beijing")
filter2 = filter1.filter(type="router")
print(filter2.inventory.hosts.keys())

# 找到组内的设备
print('-'*50 + '查找组内的设备' + '-'*50)
print(nr.inventory.children_of_group("iosxe_routers"))

