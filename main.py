import pandas as pd
import streamlit as st
import requests
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import main_functions
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(
    page_title='COP 4813 - Project 1'
)
st.title('COP 4813 - Web Application Programming')
st.title('Project 1')

st.header('Part A - The Top Stories API')
st.write('This app uses the Top Stories API to display the most common words used in the top current articles based '
         'on a specified topic selected by the user. '
         'The data is displayed as a line chart and as a wordcloud image.')
st.subheader('I - Topic Selection')

full_name = st.text_input('Please enter your name')
drop_down = st.selectbox('Select a topic:',
                         ["Arts",
                          "Automobiles",
                          "Books",
                          "Business",
                          "Fashion",
                          "Food",
                          "Health",
                          "Home",
                          "Insider",
                          "Magazine",
                          "Movies",
                          "Nyregion",
                          "Obituaries",
                          "Opinion",
                          "Politics",
                          "Real-Estate",
                          "Science",
                          "Sports",
                          "SundayReview",
                          "Technology",
                          "Theater",
                          "T-Magazine",
                          "Travel",
                          "Upshot",
                          "US",
                          "World"]
                         )

confirm_info = st.checkbox("See inputted information:")
if confirm_info:
    st.write("Hi",full_name,"! You are interested in", drop_down,".")

api_key_dict = main_functions.read_from_file("JSON_Files/api_key.json")
api_key = api_key_dict["my_key"]

url = "https://api.nytimes.com/svc/topstories/v2/" + drop_down + ".json?api-key=" + api_key

response = requests.get(url).json()
main_functions.save_to_file(response, "JSON_Files/response.json")
my_articles = main_functions.read_from_file("JSON_Files/response.json")

str1 = ""
for i in my_articles["results"]:
    str1 = str1 + i["abstract"]
print(str1)

sentences = sent_tokenize(str1)
words = word_tokenize(str1)

if confirm_info:
    st.subheader('II - Frequency Distribution')
    fdist = FreqDist(words)

    words_no_punct = []
    for w in words:
        if w.isalpha():
            words_no_punct.append(w.lower())

    fdist2 = FreqDist(words_no_punct)
    stopwords = stopwords.words("english")

    clean_words = []
    for w in words_no_punct:
        if w not in stopwords:
            clean_words.append(w)

    fdist3 = FreqDist(clean_words)
    cw = (fdist3.most_common(10))

    freqdist_plot = st.checkbox("Click here to generate frequency distribution")
    if freqdist_plot:
        df = pd.DataFrame(
            dict(
                words=[
                    cw[0][0], cw[1][0], cw[2][0], cw[3][0], cw[4][0], cw[5][0], cw[6][0], cw[7][0], cw[8][0], cw[9][0]
                ],
                number=[
                    cw[0][1], cw[1][1], cw[2][1], cw[3][1], cw[4][1], cw[5][1], cw[6][1], cw[7][1], cw[8][1], cw[9][1]
                ]
            )
        )
        df = df.sort_values(by="number")
        figure = px.line(df, x="words", y="number", title="Frequency Distribution")
        st.plotly_chart(figure)
if confirm_info:
    st.subheader('III - Wordcloud')
    wordcloudshow = st.checkbox("Click here to generate wordcloud")
    if wordcloudshow:
        wordcloud1 = WordCloud().generate(str1)
        wordcloud1.to_file("wordcloudimg/top_stories.png")
        plt.imshow(wordcloud1, interpolation='bilinear')
        plt.figure(figsize=(20, 20))
        plt.imshow(wordcloud1)
        plt.axis("off")
        st.image("wordcloudimg/top_stories.png")
        st.caption("Wordcloud generated for " + drop_down + " topic.")

st.header('Part B - Most Popular Articles')
st.write('Select if you want to see the most shared, emailed or viewed articles.')
prefer = st.selectbox('Select your preferred set of articles',
                      ["shared",
                       "emailed",
                       "viewed"])
occur = st.selectbox('Select the period of time (last days)',
                     ["1",
                      "7",
                      "30"])
api_key_dict = main_functions.read_from_file("JSON_Files/api_key.json")
api_key = api_key_dict["my_key"]

if prefer == "shared":
    url2 = "https://api.nytimes.com/svc/mostpopular/v2/shared/" + occur + "/facebook.json?api-key=" + api_key
else:
    url2 = "https://api.nytimes.com/svc/mostpopular/v2/" + prefer + "/" + occur + ".json?api-key=" + api_key

response = requests.get(url2).json()
main_functions.save_to_file(response, "JSON_Files/response.json")
my_articles = main_functions.read_from_file("JSON_Files/response.json")
if confirm_info:
    str2 = ""
    for i in my_articles["results"]:
        str2 = str2 + i["abstract"]

    print(str2)

    sentences = sent_tokenize(str2)
    words = word_tokenize(str2)

    fdist = FreqDist(words)
    words_no_punct = []
    for w in words:
        if w.isalpha():
            words_no_punct.append(w.lower())

    fdist2 = FreqDist(words_no_punct)

    clean_words = []
    for w in words_no_punct:
        if w not in stopwords:
            clean_words.append(w)

    fdist3 = FreqDist(clean_words).most_common(10)

    wordcloud2 = WordCloud().generate(str2)
    wordcloud2.to_file("wordcloudimg/most_popular.png")
    plt.imshow(wordcloud2, interpolation='bilinear')
    plt.figure(figsize=(20, 20))
    plt.imshow(wordcloud2)
    plt.axis("off")
    # plt.show()
    st.image("wordcloudimg/most_popular.png")
    st.caption("Wordcloud generated from" + prefer + " in the last " + occur + " day(s).")
