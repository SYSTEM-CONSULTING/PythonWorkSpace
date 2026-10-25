import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean

CSV_FILE = Path(__file__).with_name("monitor.csv")

SLOW_THRESHOLD = 2.0
MAX_MEASUREMENTS = 5

CURRENT_PROTOCOLS = ("[IPv4]", "[IPv6]")


def get_response_time(row):
    """Liefert eine gültige Antwortzeit oder None."""
    try:
        value = float(row["antwortzeit_s"])
        if value >= 0:
            return value
    except (ValueError, TypeError, KeyError):
        pass

    return None


def analyze_service(url, rows):
    recent = rows[-MAX_MEASUREMENTS:]

    valid_rows = [
        row for row in recent
        if get_response_time(row) is not None
        and row.get("ergebnis") != "FEHLER"
    ]

    times = [get_response_time(row) for row in valid_rows]

    errors = sum(
        row.get("ergebnis") == "FEHLER"
        for row in recent
    )

    slow_count = sum(
        value >= SLOW_THRESHOLD
        for value in times
    )

    latest = recent[-1] if recent else None

    current = (
        get_response_time(latest)
        if latest is not None
        and latest.get("ergebnis") != "FEHLER"
        else None
    )

    print(f"\nDienst: {url}")
    print(f"Messungen insgesamt: {len(rows)}")
    print(f"Ausgewertete Messungen: {len(recent)}")

    if current is not None:
        print(f"Aktuelle Antwortzeit: {current:.3f} Sekunden")

    if times:
        print(f"Kurzzeitmittel: {mean(times):.3f} Sekunden")
    else:
        print("Kurzzeitmittel: nicht verfügbar")

    print(f"Langsame Antworten: {slow_count}/{len(times)}")
    print(f"Fehler: {errors}/{len(recent)}")

    if errors:
        status = "FEHLER"
        print("BEWERTUNG: Fehler in den letzten Messungen.")
    elif not times:
        status = "UNBEKANNT"
        print("BEWERTUNG: Keine gültigen Messwerte.")
    elif slow_count >= 3:
        status = "LANGSAM"
        print("BEWERTUNG: Wiederholt langsame Antworten.")
    elif slow_count:
        status = "WARNUNG"
        print("BEWERTUNG: Einzelne langsame Antworten.")
    else:
        status = "OK"
        print("BEWERTUNG: Aktuell unauffällig.")

    return status


def main():
    if not CSV_FILE.exists():
        print("Keine Messwertdatei gefunden.")
        return

    measurements = defaultdict(list)

    with CSV_FILE.open(
        "r", newline="", encoding="utf-8"
    ) as file:
        reader = csv.DictReader(file)

        required_columns = {
            "url",
            "antwortzeit_s",
            "ergebnis",
        }

        if not reader.fieldnames or not required_columns.issubset(
            reader.fieldnames
        ):
            print("Fehler: Unerwartetes CSV-Format.")
            return

        for row in reader:
            measurements[row["url"]].append(row)

    print("\nRASPI-AGENT: MESSWERTANALYSE")
    print("=" * 70)

    statuses = {}
    historical = []

    for url, rows in measurements.items():
        status = analyze_service(url, rows)

        if any(protocol in url for protocol in CURRENT_PROTOCOLS):
            statuses[url] = status
        else:
            historical.append((url, status))

    print("\n\nRASPI-AGENT: GESAMTSTATUS")
    print("=" * 70)

    if statuses:
        for url, status in statuses.items():
            print(f"{url}: {status}")
    else:
        print("Keine getrennten IPv4-/IPv6-Messreihen gefunden.")

    print("\nHistorische Messreihen ohne Protokolltrennung:")

    if historical:
        for url, status in historical:
            print(f"{url}: {status} (historisch)")
    else:
        print("Keine älteren Messreihen vorhanden.")

    if not statuses:
        overall = "UNBEKANNT"
    elif any(status == "FEHLER" for status in statuses.values()):
        overall = "FEHLER"
    elif any(status == "UNBEKANNT" for status in statuses.values()):
        overall = "UNVOLLSTÄNDIG"
    elif any(
        status in ("LANGSAM", "WARNUNG")
        for status in statuses.values()
    ):
        overall = "WARNUNG"
    else:
        overall = "UNAUFFÄLLIG"

    print(f"\nAKTUELLER GESAMTZUSTAND: {overall}")
    print("\nAnalyse abgeschlossen.")


if __name__ == "__main__":
    main()

