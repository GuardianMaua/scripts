import socket
import threading
import queue

# Definir limite de threads simultâneas
THREAD_LIMIT = 20

# Fila para armazenar portas a serem escaneadas
port_queue = queue.Queue()

# Lista para armazenar portas abertas
open_ports = []

# Função para escanear uma única porta
def scan_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Timeout de 1 segundo
        result = sock.connect_ex((target, port))
        if result == 0:
            print(f"[+] Porta {port} está ABERTA")
            open_ports.append(port)  # Adiciona à lista de portas abertas
        sock.close()
    except Exception:
        pass

# Função para criar e gerenciar as threads
def port_scanner(target, ports):
    total_ports = len(ports)  # Total de portas a escanear
    scanned_ports = 0  # Contador de portas escaneadas
    progress_threshold = 10  # Percentual de progresso para printar
    progress_next = progress_threshold  # Próxima marca de progresso

    print(f"[*] Escaneando {target} em busca de portas abertas...\n")

    # Preencher a fila com as portas a serem escaneadas
    for port in ports:
        port_queue.put(port)

    # Criar lista de threads
    threads = []
    for _ in range(min(THREAD_LIMIT, total_ports)):  # Criar até 20 threads
        thread = threading.Thread(target=worker, args=(target,))
        threads.append(thread)
        thread.start()

    while scanned_ports < total_ports:
        scanned_ports = total_ports - port_queue.qsize()  # Atualiza progresso
        progress = (scanned_ports / total_ports) * 100
        if progress >= progress_next:
            print(f"[*] Progresso: {int(progress)}% concluído...")
            progress_next += progress_threshold  # Atualizar próximo limite

    for thread in threads:
        thread.join()  # Esperar todas as threads finalizarem

    # Exibir e salvar portas abertas ao final do escaneamento
    if open_ports:
        print("\n[+] Escaneamento concluído! Portas abertas encontradas:")
        for port in open_ports:
            print(f"    - Porta {port} está ABERTA")

        # Salvar no arquivo
        with open("portas_abertas.txt", "w") as f:
            f.write(f"Portas abertas em {target}:\n")
            for port in open_ports:
                f.write(f"Porta {port} está ABERTA\n")
        
        print("\n[💾] As portas abertas foram salvas em 'portas_abertas.txt'!")
    else:
        print("\n[-] Nenhuma porta aberta foi encontrada.")

# Função worker para consumir a fila e escanear portas
def worker(target):
    while not port_queue.empty():
        port = port_queue.get()
        scan_port(target, port)
        port_queue.task_done()

# Entrada do usuário
target_ip = input("Digite o IP alvo: ")
port_range = range(1, 1025)  # Escaneia portas de 1 a 1024

# Executar o scanner
port_scanner(target_ip, port_range)
