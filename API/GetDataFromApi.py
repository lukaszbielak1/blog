# Databricks notebook source
import requests
import json
import pandas as pd
from datetime import date, timedelta
import calendar
dbutils.widgets.text("Data","202110")

# COMMAND ----------

apiURL = "https://api.cepik.gov.pl/"
metoda = "pojazdy?"
limit = "&limit=500"

#obsługa pełnego miesiąca
dataOd = "&data-od="+dbutils.widgets.get("Data")+"01"
start_date = date(int(dbutils.widgets.get("Data")[:4]), 7, 1)
days_in_month = calendar.monthrange(start_date.year, start_date.month)[1]
end_date = start_date + timedelta(days=days_in_month)
dataDo = "&data-do="+end_date.strftime('%Y%m%d') 


# COMMAND ----------

#Pobieranie 
wojewodztwa = json.loads(requests.get(apiURL+"/slowniki/wojewodztwa").text)
wojewodztwa = pd.json_normalize(wojewodztwa['data']['attributes']['dostepne-rekordy-slownika'])['klucz-slownika']
wojewodztwa = wojewodztwa.values.tolist()

# COMMAND ----------

wszystkie_rejestracje = []
rejestracje = ""
for w in wojewodztwa:
  rejestracje = requests.get(apiURL+metoda+dataOd+dataDo+limit+"&wojewodztwo="+w).json()
  wszystkie_rejestracje.append(rejestracje)
  rejestracje
data = pd.json_normalize(wszystkie_rejestracje, record_path =['data']).drop(['type','links.self'],axis=1)


# COMMAND ----------

data
