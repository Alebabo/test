# C24 – Test mit Claude Automation

**Zuerst `CLAUDE_TEST_START.md` lesen.** Dieses ZIP ist für den Test mit einer stündlichen Claude-Aufgabe vorbereitet. Direkte Anthropic-API-Aufrufe sind deaktiviert; Claude bewertet die Übergabedatei selbst. Keinen zusätzlichen Zeitplan installieren. Die folgenden Abschnitte erklären auch den späteren Betrieb über Windows/Cron und die optionale direkte API.

Erweitertes Paket für C24, N26, Revolut, bunq, Trade Republic, DKB, ING, comdirect, Wise, Vivid und Tomorrow. Der ursprüngliche PowerShell-Reddit-Monitor bleibt enthalten. Der neue gemeinsame Einstieg ist **run-monitor.ps1** bzw. **monitor.py**.

## Schnellstart unter Windows

1. ZIP in einen dauerhaften Ordner entpacken.
2. Python **3.10 oder neuer** installieren (python.org); keine zusätzlichen Python-Pakete nötig.
3. PowerShell in diesem Ordner öffnen und einen Tageslauf starten:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run-monitor.ps1 -Mode Daily
```

4. Automatischen Lauf jede Stunde einrichten:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\install-scheduled-task.ps1
```

Die Aufgabe läuft mit normalen Benutzerrechten, während der Benutzer angemeldet ist. Der Installationsbefehl muss auf deinem Windows-PC ausgeführt werden; das Entpacken allein aktiviert keinen Zeitplan. Python muss für diesen Benutzer verfügbar sein. Überschneidende Läufe werden verhindert. Die Installation ersetzt keine vorhandene gleichnamige Aufgabe.

Entfernen des Zeitplans:

```powershell
Unregister-ScheduledTask -TaskName C24-Multisource-Monitor -Confirm:$false
```

Auf macOS/Linux oder direkt unter Windows:

```bash
python monitor.py --mode Daily
python monitor.py --mode Automation --quiet
python monitor.py --mode WatchC24
```

`Automation` berücksichtigt die Intervalle der einzelnen Quellen und erstellt ab 07:00 Uhr lokaler Zeit einen Tagesbericht. `Daily` ruft alle eingerichteten Quellen unabhängig vom Intervall ab. `WatchC24` berücksichtigt ebenfalls alle Quellen und ihre Intervalle, erzeugt aber keinen Tagesbericht. Für einen Linux-Zeitplan kann `python3 /absoluter/pfad/monitor.py --mode Automation --quiet` jede Stunde per cron ausgeführt werden.

## Enthaltene Quellen

| Quellen | Umsetzung | Einrichtung / Grenzen |
|---|---|---|
| Alle bisherigen neun Reddit-Communities | RSS, zusätzlich Kommentare der drei neuesten Beiträge pro Community | Kein Schlüssel; Reddit kann Abrufe begrenzen oder blockieren. Kommentare sind eine Stichprobe, keine Vollerfassung. |
| Apple App Store, elf Banken | Deutsche Bewertungen und Versionshinweise über Apple RSS/Lookup | App-IDs anhand von Name und Herausgeber live geprüft. Feed liefert nur die neuesten bis zu 50 Bewertungen. |
| Offizielle Produktseiten, ausgewählte Hilfecenter und Konditionenseiten | Vergleich des sichtbaren HTML-Textes | Erste Erfassung ist nur Ausgangsstand. Spätere Änderungen erzeugen Signale; Cookiebanner und wechselnde Seitenelemente können Rauschen erzeugen. |
| Finanz-Szene, Finextra | RSS | Finanz-Szene war aus der Testumgebung zeitweise nicht erreichbar. |
| BankingHub | Seitenänderungen | Der getestete Feed lieferte HTML; daher Startseite als Ersatzquelle. |
| Finanzfluss | Öffentliche Website | Kein zugänglicher Community-Feed gefunden. Private Community-Beiträge werden nicht erfasst. |
| Finanztip Forum | Feed-Erkennung | Getestete Adresse war nicht erreichbar; passende Feed-URL in der Konfiguration ergänzen. |
| mydealz | Änderung der C24-Suchseite | Keine vollständige Kommentarerfassung; Suchseite kann dynamisch sein. |
| Revolut, N26, Wise, bunq Status | Seitenänderungen | bunq lieferte zu wenig HTML und wird als Fehler gemeldet. Keine automatische semantische Bestätigung eines Ausfalls. |
| YouTube | YouTube Data API, Videosuche | `YOUTUBE_API_KEY` nötig; keine Video-Kommentare. Suche kostet API-Quota. |
| X | Recent Search API | `X_BEARER_TOKEN` und passender API-Zugang nötig; Plattformlimits gelten. |
| Google Play, Trustpilot, LinkedIn, Allestörungen | Konfigurierbarer JSON-Datenanbieter | Anbieter-Endpunkt und gegebenenfalls Token nötig. Kein öffentlicher Universalzugang wird vorausgesetzt. |

