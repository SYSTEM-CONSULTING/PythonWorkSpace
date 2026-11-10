import unittest

from analyze import analyze_service


class TestAnalyzeService(unittest.TestCase):

    def test_all_measurements_ok(self):

        rows = [
            {"antwortzeit_s": "0.05", "ergebnis": "OK"},
            {"antwortzeit_s": "0.06", "ergebnis": "OK"},
            {"antwortzeit_s": "0.04", "ergebnis": "OK"},
            {"antwortzeit_s": "0.05", "ergebnis": "OK"},
            {"antwortzeit_s": "0.03", "ergebnis": "OK"},
        ]

        status = analyze_service("TEST", rows)

        self.assertEqual(status, "OK")


    def test_earlier_error_latest_ok(self):

        rows = [
            {"antwortzeit_s": "0.05", "ergebnis": "OK"},
            {"antwortzeit_s": "", "ergebnis": "FEHLER"},
            {"antwortzeit_s": "0.06", "ergebnis": "OK"},
            {"antwortzeit_s": "0.04", "ergebnis": "OK"},
            {"antwortzeit_s": "0.03", "ergebnis": "OK"},
        ]

        status = analyze_service("TEST", rows)

        self.assertEqual(status, "WARNUNG")


    def test_latest_measurement_error(self):

        rows = [
            {"antwortzeit_s": "0.05", "ergebnis": "OK"},
            {"antwortzeit_s": "0.06", "ergebnis": "OK"},
            {"antwortzeit_s": "0.04", "ergebnis": "OK"},
            {"antwortzeit_s": "0.05", "ergebnis": "OK"},
            {"antwortzeit_s": "", "ergebnis": "FEHLER"},
        ]

        status = analyze_service("TEST", rows)

        self.assertEqual(status, "FEHLER")


if __name__ == "__main__":
    unittest.main()