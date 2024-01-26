#!/usr/bin/env python3
import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.sqlite3'
db = SQLAlchemy(app)
app.app_context().push()
class Weather(db.Model):
    time = db.Column(db.DateTime, primary_key=True, default=datetime.utcnow())
    interval = db.Column(db.Integer,  default=0)
    temperature_2m = db.Column(db.Double, nullable=False)

def get_temperature():
    response = requests.get("https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m")
    data = dict(response.json()["current"])
    return data

if __name__ == "__main__":
    current_temperature = get_temperature()
    db.create_all()
    new_entry = Weather(temperature_2m=current_temperature['temperature_2m'])
    db.session.add(new_entry)
    db.session.commit()
    print(f"Data {current_temperature} inserted successfully!")
