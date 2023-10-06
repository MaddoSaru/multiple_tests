import pandas as pd
import requests
from typing import Optional
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

cryptocompare_api_key = os.getenv("CRYPTOCOMPARE_API_KEY")
url = "https://min-api.cryptocompare.com/data/v2/histoday?fsym=BTC&tsym=USD&limit=2000&api_key={api_key}"


def request_to_df(url: str, api_key: str) -> pd.DataFrame:
    request = requests.get(url.format(api_key=api_key))
    request_json = request.json()["Data"]["Data"]
    request_df = pd.DataFrame(request_json)
    request_df["date"] = pd.to_datetime(request_df["time"], unit="s")
    return request_df


def df_save_as_csv(
    dataframe: Optional[pd.DataFrame],
) -> str:
    if not os.path.exists("utils/csv_files/"):
        os.makedirs("utils/csv_files/")
    dataframe.to_csv(f"utils/csv_files/btc_price_{datetime.now().strftime('%Y_%m_%d')}")
    pass


def csv_to_df(
    file_path: Optional[
        str
    ] = f"utils/csv_files/btc_price_{datetime.now().strftime('%Y_%m_%d')}",
) -> pd.DataFrame:
    if not os.path.exists(file_path):
        df_save_as_csv(dataframe=request_to_df(url=url, api_key=cryptocompare_api_key))
    dataframe = pd.read_csv(file_path)
    return dataframe
