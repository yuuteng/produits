import json
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('127.0.0.1', 1919))

while True:
    command = input("--search=")

    # eg: 'published:true'
    if command == "\'published:true\'":
        s.send(b'publish')
        response = s.recv(1024)
        json_response = json.loads(response.decode('utf-8'))
        print(json_response)

    # eg: ’id:545b4e3dfaee4c10def3db24’
    elif 'id:' in command:
        s.send(command.encode('utf-8'))
        response = s.recv(1024)
        json_response = json.loads(response.decode('utf-8'))
        print(json_response)
    # eg: 'exit'
    elif command == "\'exit\'":
        break
    else:
        print("Input Wrong")

s.send(b'exit')
s.close()

