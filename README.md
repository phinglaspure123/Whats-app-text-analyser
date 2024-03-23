
# Whatsapp Chat Analyzer
The Whatsapp Chat Analyzer is a Python-based tool designed to analyze chat data exported from WhatsApp. It provides insights into various aspects of the chat, including statistics, timelines, activity patterns, sentiment analysis, word clouds, and emoji usage. With interactive visualizations, users can gain a deeper understanding of their chat dynamics and communication patterns.


## Key Features

- Upload and analyze WhatsApp chat data.
- View statistics such as total messages, words, media, and links.
- Explore monthly and daily timelines of chat activity.
- Visualize activity maps showcasing busy days and months.
- Generate word clouds to identify frequently used words.
- Analyze sentiment to understand overall chat tone.
- Examine emoji usage patterns.
- Identify the most active users in the chat group.
## Libraries Used

- Streamlit: For building interactive web applications.
- Pandas: For data manipulation and analysis.
- Matplotlib and Seaborn: For data visualization.
- NLTK: For sentiment analysis.
- WordCloud: For generating word clouds.
- URLExtract: For extracting URLs from messages.
## Project Components
#### app.py: 
- Main application script containing the Streamlit web interface and analysis functionalities.
#### helper.py: 
- Module containing helper functions for data analysis and visualization.
#### preprocessor.py: 
- Module for preprocessing raw WhatsApp chat data.
#### stop_hinglish.txt: 
- Text file containing stopwords for Hindi language.
## Usage/Examples

- Upload the exported WhatsApp chat file.
- Select the user or view overall analysis.
- Click on "Show Analysis" to generate insights and visualizations.
- Explore various tabs and visualizations to understand chat dynamics.
- Analyze sentiments, word clouds, and emoji usage for deeper insights.
## Installation

requirements.txt

run this command in terminal
```bash
  pip install -r requirements.txt
```
    
## Run Locally

Clone the project

```bash
  git clone https://github.com/phinglaspure123/Whatsapp-Chat-Analyzer.git
```

Go to the project directory

```bash
  "Whatsapp Chat Analyzer"
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  streamlit run app.py
```


## Deployment

To deploy this project run

```bash
  
```


## Authors

- [@phinglaspure123](https://github.com/phinglaspure123)

