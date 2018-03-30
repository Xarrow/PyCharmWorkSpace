# -*- coding:utf-8 -*-
"""
sample of typing in Python3.6.4
"""


# sample 1 : duck type
class Parrot:
    def fly(self):
        print("Parrot flying")


class Airplane:
    def fly(self):
        print("Airplane flying")


class Bird:
    def fly(self):
        print("Birder flying")


def react_fly(entry):
    entry.fly()


parrot = Parrot()
airplane = Airplane()
bird = Bird()

react_fly(parrot)
react_fly(airplane)
react_fly(bird)


# sample 2: basic usage

def say_greeting(name: str) -> str:
    return "Hi," + name


say_greeting("jian")

# sample 3: Type Alias
from typing import List

Vector = List[float]


def scale(scalar: float, vector: Vector) -> Vector:
    return [scalar * num for num in vector]


print(scale(0.5, [1.3, 1.2, 1.2, 1.0]))

# sample 3.1 Type Alias of Socket
from typing import Tuple

Address = Tuple[str, int]


def build_simple_server(server_address: Address) -> None:
    # function anotations
    import socket
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.bind(server_address)
    while True:
        socket.listen()
        client, address = socket.accept()
        data = client.recv()
        print(str(data, encoding='utf-8'))

build_simple_server(('127.0.0.1', 80))

# sample 4: Dict, Any, Tuple And List
from typing import Dict, Any, Tuple, List

MyDict = Dict[str, Any]
MyTuple = Tuple[str, int]
MyList = List[str]


def show_dict(my_tuple: MyTuple, my_dict: MyDict, my_list: MyList) -> None:
    assert (isinstance(my_dict, dict))
    assert (isinstance(my_tuple, tuple))
    print(my_dict)
    print(my_tuple)


show_dict(my_tuple=("1", 1), my_dict={'1': 1}, my_list=["1", "2"])

# sample 5:  NewType

from typing import NewType

UserId = NewType("UserId", int)
user_a = UserId(121)
user_b = UserId(2112)
print(user_a + user_b)

# generic
from typing import TypeVar, List

T = TypeVar('T', int, float)


def sum_from_list(li: List[T]) -> T:
    return sum([x for x in li])


print(sum_from_list([1.1, 2, 3, 43, 43, 4]))

# sample 6: Any
from typing import Any


def show_any(param: Any) -> Any:
    return 1, param, True

a, b, c = show_any(param='any_param')
print("==>")
print(a, b, c)

# sample 7: overload
from typing import overload


@overload
def wink(person_name: str) -> str:
    pass


@overload
def wink(wink_count: int) -> None: pass


def wink(response: Any) -> Any:
    if isinstance(response, str):
        return "Person: " + response + " winking."
    if isinstance(response, int):
        print("wink count is :" + str(response))


wink(11)

# sample 8: callable
from typing import Callable, TypeVar
from requests import Session
from requests import models

T = TypeVar('T', bound=models.Response)


def async_request(url: str, on_success: Callable[[T], None]) -> None:
    response = Session().get(url=url, verify=False)
    if response.status_code == 200:
        on_success(response)


async_request(url='https://www.baidu.com', on_success=lambda response: print("request_call:%s", response.text))

# sample 9: Union
from typing import Union

assert Union[Union[int, str], float] == Union[int, str, float]

var2 = Union[int] == int
print(var2)

var3 = Union[str, int] == Union[int, str]
print(var3)
