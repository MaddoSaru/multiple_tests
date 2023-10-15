from utils.ddbb_utils import build_time_series_df
import pandas as pd
import statsmodels.api as sm

file_open = open("utils/queries/read_data.sql", "r")
str_query = file_open.read()

time_series_df = build_time_series_df(
    "cryptocompare_OHCLV", str_query
)

time_series_df["datetime"] = pd.to_datetime(time_series_df["time"], unit="s")
time_series_df = time_series_df[["datetime", "close"]]

time_series_df.set_index(keys="datetime", inplace=True)

# Fit an AR(2) Model
mod_ar2 = sm.tsa.SARIMAX(time_series_df, order = (2,0,0))
res_ar2 = mod_ar2.fit()

print(res_ar2.forecast(steps=10, signal_only=False))

# Fit a SARIMA(1,1,1) x (0,1,1,4) Model:
mod_sarimax = sm.tsa.SARIMAX(time_series_df, order=(1,1,1),
                             seasonal_order=(0,1,1,4))
res_sarimax = mod_sarimax.fit()

print(res_sarimax.forecast(steps=10, signal_only=False))
