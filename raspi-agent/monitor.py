import csv
import subprocess
import time

from datetime import datetime
from pathlib import Path

# Zu überwachende Dienste
URLS = [
    "https://home.bernhard-david.de/",
    "https://stats.bernhard-david.de/",
]

TIMEOUT = 15
SLOW_THRESHOLD = 2.0

# CSV-Datei im Projektverzeichnis
CSV_FILE = Path(__file__).with_name("monitor.csv")

FIELDS = [
    "zeitpunkt",
    "url",
    "http_status",
    "antwortzeit_s",
    "ergebnis",
    "fehler",
]


def check_url(url, family):
    """Prüft eine URL gezielt über IPv4 oder IPv6."""

    start = time.perf_counter()

    status = "-"
    error = ""
    elapsed = 0.0

    family_option = "-4" if family == "IPv4" else "-6"

    command = [
        "curl",
        family_option,
        "--connect-timeout", "5",
        "--max-time", str(TIMEOUT),
        "--silent",
        "--show-error",
        "--output", "/dev/null",
        "--write-out", "%{http_code};%{time_total}",
        url,
    ]

    try:
        response = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=TIMEOUT + 2,
            check=False,
        )

        elapsed = time.perf_counter() - start
        output = response.stdout.strip()

        if ";" in output:
            http_code, curl_time = output.split(";", 1)

            if http_code.isdigit() and int(http_code) > 0:
                status = int(http_code)

            try:
                elapsed = float(curl_time)
            except ValueError:
                pass

        if response.returncode != 0:
            error = response.stderr.strip()

            if not error:
                error = f"curl beendet mit Status {response.returncode}"

    except subprocess.TimeoutExpired:
        elapsed = time.perf_counter() - start
        error = f"Zeitüberschreitung nach {TIMEOUT + 2} Sekunden"

    except Exception as exc:
        elapsed = time.perf_counter() - start
        error = str(exc)

    # Ergebnis bestimmen
    if not isinstance(status, int) or status >= 400:
        result = "FEHLER"
    elif error:
        result = "FEHLER"
    elif elapsed >= SLOW_THRESHOLD:
        result = "WARNUNG"
    else:
        result = "OK"

    return {
        "zeitpunkt": datetime.now().astimezone().isoformat(
            timespec="seconds"
        ),
        "url": f"{url} [{family}]",
        "http_status": status,
        "antwortzeit_s": round(elapsed, 3),
        "ergebnis": result,
        "fehler": error,
    }


def save_results(results):
    """Hängt Messwerte an die vorhandene CSV-Datei an."""

    new_file = (
        not CSV_FILE.exists()
        or CSV_FILE.stat().st_size == 0
    )

    with CSV_FILE.open(
        "a", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=FIELDS,
        )

        if new_file:
            writer.writeheader()

        writer.writerows(results)

def main():
    print(f"\nPrüfung: {datetime.now().astimezone()}")
    print("=" * 85)

    results = []

    # Alle Websites über IPv4 und IPv6 prüfen
    for url in URLS:
        for family in ("IPv4", "IPv6"):
            result = check_url(url, family)
            results.append(result)

    # IPv6-DNS-Fehler von einem Serverausfall unterscheiden
    for url in URLS:
        ipv4_result = next(
            r for r in results
            if r["url"] == f"{url} [IPv4]"
        )

        ipv6_result = next(
            r for r in results
            if r["url"] == f"{url} [IPv6]"
        )

        ipv4_ok = (
            isinstance(ipv4_result["http_status"], int)
            and ipv4_result["http_status"] < 400
            and not ipv4_result["fehler"]
        )

        ipv6_error = ipv6_result["fehler"].lower()

        dns_error = (
            "resolv" in ipv6_error
            or "resolve" in ipv6_error
        )

        if ipv4_ok and dns_error:
            ipv6_result["ergebnis"] = "WARNUNG"
            ipv6_result["fehler"] = (
                "IPv6-DNS gestört; "
                "Dienst über IPv4 erreichbar"
            )

    # Ergebnisse ausgeben
    for result in results:
        print(
            f"{result['ergebnis']:8} "
            f"{result['antwortzeit_s']:7.3f} s  "
            f"HTTP {result['http_status']}  "
            f"{result['url']}"
        )

        if result["fehler"]:
            print(f"         Hinweis: {result['fehler']}")

    # Messwerte anhängen
    save_results(results)

    print("=" * 85)
    print(f"Messwerte gespeichert: {CSV_FILE}")

if __name__ == "__main__":
    main()
