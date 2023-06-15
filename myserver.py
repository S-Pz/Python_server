import socket
import os 

def list_files(directory):
    print(directory)
    entries = os.listdir(directory)
    links = []
    for entry in entries:
        entry_path = os.path.join(directory, entry)
        if os.path.isfile(entry_path):
            link = f'<a href="{entry}">{entry}</a>'
            links.append(link)
        elif os.path.isdir(entry_path):
            link = f'<a href="{entry}/">{entry}/</a>'
            links.append(link)
    return "<br>".join(links)

def handle_Client(client_socket, dir):

    msg = client_socket.recv(1024).decode()
    print(msg)
    
    parts = msg.split(" ")
    path = parts[1]

    if path == "/HEADER":
        client_socket.send(b"HTTP/1.1 200 OK\r\n")
        client_socket.send(b"Content-Type: text/html\r\n")
        client_socket.send(b"\r\n")
        client_socket.send(b"<html><body><h1>Hello World!</h1></body></html>")
        client_socket.send(b"\r\n")

    if os.path.isdir(dir + path):
        client_socket.send(b"HTTP/1.1 200 OK\r\n")
        client_socket.send(b"Content-Type: text/html\r\n")
        client_socket.send(b"\r\n")
        client_socket.send(list_files(dir + path).encode())
        client_socket.send(b"\r\n")

    if os.path.isfile(dir+path):

       # response_headers = f'HTTP/1.0 200 OK\nContent-Disposition: attachment; filename={file}\n'

        #with open(path, 'rb') as file:
           # content = file.read()

       # response_headers += 'Content-Length: {}\n'.format(len(content))
        #response = response_headers.encode() + b'\n' + content
        #client_socket.send(response)

        with open(dir + path, "rb") as file:
            content = file.read()
        header = "HTTP/1.1 200 OK " + "Content-Type: application/octet-stream"
        print(header)
        client_socket.send(header.encode() + content)

    client_socket.close()

def start_Server(Host, Port, dir):

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind((Host, Port))
        server_socket.listen(1)
        
        print("Starting conection")
        
        while True:
            client_socket, client_adress = server_socket.accept()
            handle_Client(client_socket, dir)
        server_socket.close()

    except:
        print ("error")
        server_socket.close()

if __name__ == '__main__':
    
    dir = '/home/saviofrancisco'
    start_Server('0.0.0.0', 9644, dir)
   