# Prüfprotokoll – 07.10.2026

- Python: Syntaxprüfung erfolgreich; sieben automatisierte Tests erfolgreich.
- Live-Bericht mit C24-Produktseite, C24-App-Store und Finextra: Exit-Code 0, alle drei Quellen `ok`, JSON und Markdown erzeugt. Ein Beispiel liegt unter `examples/`; es ist kein aktueller Gesamtreport.
- Öffentliche Quellen wurden einzeln live geprüft. Ergebnisse stehen in `live-source-check.json`; Reddit-Kommentarfeeds wurden dabei nicht separat geprüft. Die App-Abfrage wurde danach um den alternativen Apple-Sortierparameter ergänzt: N26, Revolut, comdirect und Tomorrow lieferten darüber jeweils 50 Bewertungen.
- Apple liefert für manche Apps gültige, aber leere Bewertungsfeeds. Versionshinweise werden dann trotzdem abgefragt. Ein erfolgreicher Abruf bedeutet nicht, dass Bewertungen verfügbar waren.
- Reddit war abhängig vom einzelnen Abruf erreichbar oder lieferte Verbindungsabbrüche. Finanz-Szene ebenfalls aus dieser Umgebung nicht erreichbar. Der Monitor protokolliert diese Lücken.
- Trade-Republic-Produktseite: HTTP 404; comdirect-Produktseite: HTTP 401; Finanztip: Redirect-/404-Probleme; bunq Status: zu wenig Inhalt. Ersatz-URLs/Zugänge müssen bei diesen Quellen überprüft werden.
- BankingHub: erwarteter RSS-Feed war HTML; auf Website-Änderungen umgestellt. Finanzfluss: öffentliche Website als Ersatz, keine vollständige Community-Abdeckung. mydealz: Suchseite statt nicht auffindbarem RSS.
- YouTube, X sowie Anbieter für Google Play, Trustpilot, LinkedIn und Allestörungen: vorbereitet, aber keine Zugangsdaten vorhanden; nicht live verifiziert.
- Windows-Aufgabenplanung und PowerShell-Wrapper konnten in der Linux-Testumgebung nicht ausgeführt werden. Python 3.10+ ist Voraussetzung auf dem Zielrechner.
- Keine Zugangsdaten, persönlichen Zustandsdateien oder installierten Zeitpläne im ZIP. Die Beispielberichte enthalten öffentliche Inhalte und sind als untrusted zu behandeln.

## Erweiterung: stündlicher Scan / kurzer KI-Bericht

Zwölf Tests bestanden. Neu geprüft: gewöhnlicher Support löst keinen KI-Aufruf aus; kritische Regel-Auswahl verlangt aktive offizielle Hinweise oder mehrere Quellen; Modellantworten mit ungültigen Indizes werden verworfen; Kurzbericht-Limit und Quellenlinks; zweite Automation am selben Tag bleibt still und bezahlt keine zweite Tageszusammenfassung. Anthropic-Antworten wurden simuliert: kein echter API-Schlüssel vorhanden und kein bezahlter Modellaufruf ausgeführt. Der frühere Live-Beispielbericht zeigt noch das ausführliche Vorformat; aktuelle Kurzberichte sind auf fünf Punkte begrenzt.
