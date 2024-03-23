import streamlit as st
from preprocessor import preprocess
import helper
import matplotlib.pyplot as plt
import re
import seaborn as sns

st.set_page_config(layout='wide',page_title='Whatsapp Chat Analyzer')

def main():
    st.sidebar.title("Whatsapp Chat Analyzer")
    st.sidebar.write("To export chat")
    st.sidebar.write("1. Open the chat \n2. Tap More options \n3. More > Export chat > Without media")
    # upload chat
    uploaded_file=st.sidebar.file_uploader("Choose a File")
    if uploaded_file is not None:
        bytes_data=uploaded_file.getvalue()  # file is in bytes
        data=bytes_data.decode("utf-8")
        # st.text(data)
        df=preprocess(data)
        # st.dataframe(df)
        
        # fetch unique users
        user_list=df['user'].unique().tolist()
        # user_list.remove("group notification")
        user_list.sort()
        user_list.insert(0,"Overall")
        
        selected_user=st.sidebar.selectbox("Show Analysis W.R.T",user_list)
        # stats
        st.header("Top Statistics ")
        num_messages,words,num_media,num_links=helper.fetch_stats(selected_user,df)
        col1,col2,col3,col4=st.columns(4)
        
        with col1:
            st.subheader("Total Messages")
            st.header(num_messages)
        with col2:
            st.subheader("Total Words")
            st.header(words)
        with col3:
            st.subheader("Total Media")
            st.header(num_media)
        with col4:
            st.subheader("Total Links")
            st.header(num_links)
        st.markdown("---")
        # MOnthly Timeline
        st.header("Monthly Timeline")
        time_line=helper.monthly_timeline(selected_user,df)
        plt.xticks(rotation='vertical')
        st.line_chart(time_line,x='Time',y='message',color='#ffaa00')
        
        # daily Time Line
        st.header("Daily Timeline")
        daily_timeline=helper.daily_timeline(selected_user,df)
        plt.xticks(rotation='vertical')
        # st.pyplot(fig)
        st.line_chart(daily_timeline,x='only_date',y='message',color='#057B05')
        st.markdown("---")
        # Activity map
        st.header("Activity Map")
        col1,col2=st.columns(2)
        with col1:
            st.subheader("Most Busy Day")
            busy_day=helper.week_activity_map(selected_user,df)
            # fig,ax=plt.subplots()
            # ax.bar(busy_day.index,busy_day.values,color='m')
            plt.xticks(rotation='vertical')
            st.bar_chart(busy_day,color='#580257')
        
        with col2:
            st.subheader("Most Busy Month")
            busy_month=helper.month_activity_map(selected_user,df)
            # fig,ax=plt.subplots()
            # ax.bar(busy_month.index,busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.bar_chart(busy_month,color='#F18905')
        st.markdown("---")
        # Activity Heatmap
        st.header("Weekly Activity Heat Map")
        pivoit_table=helper.activity_heatmap(selected_user,df)
        fig,ax=plt.subplots(figsize=(18,5))
        ax=sns.heatmap(pivoit_table,cmap='Greens')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        # finding the busiest user in group (only in grop level)
        if selected_user=='Overall':
            st.header("Most Active User")
            x,new_df=helper.fetch_most_busy_user(df)
            fig,ax=plt.subplots(figsize=(10,10))
            col1,col2=st.columns(2)
            with col1:
                ax.bar(x.index,x.values)
                plt.xticks(rotation='vertical')
                st.bar_chart(x,color='#D07621')
            with col2:
                st.dataframe(new_df)
        
        # word cloud
        st.markdown("---")
        st.header("Most Used Words")
        try:
            df_wc=helper.creat_word_cloud(selected_user,df) 
            fig,ax=plt.subplots(figsize=(20,10))
            ax.imshow(df_wc,interpolation='bilinear')
            plt.axis("off")
            st.pyplot(fig)
        except:
            st.error(f"No Text shared by {selected_user}")
        st.markdown("---")
        # most commmon 20 words
        most_common_df,df_processed=helper.most_common_words(selected_user,df)
        if most_common_df.shape[0]!=0:
            plt.xticks(rotation='vertical')
            st.header("Most Common Words")
            st.bar_chart(most_common_df,x='Words',y='Count')
            # st.dataframe(df_processed)
        else:pass
        
        # Overall Chat sentiment
        sentiment=helper.sentiment_analysis(selected_user,df) 
        st.header(f"Over all Chat Sentiment is {sentiment}")
        # st.subheader(sentiment)
        
        #emoji analysis
        st.markdown("---")
        st.header("Emoji Analysis")
        emoji_df=helper.emoji_count(selected_user,df)
        if emoji_df.shape[0]!=0:
            col1,col2=st.columns(2)
            with col1:
                st.table(emoji_df.head(15))
            with col2:
                fig,ax=plt.subplots()
                # st.subheader("Emoji Piechart")
                plt.rcParams['font.family'] = 'Segoe UI Emoji'
                ax.pie(emoji_df['Count'].head(),labels=emoji_df['Emoji'].head(),autopct="%0.2f%%")
                st.pyplot(fig)
        
        else:
            st.error(f"No Emoji shared by {selected_user}")
                
if __name__ == "__main__":
    main()
