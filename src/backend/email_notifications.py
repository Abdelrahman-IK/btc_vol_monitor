from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import time
import json
import pandas as pd


JSON_PATH = 'src/backend/emails_settings.json'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BTC.sqlite3'
app.app_context().push()
db = SQLAlchemy(app)

class BTC(db.Model):
    time = db.Column(db.Integer, primary_key=True)
    volume = db.Column(db.Integer,  default=0)

def load_data():
    btc_data = BTC.query.all()
    data = [{'time': entry.time, 'volume': entry.volume} for entry in btc_data]
    return data[-1]['volume']

def load_configs(volume_data):
    with open(JSON_PATH, 'r') as file:
        json_data = json.load(file)
    df = pd.DataFrame(json_data)
    emails = df[df.volume>=volume_data]['email'].values
    return emails

while True:
    emails = load_configs(load_data())
    if len(emails)>=0:
        print(f"""
        FROM: btc_monitor@btcmonitor.com
        TO: {str(emails)}
        Subjet: BTC volume reached
        --------------------------------
        Your BTC volume has been reached {load_data()}
            """)
    else:
        print("No volume level has been reached!")
    time.sleep(5)