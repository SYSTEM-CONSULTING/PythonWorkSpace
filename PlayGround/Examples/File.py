#!/usr/bin/env python3
# -*- coding: utf-8 -*-
MyDat = "ING.csv"

# Textdatei zeilenweise lesen
with open(MyDat, "r") as f:
    try:
        for zeile in f:
              print(zeile.strip())
    except:
         print("Fehler beim Lesen der Datei")
         
         


