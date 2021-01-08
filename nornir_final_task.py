from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command, netmiko_send_config
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.functions import print_result


nr = InitNornir(
    config_file="config.yaml",
    # dry_run=True
)

routers = nr.filter(
    type="router",
    # site='beijing'
)


# result = routers.run(netmiko_send_command, command_string="show ip int br")
# print_result(result)


def config_routers(task):
    interface_template = task.run(
        task=template_file, template='cisco_ios_interface.template', path='./templates/'
    )
    task.run(netmiko_send_config, config_commands=interface_template.result.split('\n'), cmd_verify=True)

    ospf_template = task.run(
        task=template_file, template='cisco_ios_ospf.template', path='./templates/'
    )
    task.run(netmiko_send_config, config_commands=ospf_template.result.split('\n'), cmd_verify=True)


run_result = routers.run(config_routers)
print_result(run_result)
