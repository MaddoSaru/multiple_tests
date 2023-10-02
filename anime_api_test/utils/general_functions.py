import requests
import pandas as pd
import sleep


def request_to_df(
    url : str
) -> pd.DataFrame:
        
    last_visible_page = requests.get(f"https://api.jikan.moe/v4/anime").json()["pagination"]["last_visible_page"]

    sleep(5)

    anime_df = pd.DataFrame()

    for page_number in range(1, last_visible_page):
        response = requests.get(f"https://api.jikan.moe/v4/anime?sort_by=mal_id&page={page_number}").json()["data"]
        new_page_df = pd.DataFrame(response)
        new_page_df["page_number"] = page_number
        anime_df = pd.concat([anime_df, new_page_df], ignore_index = True, join = "outer")

        sleep(5)


    print(pd.DataFrame(response).describe())