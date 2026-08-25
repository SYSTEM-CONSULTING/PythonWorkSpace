#!/usr/bin/env python3
import socket
# Öffentliche IP deiner FritzBox hier eintragen (oder DynDNS-Adresse, z.B. dahier.dynv6.net)
def str h:
input("enter name of host",h)
# HOST = "fritz.box"
HOST1 = "web.de"

# Ports, die geprüft werden sollen (beliebig erweiterbar)
PORTS = [22, 80, 443, 8080, 8443, 42091]

def check_port(host, port, timeout=2):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((host, port))
    except (socket.timeout, socket.error):
        return False
    else:
        return True
    finally:
        sock.close()

print(f"Prüfe Ports auf {HOST}...\n")
for port in PORTS:
    if check_port(HOST, port):
        print(f"✅ In  Port {port} ist OFFEN")
    else:
        print(f"❌ In  Port {port} ist GESCHLOSSEN")
    if check_port(HOST1, port):
        print(f"✅ Out Port {port} ist OFFEN")
    else:
        print(f"❌ Out Port {port} ist GESCHLOSSEN")
