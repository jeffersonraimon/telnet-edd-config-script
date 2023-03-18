import telnetlib
import socket
import time
import getpass


####################### FUNCTIONS
   

def telnet():  ##LOGIN IN DEVICE WITH TELNET
    tn = telnetlib.Telnet(HOST,23)
    tn.read_until(b"login: ")
    tn.write(user.encode('utf-8') + b"\n")
    tn.read_until(b"Password: ")
    tn.write(password.encode('utf-8') + b"\n")
    time.sleep(2)

    ####### config / CHANGE SNTP SERVER AND SET CLOCK TIMEZONE
    tn.write(b"config\n")
    time.sleep(1)
    tn.write(b"sntp client\n")
    time.sleep(1)
    tn.write(b"sntp server X.X.X.X\n")
    time.sleep(1)
    tn.write(b"clock timezone BRA -3\n")
    time.sleep(1)
    tn.write(b"exit\n")
    time.sleep(1)
    tn.write(b"copy running-config startup-config\n") #SAVE CONFIGS
    time.sleep(2)  
    tn.close()

def testeTelnet(ip):
    IP = ip 
    PORT = 23 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    sock.settimeout(3)  
    result = sock.connect_ex((IP, PORT))  
    if result == 0:
        print(f"{HOST} com conexao telnet")
    else:
        print(f"{HOST} sem conexao telnet")
    sock.close() 
    return result

def testeLogin(user,password,host):

    tn = telnetlib.Telnet(host,23)

    tn.read_until(b"login: ")
    tn.write(user.encode('utf-8') + b"\n")

    tn.read_until(b"Password: ")
    tn.write(password.encode('utf-8') + b"\n")
    login_result = tn.read_until(b"Login incorrect",timeout=2)
    if b"Login incorrect" in login_result:
        print("Usuário ou senha incorretos.")
        return False
    else:
        print("")
        return True
    
############################################# SCRIPT

hosts = [
 "A.B.C.D","A.B.C.D","x"
]

user = input("Digite seu usuario: ")
password = getpass.getpass("Digite sua senha: ")


for host in hosts:
    if host != "x":

        ip = host

        HOST = host

        if testeTelnet(HOST) == 0:

            program = testeLogin(user,password,HOST)

            while ip != "x":

                if program == True:
                
                    print(f"Aplicando config em {ip}")

                    telnet()

                    print(f"{HOST} config ok")

                    break
                else:
                    print("Inicie novamente o programa com as credenciais corretas")
                    break
        else:
            continue
    else:
        break

print ("Fim")