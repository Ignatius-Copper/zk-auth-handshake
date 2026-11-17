import secrets
import socket
import threading

from utils import (
    generat_numbers,
    turn_into_json,
    turn_into_readbly_format,
)

rooms = {"room1": []}
usersdb = {}


def server(t: int):
    e_list = []
    for i in range(t):
        e = secrets.randbelow(2)
        e_list.append(e)
    return e_list  # conn.sendall(e_list)


def verifacation(y_list: list, e_list: list, x_list: list, n, v_list: list):
    if not v_list or not (
        len(y_list) == len(e_list) == len(x_list) == len(v_list) == t
    ):
        return False

    for y, e, x, v in zip(y_list, e_list, x_list, v_list):
        if (
            pow(y, 2, n) == pow(x, 1, n)
            and e == 0
            or e == 1
            and pow(y, 2, n) == pow(x * v, 1, n)
        ):
            print("Check... status: OK")
        else:
            print("Check... status: Nope")
            return False
    return True


n = generat_numbers()
t = secrets.SystemRandom().randint(4, 20)


def handle_client(conn, addr):
    print(f"[New connection ] {addr} connected")
    x_list = []
    e_list = []
    name = None
    verif = False
    with conn:
        while True:
            data = conn.recv(8192).decode("utf-8")
            if verif == False:
                if not data:
                    break
                data_format = turn_into_readbly_format(data)
                if data_format["type"] == "get_params":
                    t_n = {"t": t, "n": n}
                    t_n_json = turn_into_json(t_n)
                    conn.sendall(t_n_json)
                elif data_format["type"] == "registrate":
                    name = data_format["username"]
                    usersdb["username"] = name
                    v = data_format["v"]
                    usersdb[name] = v
                    status = {"status": "Ok"}
                    status_json = turn_into_json(status)
                    conn.sendall(status_json)
                elif data_format["type"] == "auth_init":
                    x_list = data_format["x"]
                    e_list = server(t)
                    e = {"e": e_list}
                    e_list_json = turn_into_json(e)
                    conn.sendall(e_list_json)
                elif data_format["type"] == "auth_responce":
                    y_list = data_format["y"]
                    verif = verifacation(
                        y_list,
                        e_list,
                        x_list,
                        n,
                        usersdb.get(name),
                    )
                    if verif == False:
                        break
                    status = {"status": verif}
                    status_json = turn_into_json(status)
                    conn.sendall(status_json)

            else:
                message = data
                if not data:
                    break
                if message == "/users":
                    conn.sendall(
                        b"rooms3"
                    )  # this messege only for checking work server
                elif message == "/all_rooms":
                    conn.sendall(b"rooms")  # this messege only for checking work server
                else:
                    conn.sendall(message.encode("utf-8"))
                print(f"[{addr}]{message}".encode())
    print(f"[turn off] {addr}")


def start_server(host="127.0.0.1", port=65432):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"[turn on ] Server is working {host}:{port}")
    while True:
        conn, addr = server.accept()
        tread = threading.Thread(target=handle_client, args=(conn, addr))
        tread.start()
        print(f"active connection {threading.active_count() - 1}")


if __name__ == "__main__":
    start_server()
