import socket
import os 

def start_Server(Host,Port):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((Host, Port))
        s.listen(1)
        
        #print("Starting conection")

        con,addr = s.accept()

        print(s.accept())
        #print("Connect",addr)

        while True:
            msg = con.recv(1024)
            print(con,'\n\n')
            print(msg.decode())
        s.close()
    except Exception as error:

        print ("error")
        s.close()

if __name__ == '__main__':
 
    start_Server('0.0.0.0', 9999)