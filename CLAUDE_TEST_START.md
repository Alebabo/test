# Zuerst in Claude Automation testen

1. ZIP entpacken, z. B. nach `C:\Users\User\Documents\C24Monitor` (Skripte müssen direkt darin liegen).
2. Python 3.10+ muss installiert sein. Claude muss lokale Befehle ausführen und Dateien dieses Ordners lesen können. Eine reine Chat-Aufgabe ohne lokalen Toolzugriff kann das Skript nicht ausführen.
3. Eine stündliche Aufgabe in deiner Claude-Umgebung anlegen, falls unterstützt. Sonnet in der Aufgabe auswählen, sofern auswählbar. Den Prompt aus `CLAUDE_AUTOMATION_PROMPT.md` übernehmen und den Pfad anpassen.
4. Für einen ersten manuellen Test `run-monitor.ps1 -Mode Daily` ausführen lassen und den Tagesbericht erzeugen. Danach stündlich mit `-Mode Automation` weiterlaufen lassen. Ohne neue kritische Hinweise bleibt die Ausgabe zwischen Tagesberichten leer.

`ai.enabled` ist in diesem Testpaket **false**: keine direkte Anthropic-API, kein zusätzlicher Anthropic-Schlüssel. Claude übernimmt die Bewertung in seinem geplanten Turn. Andere Quellen wie YouTube/X benötigen weiterhin ihre eigenen Zugänge; nicht eingerichtete Quellen erscheinen als Abdeckungslücken. Gewöhnliche Quellen laufen ohne diese Zugänge weiter.

Tagesbericht einmal pro Kalendertag ab 07:00 Uhr lokaler Rechnerzeit; maximal fünf Punkte mit Links. Ein erster Test mit `Daily` zählt bereits als Tagesbericht. Zum erneuten Test am selben Tag kann die Tagesanweisung einmal manuell auf den vorhandenen Tagesdaten ausgeführt werden, ohne die geplante Aufgabe mehrfach zu starten.

Während dieses Tests **nicht zusätzlich** `install-scheduled-task.ps1` ausführen. Dieser und `crontab.example` sind nur Alternativen für später. Das Paket ist vorbereitet; in deinem Claude-Konto wurde keine Aufgabe angelegt. Ob stündliche Aufgaben, Sonnet-Auswahl und lokale Ausführung möglich sind, hängt von deiner Claude-Umgebung ab.
