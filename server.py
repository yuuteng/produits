import json
import socket
import threading


def tcplink(sock, addr):
    # print('Accept new connection from %s:%s...' % addr)

    # read json file
    with open("./products.json", 'r', encoding='utf-8') as json_file:
        dict_products = json.load(json_file)

    while True:
        data = sock.recv(1024)
        if data.decode('utf-8') == 'publish':
            str_products = json.dumps(dict_products)
            sock.send(str_products.encode('utf-8'))

        elif 'id:' in data.decode('utf-8'):
            id_product = data.decode('utf-8')[4:-1]
            print("id is " + id_product)
            flag = False
            for item in dict_products.items():
                print("item is " + item[1]['id'])
                if item[1]['id'] == id_product:
                    print("success")
                    str_item = json.dumps(item)
                    flag = True
                    sock.send(str_item.encode('utf-8'))
            if flag == False:
                sock.send(b'This id is not exist')
                continue

        if not data or data.decode('utf-8') == 'exit':
            break

    sock.close()
    # print('Connection from %s:%s closed.' % addr)



# TCP 1919
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(('127.0.0.1', 1919))
s.listen(5)
# print('Waiting for connection...')

while True:
    sock, addr = s.accept()
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()


