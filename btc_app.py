import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from streamlit_autorefresh import st_autorefresh

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BTC.sqlite3'
app.app_context().push()
db = SQLAlchemy(app)
st.set_option('deprecation.showPyplotGlobalUse', False)
refresh_page = st_autorefresh(interval=2000, key="counter")


class BTC(db.Model):
    time = db.Column(db.Integer, primary_key=True)
    volume = db.Column(db.Integer,  default=0)

def load_data():
    btc_data = BTC.query.all()
    data = [{'time': entry.time, 'volume': entry.volume} for entry in btc_data]
    df = pd.DataFrame(data)
    return df

@st.cache_data(ttl=10)
def main():
    st.title("Real-time BTC Volume Visualizer")

    # Load data from SQLite
    btc_data = load_data()

    # Display the first few rows of the DataFrame
    st.subheader("BTC Data:")
    st.write(btc_data.tail())

    # Create a time series chart
    st.subheader("Volume Time Series Chart:")
    plt.figure(figsize=(12, 6))
    plt.plot(btc_data['time'], btc_data['volume'])
    plt.xlabel('Time')
    plt.ylabel('Volume')
    plt.title('BTC Volume Time Series')
    st.pyplot()

if __name__ == "__main__":
    main()