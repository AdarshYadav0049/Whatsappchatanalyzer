import re
import pandas as pd

def preprocess12(data):
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

def preprocess24(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # convert message_date type
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %H:%M - ')

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['dayofweek']=df['day_name']
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['datetime']=df['date']

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df