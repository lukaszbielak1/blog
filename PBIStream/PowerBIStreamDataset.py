# Databricks notebook source
import pyspark.sql
import time
from datetime import datetime
import requests
import json

# COMMAND ----------

urlPBI = ""

# post/push data to the streaming API
headers = {
  "Content-Type": "application/json"
  }

urlWiki = "https://en.wikipedia.org/w/api.php"

paramsWiki = {
    "format": "json",
    "list": "recentchanges",
    "action": "query",
    "rctype": "edit|new",
    "rclimit": "10"
}

# COMMAND ----------

while 1:
    wikiData = requests.get(url=urlWiki, params=paramsWiki).json()
    recentChanges = spark.createDataFrame(wikiData["query"]["recentchanges"]).select("type", "title","ns")

    requests.post(
        url=urlPBI,
        headers=headers,
        data=recentChanges.toPandas().to_json(orient="records"),
    )
    time.sleep(5)


# COMMAND ----------


