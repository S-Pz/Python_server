import socket
import os 

def list_files(directory):
    # Função para listar os arquivos e diretórios em um diretório específico
    print(directory)
    entries = os.listdir(directory)
    links = []
    for entry in entries:
        entry_path = os.path.join(directory, entry)
        if os.path.isfile(entry_path):
            # Se for um arquivo, cria um link HTML para o arquivo
            link = f'<a href="{entry}">{entry}</a>'
            links.append(link)
        elif os.path.isdir(entry_path):
            # Se for um diretório, cria um link HTML para o diretório
            link = f'<a href="{entry}/">{entry}/</a>'
            links.append(link)
    return "<br>".join(links)

def handle_Client(client_socket, dir):
    # Função para lidar com a solicitação de um cliente

    msg = client_socket.recv(1024).decode()
    print(msg)
    
    parts = msg.split(" ")
    path = parts[1]

    if path == "/HEADER":
        # Se o caminho solicitado for "/HEADER", retorna uma resposta HTTP com os cabeçalhos
        response = 'HTTP/1.1 200 OK\r\n'
        response += 'Content-Type: text/html\r\n'
        response += '\r\n'
        response += msg
        client_socket.send(response.encode())

    if os.path.isdir(dir + path):
        # Se o caminho for um diretório, envia a lista de arquivos e diretórios como resposta HTTP
        client_socket.send(b"HTTP/1.1 200 OK\r\n")
        client_socket.send(b"Content-Type: text/html\r\n")
        client_socket.send(b"\r\n")
        client_socket.send(list_files(dir + path).encode())
        client_socket.send(b"\r\n")

    if os.path.isfile(dir+path):
        # Se o caminho for um arquivo, lê o conteúdo do arquivo e envia como resposta HTTP
        with open(dir + path, 'rb') as file:
            content = file.read()
            
        response_headers = f'HTTP/1.0 200 OK\nContent-Disposition: inline; attachment; filename={path}\n'
        print("Response Answer", response_headers)
        
        response_headers += 'Content-Length: {}\n'.format(len(content))
        response = response_headers.encode() + b'\n' + content
        client_socket.send(response)

    client_socket.close()

def start_Server(Host, Port, dir):
    # Função para iniciar o servidor

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind((Host, Port))
        server_socket.listen(1)
        
        print("Starting connection")
        
        while True:
            client_socket, client_adress = server_socket.accept()
            handle_Client(client_socket, dir)
        server_socket.close()
    
    except:
        print("error")
        server_socket.close()

if __name__ == '__main__':
    dir = '/home'  # Diretório raiz do servidor
    start_Server('0.0.0.0', 9999, dir)  # Inicia o servidor na porta 9999
