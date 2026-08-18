import pandas as pd

data = {
    "Name": ["Anna", "Ben", "Clara", "David"],
    "Alter": [28, 34, 29, 42],
    "Stadt": ["Berlin", "München", "Hamburg", "Berlin"]
}

df = pd.DataFrame(data)
print(df)

# Gruppieren und Mittelwert
print("\nØ Alter je Stadt:")
print(df.groupby("Stadt")["Alter"].mean())
