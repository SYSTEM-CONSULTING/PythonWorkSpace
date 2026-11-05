
from analyze import analyze_service

print("\nTEST 1: Alle Messungen OK")

rows = [
    {"antwortzeit_s": "0.05", "ergebnis": "OK"},
    {"antwortzeit_s": "0.06", "ergebnis": "OK"},
    {"antwortzeit_s": "0.04", "ergebnis": "OK"},
    {"antwortzeit_s": "0.05", "ergebnis": "OK"},
    {"antwortzeit_s": "0.03", "ergebnis": "OK"},
]
status = analyze_service("TEST", rows)
print("Erwartet: OK | Erhalten:", status)


print("\nTEST 2: Früherer Fehler, letzte Messung OK")

rows = [
    {"antwortzeit_s": "0.05", "ergebnis": "OK"},
    {"antwortzeit_s": "", "ergebnis": "FEHLER"},
    {"antwortzeit_s": "0.06", "ergebnis": "OK"},
    {"antwortzeit_s": "0.04", "ergebnis": "OK"},
    {"antwortzeit_s": "0.03", "ergebnis": "OK"},
]

status = analyze_service("TEST", rows)
print("Erwartet: WARNUNG | Erhalten:", status)

print("\nTEST 3: Letzte Messung FEHLER")

rows = [
    {"antwortzeit_s": "0.05", "ergebnis": "OK"},
    {"antwortzeit_s": "0.06", "ergebnis": "OK"},
    {"antwortzeit_s": "0.04", "ergebnis": "OK"},
    {"antwortzeit_s": "0.05", "ergebnis": "OK"},
    {"antwortzeit_s": "", "ergebnis": "FEHLER"},
]

status = analyze_service("TEST", rows)
print("Erwartet: FEHLER | Erhalten:", status)
