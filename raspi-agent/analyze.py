import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean

CSV_FILE = Path(__file__).with_name("monitor.csv")

SLOW_THRESHOLD = 2.0
MAX_MEASUREMENTS = 5


def main():
    measurements = defaultdict(list)

    if not CSV_FILE.exists():
        print("Keine Messwertdatei gefunden.")
        return

    with CSV_FILE.open(
        "r", newline="", encoding="utf-8"
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            measurements[row["url"]].append(row)

    print("\nRASPI-AGENT: MESSWERTANALYSE")
    print("=" * 65)

    for url, rows in measurements.items():
        recent = rows[-MAX_MEASUREMENTS:]

        times = [
            float(row["antwortzeit_s"])
            for row in recent
        ]

        slow_count = sum(
            t >= SLOW_THRESHOLD for t in times
        )

        errors = sum(
            row["ergebnis"] == "FEHLER"
            for row in recent
        )

        print(f"\nDienst: {url}")
        print(f"Messungen insgesamt: {len(rows)}")
        print(f"Ausgewertete Messungen: {len(recent)}")
        print(f"Mittlere Antwortzeit: {mean(times):.2f} Sekunden")
        print(f"Langsame Antworten: {slow_count}/{len(recent)}")
        print(f"Fehler: {errors}/{len(recent)}")

        if errors:
            print("BEWERTUNG: Fehler erkannt.")
        elif slow_count >= 3:
            print("BEWERTUNG: Wiederholt langsame Antworten.")
        elif slow_count:
            print("BEWERTUNG: Einzelne langsame Antworten.")
        else:
            print("BEWERTUNG: Unauffällig.")

    print("\nAnalyse abgeschlossen.")


if __name__ == "__main__":
    main()
