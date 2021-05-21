import os
from socket import *
from os import walk, path
serverPort = 12000
#Cria o Socket TCP (SOCK_STREAM) para rede IPv4 (AF_INET)
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
#Socket fica ouvindo conexoes. O valor 1 indica que uma conexao pode ficar na fila
serverSocket.listen(1)

print("Servidor pronto para receber mensagens. Digite Ctrl+C para terminar.")

userfile = open('users.txt', 'r')
users = userfile.readlines()
for i in range(len(users)):
    users[i] = users[i].replace('\n','')
userfile.close()

listaArquivos = os.listdir("pta-server/files")

def atorizacao (user):
    if user in users:
        return True
    return False

def msg_ok (msg):
    return msg + ' OK'

def msg_nok (msg):
    return msg + ' NOK'

conect = False

while 1:
    try:
        #Cria um socket para tratar a conexao do cliente
        if not conect:
            connectionSocket, addr = serverSocket.accept()
        msg = connectionSocket.recv(1024).decode().split()
        if conect:
            if msg[1] == 'TERM':
                conect = False
                message = msg_ok(msg[0])
            elif msg[1] == 'PEGA':
                if msg[2] in listaArquivos:
                    arquivo = open('files/'+msg[2]).read()
                    size = path.getsize('files/'+msg[2])
                    message = '%s ARQ %d %s' % (msg[0],size,arquivo)
                else:
                    message = msg_nok(msg[2])
            elif msg[1] == 'LIST':
                try:
                    qtdArquivos = len(listaArquivos)
                    nomeArquivos = ", ".join(listaArquivos)
                    message =  '%s ARQ %d %s' % (msg[0],qtdArquivos,nomeArquivos)
                except:
                    message = msg_nok(msg[0])



        else:
            if msg[1] == 'CUMP' and atorizacao(msg[2]):#verifica se CUMP é a mensagem inicial e seo client está na lista
                conect = True
                message = msg_ok(msg[0])
            else:
                message = msg_nok(msg[0])
        connectionSocket.send(message.encode('ascii'))
    except(KeyboardInterrupt, SystemExit):
            break

serverSocket.shutdown(SHUT_RDWR)
serverSocket.close()