import streamlit as st
import pandas as pd
from pandas import DataFrame

import preprocessing
from urlextract import URLExtract
import seaborn as sns
import matplotlib.pyplot as plt
import helper

extract = URLExtract()

st.sidebar.title("Whatsapp Chat Analyzer")
st.sidebar.text("->Go to your chat\n->click on the three dots on the top right\n->click on export chat\n->upload the "
                "file here")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessing.preprocess(data)
    st.dataframe(df[["message", "user", "datetime"]])
    # st.dataframe(df)

    users = df['user'].unique()
    user_list = users.tolist()
    user_list.sort()
    user_list.insert(0, "all")
    user = st.sidebar.selectbox("Show analysis of", user_list)
    df2: DataFrame = df
    if user != "all":
        df2 = df2[df2['user'] == user]
    if st.sidebar.button("show analysis"):
        st.header("Quick stats")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.header("total messages")
            if user == "all":
                st.text(len(df))
            else:
                st.text(len(df[df['user'] == user]))
        with c2:
            st.header("total words")
            if user == "all":
                tot_mess = 0
                for i in df['message']:
                    tot_mess += len(i.split())
                st.text(tot_mess)
            else:
                tot_mess = 0
                for i in df[df['user'] == user]['message']:
                    tot_mess += len(i.split())
                st.text(tot_mess)
        with c3:
            st.header("total media shared")
            if user == "all":
                st.text(len(df[df['message'] == "<Media omitted>\n"]))
            else:
                st.text(len(df[df['message'] == "<Media omitted>\n"][df['user'] == user]))
        with c4:
            st.header("total media shared")
            if user == "all":
                links = []
                for message in df['message']:
                    links.extend(extract.find_urls(message))
                st.text(len(links))
            else:
                links = []
                for message in df[df['user'] == user]['message']:
                    links.extend(extract.find_urls(message))
                st.text(len(links))
        df3 = df2
        st.header("Hourly Activity")
        helper.hourly_activity(df3)

        st.header("weekly Activity")
        helper.dayofweek_activity(df3)
        # st.dataframe(df2)
        st.header("Daily Activity")
        helper.daily_activity(df3)
        # st.dataframe(df2)
        st.header("Monthly Activity")
        helper.monthly_activity(df3)
        if user == "all":
            st.header("Most frequent users")
            user_mess = []
            for i in users:
                user_mess.append(len(df[df['user'] == i]))
            Mfc = pd.DataFrame({'name': users, 'NoM': user_mess})
            Mfc.sort_values(by='NoM', ascending=False, inplace=True, ignore_index=True)
            Mfc['%'] = (Mfc['NoM'] / len(df)) * 100
            clo1, clo2 = st.columns(2)
            with clo1:
                st.dataframe(Mfc)
            with clo2:
                xx = 10
                fig = plt.figure()
                f = sns.barplot(data=Mfc.head(xx), x='name', y='NoM', palette="blend:#F44C7D,#F4E900,#9BD46A")
                f.set_xticklabels(labels=Mfc.head(xx)['name'], rotation=90)
                st.pyplot(fig)
        st.header("WordCloud of most occuring words")
        helper.mostUsedWords(df2)
        st.header("Emojis")
        helper.emoji_count(df2)