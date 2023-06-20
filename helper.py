import streamlit as st
from urlextract import URLExtract
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import os
extract = URLExtract()


def daily_activity(df):
    daily_counts = df.set_index('datetime')['message'].resample('D').count()
    daily_counts = daily_counts.reset_index()
    f = plt.figure(figsize=(12, 6))
    sns.lineplot(x='datetime', y='message', data=daily_counts, marker='o', markersize=5, color="#6B9AC4", size=15)
    plt.xlabel('Date')
    plt.ylabel('Number of Messages')
    plt.title('Number of Messages Sent per Day')
    plt.grid(True)
    st.pyplot(f)


def monthly_activity(df):
    monthly_counts = df.set_index('datetime')['message'].resample('M').count()
    monthly_counts = monthly_counts.reset_index()

    f=plt.figure(figsize=(12, 6))
    sns.lineplot(x=monthly_counts['datetime'].dt.month_name(), y=monthly_counts['message'], hue=monthly_counts['datetime'].dt.year,
                 marker='o', markersize=8,palette="blend:#F44C7D,#F4E900,#9BD46A",size=50)
    plt.xlabel('Month')
    plt.ylabel('Number of Messages')
    plt.title('Number of Messages Sent per Month')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend(title='Year')
    st.pyplot(f)

def dayofweek_activity(df):
    dayofweek_counts = df['dayofweek'].value_counts()
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    f = plt.figure(figsize=(12, 6))
    sns.barplot(x=dayofweek_counts.index, y=dayofweek_counts.values, order=day_order,
                palette="blend:#00cfdd,#b8f10b,#29d0fe")
    plt.xlabel('Days of the week')
    plt.ylabel('Number of Messages')
    plt.title('Number of Messages Sent per Day')
    plt.grid(True)
    st.pyplot(f)
def hourly_activity(df):
    hour_counts = df['hour'].value_counts().sort_index()
    f=plt.figure(figsize=(12, 6))
    sns.barplot(x=hour_counts.index,y=hour_counts.values,palette="blend:#011936,#0015dd,#f10b5b,#fecf29,#f10b5b,#0015dd,#011936")
    plt.xlabel('Hour')
    plt.ylabel('Number of Messages')
    plt.title('Number of Messages Sent per Hour')
    # plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot(f)
def mostUsedWords(df):
    words=[]
    stop_words=open('stop_hinglish.txt','r').read()
    for i in df[df['user']!='system'][df['message']!="<Media omitted>\n"][df['message']!="This message was deleted\n"][df['message']!="You deleted this message\n"]['message']:
        curr=i.split(" ")
        for j in curr:
            if j.lower() not in stop_words:
                words.append(j)
    temp=pd.DataFrame(Counter(words).most_common(20))
    temp[0] = temp[0].str.replace('\n', '')
    c1,c2=st.columns([1,3])
    with c1:
        st.dataframe(temp)
    with c2:
        word_freq = dict(zip(temp[0], temp[1]))
        wc=WordCloud(width=1600, height=1250, background_color='white', collocations=False,colormap="Blues")
        wc.generate_from_frequencies(word_freq)
        f=plt.figure(figsize=(10, 20))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        st.pyplot(f)

def emoji_count(df):
    emjs=[]
    for i in df['message']:
        emjs.extend([c for c in i if c in emoji.EMOJI_DATA])
    emcount=pd.DataFrame(Counter(emjs).most_common())
    c1, c2 = st.columns([1, 3])
    with c1:
        st.dataframe(emcount)
        emcount=emcount.head(10)
    with c2:
        f=plt.figure()
        sns.barplot(x=emcount[0],y=emcount[1],palette="blend:#F44C7D,#F4E900,#9BD46A")
        plt.title("Top 10 emojis")
        st.pyplot(f)