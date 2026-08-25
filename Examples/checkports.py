import socket

# Öffentliche IP deiner FritzBox hier eintragen (oder DynDNS-Adresse, z.B. dahier.dynv6.net)
HOSTS = ["dahier.dynv6.net","fritz.box","web.de"]


# List of Ports, die geprüft werden sollen (beliebig erweiterbar)
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
for host in HOSTS:
    print(f"Prüfe Ports auf {host}..")
    for port in PORTS:
        if check_port(host, port):
            print(f"✅ Port {port} ist OFFEN")
        else:
            print(f"❌ Port {port} ist GESCHLOSSEN")
    print()