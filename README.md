### Real-time BTC Volume Monitor

1- Install the project requirements
```
pip install -r requirements.txt
```
2- Run docker-compose
```
docker-compose up
```
3- Run the backend
```
a. python src/backend/data_collection.py
b. python src/backend/data_analytics.py
c. python src/backend/email_notifications.py
```
4- Run the web app
```
streamlit run src/web_app/btc_app.py
```