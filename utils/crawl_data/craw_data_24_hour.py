# 1) 基础工具
import os
import math
import json
import requests
import importlib
import numpy as np
import pickle as pk
import pandas as pd
from tqdm import trange
from datetime import datetime

# 获取json数据
def get_json_contents(url):
    res = requests.get(url).json()
    predictions_hourly = res["result"]["hourly"]
    return predictions_hourly


# 返回DataFrame数据
def return_df(predictions_hourly, position_name):
    params = [x for x in predictions_hourly.keys()]
    params.remove("status")
    params.remove("description")

    dates = [idate["datetime"][:16].replace("T", " ") for idate in predictions_hourly["temperature"]]

    df = pd.DataFrame(index=dates)
    df["position_name"] = position_name
    df.index = pd.to_datetime(df.index)

    for param in params:
        if param == "wind":
            df["ws"] = [item["speed"] for item in predictions_hourly["wind"]]
            df["wd"] = [item["direction"] for item in predictions_hourly["wind"]]
        elif param == "air_quality":
            df["aqi"] = [item["value"]["chn"] for item in predictions_hourly["air_quality"]["aqi"]]
            df["pm25"] = [item["value"] for item in predictions_hourly["air_quality"]["pm25"]]
        else:
            values = [item["value"] for item in predictions_hourly[param]]
            df[param] = values
    df["pressure"] = df["pressure"] / 100

    return df


# 保存数据
def save_data(df):
    fil_name = "crawl_data.xlsx"
    print("-- Saving the result into {}...".format(fil_name))

    columns = ['position_name', 'cloudrate', 'dswrf', 'humidity', 'precipitation', 'pressure', 'skycon', 'temperature',
               'visibility', 'wd', 'ws', 'pm25', 'aqi']
    df[columns].to_excel(fil_name)

    print("-- Finished!")


if __name__ == "__main__":

    token = "wk8fcsuDNtKRYfF5"

    loc_dic = {
        "雪浪": (120.269, 31.4867),
        "黄巷": (120.275, 31.6219),
        "曹张": (120.294, 31.56),
        "漆塘": (120.242, 31.5031),
        "东亭": (120.354, 31.5848),
        "旺庄": (120.354, 31.5475),
        "荣巷": (120.245, 31.5631),
        "堰桥": (120.288, 31.6842),
        "无锡": (120.299, 31.568),
    }

    df = pd.DataFrame()

    for stat in loc_dic:
        lon, lat = loc_dic[stat]

        url = "https://api.caiyunapp.com/v2.5/{}/{},{}/hourly.json".format(token, lon, lat)

        result = get_json_contents(url)

        df = df.append(return_df(result, position_name=stat))

    save_data(df)