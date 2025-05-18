from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from datetime import datetime, timezone
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dein-geheimer-schluessel'  # Ändern Sie dies in einen sicheren Schlüssel
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hochzeit.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# E-Mail Konfiguration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')  # Ihre E-Mail-Adresse
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')  # Ihr App-Passwort

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Datenbankmodell für RSVP
class RSVP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    guests = db.Column(db.Integer, default=1)
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<RSVP {self.name}>'

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
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(512), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        user = User.query.first()  # Wir haben nur einen Benutzer
        
        if user and user.check_password(password):
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
        guests = request.form.get('guests', type=int)
        message = request.form.get('message')

        if not name or not email:
            flash('Bitte füllen Sie alle Pflichtfelder aus.')
            return redirect(url_for('rsvp'))

        rsvp = RSVP(name=name, email=email, guests=guests, message=message)
        db.session.add(rsvp)
        db.session.commit()

        # Sende E-Mail nur mit dem neuen Eintrag
        send_rsvp_data(rsvp)

        flash('Vielen Dank für Ihre Anmeldung!')
        return redirect(url_for('thank_you'))

    return render_template('rsvp.html')

@app.route('/thank-you')
@login_required
def thank_you():
    return render_template('thank_you.html')

# Erstelle Benutzer beim ersten Start
def init_db():
    with app.app_context():
        # Erstelle die Datenbank, falls sie nicht existiert
        db.create_all()
        
        # Prüfe, ob bereits ein Benutzer existiert
        if not User.query.first():
            # Erstelle den Benutzer mit dem Passwort
            user = User()
            user.set_password('20260620')
            db.session.add(user)
            db.session.commit()

# Initialisiere die Datenbank beim App-Start
init_db()

@app.route('/test')
def test():
    return f'App läuft! Aktuelle UTC-Zeit: {datetime.now(timezone.utc)}'

def send_rsvp_data(rsvp):
    """Sendet nur den neuen RSVP-Eintrag per E-Mail."""
    try:
        # Daten des neuen RSVP-Eintrags
        rsvp_data = {
            'name': rsvp.name,
            'email': rsvp.email,
            'guests': rsvp.guests,
            'message': rsvp.message,
            'created_at': rsvp.created_at.isoformat()
        }

        # E-Mail erstellen
        msg = MIMEMultipart()
        msg['From'] = app.config['MAIL_USERNAME']
        msg['To'] = app.config['MAIL_USERNAME']  # An Sie selbst
        msg['Subject'] = 'Neuer RSVP für Ihre Hochzeit'

        # E-Mail-Inhalt erstellen
        body = f"""
        Neuer RSVP-Eintrag für Ihre Hochzeit:

        {json.dumps(rsvp_data, indent=2, ensure_ascii=False)}

        Diese Daten wurden automatisch generiert.
        """

        msg.attach(MIMEText(body, 'plain'))

        # E-Mail senden
        with smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT']) as server:
            server.starttls()
            server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            server.send_message(msg)

        return True
    except Exception as e:
        print(f"Fehler beim Senden der E-Mail: {str(e)}")
        return False

if __name__ == '__main__':
    app.run(debug=True) 