# 1) 基础工具
import sys
import os
import time

dir = os.path.abspath('..')
sys.path.append(dir)
from dao.mlmetDB import MlmetDB
import math
import json
import requests
import importlib
import numpy as np
import pickle as pk
import pandas as pd
from datetime import datetime,timedelta
from dao.mloutDB import MloutDB
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

#模型预测
def make_predicitons():

    #打开模型的权重文件
    with open("./utils/make_predicitions/X_train_o3", "rb") as X_scalar_file:
        X_train_scalar_o3 = pk.load(X_scalar_file)

    with open("./utils/make_predicitions/o3_api_model", "rb") as model_file:
        model_o3 = pk.load(model_file)

    with open("./utils/make_predicitions/X_train_pm25", "rb") as X_scalar_file:
        X_train_scalar_pm25 = pk.load(X_scalar_file)

    with open("./utils/make_predicitions/pm25_api_model", "rb") as model_file:
        model_pm25 = pk.load(model_file)

    #获取爬取的数据
    df = get_craw_data()
    #获取爬取的位置信息
    position_list = df["position_name"].unique()
    #预测物
    substance_list = ["O3", "PM25"]
    #定义数据库操作对象
    mloutDB = MloutDB()
    #获取当前时间整点时刻，向下取整
    date = datetime.now().date()
    hour = datetime.now().hour
    minSecond = "00:00"
    predict_start_time = str(date) + " " + str(hour) + ":" + minSecond
    predict_start_time = pd.to_datetime(predict_start_time)
    time_delta = timedelta(hours=24)
    predict_end_time = predict_start_time + time_delta
    #只删除一次
    hasDelete = False

    for position_name in position_list:
        for substance in substance_list:
            print(position_name + " " + substance)
            temp_df = df[df["position_name"] == position_name]
            temp_df = temp_df[predict_start_time:predict_end_time]

            if substance == "O3":
                features = ['precipitation', 'temperature', 'ws', 'wd', 'humidity', 'cloudrate', 'pressure', 'visibility',
                            'dswrf']

                X = temp_df[features]
                X_std = (X - X_train_scalar_o3.min(axis=0)) / (X_train_scalar_o3.max(axis=0) - X_train_scalar_o3.min(axis=0))

                predictions = pd.Series(model_o3.predict(X_std), index=X_std.index)
                list_values = []
                time_list = []
                for time_point, prediciton_value in predictions.items():
                    time_list.append(time_point)
                    temp_list = [time_point, position_name, substance, prediciton_value]
                    list_values.append(temp_list)
                # 删除存在的数据, 如果操作成功，将预测数据插入到数据库中
                if hasDelete == False:
                    count = mloutDB.deleteByTimePoint(time_list)
                    hasDelete = True
                if count != -1:
                    mloutDB.insertMany(list_values)
            else:
                features = ['precipitation', 'temperature', 'ws', 'wd', 'humidity', 'cloudrate', 'pressure',
                            'visibility',
                            'dswrf', 'pm25']

                X = temp_df[features]
                X_std = (X - X_train_scalar_pm25.min(axis=0)) / (
                        X_train_scalar_pm25.max(axis=0) - X_train_scalar_pm25.min(axis=0))

                predictions = pd.Series(model_pm25.predict(X_std), index=X_std.index)

                list_values = []
                time_list = []
                for time_point, prediciton_value in predictions.items():
                    time_list.append(time_point)
                    temp_list = [time_point, position_name, substance, prediciton_value]
                    list_values.append(temp_list)
                # 删除存在的数据, 如果操作成功，将预测数据插入到数据库中
                if hasDelete == False:
                    count = mloutDB.deleteByTimePoint(time_list)
                    hasDelete = True
                if count != -1:
                    mloutDB.insertMany(list_values)
#抓取数据
def get_craw_data():

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
    return df


if __name__ == '__main__':
    make_predicitons()