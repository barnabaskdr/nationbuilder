import json
import math
import os
import re
import sqlite3
import sys

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN", "")


def requests_get(host, endpoint, params):
    response = requests.get(host + endpoint, params=params)
    result = json.loads(response.text)
    return result


def dataframify(request_result, conn):
    df = pd.json_normalize(request_result["results"], max_level=2)
    df = pd.DataFrame(df)
    df.columns = [
        x.replace("primary_address.", "addr_").rstrip("_") for x in df.columns
    ]
    # df = df[
    #     [
    #         "birthdate",
    #         "created_at",
    #         "middle_name",
    #         "first_name",
    #         "last_name",
    #         "id",
    #         "is_volunteer",
    #         "occupation",
    #         "party",
    #         "addr_country_code",
    #         "addr_lat",
    #         "addr_lng",
    #         "addr_city",
    #         "sex",
    #         "tags",
    #         "volunteer",
    #         "why_atlas",
    #     ]
    # ]
    df["tags"] = [" ".join(x) for x in df["tags"]]
    df.to_sql("people", conn, if_exists="append", index=False)


def start_db():
    conn = sqlite3.connect("result/nationbuilder.db")
    return conn


def update_params(pagination, params):
    if pagination:
        for x in re.split("\?|&", pagination):
            if "=" in x:
                k, v = x.split("=")
                params[k] = v
    else:
        print(f"pagination is: {pagination} \nProcess exit!")
        sys.exit()
    return params


def close_db(conn):
    df = pd.read_sql("select * from people", conn)
    conn.commit()
    conn.close()
    print("total rows: ", len(df))


def execute():
    host = "https://atlasmovement.nationbuilder.com/api/v1/"
    endpoint = "people"
    limit = 100
    request_body = requests_get(host, "people/count", {"access_token": ACCESS_TOKEN})
    total = math.ceil(request_body["people_count"] / limit)
    params = {"access_token": ACCESS_TOKEN, "limit": limit}
    current_params = params
    conn = start_db()
    for r in range(total):
        request_body = requests_get(host, endpoint, params)
        current_params = update_params(request_body["next"], current_params)
        dataframify(request_body, conn)
        print(f"round {r+1} of {total} done")
    close_db(conn)


# execute()
