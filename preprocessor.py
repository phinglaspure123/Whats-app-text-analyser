import re
import pandas as pd

def preprocess(data):
    # to chk time format of data
    pattern='^\d{1,2}\/\d{1,2}\/\d{2,4}\,\s\d{1,2}:\d{2}\s|\s-\s.*'
    x=re.sub(pattern,'',data,count=1)[:2].lower()
    chk_list=['am','pm']
    if re.sub(pattern,'',x,count=1)[:2].lower() in chk_list:
        df_format=12
        pattern_data=r'\d{1,2}\/\d{1,2}\/\d{2,4},\s\d{1,2}:\d{2}\s(?:AM|PM|am|pm)\s-\s'

    else:
        df_format=24
        pattern_data=r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    msg=re.split(pattern_data,data)[1:]
    dates=re.findall(pattern_data,data)
    df=pd.DataFrame({
        'user_name':msg,
        'msg_date':dates
    })
    
    if df_format==12:
        # Remove unwanted characters from the datetime column
        df['msg_date'] = df['msg_date'].str.replace("\u202F", "").str.replace(" -", "")
        # Adjust the format string to handle the extra space
        format_string ="%d/%m/%y, %I:%M%p "
        # Convert the datetime column to datetime format
        df['msg_date'] = pd.to_datetime(df['msg_date'], format=format_string)
    
    else:
        df['msg_date']=pd.to_datetime(df['msg_date'], format='%d/%m/%Y, %H:%M - ')
    
    
    users=[]
    msg=[]

    for message in df['user_name']:
        entry=re.split('([\w\W]+?):\s',message)
        if entry[1:]:
            # user name
            users.append(entry[1])
            msg.append(entry[2])
        else:
            users.append('group notification')
            msg.append(entry[0])

    df['user']=users
    df['message']=msg
    df.drop(columns=['user_name'],inplace=True)
    
    df['year']=df['msg_date'].dt.year
    df['month']=df['msg_date'].dt.month_name()
    df['month_num']=df['msg_date'].dt.month
    df['day']=df['msg_date'].dt.day
    df['day_name']=df['msg_date'].dt.day_name()
    df['only_date']=df['msg_date'].dt.date
    df['Hour']=df['msg_date'].dt.hour
    df['minute']=df['msg_date'].dt.minute
    
    period=[]
    for hour in df[['day_name','Hour']]['Hour']:
        if hour==23:
            period.append(str(hour)+"-"+str("00"))
        elif hour ==0:
            period.append(str('00')+"-"+str(hour+1))
        else:
            period.append(str(hour)+"-"+str(hour+1))
    df['period']=period
    
    # removing group notification
    df=df[df['user']!='group notification']
    return df