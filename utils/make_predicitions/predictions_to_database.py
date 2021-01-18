# 1) 基础工具
import sys
import os
dir=os.path.abspath('..')
sys.path.append(dir)
from dao.mloutDB import MloutDB
import pickle as pk
import pandas as pd
from datetime import datetime, timedelta
import xlrd
import lightgbm
# 2) 绘图工具
import matplotlib.pyplot as plt

def mypreditions_to_database():
    with open("./utils/make_predicitions/X_train_o3", "rb") as X_scalar_file:
        X_train_scalar_o3 = pk.load(X_scalar_file)

    with open("./utils/make_predicitions/o3_api_model", "rb") as model_file:
        model_o3 = pk.load(model_file)

    with open("./utils/make_predicitions/X_train_pm25", "rb") as X_scalar_file:
        X_train_scalar_pm25 = pk.load(X_scalar_file)

    with open("./utils/make_predicitions/pm25_api_model", "rb") as model_file:
        model_pm25 = pk.load(model_file)

    try:
        predict_start_time = pd.to_datetime(input("-- 请输入预报起始时间: "))
        predict_time_len = int(input("-- 请输入预报时长: "))
        pollutant = input("-- 请输入预报污染物（O3/PM25）: ")
        # predict_start_time = pd.to_datetime("20201214 13:00:00")
        # predict_time_len = 24
        # pollutant = "O3"
    except:
        print("-- 请按指定格式重新输入数据.")

    time_delta = timedelta(hours=predict_time_len)
    predict_end_time = predict_start_time + time_delta

    print("\n")
    print("-- 预报污染物: {}".format(pollutant))
    print("-- 预报时长{} to {}".format(predict_start_time, predict_end_time))

    df = pd.read_excel("./utils/make_predicitions/wuxi_meteos.xlsx", index_col="time_point")

    df = df[predict_start_time:predict_end_time]

    #存入数据库
    mloutDB = MloutDB()

    if pollutant == "O3":
        features = ['precipitation', 'temperature', 'ws', 'wd', 'humidity', 'cloudrate', 'pressure', 'visibility',
                    'dswrf']

        X = df[df["position_name"] == "东亭"][features]
        X_std = (X - X_train_scalar_o3.min(axis=0)) / (X_train_scalar_o3.max(axis=0) - X_train_scalar_o3.min(axis=0))
        predictions = pd.Series(model_o3.predict(X_std), index=X_std.index)
        list_value = []
        for time_point, value in predictions.items():
            tempList = [time_point, '东亭', 2, value]
            list_value.append(tempList)
        count = mloutDB.insertMany(list_value)
        print(count)
    elif pollutant == "PM25":
        features = ['precipitation', 'temperature', 'ws', 'wd', 'humidity', 'cloudrate', 'pressure', 'visibility',
                    'dswrf', 'pm25']

        X = df[df["position_name"] == "东亭"][features]
        X_std = (X - X_train_scalar_pm25.min(axis=0)) / (
                    X_train_scalar_pm25.max(axis=0) - X_train_scalar_pm25.min(axis=0))
        list_value = []
        predictions = pd.Series(model_pm25.predict(X_std), index=X_std.index)
        for time_point, value in predictions.items():
            tempList = [time_point, '东亭', 2, value]
            list_value.append(tempList)
        count = mloutDB.insertMany(list_value)
        print(count)
