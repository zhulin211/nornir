# https://nornir.readthedocs.io/en/latest/tutorial/task_results.html
import logging
from nornir import InitNornir
from nornir.core.task import Task, Result

# instantiate the nr object
nr = InitNornir(config_file="config.yaml")
# let's filter it down to simplify the output
cmh = nr.filter(type="router")


def count(task: Task, number: int) -> Result:
    return Result(
        host=task.host,
        result=f"{[n for n in range(0, number)]}"
    )


def say(task: Task, text: str) -> Result:
    if task.host.name == "csr2":
        raise Exception("I can't say anything right now")
    return Result(
        host=task.host,
        result=f"{task.host.name} says {text}"
    )


def greet_and_count(task: Task, number: int):
    task.run(
        name="Greeting is the polite thing to do",
        severity_level=logging.DEBUG,
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
        severity_level=logging.DEBUG,
        task=say,
        text="bye!",
    )

    # let's inform if we counted even or odd times
    even_or_odds = "even" if number % 2 == 1 else "odd"
    return Result(
        host=task.host,
        result=f"{task.host} counted {even_or_odds} times!",
    )


result = cmh.run(
    task=greet_and_count,
    number=5,
)


from nornir_utils.plugins.functions import print_result

# print_result(result)

# As you probably noticed, not all the tasks were printed.
# This is due to the severity_level argument we passed.
# This let’s us flag tasks with any of the logging levels.
# Then print_result is able to follow logging rules to print the results.
# By default only tasks marked as INFO will be printed
# (this is also the default for the tasks if none is specified).

# print_result(result, severity_level=logging.DEBUG)
# print_result(result['csr1'][2])
print(result['csr1'][2])
print("changed: ", result["csr1"].changed)