Bei Trade Republic (Produktseite), comdirect (Produktseite), Finanztip und bunq Status schlugen die Live-Abrufe fehl. Diese Einträge bleiben als sichtbare Abrufversuche enthalten; sie sind **keine bestätigte aktive Abdeckung**. Erreichbarkeit kann vom Netzwerk und Standort abhängen. JavaScript-Seiten, Zugangsschutz und private Bereiche benötigen andere autorisierte Datenzugänge. Das Skript umgeht keinen Zugangsschutz.

## Konfiguration

- `monitor-config.json`: bisherige Marken, Servicebegriffe und Uhrzeit; bleibt mit dem Original kompatibel.
- `sources-config.json`: alle zusätzlichen Anbindungen einschließlich Reddit für den gemeinsamen Bericht.
- Je Quelle: `enabled`, `intervalMinutes`, `includeAll`, optional `brand` und `ignorePatterns`.
- Quellen ohne Markenbezug werden standardmäßig ausgefiltert. Bei dedizierten Bankquellen wird die Bank als Marke ergänzt.
- Webseiten werden überwiegend stündlich geprüft. Der Scheduler startet zu jeder vollen Stunde.
- `lookbackDays: 7`: beim Abruf ältere datierte Beiträge überspringen. Der erste Lauf kann bis zu sieben Tage alte Beiträge melden.
- `retentionDays: 30`: lokale Aufbewahrung und Duplikaterkennung. Quellen ohne Datum können nach Ablauf der Aufbewahrung erneut auftauchen.
- `clusterWindowHours: 24`, `clusterAlertThreshold: 3`: Meldung bei mindestens drei Beiträgen zu Marke/Thema innerhalb des Beobachtungsfensters. Das ist ein Hinweis, kein statistisch bestätigter Trend. Themen sind einfache Schlüsselwortgruppen.

### Zugänge für YouTube und X

Temporär für einen manuellen Lauf in PowerShell:

```powershell
$env:YOUTUBE_API_KEY = 'DEIN_SCHLUESSEL'
$env:X_BEARER_TOKEN = 'DEIN_TOKEN'
.\run-monitor.ps1 -Mode Daily
```

Für geplante Läufe müssen diese Variablen im Benutzerkontext der Aufgabe verfügbar sein. Bereits laufende Prozesse übernehmen geänderte Benutzer-Umgebungsvariablen nicht automatisch; gegebenenfalls neu anmelden. Tokens nicht in die JSON-Konfiguration schreiben.

### Google Play, Trustpilot, LinkedIn und Allestörungen

Einen berechtigten Datenanbieter oder eigenen autorisierten Export-Endpunkt verwenden. Im passenden `json_provider`-Eintrag die echte HTTPS-`url` eintragen. Falls erforderlich, den Token als Benutzer-Umgebungsvariable mit dem in `tokenEnv` angegebenen Namen hinterlegen. Bei Endpunkten ohne Authentifizierung `tokenEnv` entfernen.

Erwartetes Antwortformat:

```json
{
  "items": [
    {
      "id": "provider-123",
      "title": "C24 Kundenservice",
      "text": "Inhalt einer Bewertung oder Meldung",
      "url": "https://example.org/review/123",
      "publishedAt": "2026-10-07T07:30:00Z",
      "rating": 2
    }
  ]
}
```

