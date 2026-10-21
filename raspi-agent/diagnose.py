import socket
import ssl
import time
from urllib.parse import urlparse

URL = "https://stats.bernhard-david.de/"
TIMEOUT = 20


def diagnose(url):
    parsed = urlparse(url)
    host = parsed.hostname
    port = parsed.port or 443

    print(f"\nDiagnose: {url}")
    print("=" * 60)

    start = time.perf_counter()

    # 1. DNS-Auflösung
    try:
        addresses = socket.getaddrinfo(
            host, port, type=socket.SOCK_STREAM
        )
        dns_time = time.perf_counter() - start

        print(f"DNS-Auflösung:       {dns_time:.3f} s")
        print("IP-Adressen:")

        for address in addresses:
            print(f"  {address[4][0]}")

    except Exception as exc:
        print(f"DNS-FEHLER: {exc}")
        return

    # 2. TCP-Verbindung
    tcp_start = time.perf_counter()

    try:
        raw_socket = socket.create_connection(
            (host, port), timeout=TIMEOUT
        )
        tcp_time = time.perf_counter() - tcp_start

        print(f"TCP-Verbindung:      {tcp_time:.3f} s")

    except Exception as exc:
        print(f"TCP-FEHLER: {exc}")
        return

    # 3. TLS-Handshake
    tls_start = time.perf_counter()

    try:
        context = ssl.create_default_context()

        with context.wrap_socket(
            raw_socket, server_hostname=host
        ) as tls_socket:

            tls_time = time.perf_counter() - tls_start
            print(f"TLS-Handshake:       {tls_time:.3f} s")

            # 4. HTTP-Anfrage und Antwortheader
            path = parsed.path or "/"

            if parsed.query:
                path += "?" + parsed.query

            request = (
                f"GET {path} HTTP/1.1\r\n"
                f"Host: {host}\r\n"
                "User-Agent: RaspiAgent/0.1\r\n"
                "Connection: close\r\n"
                "\r\n"
            )

            http_start = time.perf_counter()
            tls_socket.settimeout(TIMEOUT)
            tls_socket.sendall(request.encode("ascii"))

            response = b""

            while b"\r\n\r\n" not in response:
                chunk = tls_socket.recv(4096)

                if not chunk:
                    break

                response += chunk

            http_time = time.perf_counter() - http_start

            first_line = response.split(b"\r\n", 1)[0]

            print(f"HTTP-Antwortheader:  {http_time:.3f} s")
            print(f"Statuszeile:         {first_line.decode('latin-1')}")
            print(
                f"Gesamtdauer:         "
                f"{time.perf_counter() - start:.3f} s"
            )

    except Exception as exc:
        raw_socket.close()
        print(f"TLS-/HTTP-FEHLER: {exc}")


if __name__ == "__main__":
    diagnose(URL)
import socket
import ssl
import time
from urllib.parse import urlparse

URL = "https://stats.bernhard-david.de/"
TIMEOUT = 10


def diagnose_family(url, family, label):
    parsed = urlparse(url)
    host = parsed.hostname
    port = parsed.port or 443

    print(f"\nDiagnose {label}: {url}")
    print("=" * 60)

    total_start = time.perf_counter()

    # 1. DNS-Auflösung für genau eine Adressfamilie
    dns_start = time.perf_counter()

    try:
        addresses = socket.getaddrinfo(
            host,
            port,
            family=family,
            type=socket.SOCK_STREAM
        )

        dns_time = time.perf_counter() - dns_start
        print(f"DNS-Auflösung:       {dns_time:.3f} s")

    except socket.gaierror as exc:
        dns_time = time.perf_counter() - dns_start
        print(f"DNS-FEHLER:          {exc}")
        print(f"DNS-Dauer:           {dns_time:.3f} s")
        return

    if not addresses:
        print("Keine passenden IP-Adressen gefunden.")
        return

    # Doppelte Adressen vermeiden
    unique_addresses = []
    seen = set()

    for address in addresses:
        key = address[4]

        if key not in seen:
            seen.add(key)
            unique_addresses.append(address)

    for address in unique_addresses:
        ip = address[4][0]
        print(f"IP-Adresse:          {ip}")

    # 2. TCP-Verbindung direkt zur ermittelten IP
    for address in unique_addresses:
        ip = address[4][0]
        raw_socket = socket.socket(
            address[0], address[1], address[2]
        )
        raw_socket.settimeout(TIMEOUT)

        try:
            tcp_start = time.perf_counter()
            raw_socket.connect(address[4])
            tcp_time = time.perf_counter() - tcp_start

            print(f"TCP-Verbindung:      {tcp_time:.3f} s")

            # 3. TLS-Handshake
            context = ssl.create_default_context()
            tls_start = time.perf_counter()

            with context.wrap_socket(
                raw_socket, server_hostname=host
            ) as tls_socket:

                raw_socket = None
                tls_time = time.perf_counter() - tls_start

                print(f"TLS-Handshake:       {tls_time:.3f} s")

                # 4. HTTP-Anfrage und Antwortheader
                path = parsed.path or "/"

                if parsed.query:
                    path += "?" + parsed.query

                request = (
                    f"GET {path} HTTP/1.1\r\n"
                    f"Host: {host}\r\n"
                    "User-Agent: RaspiAgent/0.1\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                )

                http_start = time.perf_counter()
                tls_socket.sendall(request.encode("ascii"))

                response = b""

                while b"\r\n\r\n" not in response:
                    chunk = tls_socket.recv(4096)

                    if not chunk:
                        break

                    response += chunk

                http_time = time.perf_counter() - http_start

                first_line = response.split(b"\r\n", 1)[0]

                print(f"HTTP-Antwortheader:  {http_time:.3f} s")
                print(
                    f"Statuszeile:         "
                    f"{first_line.decode('latin-1')}"
                )
                print(
                    f"Gesamtdauer:         "
                    f"{time.perf_counter() - total_start:.3f} s"
                )

                return

        except Exception as exc:
            print(f"VERBINDUNGSFEHLER:   {exc}")

        finally:
            if raw_socket is not None:
                raw_socket.close()


if __name__ == "__main__":
    diagnose_family(URL, socket.AF_INET, "IPv4")
    diagnose_family(URL, socket.AF_INET6, "IPv6")
