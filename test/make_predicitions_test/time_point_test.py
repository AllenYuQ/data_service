from datetime import datetime, timedelta
import pandas as pd

if __name__ == '__main__':
    date = datetime.now().date()
    hour = datetime.now().hour
    minSecond = "00:00"
    predict_start_time = str(date) + " " + str(hour) + ":" + minSecond
    print(predict_start_time)
    time_delta = timedelta(hours=1)
    predict_start_time = pd.to_datetime(predict_start_time)
    print(predict_start_time.date())
    print(predict_start_time.hour)
    print(str(predict_start_time.date()) + " " + str(predict_start_time.hour))
    predict_start_time = time_delta + predict_start_time
    print(predict_start_time)