`itemsPath` kann etwa `data.reviews` lauten. Abweichende Felder per `fieldMap` zuordnen, z. B. `{"id":"review_id","text":"review.body","publishedAt":"created_at"}`. Standard-Authentifizierung: `Authorization: Bearer <Token>`. `authHeader` und `authPrefix` lassen sich an den Anbieter anpassen. Keine beliebige Provider-API ist ohne Anpassung automatisch kompatibel; Pagination, Quotas und die Auswahl aller gewünschten Marken müssen am Anbieter-Endpunkt eingerichtet sein. Für getrennte Endpunkte zusätzliche Quellen mit eindeutiger `id` anlegen. Kostenpflichtige Zugänge wurden nicht gebucht.

## Berichte und Meldungen

- `output/multisource-latest.json`: letzter Lauf, Quellenstatus, neue und gespeicherte Beiträge, Häufungen.
- `output/multisource-alerts-latest.json`: neue C24-Signale und neue Häufungsmeldungen.
- `output/multisource-daily-YYYY-MM-DD.json` und `.md`: JSON mit Details und sehr kurzer Markdown-Tagesbericht mit maximal fünf Punkten und Quellenlinks; Signale der letzten 24 Stunden nach erstem Beobachtungszeitpunkt.
- `.multisource-state.json`: lokale Duplikaterkennung und Seitenstände.
- `output/critical-alerts-latest.json`: kritische Meldungen des letzten Laufs.
- `output/critical-message-latest.txt`: nur vorhanden, wenn dieser Lauf kritische Meldungen erzeugt hat.
- Der Windows-Wrapper verwendet `--quiet`: Ausgabe nur bei kritischen Meldungen oder einem Tagesbericht; gewöhnliche Stundenscans bleiben still. Technische Fehler werden in den lokalen Berichten protokolliert; fatale Fehler erscheinen auf stderr.
- Ohne `--quiet` gibt es Diagnose-Zähler: `C24_ALERT_COUNT`, `CLUSTER_ALERT_COUNT`, `SOURCE_ERRORS`, `DAILY_REPORT_CREATED`. Diese Rohzähler sind keine Benachrichtigungskriterien.
- Quellenstatus: `ok`, `cached` (noch nicht wieder fällig), `error`, `needs_credentials`, `needs_configuration`, `disabled`.
- Exit-Code 0: kein Abruffehler; 1: mindestens ein Quellenfehler; 2: fataler Fehler. Fehlende Einrichtung erscheint im Bericht und ist nicht gleichbedeutend mit einem erfolgreichen Abruf.

JSON und Markdown werden lokal erstellt. Eine E-Mail-, Slack- oder Push-Zustellung ist nicht eingerichtet. Eine bestehende Claude-Automation kann die Dateien anhand der beigefügten Prompt-Vorlage auswerten. Mit `ANTHROPIC_API_KEY` nutzt der Kurzbericht die konfigurierte Anthropic-API; ohne Schlüssel gibt es eine regelbasierte Kurzfassung. Für externe Zustellung ist weiterhin eine bestehende Automation nötig.

## Stündlich still, einmal täglich kurz

Alle eingerichteten Quellen werden stündlich geprüft. Ab 07:00 Uhr lokaler Zeit entsteht einmal pro Kalendertag ein Kurzbericht mit höchstens fünf Punkten und Links. Ein stillstehender Rechner holt den Bericht beim nächsten Lauf nach. Bei fehlenden Quellen entsteht trotzdem ein Bericht mit kurzem Hinweis auf die Abdeckung. Ein manueller Tageslauf am selben Tag verwendet den bestehenden Kurzbericht; keine zweite bezahlte Zusammenfassung.

Außerhalb des Tagesberichts werden ausschließlich neue kritische Signale ausgegeben. Normale Supportbeschwerden, schlechte Bewertungen, Produktänderungen und einfache Häufungen erzeugen keine Nachricht. Kritisch sind Hinweise auf schwere laufende Ausfälle, Betrug/Sicherheitsprobleme, Verlust von Geld oder verbreitete Kontosperren. Das sind Prüfhinweise, keine bestätigten Vorfälle. Ohne KI werden nur klare aktive offizielle Statusmeldungen oder schwere Hinweise aus mindestens zwei Quellen gemeldet. Die Erkennung kann Ereignisse übersehen oder falsch einordnen.

### Modell und Kosten

