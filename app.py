from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from datetime import datetime, timezone
import os
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dein-geheimer-schluessel'  # Ändern Sie dies in einen sicheren Schlüssel

# E-Mail Konfiguration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "fj.grieb@gmail.com"  # Hier Ihre Gmail-Adresse eintragen
app.config['MAIL_PASSWORD'] = "tffn kefw esgu euzm"      # Hier Ihr Gmail-App-Passwort eintragen

# Für Produktion sollten die Umgebungsvariablen verwendet werden:
# app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
# app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Hochzeitsdatum
WEDDING_DATE = datetime(2026, 6, 20)

def get_time_until_wedding():
    now = datetime.now()
    time_left = WEDDING_DATE - now
    days = time_left.days
    hours = time_left.seconds // 3600
    minutes = (time_left.seconds % 3600) // 60
    seconds = time_left.seconds % 60
    return {
        'days': days,
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds
    }

# Einfaches User-Modell mit nur einem Passwort
class User(UserMixin):
    id = 1  # Fester Wert, da wir nur einen Benutzer haben
    password_hash = generate_password_hash('20260620')  # Fester Passwort-Hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User() if int(user_id) == 1 else None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        user = User()
        
        if user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Ungültiges Passwort')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/get-countdown')
def get_countdown():
    return jsonify(get_time_until_wedding())

@app.route('/rsvp', methods=['GET', 'POST'])
@login_required
def rsvp():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        adults = request.form.get('adults', type=int)
        children = request.form.get('children', type=int)
        friday = 'friday' in request.form.getlist('events')
        saturday = 'saturday' in request.form.getlist('events')
        sunday = 'sunday' in request.form.getlist('events')
        not_attending = request.form.get('not_attending') == 'true'
        message = request.form.get('message')

        if not name or not email:
            flash('Bitte füllen Sie alle Pflichtfelder aus.', 'error')
            return redirect(url_for('rsvp'))

        # RSVP-Daten für E-Mail
        rsvp_data = {
            'name': name,
            'email': email,
            'adults': adults,
            'children': children,
            'friday': friday,
            'saturday': saturday,
            'sunday': sunday,
            'not_attending': not_attending,
            'message': message,
            'created_at': datetime.now(timezone.utc).isoformat()
        }

        # Sende E-Mail
        if send_rsvp_data(rsvp_data):
            flash('Vielen Dank für deine Antwort! Wir freuen uns über eure Teilnahme.', 'success')
            return redirect(url_for('thank_you'))
        else:
            flash('Es gab einen Fehler beim Senden der Anmeldung. Bitte versuche es später erneut oder kontaktiere uns direkt.', 'error')
            return redirect(url_for('rsvp'))

    return render_template('rsvp.html')

@app.route('/thank-you')
@login_required
def thank_you():
    return render_template('thank_you.html')

@app.route('/location')
@login_required
def location():
    return render_template('location.html')

@app.route('/test')
def test():
    return f'App läuft! Aktuelle UTC-Zeit: {datetime.now(timezone.utc)}'

def send_rsvp_data(rsvp_data):
    """Sendet die RSVP-Daten per E-Mail."""
    try:
        print("Starte E-Mail-Versand...")
        print(f"Mail-Server: {app.config['MAIL_SERVER']}")
        print(f"Mail-Port: {app.config['MAIL_PORT']}")
        print(f"Mail-Username: {app.config['MAIL_USERNAME']}")
        
        # E-Mail erstellen
        msg = MIMEMultipart()
        msg['From'] = app.config['MAIL_USERNAME']
        msg['To'] = app.config['MAIL_USERNAME']  # An Sie selbst
        msg['Subject'] = 'Neuer RSVP für Ihre Hochzeit'

        # Nur JSON-Format für einfachen Datenbank-Import
        body = json.dumps(rsvp_data, indent=2, ensure_ascii=False)

        msg.attach(MIMEText(body, 'plain'))
        print("E-Mail-Inhalt erstellt")

        # E-Mail senden
        print("Versuche Verbindung zum SMTP-Server herzustellen...")
        with smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT']) as server:
            print("Verbindung hergestellt, starte TLS...")
            server.starttls()
            print("TLS gestartet, versuche Login...")
            server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            print("Login erfolgreich, sende E-Mail...")
            server.send_message(msg)
            print(f"E-Mail erfolgreich gesendet an {app.config['MAIL_USERNAME']}")

        return True
    except smtplib.SMTPAuthenticationError as e:
        print(f"SMTP Authentifizierungsfehler: {str(e)}")
        return False
    except smtplib.SMTPException as e:
        print(f"SMTP Fehler: {str(e)}")
        return False
    except Exception as e:
        print(f"Unerwarteter Fehler beim Senden der E-Mail: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

if __name__ == '__main__':
    app.run(debug=True) 