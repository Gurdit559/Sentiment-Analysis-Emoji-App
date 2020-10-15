
import streamlit as st
# NLP Pkgs
from textblob import TextBlob
import pandas as pd
# Emoji
import emoji

# Web Scraping Pkg
from bs4 import BeautifulSoup
from urllib.request import urlopen


# Fetch Text From Url
@st.cache
def get_text(raw_url):
    page = urlopen(raw_url)
    soup = BeautifulSoup(page)
    fetched_text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    return fetched_text


def main():


    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    local_css("style.css")

    st.title("Sentiment Analysis Emoji App")

    activities = ["Sentiment", "Text Analysis on URL", "About"]
    choice = st.sidebar.selectbox("Choice", activities)

    if choice == 'Sentiment':
        st.subheader("Sentiment Analysis")
        st.write(emoji.emojize('Go ahead write your :red_heart: out :) ', use_aliases=True))
        raw_text = st.text_area("Enter Your Text below")
        if st.button("Analyze"):
            blob = TextBlob(raw_text)
            result = blob.sentiment.polarity
            if result > 0.0:
                custom_emoji = ':smile:'
                st.write(emoji.emojize(custom_emoji, use_aliases=True))
            elif result < 0.0:
                custom_emoji = ':disappointed:'
                st.write(emoji.emojize(custom_emoji, use_aliases=True))
            else:
                st.write(emoji.emojize(':expressionless:', use_aliases=True))
            st.info("Polarity Score is:: {}".format(result))

    if choice == 'Text Analysis on URL':
        st.subheader("Analysis on Text From URL")
        raw_url = st.text_input("Enter URL Here", "Type here")
        text_preview_length = st.slider("Length to Preview", 50, 100)
        if st.button("Analyze"):
            if raw_url != "Type here":
                result = get_text(raw_url)
                blob = TextBlob(result)
                len_of_full_text = len(result)
                len_of_short_text = round(len(result) / text_preview_length)
                st.success("Length of Full Text::{}".format(len_of_full_text))
                st.success("Length of Short Text::{}".format(len_of_short_text))
                st.info(result[:len_of_short_text])
                c_sentences = [sent for sent in blob.sentences]
                c_sentiment = [sent.sentiment.polarity for sent in blob.sentences]

                new_df = pd.DataFrame(zip(c_sentences, c_sentiment), columns=['Sentence', 'Sentiment'])
                st.dataframe(new_df)

    if choice == 'About':
        st.subheader("About:Sentiment Analysis Emoji App")
        st.write("With all this hate in the online world one can think twice before writing something online with this emoji text analysis app. With the polarity score it displays the respective emoji")
        st.write("Built with Streamlit,Textblob and Emoji")
        st.write(" By Gurdit Singh")
        st.markdown('github [here](https://github.com/Gurdit559)')
        


if __name__ == '__main__':
    main()