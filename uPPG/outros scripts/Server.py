import socket
import random
#HOST E PORTA
#myhost = '127.0.0.1' 
myhost = '192.168.0.106'
myport = 3003 

#criar server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((myhost, myport))
        server.listen(5)

        #config conexões
        conexao, endereco = server.accept()
        with conexao:
                print('[*] servidor conectado por', endereco)
                while True:
                        data = conexao.recv(1024)
                        if data == b'y':
                                randnum = random.randrange(100)
                                byt = bytes([randnum])
                                print(byt)
                                conexao.send(byt)
                        else: break
                        if not data: break
                        
      
