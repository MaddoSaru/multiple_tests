#import pandas as pd
import requests
from typing import List, Optional
from dotenv import load_dotenv
from pyspark.sql import SparkSession
import os

load_dotenv()

currencies : List[str] = [
    'BTC',
    'ETH',
]

api_key = os.getenv("CRYPTOCOMPARE_API_KEY")

spark = SparkSession.builder \
    .appName("Fetch API Data") \
    .getOrCreate()
sc = spark.sparkContext

def get_spark_df(
    currency : str,
):
    url = f'https://min-api.cryptocompare.com/data/v2/histohour?fsym={currency}&tsym=USD&limit=100&api_key={api_key}'    
    request = requests.get(url = url)
    json_rdd = sc.parallelize([request.text])
    df = spark.read.json(json_rdd)
    return df

df = get_spark_df('BTC')

print(df.select(df.Data).show())
