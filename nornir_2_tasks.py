# https://nornir.readthedocs.io/en/latest/tutorial/tasks.html
from nornir import InitNornir
# pip3 install nornir-utils
from nornir_utils.plugins.functions import print_result
from nornir.core.task import Task, Result

nr = InitNornir(config_file="config.yaml")

nr = nr.filter(
    type="router",
    # site='beijing'
)


print('-'*50 + 'hello_world' + '-'*50)


# hello world
def hello_world(task: Task) -> Result:
    return Result(
        host=task.host,
        result=f"{task.host.name} says hello world!"
    )


result = nr.run(task=hello_world)
print_result(result)

print('-'*50 + '传参数' + '-'*50)


# 添加参数
# Task, str, Result都是在控制类型而已
def say(task: Task, text: str) -> Result:
    return Result(
        host=task.host,
        result=f"{task.host.name} says {text}"
    )


result = nr.run(
    name="more parameters",
    task=say,
    text="welcome to qytang!"
)
print_result(result)

print('-'*50 + '一组任务' + '-'*50)


# Grouping Tasks
def count(task: Task, number: int) -> Result:
    return Result(
        host=task.host,
        result=f"{[n for n in range(0, number)]}"
    )


def greet_and_count(task: Task, number: int) -> Result:
    task.run(
        name="Greeting is the polite thing to do",
        task=say,
        text="hi!",
    )

    task.run(
        name="Counting beans",
        task=count,
        number=number,
    )
    task.run(
        name="We should say bye too",
        task=say,
        text="bye!",
    )

    # let's inform if we counted even or odd times
    even_or_odds = "even" if number % 2 == 1 else "odd"
    return Result(
        host=task.host,
        result=f"{task.host} counted {even_or_odds} times!",
    )


result = nr.run(
    name="Counting to 5 while being very polite",
    task=greet_and_count,
    number=5,
)
print_result(result)
