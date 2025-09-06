# Umgebungsvariablen Setup

## Für lokale Entwicklung

Erstellen Sie eine `.env` Datei im Hauptverzeichnis mit folgenden Inhalten:

```env
# Flask Konfiguration
SECRET_KEY=dein-geheimer-schluessel

# E-Mail Konfiguration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=fj.grieb@gmail.com
MAIL_PASSWORD=tffn kefw esgu euzm
```

## Für Render.com Deployment

Setzen Sie folgende Umgebungsvariablen in Ihrem Render Dashboard:

1. Gehen Sie zu Ihrem Service Dashboard
2. Klicken Sie auf "Environment"
3. Fügen Sie folgende Variablen hinzu:

```
SECRET_KEY = ein-sicherer-geheimer-schluessel-fuer-produktion
MAIL_SERVER = smtp.gmail.com
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = fj.grieb@gmail.com
MAIL_PASSWORD = tffn kefw esgu euzm
```

## Sicherheitshinweise

- Verwenden Sie niemals echte Passwörter in der `.env` Datei für Git
- Die `.env` Datei sollte in `.gitignore` stehen
- Für Produktion verwenden Sie starke, einzigartige SECRET_KEYs
- Gmail App-Passwörter sind sicherer als normale Passwörter

## App starten

Nach dem Erstellen der `.env` Datei:

```bash
# Virtuelle Umgebung aktivieren
.\venv\Scripts\activate

# App starten
python app.py
```