Für den Claude-Test ist `ai.enabled: false`; Sonnet in Claude auswählen. Für einen späteren direkten API-Betrieb `ai.enabled: true` setzen. In `sources-config.json` unter `ai` ist dafür **`claude-sonnet-4-6`** vorbelegt. Sonnet ist nicht das günstigste Modell; für geringere Kosten lässt sich beispielsweise **`claude-haiku-4-5-20251001`** eintragen. Es gibt keinen automatischen Wechsel auf ein teureres Modell. Modellverfügbarkeit und aktuelle Preise beim Anbieter prüfen.

```powershell
$env:ANTHROPIC_API_KEY = 'DEIN_ANTHROPIC_SCHLUESSEL'
.\run-monitor.ps1 -Mode Daily
```

Für geplante Läufe den Schlüssel im Benutzerkontext dauerhaft bereitstellen. Ausgewählte öffentliche Texte werden zur Auswertung an Anthropic gesendet. Keine API-Aufrufe bei gewöhnlichen Stundenscans ohne kritische Kandidaten. Höchstens ein Aufruf pro Stunde für bis zu zwölf kritische Kandidaten und ein zusätzlicher Aufruf pro Tag für bis zu 30 Tagesbericht-Kandidaten; jeweils maximal 700 Ausgabetokens und 600 Zeichen Inhalt pro Kandidat. Keine automatischen API-Wiederholungen. Das begrenzt Verbrauch, garantiert aber keinen festen Eurobetrag. Ein erster Lauf kann ältere kritische Beiträge als neu erkennen.

Fehlt der Schlüssel oder scheitert die API, arbeitet die Regel-Auswahl weiter und dokumentiert den Grund. `ai.enabled: false` deaktiviert KI vollständig. Modellantworten können nur vorhandene Beitragsindizes auswählen; Quellenlinks werden vom Skript angefügt.

### Bereits installierten Zeitplan aktualisieren

Eine frühere 15-Minuten-Aufgabe zuerst entfernen, dann neu installieren:

```powershell
Unregister-ScheduledTask -TaskName C24-Multisource-Monitor -Confirm:$false
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\install-scheduled-task.ps1
```

## Robustheit und Sicherheit

Timeouts, Größenlimit von 5 MB, begrenzte Wiederholungen bei 429/Serverfehlern, HTTPS, lokaler Schreibschutz gegen parallele Läufe und atomarer Austausch von JSON-Dateien. Bei Quellenfehlern wird deren bisheriger Zustand erhalten; Fehler und fehlende Zugänge bleiben sichtbar. Bei einem Prozessabbruch kann eine Sperrdatei übrig bleiben: `.multisource.lock` erst löschen, nachdem sicher kein Lauf mehr aktiv ist.

Webseitenänderungen enthalten aktuellen und vorherigen Textauszug, keinen vollständigen strukturierten Diff. HTML-Skripte werden entfernt, Links aus Beiträgen werden nicht automatisch geöffnet (Ausnahme: gezielte Reddit-Kommentarfeeds auf reddit.com). Externe Inhalte bleiben untrusted. Verdächtige Anweisungstexte werden heuristisch redigiert; die Erkennung ist keine Sicherheitsgarantie. Bewertungsdaten sind nicht repräsentativ. Keine Einzelbewertung als verifizierten Vorfall behandeln.

## Prüfung

```bash
python -m unittest discover -s tests -v
```

Zwölf Tests prüfen zusätzlich stündliche Stille, einmalige Tageszusammenfassung, kritische Auswahl, Modell-Antwortvalidierung und Link-Erhalt. Tests prüfen RSS/Atom, HTML statt Feed, DTD-Ablehnung, Markenfilter, verdächtige Inhalte, Webseiten-Ausgangsstand/Änderung, Provider-Feldmapping, Duplikate, Fehlerstatus, fehlende Zugangsdaten, Häufungen und Prozesssperre. Live-Prüfungen sind in `VALIDATION.md` dokumentiert. Windows-Aufgabenplanung wurde hier nicht ausgeführt.

## Ursprünglicher Reddit-Monitor

`get-finanzien-posts.ps1` und die ursprüngliche Konfiguration bleiben erhalten. Er kann weiterhin mit `-Mode Daily`, `WatchC24` oder `Automation` gestartet werden und schreibt seine bisherigen Reddit-Ausgaben. Für den gemeinsamen Bericht nur den neuen Einstieg planen, um doppelte Reddit-Abrufe zu vermeiden.
