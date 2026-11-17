import secrets
import socket
import sys

from utils import proving, turn_into_json, turn_into_readbly_format


def client(n: int, t: int):
    r_list = []
    x_list = []
    for i in range(t):
        r = secrets.SystemRandom().randint(1, n - 1)
        x = pow(r, 2, n)
        r_list.append(r)
        x_list.append(x)
    return r_list, x_list


def client_ansewrs(r_list: list, e_list: list, s_list: list, n):
    y_list = []
    for r, e, s in zip(r_list, e_list, s_list):
        if e == 0:
            y = r % n
            y_list.append(y)
        elif e == 1:
            y = (r * s) % n
            y_list.append(y)

    return y_list


def zip_div(payload):
    if "n" in payload and "t" in payload:
        n = payload["n"]
        t = payload["t"]
        return n, t


params_request = {"type": "get_params"}
HOST = "127.0.0.1"
PORT = 65432
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    get_params = turn_into_json(params_request)
    s.sendall(get_params)
    type_init = s.recv(8192).decode("utf-8")
    inform = turn_into_readbly_format(type_init)
    n, t = zip_div(inform)
    s_list, v_list = proving(n, t)
    r_list, x_list = client(n, t)
    print(f"Connection with server{HOST}:{PORT}")
    name = input("Input name: ")
    first_data = {"type": "registrate", "username": name, "v": v_list}
    first_json = turn_into_json(first_data)
    s.sendall(first_json)
    status_reg = s.recv(8192).decode("utf-8")
    status_format_reg = turn_into_readbly_format(status_reg)
    print(status_format_reg)
    auth_init = {"type": "auth_init", "username": name, "x": x_list}
    auth_json = turn_into_json(auth_init)
    s.sendall(auth_json)
    challenge_raw = s.recv(8192).decode("utf-8")
    challenge_format = turn_into_readbly_format(challenge_raw)
    e_list = challenge_format["e"]
    y_list = client_ansewrs(r_list, e_list, s_list, n)
    auth_sussed = {"type": "auth_responce", "y": y_list}
    s.sendall(turn_into_json(auth_sussed))
    auth_decode = s.recv(8192).decode("utf-8")
    auth_decode_format = turn_into_readbly_format(auth_decode)
    print(auth_decode_format)
    if auth_decode_format["status"] == False:
        sys.exit()
    while True:
        message = input("You: ")
        if message.lower() in ("/exit", "/quit", "exit", "quit"):
            print("disconnected from server...")
            break
        s.sendall(message.encode("utf-8"))
        data = s.recv(8192)
        if not data:
            print("server is close connection ")
            break
        print(f"Server: {data.decode('utf-8')}")
