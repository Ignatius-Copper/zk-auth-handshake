import json
import secrets


def check_on_common_numbers(q: int):
    check_number = False
    num = 2
    if q <= 1:
        return False
    while check_number != True:
        if q % num == 0:
            return False
        elif num * num > q:
            return True
        else:
            num += 1


def generat_numbers():
    equals = True
    n: int
    while equals == True:
        p = secrets.SystemRandom().randint(100000, 1000000)
        q = secrets.SystemRandom().randint(100000, 1000000)
        if p != q and check_on_common_numbers(p) and check_on_common_numbers(q):
            equals = False
            n = p * q
            break
    return n


def generator_s(n: int):
    while True:
        e = secrets.SystemRandom().randint(2, n - 1)
        b = e
        a = n
        while b != 0:
            a, b = b, a % b
        comprime = a
        if comprime == 1:
            return e


def proving(n: int, t: int):
    s_list = []
    v_list = []
    for i in range(t):
        s = generator_s(n)
        v = pow(s, 2, n)
        s_list.append(s)
        v_list.append(v)
    return s_list, v_list


def turn_into_json(payload: dict):
    data_json = json.dumps(payload).encode("utf-8")
    return data_json


def turn_into_readbly_format(server_output: str):
    data_format = json.loads(server_output)
    return data_format
