from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command, netmiko_send_config
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.functions import print_result


nr = InitNornir(
    config_file="config.yaml",
    # dry_run=True
)

# 过滤出路由器
routers = nr.filter(
    type="router",
    # site='beijing'
)

# 过滤出防火墙
asas = nr.filter(
    type="firewall",
    # site='beijing'
)


# 执行show命令
# result = routers.run(netmiko_send_command, command_string="show ip int br")
# print_result(result)


# 配置路由器函数
def config_routers(task):
    # 读取模板,并且通过参数render为具体配置
    ios_interface_template = task.run(
        task=template_file, template='cisco_ios_interface.template', path='./templates/'
    )
    # 传入具体配置, 对设备进行配置, 注意需要".split('\n')"把配置转换为列表
    task.run(netmiko_send_config, config_commands=ios_interface_template.result.split('\n'), cmd_verify=True)

    # 读取模板,并且通过参数render为具体配置
    ospf_template = task.run(
        task=template_file, template='cisco_ios_ospf.template', path='./templates/'
    )
    # 传入具体配置, 对设备进行配置, 注意需要".split('\n')"把配置转换为列表
    task.run(netmiko_send_config, config_commands=ospf_template.result.split('\n'), cmd_verify=True)


# 配置防火墙函数
def config_asas(task):
    # 读取模板,并且通过参数render为具体配置
    asa_interface_template = task.run(
        task=template_file, template='asa_interface.template', path='./templates/'
    )
    # 传入具体配置, 对设备进行配置, 注意需要".split('\n')"把配置转换为列表
    task.run(netmiko_send_config, config_commands=asa_interface_template.result.split('\n'), cmd_verify=True)


# 执行配置路由器并打印结果
run_result = routers.run(config_routers)
print_result(run_result)

# 执行配置防火墙并打印结果
run_result = asas.run(config_asas)
print_result(run_result)
