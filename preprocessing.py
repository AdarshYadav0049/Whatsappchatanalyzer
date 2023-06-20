import re
import pandas as pd

def preprocess(data):
    pattern = "\d{1,2}\/\d{1,2}\/\d{2,4},\s\d{1,2}:\d{1,2}\\u202f.m\s-\s"
    mess = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    date = []
    for i in dates:
        if i[-5] == 'a':
            if len(i) == 20:
                date.append(i[0:6] + "20" + i[6:-10] + '0' + i[-10:-6])
            else:
                date.append(i[0:6] + "20" + i[6:-6])
        else:
            a = (int)(i[10:-9])
            a += 12
            if a == 24:
                s = i[0:6] + "20" + i[6:10] + "00" + i[-9:-6]
            else:
                s = i[0:6] + "20" + i[6:10] + (str)(a) + i[-9:-6]
            date.append(s)
    df = pd.DataFrame({'user_message': mess, 'datetime': date})
    df['datetime'] = pd.to_datetime(df['datetime'], format="%d/%m/%Y, %H:%M")
    user = []
    mess = []
    for i in df['user_message']:
        y = re.split('([\w\W]+?):\s', i)
        if y[1:]:
            user.append(y[1])
            mess.append(y[2])
        else:
            user.append('system')
            mess.append(y[0])
    df['user'] = user
    df['message'] = mess
    df.drop(columns=['user_message'], inplace=True)
    df['Year'] = df['datetime'].dt.year
    df['month'] = df['datetime'].dt.month_name()
    df['dayofweek'] = df['datetime'].dt.day_name()
    df['day'] = df['datetime'].dt.day
    df['hour'] = df['datetime'].dt.hour
    return df