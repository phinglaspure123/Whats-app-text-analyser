from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import re
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def fetch_stats(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    
    # fetch num messages
    num_messages=df.shape[0]
    
    # fect no. of links,media
    words=[]
    links=[]
    extractor=URLExtract()
    for msg in df['message']:
            words.extend(msg.split())
            links.extend(extractor.find_urls(msg))
            
    # fetch no. of num media
    num_media=df[df['message']=='<Media omitted>\n'].shape[0]
    
    
    return num_messages,len(words),num_media,len(links)

def fetch_most_busy_user(df):
    x=df['user'].value_counts().head()
    
    df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={
    'user':"Name",
    'count':"Percentage"
    })
    
    return x,df

def creat_word_cloud(selected_user,df):
    f=open('stop_hinglish.txt','r')
    stop_words=f.read()
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    # <Media omitted>
    df=df[df['message']!='<Media omitted>\n']
    # what to do if no user has sent no message in the group
    if df.shape[0]==0:
        return pd.NA
    else:
        def remove_stop_words(msg):
            y=[]
            for word in msg.lower().split():
                if word not in stop_words:
                    y.append(word)
            return " ".join(y)
        df['message']=df['message'].apply(remove_stop_words)
        df_wc=wc.generate(df['message'].str.cat(sep=" "))
        return df_wc

# Problem => emojis are getting included as words
def remove_emoji(msg):
    emoji_pattern = re.compile("["
                    u"\U0001F600-\U0001F64F"  # emoticons
                    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                    u"\U0001F680-\U0001F6FF"  # transport & map symbols
                    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                    "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', msg)

# most common words
def most_common_words(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    # removing group notification
    df=df[df['message']!='<Media omitted>\n']
    # removing emoji
    df['message']=df['message'].apply(remove_emoji)
    
    # removing stop words
    f=open('stop_hinglish.txt','r')
    stop_words=f.read()
    # procssed df
    df_processed=df
    words=[]
    for msg in df['message']:
        for word in msg.lower().split():
            if word not in stop_words:
                words.append(word)
    most_common_df=pd.DataFrame(Counter(words).most_common(20),columns=["Words","Count"])
    return most_common_df,df_processed

# emoji Analysis with re 
def emoji_count(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
        
    def emoji_extract(msg):
        emoji_pattern = re.compile("["
                u"\U0001F600-\U0001F64F"  # emoticons
                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                "]+", flags=re.UNICODE)
        emoji=emoji_pattern.findall(msg) # no emoji
        # Split combined emojis into individual elements
        emoji = [char for emoji in emoji for char in emoji]
        return emoji
    chat_emojis=[]
    for msg in df['message']:
        for i in msg.split():
            w=emoji_extract(i)
            if len(w)!=0:
                chat_emojis.extend(w)
    emoji_df=pd.DataFrame(Counter(chat_emojis).most_common(20)).reindex().rename(
        columns={
            0:"Emoji",
            1:"Count"
        }
    )
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    timeline_df=df.groupby(['year','month']).count()['message'].reset_index()
    time=[]
    for i in range (timeline_df.shape[0]):
        time.append(timeline_df['month'][i]+"-"+str(timeline_df['year'][i]))
    timeline_df['Time']=time

    return timeline_df

def daily_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    daily_timeline_df=df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline_df

def week_activity_map(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    activity_pivoit_table=df.pivot_table(index='day_name',columns='period',
                   values='message',aggfunc='count').fillna(0)
    return activity_pivoit_table


def sentiment_analysis(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    # removing group notification
    df=df[df['message']!='<Media omitted>\n']
    # removing emoji
    df['message']=df['message'].apply(remove_emoji)
    df.dropna(inplace=True)
    sentiments=SentimentIntensityAnalyzer()
    df["positive"]=[sentiments.polarity_scores(i)["pos"] for i in df["message"]]
    df["negative"]=[sentiments.polarity_scores(i)["neg"] for i in df["message"]]
    df["neutral"]=[sentiments.polarity_scores(i)["neu"] for i in df["message"]]
    
    a=sum(df["positive"])
    b=sum(df["negative"])
    c=sum(df["neutral"])
    if (a>b) and (a>c):
        sentiment='Positive'
    if (b>a) and (b>c):
        sentiment='Negative'
    if (c>a) and (c>b):
        sentiment='Neutal'
    return sentiment
